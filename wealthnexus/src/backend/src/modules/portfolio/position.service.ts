import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { PrismaService } from '../../database/prisma.service';
import { Decimal } from '@prisma/client/runtime/library';

interface HoldingsOptions {
  asOfDate: Date;
  groupBy?: 'security' | 'assetClass' | 'sector';
}

interface AllocationOptions {
  asOfDate: Date;
}

@Injectable()
export class PositionService {
  private readonly logger = new Logger(PositionService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Get portfolio holdings with current valuations
   */
  async getPortfolioHoldings(
    tenantId: string,
    portfolioId: string,
    options: HoldingsOptions,
  ) {
    // Get portfolio accounts
    const portfolioAccounts = await this.prisma.portfolioAccount.findMany({
      where: { portfolioId },
      select: { accountId: true },
    });

    if (portfolioAccounts.length === 0) {
      throw new NotFoundException('Portfolio has no associated accounts');
    }

    const accountIds = portfolioAccounts.map((pa) => pa.accountId);

    // Get positions for all accounts
    const positions = await this.prisma.position.findMany({
      where: {
        tenantId,
        accountId: { in: accountIds },
        asOfDate: { lte: options.asOfDate },
      },
      include: {
        security: true,
      },
      orderBy: { asOfDate: 'desc' },
    });

    // Get latest prices for all securities
    const securityIds = [...new Set(positions.map((p) => p.securityId))];
    const prices = await this.getLatestPrices(securityIds, options.asOfDate);

    // Aggregate positions by security
    const aggregatedHoldings = this.aggregatePositions(positions, prices);

    // Calculate total portfolio value
    const totalValue = aggregatedHoldings.reduce(
      (sum, h) => sum + h.marketValue,
      0,
    );

    // Add weights
    const holdings = aggregatedHoldings.map((h) => ({
      ...h,
      weight: totalValue > 0 ? (h.marketValue / totalValue) * 100 : 0,
    }));

    // Calculate allocation
    const allocation = this.calculateAllocation(holdings);

    return {
      portfolioId,
      asOfDate: options.asOfDate,
      totalValue,
      holdings,
      allocation,
    };
  }

  /**
   * Get asset allocation breakdown
   */
  async getAssetAllocation(
    tenantId: string,
    portfolioId: string,
    options: AllocationOptions,
  ) {
    const holdings = await this.getPortfolioHoldings(tenantId, portfolioId, {
      asOfDate: options.asOfDate,
    });

    return {
      portfolioId,
      asOfDate: options.asOfDate,
      totalValue: holdings.totalValue,
      allocation: holdings.allocation,
    };
  }

  /**
   * Get positions for a specific account
   */
  async getAccountPositions(
    tenantId: string,
    accountId: string,
    asOfDate: Date,
  ) {
    const positions = await this.prisma.position.findMany({
      where: {
        tenantId,
        accountId,
        asOfDate: { lte: asOfDate },
      },
      include: {
        security: true,
      },
      orderBy: { asOfDate: 'desc' },
    });

    // Get latest position per security
    const latestPositions = new Map<string, typeof positions[0]>();
    for (const pos of positions) {
      if (!latestPositions.has(pos.securityId)) {
        latestPositions.set(pos.securityId, pos);
      }
    }

    const securityIds = [...latestPositions.keys()];
    const prices = await this.getLatestPrices(securityIds, asOfDate);

    return [...latestPositions.values()].map((pos) => {
      const price = prices.get(pos.securityId) || 0;
      const quantity = Number(pos.quantity);
      const marketValue = quantity * price;
      const costBasis = pos.costBasis ? Number(pos.costBasis) : null;

      return {
        id: pos.id,
        securityId: pos.securityId,
        symbol: pos.security.symbol,
        name: pos.security.name,
        assetClass: pos.security.assetClass,
        securityType: pos.security.securityType,
        quantity,
        price,
        marketValue,
        costBasis,
        unrealizedGain: costBasis ? marketValue - costBasis : null,
        unrealizedGainPercent: costBasis && costBasis > 0
          ? ((marketValue - costBasis) / costBasis) * 100
          : null,
        asOfDate: pos.asOfDate,
      };
    });
  }

  /**
   * Get latest prices for securities
   */
  private async getLatestPrices(
    securityIds: string[],
    asOfDate: Date,
  ): Promise<Map<string, number>> {
    if (securityIds.length === 0) {
      return new Map();
    }

    const prices = await this.prisma.marketPrice.findMany({
      where: {
        securityId: { in: securityIds },
        priceDate: { lte: asOfDate },
      },
      orderBy: { priceDate: 'desc' },
      distinct: ['securityId'],
    });

    return new Map(
      prices.map((p) => [p.securityId, Number(p.closePrice || p.adjustedClose || 0)]),
    );
  }

  /**
   * Aggregate positions across accounts
   */
  private aggregatePositions(
    positions: any[],
    prices: Map<string, number>,
  ) {
    // Group by security and get latest position for each
    const positionMap = new Map<string, {
      security: any;
      quantity: number;
      costBasis: number;
    }>();

    for (const pos of positions) {
      const existing = positionMap.get(pos.securityId);
      if (!existing) {
        positionMap.set(pos.securityId, {
          security: pos.security,
          quantity: Number(pos.quantity),
          costBasis: pos.costBasis ? Number(pos.costBasis) : 0,
        });
      } else {
        existing.quantity += Number(pos.quantity);
        if (pos.costBasis) {
          existing.costBasis += Number(pos.costBasis);
        }
      }
    }

    return [...positionMap.entries()].map(([securityId, data]) => {
      const price = prices.get(securityId) || 0;
      const marketValue = data.quantity * price;

      return {
        securityId,
        symbol: data.security.symbol,
        name: data.security.name,
        assetClass: data.security.assetClass || 'OTHER',
        sector: data.security.sector,
        quantity: data.quantity,
        price,
        marketValue,
        costBasis: data.costBasis || null,
        unrealizedGain: data.costBasis ? marketValue - data.costBasis : null,
        unrealizedGainPercent:
          data.costBasis && data.costBasis > 0
            ? ((marketValue - data.costBasis) / data.costBasis) * 100
            : null,
      };
    });
  }

  /**
   * Calculate allocation breakdowns
   */
  private calculateAllocation(holdings: any[]) {
    const totalValue = holdings.reduce((sum, h) => sum + h.marketValue, 0);

    // By Asset Class
    const byAssetClass = this.groupBy(holdings, 'assetClass', totalValue);

    // By Sector
    const bySector = this.groupBy(
      holdings.filter((h) => h.sector),
      'sector',
      totalValue,
    );

    return {
      byAssetClass,
      bySector: bySector.length > 0 ? bySector : undefined,
    };
  }

  /**
   * Group holdings by a key and calculate values
   */
  private groupBy(holdings: any[], key: string, totalValue: number) {
    const groups = new Map<string, number>();

    for (const holding of holdings) {
      const groupKey = holding[key] || 'Unknown';
      const current = groups.get(groupKey) || 0;
      groups.set(groupKey, current + holding.marketValue);
    }

    return [...groups.entries()]
      .map(([name, value]) => ({
        name,
        value,
        weight: totalValue > 0 ? (value / totalValue) * 100 : 0,
      }))
      .sort((a, b) => b.value - a.value);
  }
}
