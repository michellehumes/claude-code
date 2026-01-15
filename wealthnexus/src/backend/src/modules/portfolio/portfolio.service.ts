import {
  Injectable,
  NotFoundException,
  BadRequestException,
  Logger,
} from '@nestjs/common';
import { PrismaService } from '../../database/prisma.service';
import { CreatePortfolioDto, UpdatePortfolioDto, PortfolioListQueryDto } from './dto';
import { Prisma } from '@prisma/client';

@Injectable()
export class PortfolioService {
  private readonly logger = new Logger(PortfolioService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Find all portfolios for a tenant with pagination and filtering
   */
  async findAll(tenantId: string, query: PortfolioListQueryDto) {
    const { page = 1, limit = 20, search, type, sortBy = 'name', sortOrder = 'asc' } = query;
    const skip = (page - 1) * limit;

    const where: Prisma.PortfolioWhereInput = {
      tenantId,
      ...(search && {
        name: { contains: search, mode: 'insensitive' },
      }),
      ...(type && { portfolioType: type }),
    };

    const [items, total] = await Promise.all([
      this.prisma.portfolio.findMany({
        where,
        skip,
        take: limit,
        orderBy: { [sortBy]: sortOrder },
        include: {
          benchmark: {
            select: { id: true, name: true, symbol: true },
          },
          accounts: {
            include: {
              account: {
                select: { id: true, accountNumber: true, accountType: true },
              },
            },
          },
          _count: {
            select: { valuations: true },
          },
        },
      }),
      this.prisma.portfolio.count({ where }),
    ]);

    return {
      items: items.map(this.transformPortfolio),
      total,
      page,
      limit,
    };
  }

  /**
   * Find a single portfolio by ID
   */
  async findOne(tenantId: string, id: string) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { id, tenantId },
      include: {
        benchmark: true,
        accounts: {
          include: {
            account: {
              include: {
                client: {
                  select: { id: true, name: true, type: true },
                },
              },
            },
          },
        },
        valuations: {
          orderBy: { valuationDate: 'desc' },
          take: 1,
        },
      },
    });

    if (!portfolio) {
      throw new NotFoundException(`Portfolio with ID ${id} not found`);
    }

    return this.transformPortfolio(portfolio);
  }

  /**
   * Create a new portfolio
   */
  async create(tenantId: string, dto: CreatePortfolioDto, userId: string) {
    // Validate benchmark exists if provided
    if (dto.benchmarkId) {
      const benchmark = await this.prisma.benchmark.findFirst({
        where: {
          id: dto.benchmarkId,
          OR: [{ tenantId }, { tenantId: null }],
        },
      });

      if (!benchmark) {
        throw new BadRequestException('Invalid benchmark ID');
      }
    }

    const portfolio = await this.prisma.portfolio.create({
      data: {
        tenantId,
        name: dto.name,
        portfolioType: dto.portfolioType,
        benchmarkId: dto.benchmarkId,
        inceptionDate: dto.inceptionDate ? new Date(dto.inceptionDate) : new Date(),
        settings: dto.settings || {},
      },
      include: {
        benchmark: true,
      },
    });

    // Log audit
    await this.logAudit(tenantId, userId, 'CREATE', 'Portfolio', portfolio.id);

    this.logger.log(`Portfolio created: ${portfolio.id} by user ${userId}`);

    return this.transformPortfolio(portfolio);
  }

  /**
   * Update a portfolio
   */
  async update(tenantId: string, id: string, dto: UpdatePortfolioDto, userId: string) {
    const existing = await this.prisma.portfolio.findFirst({
      where: { id, tenantId },
    });

    if (!existing) {
      throw new NotFoundException(`Portfolio with ID ${id} not found`);
    }

    const portfolio = await this.prisma.portfolio.update({
      where: { id },
      data: {
        ...(dto.name && { name: dto.name }),
        ...(dto.portfolioType && { portfolioType: dto.portfolioType }),
        ...(dto.benchmarkId !== undefined && { benchmarkId: dto.benchmarkId }),
        ...(dto.inceptionDate && { inceptionDate: new Date(dto.inceptionDate) }),
        ...(dto.settings && { settings: dto.settings }),
      },
      include: {
        benchmark: true,
        accounts: {
          include: {
            account: true,
          },
        },
      },
    });

    await this.logAudit(tenantId, userId, 'UPDATE', 'Portfolio', id, {
      before: existing,
      after: portfolio,
    });

    this.logger.log(`Portfolio updated: ${id} by user ${userId}`);

    return this.transformPortfolio(portfolio);
  }

  /**
   * Delete a portfolio
   */
  async remove(tenantId: string, id: string, userId: string) {
    const existing = await this.prisma.portfolio.findFirst({
      where: { id, tenantId },
    });

    if (!existing) {
      throw new NotFoundException(`Portfolio with ID ${id} not found`);
    }

    // Delete related records first
    await this.prisma.$transaction([
      this.prisma.portfolioAccount.deleteMany({ where: { portfolioId: id } }),
      this.prisma.portfolioValuation.deleteMany({ where: { portfolioId: id } }),
      this.prisma.portfolio.delete({ where: { id } }),
    ]);

    await this.logAudit(tenantId, userId, 'DELETE', 'Portfolio', id);

    this.logger.log(`Portfolio deleted: ${id} by user ${userId}`);
  }

  /**
   * Get portfolio transactions
   */
  async getTransactions(
    tenantId: string,
    portfolioId: string,
    options: {
      startDate?: Date;
      endDate?: Date;
      type?: string;
    },
  ) {
    // Get account IDs for this portfolio
    const portfolioAccounts = await this.prisma.portfolioAccount.findMany({
      where: { portfolioId },
      select: { accountId: true },
    });

    const accountIds = portfolioAccounts.map((pa) => pa.accountId);

    if (accountIds.length === 0) {
      return { items: [], total: 0 };
    }

    const where: Prisma.TransactionWhereInput = {
      tenantId,
      accountId: { in: accountIds },
      ...(options.startDate && { tradeDate: { gte: options.startDate } }),
      ...(options.endDate && { tradeDate: { lte: options.endDate } }),
      ...(options.type && { transactionType: options.type as any }),
    };

    const [items, total] = await Promise.all([
      this.prisma.transaction.findMany({
        where,
        orderBy: { tradeDate: 'desc' },
        include: {
          security: {
            select: { id: true, symbol: true, name: true },
          },
          account: {
            select: { id: true, accountNumber: true },
          },
        },
      }),
      this.prisma.transaction.count({ where }),
    ]);

    return { items, total };
  }

  /**
   * Add accounts to portfolio
   */
  async addAccounts(
    tenantId: string,
    portfolioId: string,
    accountIds: string[],
    userId: string,
  ) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { id: portfolioId, tenantId },
    });

    if (!portfolio) {
      throw new NotFoundException(`Portfolio with ID ${portfolioId} not found`);
    }

    // Verify all accounts belong to tenant
    const accounts = await this.prisma.account.findMany({
      where: {
        id: { in: accountIds },
        tenantId,
      },
    });

    if (accounts.length !== accountIds.length) {
      throw new BadRequestException('One or more account IDs are invalid');
    }

    // Add accounts
    await this.prisma.portfolioAccount.createMany({
      data: accountIds.map((accountId) => ({
        portfolioId,
        accountId,
      })),
      skipDuplicates: true,
    });

    await this.logAudit(tenantId, userId, 'UPDATE', 'Portfolio', portfolioId, {
      action: 'ADD_ACCOUNTS',
      accountIds,
    });

    return this.findOne(tenantId, portfolioId);
  }

  /**
   * Remove accounts from portfolio
   */
  async removeAccounts(
    tenantId: string,
    portfolioId: string,
    accountIds: string[],
    userId: string,
  ) {
    const portfolio = await this.prisma.portfolio.findFirst({
      where: { id: portfolioId, tenantId },
    });

    if (!portfolio) {
      throw new NotFoundException(`Portfolio with ID ${portfolioId} not found`);
    }

    await this.prisma.portfolioAccount.deleteMany({
      where: {
        portfolioId,
        accountId: { in: accountIds },
      },
    });

    await this.logAudit(tenantId, userId, 'UPDATE', 'Portfolio', portfolioId, {
      action: 'REMOVE_ACCOUNTS',
      accountIds,
    });

    return this.findOne(tenantId, portfolioId);
  }

  /**
   * Transform portfolio for API response
   */
  private transformPortfolio(portfolio: any) {
    const latestValuation = portfolio.valuations?.[0];

    return {
      id: portfolio.id,
      name: portfolio.name,
      portfolioType: portfolio.portfolioType,
      inceptionDate: portfolio.inceptionDate,
      settings: portfolio.settings,
      benchmark: portfolio.benchmark,
      accounts: portfolio.accounts?.map((pa: any) => ({
        ...pa.account,
        weight: pa.weight,
      })),
      currentValue: latestValuation?.totalValue || null,
      performance: latestValuation
        ? {
            dailyReturn: latestValuation.dailyReturn,
            mtdReturn: latestValuation.mtdReturn,
            ytdReturn: latestValuation.ytdReturn,
            inceptionReturn: latestValuation.inceptionReturn,
          }
        : null,
      createdAt: portfolio.createdAt,
      updatedAt: portfolio.updatedAt,
    };
  }

  /**
   * Log audit trail
   */
  private async logAudit(
    tenantId: string,
    userId: string,
    action: string,
    entityType: string,
    entityId: string,
    changes?: any,
  ) {
    await this.prisma.auditLog.create({
      data: {
        tenantId,
        userId,
        action,
        entityType,
        entityId,
        changes,
      },
    });
  }
}
