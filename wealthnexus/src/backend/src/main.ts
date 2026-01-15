import { NestFactory } from '@nestjs/core';
import { ValidationPipe, VersioningType } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { ConfigService } from '@nestjs/config';
import * as compression from 'compression';
import helmet from 'helmet';
import { AppModule } from './app.module';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';
import { TransformInterceptor } from './common/interceptors/transform.interceptor';
import { LoggingInterceptor } from './common/interceptors/logging.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['error', 'warn', 'log', 'debug', 'verbose'],
  });

  const configService = app.get(ConfigService);

  // Security
  app.use(helmet());
  app.use(compression());

  // CORS
  app.enableCors({
    origin: configService.get('CORS_ORIGINS', 'http://localhost:3000').split(','),
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Tenant-ID', 'X-Request-ID'],
  });

  // API Versioning
  app.enableVersioning({
    type: VersioningType.URI,
    prefix: 'v',
    defaultVersion: '1',
  });

  // Global prefix
  app.setGlobalPrefix('api');

  // Global pipes
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  );

  // Global filters
  app.useGlobalFilters(new HttpExceptionFilter());

  // Global interceptors
  app.useGlobalInterceptors(
    new LoggingInterceptor(),
    new TransformInterceptor(),
  );

  // Swagger Documentation
  const swaggerConfig = new DocumentBuilder()
    .setTitle('WealthNexus API')
    .setDescription(`
      WealthNexus API - Next-Generation Wealth Management Platform

      ## Overview
      This API provides comprehensive wealth management capabilities including:
      - Portfolio Management
      - Client Management
      - Performance Analytics
      - Trading & Rebalancing
      - Reporting
      - Billing

      ## Authentication
      All endpoints require JWT authentication. Include the token in the Authorization header:
      \`Authorization: Bearer <token>\`

      ## Multi-Tenancy
      Include the tenant ID in requests:
      \`X-Tenant-ID: <tenant-id>\`
    `)
    .setVersion('1.0')
    .addBearerAuth()
    .addApiKey({ type: 'apiKey', name: 'X-Tenant-ID', in: 'header' }, 'tenant-id')
    .addTag('auth', 'Authentication endpoints')
    .addTag('clients', 'Client management')
    .addTag('portfolios', 'Portfolio management')
    .addTag('accounts', 'Account management')
    .addTag('positions', 'Position management')
    .addTag('transactions', 'Transaction management')
    .addTag('analytics', 'Performance and risk analytics')
    .addTag('reports', 'Report generation')
    .addTag('trading', 'Trading and rebalancing')
    .addTag('billing', 'Billing and invoicing')
    .addTag('alternatives', 'Alternative investments')
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('api/docs', app, document);

  // Start server
  const port = configService.get('PORT', 3001);
  await app.listen(port);

  console.log(`
  ╦ ╦┌─┐┌─┐┬ ┌┬┐┬ ┬╔╗╔┌─┐─┐ ┬┬ ┬┌─┐
  ║║║├┤ ├─┤│  │ ├─┤║║║├┤ ┌┴┬┘│ │└─┐
  ╚╩╝└─┘┴ ┴┴─┘┴ ┴ ┴╝╚╝└─┘┴ └─└─┘└─┘

  🚀 WealthNexus API Server
  📍 Running on: http://localhost:${port}
  📚 API Docs: http://localhost:${port}/api/docs
  🌍 Environment: ${configService.get('NODE_ENV', 'development')}
  `);
}

bootstrap();
