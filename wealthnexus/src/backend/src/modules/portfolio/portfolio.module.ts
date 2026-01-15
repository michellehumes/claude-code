import { Module } from '@nestjs/common';
import { PortfolioController } from './portfolio.controller';
import { PortfolioService } from './portfolio.service';
import { PositionService } from './position.service';
import { TransactionService } from './transaction.service';
import { ValuationService } from './valuation.service';

@Module({
  controllers: [PortfolioController],
  providers: [
    PortfolioService,
    PositionService,
    TransactionService,
    ValuationService,
  ],
  exports: [PortfolioService, PositionService, ValuationService],
})
export class PortfolioModule {}
