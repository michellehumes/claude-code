import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { PrismaService } from '../../database/prisma.service';
import { Prisma } from '@prisma/client';

@Injectable()
export class ClientService {
  private readonly logger = new Logger(ClientService.name);

  constructor(private readonly prisma: PrismaService) {}

  async findAll(
    tenantId: string,
    options: { page?: number; limit?: number; search?: string },
  ) {
    const { page = 1, limit = 20, search } = options;
    const skip = (page - 1) * limit;

    const where: Prisma.ClientWhereInput = {
      tenantId,
      ...(search && {
        OR: [
          { name: { contains: search, mode: 'insensitive' } },
          { email: { contains: search, mode: 'insensitive' } },
        ],
      }),
    };

    const [items, total] = await Promise.all([
      this.prisma.client.findMany({
        where,
        skip,
        take: limit,
        orderBy: { name: 'asc' },
        include: {
          _count: { select: { accounts: true } },
        },
      }),
      this.prisma.client.count({ where }),
    ]);

    return { items, total, page, limit };
  }

  async findOne(tenantId: string, id: string) {
    const client = await this.prisma.client.findFirst({
      where: { id, tenantId },
      include: {
        accounts: {
          include: {
            custodian: { select: { id: true, name: true } },
          },
        },
        householdMembers: {
          include: {
            household: true,
          },
        },
      },
    });

    if (!client) {
      throw new NotFoundException(`Client with ID ${id} not found`);
    }

    return client;
  }

  async create(tenantId: string, dto: any, userId: string) {
    const client = await this.prisma.client.create({
      data: {
        tenantId,
        name: dto.name,
        type: dto.type,
        email: dto.email,
        phone: dto.phone,
        address: dto.address,
        kycStatus: dto.kycStatus,
        riskProfile: dto.riskProfile,
        inceptionDate: dto.inceptionDate ? new Date(dto.inceptionDate) : null,
        metadata: dto.metadata || {},
      },
    });

    await this.logAudit(tenantId, userId, 'CREATE', 'Client', client.id);
    return client;
  }

  async update(tenantId: string, id: string, dto: any, userId: string) {
    const existing = await this.findOne(tenantId, id);

    const client = await this.prisma.client.update({
      where: { id },
      data: {
        ...(dto.name && { name: dto.name }),
        ...(dto.type && { type: dto.type }),
        ...(dto.email !== undefined && { email: dto.email }),
        ...(dto.phone !== undefined && { phone: dto.phone }),
        ...(dto.address !== undefined && { address: dto.address }),
        ...(dto.kycStatus && { kycStatus: dto.kycStatus }),
        ...(dto.riskProfile && { riskProfile: dto.riskProfile }),
        ...(dto.metadata && { metadata: dto.metadata }),
      },
    });

    await this.logAudit(tenantId, userId, 'UPDATE', 'Client', id, {
      before: existing,
      after: client,
    });

    return client;
  }

  async remove(tenantId: string, id: string, userId: string) {
    await this.findOne(tenantId, id);

    await this.prisma.client.delete({ where: { id } });

    await this.logAudit(tenantId, userId, 'DELETE', 'Client', id);
  }

  async getClientAccounts(tenantId: string, clientId: string) {
    await this.findOne(tenantId, clientId);

    return this.prisma.account.findMany({
      where: { tenantId, clientId },
      include: {
        custodian: { select: { id: true, name: true, code: true } },
      },
    });
  }

  async getClientPerformance(
    tenantId: string,
    clientId: string,
    options: { startDate?: Date; endDate?: Date },
  ) {
    await this.findOne(tenantId, clientId);

    // Get all accounts for this client
    const accounts = await this.prisma.account.findMany({
      where: { tenantId, clientId },
      select: { id: true },
    });

    if (accounts.length === 0) {
      return { totalValue: 0, performance: null };
    }

    // This would aggregate performance across all client accounts
    // For now, return placeholder data
    return {
      clientId,
      totalAccounts: accounts.length,
      totalValue: 0, // Would be calculated from positions
      performance: {
        mtdReturn: 0,
        ytdReturn: 0,
        inceptionReturn: 0,
      },
    };
  }

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
