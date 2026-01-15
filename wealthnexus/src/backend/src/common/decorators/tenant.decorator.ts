import { createParamDecorator, ExecutionContext, BadRequestException } from '@nestjs/common';

/**
 * Extract tenant ID from request
 * Tries in order: JWT payload, X-Tenant-ID header, query param
 */
export const TenantId = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): string => {
    const request = ctx.switchToHttp().getRequest();

    // First, try from authenticated user (JWT payload)
    if (request.user?.tenantId) {
      return request.user.tenantId;
    }

    // Second, try from header
    const headerTenantId = request.headers['x-tenant-id'];
    if (headerTenantId) {
      return headerTenantId;
    }

    // Third, try from query param
    const queryTenantId = request.query.tenantId;
    if (queryTenantId) {
      return queryTenantId;
    }

    throw new BadRequestException('Tenant ID is required');
  },
);
