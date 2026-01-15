import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: {
    timestamp: string;
    requestId?: string;
    pagination?: {
      page: number;
      limit: number;
      total: number;
      totalPages: number;
    };
  };
}

@Injectable()
export class TransformInterceptor<T>
  implements NestInterceptor<T, ApiResponse<T>>
{
  intercept(
    context: ExecutionContext,
    next: CallHandler,
  ): Observable<ApiResponse<T>> {
    const request = context.switchToHttp().getRequest();

    return next.handle().pipe(
      map((data) => {
        // If response already has the expected structure, return as-is
        if (data && typeof data === 'object' && 'success' in data) {
          return data;
        }

        // Handle paginated responses
        if (data && typeof data === 'object' && 'items' in data && 'total' in data) {
          return {
            success: true,
            data: data.items,
            meta: {
              timestamp: new Date().toISOString(),
              requestId: request.headers['x-request-id'],
              pagination: {
                page: data.page || 1,
                limit: data.limit || 20,
                total: data.total,
                totalPages: Math.ceil(data.total / (data.limit || 20)),
              },
            },
          };
        }

        return {
          success: true,
          data,
          meta: {
            timestamp: new Date().toISOString(),
            requestId: request.headers['x-request-id'],
          },
        };
      }),
    );
  }
}
