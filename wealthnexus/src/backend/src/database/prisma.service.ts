import { Injectable, OnModuleInit, OnModuleDestroy, Logger } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(PrismaService.name);

  constructor() {
    super({
      log: [
        { emit: 'event', level: 'query' },
        { emit: 'stdout', level: 'info' },
        { emit: 'stdout', level: 'warn' },
        { emit: 'stdout', level: 'error' },
      ],
    });
  }

  async onModuleInit() {
    await this.$connect();
    this.logger.log('Database connection established');

    // Query logging in development
    if (process.env.NODE_ENV === 'development') {
      this.$on('query' as never, (e: { query: string; duration: number }) => {
        this.logger.debug(`Query: ${e.query}`);
        this.logger.debug(`Duration: ${e.duration}ms`);
      });
    }
  }

  async onModuleDestroy() {
    await this.$disconnect();
    this.logger.log('Database connection closed');
  }

  /**
   * Execute operations within a transaction
   */
  async executeInTransaction<T>(
    operations: (prisma: PrismaClient) => Promise<T>,
  ): Promise<T> {
    return this.$transaction(async (prisma) => {
      return operations(prisma as PrismaClient);
    });
  }

  /**
   * Soft delete helper - adds deletedAt timestamp
   */
  async softDelete(model: string, id: string): Promise<void> {
    await (this as any)[model].update({
      where: { id },
      data: { deletedAt: new Date() },
    });
  }
}
