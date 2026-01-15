import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
  HttpStatus,
  ParseUUIDPipe,
} from '@nestjs/common';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiParam,
  ApiQuery,
} from '@nestjs/swagger';
import { PortfolioService } from './portfolio.service';
import { PositionService } from './position.service';
import { ValuationService } from './valuation.service';
import {
  CreatePortfolioDto,
  UpdatePortfolioDto,
  PortfolioResponseDto,
  PortfolioListQueryDto,
  PortfolioPerformanceDto,
  PortfolioHoldingsDto,
} from './dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { TenantId } from '../../common/decorators/tenant.decorator';
import { CurrentUser } from '../../common/decorators/user.decorator';

@ApiTags('portfolios')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('portfolios')
export class PortfolioController {
  constructor(
    private readonly portfolioService: PortfolioService,
    private readonly positionService: PositionService,
    private readonly valuationService: ValuationService,
  ) {}

  @Get()
  @ApiOperation({ summary: 'List all portfolios' })
  @ApiResponse({ status: HttpStatus.OK, type: [PortfolioResponseDto] })
  @ApiQuery({ name: 'page', required: false, type: Number })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  @ApiQuery({ name: 'search', required: false, type: String })
  @ApiQuery({ name: 'type', required: false, enum: ['MODEL', 'COMPOSITE', 'ACCOUNT', 'HOUSEHOLD'] })
  async findAll(
    @TenantId() tenantId: string,
    @Query() query: PortfolioListQueryDto,
  ) {
    return this.portfolioService.findAll(tenantId, query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get portfolio by ID' })
  @ApiParam({ name: 'id', type: String })
  @ApiResponse({ status: HttpStatus.OK, type: PortfolioResponseDto })
  @ApiResponse({ status: HttpStatus.NOT_FOUND, description: 'Portfolio not found' })
  async findOne(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
  ) {
    return this.portfolioService.findOne(tenantId, id);
  }

  @Post()
  @ApiOperation({ summary: 'Create a new portfolio' })
  @ApiResponse({ status: HttpStatus.CREATED, type: PortfolioResponseDto })
  @ApiResponse({ status: HttpStatus.BAD_REQUEST, description: 'Invalid input' })
  async create(
    @TenantId() tenantId: string,
    @CurrentUser() user: { id: string },
    @Body() createPortfolioDto: CreatePortfolioDto,
  ) {
    return this.portfolioService.create(tenantId, createPortfolioDto, user.id);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update a portfolio' })
  @ApiParam({ name: 'id', type: String })
  @ApiResponse({ status: HttpStatus.OK, type: PortfolioResponseDto })
  @ApiResponse({ status: HttpStatus.NOT_FOUND, description: 'Portfolio not found' })
  async update(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @CurrentUser() user: { id: string },
    @Body() updatePortfolioDto: UpdatePortfolioDto,
  ) {
    return this.portfolioService.update(tenantId, id, updatePortfolioDto, user.id);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete a portfolio' })
  @ApiParam({ name: 'id', type: String })
  @ApiResponse({ status: HttpStatus.NO_CONTENT })
  @ApiResponse({ status: HttpStatus.NOT_FOUND, description: 'Portfolio not found' })
  async remove(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @CurrentUser() user: { id: string },
  ) {
    return this.portfolioService.remove(tenantId, id, user.id);
  }

  // Performance endpoints
  @Get(':id/performance')
  @ApiOperation({ summary: 'Get portfolio performance metrics' })
  @ApiParam({ name: 'id', type: String })
  @ApiQuery({ name: 'startDate', required: false, type: String })
  @ApiQuery({ name: 'endDate', required: false, type: String })
  @ApiQuery({ name: 'frequency', required: false, enum: ['daily', 'monthly', 'quarterly'] })
  @ApiResponse({ status: HttpStatus.OK, type: PortfolioPerformanceDto })
  async getPerformance(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
    @Query('frequency') frequency?: 'daily' | 'monthly' | 'quarterly',
  ) {
    return this.valuationService.getPerformance(tenantId, id, {
      startDate: startDate ? new Date(startDate) : undefined,
      endDate: endDate ? new Date(endDate) : undefined,
      frequency,
    });
  }

  // Holdings endpoints
  @Get(':id/holdings')
  @ApiOperation({ summary: 'Get portfolio holdings' })
  @ApiParam({ name: 'id', type: String })
  @ApiQuery({ name: 'asOfDate', required: false, type: String })
  @ApiQuery({ name: 'groupBy', required: false, enum: ['security', 'assetClass', 'sector'] })
  @ApiResponse({ status: HttpStatus.OK, type: PortfolioHoldingsDto })
  async getHoldings(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Query('asOfDate') asOfDate?: string,
    @Query('groupBy') groupBy?: 'security' | 'assetClass' | 'sector',
  ) {
    return this.positionService.getPortfolioHoldings(tenantId, id, {
      asOfDate: asOfDate ? new Date(asOfDate) : new Date(),
      groupBy,
    });
  }

  // Asset allocation
  @Get(':id/allocation')
  @ApiOperation({ summary: 'Get portfolio asset allocation' })
  @ApiParam({ name: 'id', type: String })
  @ApiQuery({ name: 'asOfDate', required: false, type: String })
  async getAllocation(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Query('asOfDate') asOfDate?: string,
  ) {
    return this.positionService.getAssetAllocation(tenantId, id, {
      asOfDate: asOfDate ? new Date(asOfDate) : new Date(),
    });
  }

  // Transactions
  @Get(':id/transactions')
  @ApiOperation({ summary: 'Get portfolio transactions' })
  @ApiParam({ name: 'id', type: String })
  @ApiQuery({ name: 'startDate', required: false, type: String })
  @ApiQuery({ name: 'endDate', required: false, type: String })
  @ApiQuery({ name: 'type', required: false, type: String })
  async getTransactions(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
    @Query('type') type?: string,
  ) {
    return this.portfolioService.getTransactions(tenantId, id, {
      startDate: startDate ? new Date(startDate) : undefined,
      endDate: endDate ? new Date(endDate) : undefined,
      type,
    });
  }
}
