import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import {
  IsString,
  IsOptional,
  IsEnum,
  IsUUID,
  IsDateString,
  IsObject,
  IsNumber,
  Min,
  Max,
} from 'class-validator';
import { Type } from 'class-transformer';

// Enums
export enum PortfolioType {
  MODEL = 'MODEL',
  COMPOSITE = 'COMPOSITE',
  ACCOUNT = 'ACCOUNT',
  HOUSEHOLD = 'HOUSEHOLD',
}

// Create Portfolio DTO
export class CreatePortfolioDto {
  @ApiProperty({ description: 'Portfolio name' })
  @IsString()
  name: string;

  @ApiProperty({ enum: PortfolioType, description: 'Type of portfolio' })
  @IsEnum(PortfolioType)
  portfolioType: PortfolioType;

  @ApiPropertyOptional({ description: 'Benchmark ID' })
  @IsOptional()
  @IsUUID()
  benchmarkId?: string;

  @ApiPropertyOptional({ description: 'Inception date' })
  @IsOptional()
  @IsDateString()
  inceptionDate?: string;

  @ApiPropertyOptional({ description: 'Portfolio settings' })
  @IsOptional()
  @IsObject()
  settings?: Record<string, any>;
}

// Update Portfolio DTO
export class UpdatePortfolioDto extends PartialType(CreatePortfolioDto) {}

// Portfolio List Query DTO
export class PortfolioListQueryDto {
  @ApiPropertyOptional({ default: 1 })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(1)
  page?: number;

  @ApiPropertyOptional({ default: 20 })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(1)
  @Max(100)
  limit?: number;

  @ApiPropertyOptional({ description: 'Search by name' })
  @IsOptional()
  @IsString()
  search?: string;

  @ApiPropertyOptional({ enum: PortfolioType })
  @IsOptional()
  @IsEnum(PortfolioType)
  type?: PortfolioType;

  @ApiPropertyOptional({ default: 'name' })
  @IsOptional()
  @IsString()
  sortBy?: string;

  @ApiPropertyOptional({ enum: ['asc', 'desc'], default: 'asc' })
  @IsOptional()
  @IsEnum(['asc', 'desc'])
  sortOrder?: 'asc' | 'desc';
}

// Portfolio Response DTO
export class PortfolioResponseDto {
  @ApiProperty()
  id: string;

  @ApiProperty()
  name: string;

  @ApiProperty({ enum: PortfolioType })
  portfolioType: PortfolioType;

  @ApiPropertyOptional()
  inceptionDate?: Date;

  @ApiPropertyOptional()
  benchmark?: {
    id: string;
    name: string;
    symbol: string;
  };

  @ApiPropertyOptional()
  accounts?: Array<{
    id: string;
    accountNumber: string;
    accountType: string;
    weight?: number;
  }>;

  @ApiPropertyOptional()
  currentValue?: number;

  @ApiPropertyOptional()
  performance?: {
    dailyReturn?: number;
    mtdReturn?: number;
    ytdReturn?: number;
    inceptionReturn?: number;
  };

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;
}

// Portfolio Performance DTO
export class PortfolioPerformanceDto {
  @ApiProperty()
  portfolioId: string;

  @ApiProperty()
  startDate: Date;

  @ApiProperty()
  endDate: Date;

  @ApiProperty()
  returns: {
    totalReturn: number;
    annualizedReturn: number;
    dailyReturns?: number[];
    monthlyReturns?: number[];
  };

  @ApiProperty()
  risk: {
    volatility: number;
    sharpeRatio: number;
    maxDrawdown: number;
    beta?: number;
  };

  @ApiPropertyOptional()
  benchmarkComparison?: {
    benchmarkReturn: number;
    alpha: number;
    trackingError: number;
    informationRatio: number;
  };
}

// Portfolio Holdings DTO
export class PortfolioHoldingsDto {
  @ApiProperty()
  portfolioId: string;

  @ApiProperty()
  asOfDate: Date;

  @ApiProperty()
  totalValue: number;

  @ApiProperty()
  holdings: Array<{
    securityId: string;
    symbol: string;
    name: string;
    assetClass: string;
    quantity: number;
    price: number;
    marketValue: number;
    weight: number;
    costBasis?: number;
    unrealizedGain?: number;
    unrealizedGainPercent?: number;
  }>;

  @ApiPropertyOptional()
  allocation?: {
    byAssetClass: Array<{ name: string; value: number; weight: number }>;
    bySector?: Array<{ name: string; value: number; weight: number }>;
    byGeography?: Array<{ name: string; value: number; weight: number }>;
  };
}

// Add Accounts DTO
export class AddAccountsDto {
  @ApiProperty({ type: [String], description: 'Array of account IDs' })
  @IsUUID('4', { each: true })
  accountIds: string[];
}
