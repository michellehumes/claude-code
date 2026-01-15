import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { PrismaService } from '../../database/prisma.service';
import { Prisma } from '@prisma/client';

interface TransactionFilters {
  startDate?: Date;
  endDate?: Date;
  type?: string;
  securityId?: string;
  minAmount?: number;
  maxAmount?: number;
}

interface CreateTransactionDto {
  accountId: string;
  securityId?: string;
  transactionType: string;
  tradeDate: Date;
  settlementDate?: Date;
  quantity?: number;
  price?: number;
  amount: number;
  fees?: number;
  currency?: string;
  description?: string;
  externalId?: string;
  source?: string;
  metadata?: Record<string, any>;
}

@Injectable()
export class TransactionService {
  private readonly logger = new Logger(TransactionService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Get transactions for an account
   */
  async getAccountTransactions(
    tenantId: string,
    accountId: string,
    filters: TransactionFilters,
    page = 1,
    limit = 50,
  ) {
    const where: Prisma.TransactionWhereInput = {
      tenantId,
      accountId,
      ...(filters.startDate && { tradeDate: { gte: filters.startDate } }),
      ...(filters.endDate && { tradeDate: { lte: filters.endDate } }),
      ...(filters.type && { transactionType: filters.type as any }),
      ...(filters.securityId && { securityId: filters.securityId }),
      ...(filters.minAmount && { amount: { gte: filters.minAmount } }),
      ...(filters.maxAmount && { amount: { lte: filters.maxAmount } }),
    };

    const [items, total] = await Promise.all([
      this.prisma.transaction.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { tradeDate: 'desc' },
        include: {
          security: {
            select: { id: true, symbol: true, name: true },
          },
        },
      }),
      this.prisma.transaction.count({ where }),
    ]);

