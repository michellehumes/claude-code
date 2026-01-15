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
} from '@nestjs/swagger';
import { ClientService } from './client.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { TenantId } from '../../common/decorators/tenant.decorator';
import { CurrentUser } from '../../common/decorators/user.decorator';

@ApiTags('clients')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('clients')
export class ClientController {
  constructor(private readonly clientService: ClientService) {}

  @Get()
  @ApiOperation({ summary: 'List all clients' })
  @ApiResponse({ status: HttpStatus.OK })
  async findAll(
    @TenantId() tenantId: string,
    @Query('page') page?: number,
    @Query('limit') limit?: number,
    @Query('search') search?: string,
  ) {
    return this.clientService.findAll(tenantId, { page, limit, search });
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get client by ID' })
  @ApiResponse({ status: HttpStatus.OK })
  async findOne(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
  ) {
    return this.clientService.findOne(tenantId, id);
  }

  @Post()
  @ApiOperation({ summary: 'Create a new client' })
  @ApiResponse({ status: HttpStatus.CREATED })
  async create(
    @TenantId() tenantId: string,
    @CurrentUser() user: { id: string },
    @Body() createClientDto: any,
  ) {
    return this.clientService.create(tenantId, createClientDto, user.id);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update a client' })
  @ApiResponse({ status: HttpStatus.OK })
  async update(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @CurrentUser() user: { id: string },
    @Body() updateClientDto: any,
  ) {
    return this.clientService.update(tenantId, id, updateClientDto, user.id);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete a client' })
  @ApiResponse({ status: HttpStatus.NO_CONTENT })
  async remove(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @CurrentUser() user: { id: string },
  ) {
    return this.clientService.remove(tenantId, id, user.id);
  }

  @Get(':id/accounts')
  @ApiOperation({ summary: 'Get client accounts' })
  @ApiResponse({ status: HttpStatus.OK })
  async getAccounts(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
  ) {
    return this.clientService.getClientAccounts(tenantId, id);
  }

  @Get(':id/performance')
  @ApiOperation({ summary: 'Get client aggregate performance' })
  @ApiResponse({ status: HttpStatus.OK })
  async getPerformance(
    @TenantId() tenantId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
  ) {
    return this.clientService.getClientPerformance(tenantId, id, {
      startDate: startDate ? new Date(startDate) : undefined,
      endDate: endDate ? new Date(endDate) : undefined,
    });
  }
}
