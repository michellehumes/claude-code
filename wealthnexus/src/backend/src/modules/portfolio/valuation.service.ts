import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { PrismaService } from '../../database/prisma.service';

interface PerformanceOptions {
  startDate?: Date;
  endDate?: Date;
  frequency?: 'daily' | 'monthly' | 'quarterly';
}

@Injectable()
export class ValuationService {
  private readonly logger = new Logger(ValuationService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Get portfolio performance metrics
   */
  async getPerformance(
    tenantId: string,
    portfolioId: string,
    options: PerformanceOptions,
  ) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { id: portfolioId, tenantId },
      include: { benchmark: true },
    });

    if (!portfolio) {
      throw new NotFoundException(`Portfolio with ID ${portfolioId} not found`);
    }

    const endDate = options.endDate || new Date();
    const startDate =
      options.startDate ||
      portfolio.inceptionDate ||
      new Date(endDate.getTime() - 365 * 24 * 60 * 60 * 1000);

    // Get valuations for the period
    const valuations = await this.prisma.portfolioValuation.findMany({
      where: {
        portfolioId,
        valuationDate: {
          gte: startDate,
          lte: endDate,
        },
      },
      orderBy: { valuationDate: 'asc' },
    });

    if (valuations.length === 0) {
      return {
        portfolioId,
        portfolioName: portfolio.name,
        startDate,
        endDate,
        returns: {
          totalReturn: 0,
          annualizedReturn: 0,
        },
        risk: {
          volatility: 0,
          sharpeRatio: 0,
          maxDrawdown: 0,
        },
      };
    }

    // Calculate returns
    const returns = this.calculateReturns(valuations, options.frequency);
    const riskMetrics = this.calculateRiskMetrics(valuations);

    // Get benchmark performance if available
    let benchmarkComparison = null;
    if (portfolio.benchmark) {
      benchmarkComparison = await this.getBenchmarkComparison(
        portfolio.benchmark.id,
        startDate,
        endDate,
        returns.totalReturn,
        riskMetrics.volatility,
      );
    }

    return {
      portfolioId,
      portfolioName: portfolio.name,
      startDate,
      endDate,
      returns,
      risk: riskMetrics,
      benchmarkComparison,
    };
  }

  /**
   * Calculate returns from valuations
   */
  private calculateReturns(valuations: any[], frequency?: string) {
    if (valuations.length < 2) {
      return {
        totalReturn: 0,
        annualizedReturn: 0,
        dailyReturns: [],
      };
    }

    const startValue = Number(valuations[0].totalValue);
    const endValue = Number(valuations[valuations.length - 1].totalValue);
    const totalReturn =
      startValue > 0 ? ((endValue - startValue) / startValue) * 100 : 0;

    // Calculate daily returns
    const dailyReturns: number[] = [];
    for (let i = 1; i < valuations.length; i++) {
      const prevValue = Number(valuations[i - 1].totalValue);
      const currValue = Number(valuations[i].totalValue);
      const dailyReturn =
        prevValue > 0 ? ((currValue - prevValue) / prevValue) * 100 : 0;
      dailyReturns.push(dailyReturn);
    }

    // Calculate annualized return
    const startDate = new Date(valuations[0].valuationDate);
    const endDate = new Date(valuations[valuations.length - 1].valuationDate);
    const years =
      (endDate.getTime() - startDate.getTime()) / (365.25 * 24 * 60 * 60 * 1000);
    const annualizedReturn =
      years > 0
        ? (Math.pow(1 + totalReturn / 100, 1 / years) - 1) * 100
        : totalReturn;

    // Aggregate by frequency if requested
    let aggregatedReturns: number[] | undefined;
    if (frequency === 'monthly') {
      aggregatedReturns = this.aggregateReturnsByMonth(valuations);
    } else if (frequency === 'quarterly') {
      aggregatedReturns = this.aggregateReturnsByQuarter(valuations);
    }

    return {
      totalReturn,
      annualizedReturn,
      dailyReturns: frequency === 'daily' ? dailyReturns : undefined,
      monthlyReturns: frequency === 'monthly' ? aggregatedReturns : undefined,
      quarterlyReturns:
        frequency === 'quarterly' ? aggregatedReturns : undefined,
    };
  }

  /**
   * Calculate risk metrics
   */
  private calculateRiskMetrics(valuations: any[]) {
    if (valuations.length < 2) {
      return {
        volatility: 0,
        sharpeRatio: 0,
        maxDrawdown: 0,
        sortinoRatio: 0,
      };
    }

    // Calculate daily returns
    const dailyReturns: number[] = [];
    for (let i = 1; i < valuations.length; i++) {
      const prevValue = Number(valuations[i - 1].totalValue);
      const currValue = Number(valuations[i].totalValue);
      dailyReturns.push(prevValue > 0 ? (currValue - prevValue) / prevValue : 0);
    }

    // Volatility (annualized standard deviation)
    const avgReturn =
      dailyReturns.reduce((a, b) => a + b, 0) / dailyReturns.length;
    const variance =
      dailyReturns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) /
      dailyReturns.length;
    const dailyStdDev = Math.sqrt(variance);
    const volatility = dailyStdDev * Math.sqrt(252) * 100; // Annualized

    // Sharpe Ratio (assuming 0% risk-free rate for simplicity)
    const annualizedReturn = avgReturn * 252 * 100;
    const sharpeRatio = volatility > 0 ? annualizedReturn / volatility : 0;

    // Sortino Ratio (downside deviation)
    const negativeReturns = dailyReturns.filter((r) => r < 0);
    const downsideVariance =
      negativeReturns.length > 0
        ? negativeReturns.reduce((sum, r) => sum + Math.pow(r, 2), 0) /
          negativeReturns.length
        : 0;
    const downsideDeviation = Math.sqrt(downsideVariance) * Math.sqrt(252) * 100;
    const sortinoRatio =
      downsideDeviation > 0 ? annualizedReturn / downsideDeviation : 0;

    // Max Drawdown
    let maxDrawdown = 0;
    let peak = Number(valuations[0].totalValue);
    for (const val of valuations) {
      const value = Number(val.totalValue);
      if (value > peak) {
        peak = value;
      }
      const drawdown = peak > 0 ? ((peak - value) / peak) * 100 : 0;
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown;
      }
    }

    return {
      volatility,
      sharpeRatio,
      maxDrawdown,
      sortinoRatio,
    };
  }

  /**
   * Get benchmark comparison metrics
   */
  private async getBenchmarkComparison(
    benchmarkId: string,
    startDate: Date,
    endDate: Date,
    portfolioReturn: number,
    portfolioVolatility: number,
  ) {
    // In a real implementation, this would fetch benchmark returns
    // For now, return placeholder values
    const benchmarkReturn = portfolioReturn * 0.9; // Placeholder
    const alpha = portfolioReturn - benchmarkReturn;
    const trackingError = portfolioVolatility * 0.5; // Placeholder
    const informationRatio =
      trackingError > 0 ? alpha / trackingError : 0;

    return {
      benchmarkReturn,
      alpha,
      trackingError,
      informationRatio,
    };
  }

  /**
   * Aggregate returns by month
   */
  private aggregateReturnsByMonth(valuations: any[]): number[] {
    const monthlyReturns: number[] = [];
    let currentMonth = -1;
    let monthStart = 0;

    for (let i = 0; i < valuations.length; i++) {
      const date = new Date(valuations[i].valuationDate);
      const month = date.getMonth();

      if (currentMonth === -1) {
        currentMonth = month;
        monthStart = Number(valuations[i].totalValue);
      } else if (month !== currentMonth) {
        const monthEnd = Number(valuations[i - 1].totalValue);
        const monthReturn =
          monthStart > 0 ? ((monthEnd - monthStart) / monthStart) * 100 : 0;
        monthlyReturns.push(monthReturn);
        currentMonth = month;
        monthStart = Number(valuations[i].totalValue);
      }
    }

    // Add final month
    if (valuations.length > 0) {
      const monthEnd = Number(valuations[valuations.length - 1].totalValue);
      const monthReturn =
        monthStart > 0 ? ((monthEnd - monthStart) / monthStart) * 100 : 0;
      monthlyReturns.push(monthReturn);
    }

    return monthlyReturns;
  }

  /**
   * Aggregate returns by quarter
   */
  private aggregateReturnsByQuarter(valuations: any[]): number[] {
    const quarterlyReturns: number[] = [];
    let currentQuarter = -1;
    let quarterStart = 0;

    for (let i = 0; i < valuations.length; i++) {
      const date = new Date(valuations[i].valuationDate);
      const quarter = Math.floor(date.getMonth() / 3);

      if (currentQuarter === -1) {
        currentQuarter = quarter;
        quarterStart = Number(valuations[i].totalValue);
      } else if (quarter !== currentQuarter) {
        const quarterEnd = Number(valuations[i - 1].totalValue);
        const quarterReturn =
          quarterStart > 0
            ? ((quarterEnd - quarterStart) / quarterStart) * 100
            : 0;
        quarterlyReturns.push(quarterReturn);
        currentQuarter = quarter;
        quarterStart = Number(valuations[i].totalValue);
      }
    }

    // Add final quarter
    if (valuations.length > 0) {
      const quarterEnd = Number(valuations[valuations.length - 1].totalValue);
      const quarterReturn =
        quarterStart > 0
          ? ((quarterEnd - quarterStart) / quarterStart) * 100
          : 0;
      quarterlyReturns.push(quarterReturn);
    }

    return quarterlyReturns;
  }

  /**
   * Calculate valuations for a portfolio (batch job)
   */
  async calculateValuation(tenantId: string, portfolioId: string, date: Date) {
    const portfolioAccounts = await this.prisma.portfolioAccount.findMany({
      where: { portfolioId },
      select: { accountId: true },
    });

    if (portfolioAccounts.length === 0) {
      return null;
    }

    const accountIds = portfolioAccounts.map((pa) => pa.accountId);

    // Get latest positions
    const positions = await this.prisma.position.findMany({
      where: {
        tenantId,
        accountId: { in: accountIds },
        asOfDate: { lte: date },
      },
      include: { security: true },
      orderBy: { asOfDate: 'desc' },
      distinct: ['accountId', 'securityId'],
    });

    // Get prices
    const securityIds = [...new Set(positions.map((p) => p.securityId))];
    const prices = await this.prisma.marketPrice.findMany({
      where: {
        securityId: { in: securityIds },
        priceDate: { lte: date },
      },
      orderBy: { priceDate: 'desc' },
      distinct: ['securityId'],
    });

    const priceMap = new Map(
      prices.map((p) => [p.securityId, Number(p.closePrice || 0)]),
    );

    // Calculate values
    let marketValue = 0;
    let cashValue = 0;

    for (const pos of positions) {
      const price = priceMap.get(pos.securityId) || 0;
      const value = Number(pos.quantity) * price;

      if (pos.security.securityType === 'CASH') {
        cashValue += value;
      } else {
        marketValue += value;
      }
    }

    const totalValue = marketValue + cashValue;

    // Get previous valuation for return calculation
    const prevValuation = await this.prisma.portfolioValuation.findFirst({
      where: { portfolioId, valuationDate: { lt: date } },
      orderBy: { valuationDate: 'desc' },
    });

    const prevTotal = prevValuation ? Number(prevValuation.totalValue) : totalValue;
    const dailyReturn =
      prevTotal > 0 ? ((totalValue - prevTotal) / prevTotal) * 100 : 0;

    // Create or update valuation
    const valuation = await this.prisma.portfolioValuation.upsert({
      where: {
        portfolioId_valuationDate: {
          portfolioId,
          valuationDate: date,
        },
      },
      create: {
        tenantId,
        portfolioId,
        valuationDate: date,
        marketValue,
        cashValue,
        totalValue,
        dailyReturn,
      },
      update: {
        marketValue,
        cashValue,
        totalValue,
        dailyReturn,
      },
    });

    return valuation;
  }
}