    return {
      items: items.map(this.transformTransaction),
      total,
      page,
      limit,
    };
  }

  /**
   * Get a single transaction
   */
  async getTransaction(tenantId: string, id: string) {
    const transaction = await this.prisma.transaction.findFirst({
      where: { id, tenantId },
      include: {
        security: true,
        account: {
          select: { id: true, accountNumber: true, accountType: true },
        },
      },
    });

    if (!transaction) {
      throw new NotFoundException(`Transaction with ID ${id} not found`);
    }

    return this.transformTransaction(transaction);
  }

  /**
   * Create a transaction
   */
  async createTransaction(
    tenantId: string,
    dto: CreateTransactionDto,
    userId: string,
  ) {
    // Verify account exists
    const account = await this.prisma.account.findFirst({
      where: { id: dto.accountId, tenantId },
    });

    if (!account) {
      throw new NotFoundException(`Account with ID ${dto.accountId} not found`);
    }

    // Verify security exists if provided
    if (dto.securityId) {
      const security = await this.prisma.security.findFirst({
        where: {
          id: dto.securityId,
          OR: [{ tenantId }, { tenantId: null }],
        },
      });

      if (!security) {
        throw new NotFoundException(
          `Security with ID ${dto.securityId} not found`,
        );
      }
    }

    const transaction = await this.prisma.transaction.create({
      data: {
        tenantId,
        accountId: dto.accountId,
        securityId: dto.securityId,
        transactionType: dto.transactionType as any,
        tradeDate: dto.tradeDate,
        settlementDate: dto.settlementDate,
        quantity: dto.quantity,
        price: dto.price,
        amount: dto.amount,
        fees: dto.fees || 0,
        currency: dto.currency || 'USD',
        description: dto.description,
        externalId: dto.externalId,
        source: dto.source || 'manual',
        metadata: dto.metadata || {},
      },
      include: {
        security: true,
      },
    });

    // Update position if it's a buy/sell
    if (
      dto.securityId &&
      dto.quantity &&
      ['BUY', 'SELL'].includes(dto.transactionType)
    ) {
      await this.updatePositionFromTransaction(tenantId, transaction);
    }

    // Log audit
    await this.prisma.auditLog.create({
      data: {
        tenantId,
        userId,
        action: 'CREATE',
        entityType: 'Transaction',
        entityId: transaction.id,
      },
    });

    return this.transformTransaction(transaction);
  }

  /**
   * Batch import transactions
   */
  async batchImport(
    tenantId: string,
    transactions: CreateTransactionDto[],
    userId: string,
  ) {
    const results = {
      success: 0,
      failed: 0,
      errors: [] as { index: number; error: string }[],
    };

    for (let i = 0; i < transactions.length; i++) {
      try {
        await this.createTransaction(tenantId, transactions[i], userId);
        results.success++;
      } catch (error) {
        results.failed++;
        results.errors.push({
          index: i,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    }

    return results;
  }

  /**
   * Get transaction summary for an account
   */
  async getTransactionSummary(
    tenantId: string,
    accountId: string,
    startDate: Date,
    endDate: Date,
  ) {
    const transactions = await this.prisma.transaction.findMany({
      where: {
        tenantId,
        accountId,
        tradeDate: { gte: startDate, lte: endDate },
      },
    });

    const summary = {
      totalTransactions: transactions.length,
      byType: {} as Record<string, { count: number; amount: number }>,
      netCashFlow: 0,
      totalFees: 0,
    };

    for (const tx of transactions) {
      const type = tx.transactionType;
      if (!summary.byType[type]) {
        summary.byType[type] = { count: 0, amount: 0 };
      }
      summary.byType[type].count++;
      summary.byType[type].amount += Number(tx.amount);
      summary.totalFees += Number(tx.fees);

      // Calculate net cash flow
      if (['DEPOSIT', 'TRANSFER_IN', 'DIVIDEND', 'INTEREST'].includes(type)) {
        summary.netCashFlow += Number(tx.amount);
      } else if (['WITHDRAWAL', 'TRANSFER_OUT', 'FEE', 'TAX'].includes(type)) {
        summary.netCashFlow -= Math.abs(Number(tx.amount));
      }
    }

    return summary;
  }

  /**
   * Update position from transaction
   */
  private async updatePositionFromTransaction(
    tenantId: string,
    transaction: any,
  ) {
    const { accountId, securityId, transactionType, quantity, tradeDate, price } =
      transaction;

    if (!securityId || !quantity) return;

    const quantityChange =
      transactionType === 'BUY' ? Number(quantity) : -Number(quantity);
    const costBasisChange =
      transactionType === 'BUY'
        ? Number(quantity) * Number(price || 0)
        : 0;

    // Find existing position
    const existingPosition = await this.prisma.position.findFirst({
      where: {
        tenantId,
        accountId,
        securityId,
        asOfDate: tradeDate,
      },
    });

    if (existingPosition) {
      const newQuantity = Number(existingPosition.quantity) + quantityChange;
      const newCostBasis =
        (Number(existingPosition.costBasis) || 0) + costBasisChange;

      await this.prisma.position.update({
        where: { id: existingPosition.id },
        data: {
          quantity: newQuantity,
          costBasis: newCostBasis,
        },
      });
    } else {
      // Create new position
      await this.prisma.position.create({
        data: {
          tenantId,
          accountId,
          securityId,
          quantity: quantityChange,
          costBasis: costBasisChange,
          acquisitionDate: tradeDate,
          asOfDate: tradeDate,
        },
      });
    }
  }

  /**
   * Transform transaction for API response
   */
  private transformTransaction(transaction: any) {
    return {
      id: transaction.id,
      accountId: transaction.accountId,
      account: transaction.account,
      security: transaction.security
        ? {
            id: transaction.security.id,
            symbol: transaction.security.symbol,
            name: transaction.security.name,
          }
        : null,
      transactionType: transaction.transactionType,
      tradeDate: transaction.tradeDate,
      settlementDate: transaction.settlementDate,
      quantity: transaction.quantity ? Number(transaction.quantity) : null,
      price: transaction.price ? Number(transaction.price) : null,
      amount: Number(transaction.amount),
      fees: Number(transaction.fees),
      currency: transaction.currency,
      description: transaction.description,
      source: transaction.source,
      createdAt: transaction.createdAt,
    };
  }
}
