# WealthNexus Technical Architecture

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [Infrastructure](#infrastructure)
4. [Backend Services](#backend-services)
5. [Data Architecture](#data-architecture)
6. [Frontend Architecture](#frontend-architecture)
7. [Security Architecture](#security-architecture)
8. [Integration Layer](#integration-layer)
9. [AI/ML Platform](#aiml-platform)
10. [DevOps & Observability](#devops--observability)

---

## System Overview

### High-Level Architecture

```
                                   ┌─────────────────────────────────────────┐
                                   │             CDN (CloudFlare)             │
                                   └─────────────────────────────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Load Balancer (AWS ALB)                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────────────┐
                    │                                 │                              │
                    ▼                                 ▼                              ▼
         ┌──────────────────┐              ┌──────────────────┐           ┌──────────────────┐
         │   Web Frontend   │              │   Mobile BFF     │           │   API Gateway    │
         │   (Next.js)      │              │                  │           │   (Kong)         │
         └──────────────────┘              └──────────────────┘           └──────────────────┘
                    │                                 │                              │
                    └─────────────────────────────────┼──────────────────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    Service Mesh (Istio)                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│   │  Portfolio  │  │   Client    │  │  Reporting  │  │   Trading   │  │  Analytics  │     │
│   │  Service    │  │   Service   │  │   Service   │  │   Service   │  │   Service   │     │
│   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│   │   Billing   │  │  Compliance │  │   Data      │  │    Auth     │  │  Notification│    │
│   │   Service   │  │   Service   │  │   Ingestion │  │   Service   │  │   Service   │     │
│   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                                              │
│   ┌─────────────┐  ┌─────────────┐                                                          │
│   │  AI/ML      │  │  Document   │                                                          │
│   │  Service    │  │  Service    │                                                          │
│   └─────────────┘  └─────────────┘                                                          │
│                                                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────────────┐
                    │                                 │                              │
                    ▼                                 ▼                              ▼
         ┌──────────────────┐              ┌──────────────────┐           ┌──────────────────┐
         │   PostgreSQL     │              │   TimescaleDB    │           │   Redis Cluster  │
         │   (Primary)      │              │   (Time Series)  │           │   (Cache)        │
         └──────────────────┘              └──────────────────┘           └──────────────────┘
                    │                                                              │
                    ▼                                                              ▼
         ┌──────────────────┐              ┌──────────────────┐           ┌──────────────────┐
         │   Elasticsearch  │              │   S3             │           │   Kafka          │
         │   (Search)       │              │   (Documents)    │           │   (Events)       │
         └──────────────────┘              └──────────────────┘           └──────────────────┘
```

---

## Architecture Principles

### Core Principles

1. **API-First Design** - All functionality exposed via well-documented APIs
2. **Microservices** - Loosely coupled, independently deployable services
3. **Event-Driven** - Asynchronous communication for scalability
4. **Security by Design** - Zero-trust architecture, encryption everywhere
5. **Cloud-Native** - Containerized, orchestrated, auto-scaling
6. **Multi-Tenancy** - Single codebase, isolated tenant data
7. **Observability** - Comprehensive logging, metrics, tracing
8. **Fault Tolerance** - Graceful degradation, circuit breakers

### Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Frontend** | Next.js 14, React 18, TypeScript | SSR, performance, type safety |
| **Mobile** | React Native | Code sharing, native performance |
| **API Gateway** | Kong | Rate limiting, auth, routing |
| **Backend** | Node.js (NestJS), Python (FastAPI) | Performance + ML capabilities |
| **Database** | PostgreSQL 16, TimescaleDB | Reliability, time-series support |
| **Cache** | Redis Cluster | Performance, pub/sub |
| **Search** | Elasticsearch | Full-text search, analytics |
| **Message Queue** | Apache Kafka | Event streaming, reliability |
| **Object Storage** | AWS S3 | Documents, reports |
| **Container** | Docker, Kubernetes | Orchestration, scaling |
| **Service Mesh** | Istio | Traffic management, security |
| **ML Platform** | AWS SageMaker, PyTorch | Model training, serving |

---

## Infrastructure

### Cloud Architecture (AWS)

```
AWS Multi-Region Architecture
═════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                           Route 53 (DNS)                                 │
│                    Latency-based routing, health checks                  │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           │                                                    │
           ▼                                                    ▼
┌─────────────────────────────┐              ┌─────────────────────────────┐
│     US-EAST-1 (Primary)     │              │     US-WEST-2 (Secondary)   │
├─────────────────────────────┤              ├─────────────────────────────┤
│                             │              │                             │
│  ┌───────────────────────┐  │              │  ┌───────────────────────┐  │
│  │        VPC            │  │              │  │        VPC            │  │
│  │  ┌─────────────────┐  │  │              │  │  ┌─────────────────┐  │  │
│  │  │ Public Subnet   │  │  │              │  │  │ Public Subnet   │  │  │
│  │  │ - ALB           │  │  │              │  │  │ - ALB           │  │  │
│  │  │ - NAT Gateway   │  │  │              │  │  │ - NAT Gateway   │  │  │
│  │  └─────────────────┘  │  │              │  │  └─────────────────┘  │  │
│  │  ┌─────────────────┐  │  │              │  │  ┌─────────────────┐  │  │
│  │  │ Private Subnet  │  │  │              │  │  │ Private Subnet  │  │  │
│  │  │ - EKS Cluster   │  │  │              │  │  │ - EKS Cluster   │  │  │
│  │  │ - RDS Primary   │  │  │              │  │  │ - RDS Replica   │  │  │
│  │  │ - ElastiCache   │  │  │              │  │  │ - ElastiCache   │  │  │
│  │  └─────────────────┘  │  │              │  │  └─────────────────┘  │  │
│  └───────────────────────┘  │              │  └───────────────────────┘  │
│                             │              │                             │
│  ┌───────────────────────┐  │              │  ┌───────────────────────┐  │
│  │      S3 Buckets       │◄─┼──Replication─┼──│      S3 Buckets       │  │
│  └───────────────────────┘  │              │  └───────────────────────┘  │
│                             │              │                             │
└─────────────────────────────┘              └─────────────────────────────┘
                │                                           │
                └──────────────────┬────────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │   Global Accelerator        │
                    │   (Performance optimization)│
                    └─────────────────────────────┘
```

### Kubernetes Cluster Layout

```yaml
# Namespace Organization
namespaces:
  - production
  - staging
  - monitoring
  - istio-system
  - cert-manager
  - logging

# Node Groups
nodeGroups:
  - name: general
    instanceType: m6i.2xlarge
    minSize: 3
    maxSize: 20
    labels:
      workload: general

  - name: compute
    instanceType: c6i.4xlarge
    minSize: 2
    maxSize: 15
    labels:
      workload: compute

  - name: memory
    instanceType: r6i.2xlarge
    minSize: 2
    maxSize: 10
    labels:
      workload: memory

  - name: ml
    instanceType: g4dn.xlarge
    minSize: 1
    maxSize: 5
    labels:
      workload: ml
    taints:
      - key: nvidia.com/gpu
        effect: NoSchedule
```

---

## Backend Services

### Service Catalog

| Service | Responsibility | Language | Database |
|---------|---------------|----------|----------|
| **portfolio-service** | Portfolio management, holdings | Node.js/NestJS | PostgreSQL |
| **client-service** | Client/account management | Node.js/NestJS | PostgreSQL |
| **analytics-service** | Performance, risk calculations | Python/FastAPI | TimescaleDB |
| **reporting-service** | Report generation | Python/FastAPI | PostgreSQL |
| **trading-service** | Order management, execution | Node.js/NestJS | PostgreSQL |
| **billing-service** | Fee calculation, invoicing | Node.js/NestJS | PostgreSQL |
| **compliance-service** | Rule checking, alerts | Node.js/NestJS | PostgreSQL |
| **data-ingestion** | Data feeds, aggregation | Python/FastAPI | PostgreSQL |
| **auth-service** | Authentication, authorization | Node.js/NestJS | PostgreSQL |
| **notification-service** | Emails, push, SMS | Node.js/NestJS | Redis |
| **ai-service** | NLP, ML predictions | Python/FastAPI | - |
| **document-service** | Doc storage, parsing | Python/FastAPI | S3, PostgreSQL |

### Service Communication

```
Communication Patterns
══════════════════════

Synchronous (REST/gRPC):
├── Client queries → API Gateway → Services
├── Inter-service calls for immediate responses
└── Health checks

Asynchronous (Kafka Events):
├── portfolio.position.updated
├── trade.executed
├── report.generated
├── compliance.violation.detected
├── market.data.received
├── document.processed
└── notification.requested

Event Schema Example:
{
  "eventId": "uuid",
  "eventType": "portfolio.position.updated",
  "timestamp": "2026-01-15T10:30:00Z",
  "tenantId": "tenant-123",
  "payload": {
    "portfolioId": "portfolio-456",
    "securityId": "AAPL",
    "previousQuantity": 100,
    "newQuantity": 150,
    "source": "trade"
  },
  "metadata": {
    "correlationId": "corr-789",
    "userId": "user-012"
  }
}
```

### Portfolio Service Detail

```
portfolio-service/
├── src/
│   ├── modules/
│   │   ├── portfolio/
│   │   │   ├── portfolio.controller.ts
│   │   │   ├── portfolio.service.ts
│   │   │   ├── portfolio.repository.ts
│   │   │   ├── portfolio.entity.ts
│   │   │   └── dto/
│   │   │       ├── create-portfolio.dto.ts
│   │   │       ├── update-portfolio.dto.ts
│   │   │       └── portfolio-response.dto.ts
│   │   ├── position/
│   │   │   ├── position.controller.ts
│   │   │   ├── position.service.ts
│   │   │   └── position.entity.ts
│   │   ├── transaction/
│   │   │   ├── transaction.controller.ts
│   │   │   ├── transaction.service.ts
│   │   │   └── transaction.entity.ts
│   │   └── valuation/
│   │       ├── valuation.service.ts
│   │       └── pricing.service.ts
│   ├── common/
│   │   ├── interceptors/
│   │   ├── guards/
│   │   ├── filters/
│   │   └── decorators/
│   ├── config/
│   └── main.ts
├── test/
├── Dockerfile
└── package.json
```

---

## Data Architecture

### Database Schema (Core Tables)

```sql
-- Tenant & Organization
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}',
    subscription_tier VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL,
    permissions JSONB DEFAULT '[]',
    mfa_enabled BOOLEAN DEFAULT false,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

-- Client Management
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    external_id VARCHAR(100),
    type VARCHAR(50) NOT NULL, -- individual, trust, entity, etc.
    name VARCHAR(255) NOT NULL,
    tax_id_encrypted BYTEA,
    contact_info JSONB DEFAULT '{}',
    kyc_status VARCHAR(50),
    risk_profile VARCHAR(50),
    inception_date DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, external_id)
);

CREATE TABLE households (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    primary_contact_id UUID REFERENCES clients(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE household_members (
    household_id UUID REFERENCES households(id),
    client_id UUID REFERENCES clients(id),
    relationship VARCHAR(100),
    PRIMARY KEY (household_id, client_id)
);

-- Accounts & Portfolios
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    client_id UUID REFERENCES clients(id),
    account_number VARCHAR(100),
    account_type VARCHAR(50) NOT NULL, -- brokerage, ira, trust, etc.
    custodian_id UUID,
    status VARCHAR(50) DEFAULT 'active',
    tax_status VARCHAR(50), -- taxable, tax-deferred, tax-exempt
    inception_date DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, account_number)
);

CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    portfolio_type VARCHAR(50), -- model, composite, account
    benchmark_id UUID,
    inception_date DATE,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE portfolio_accounts (
    portfolio_id UUID REFERENCES portfolios(id),
    account_id UUID REFERENCES accounts(id),
    weight DECIMAL(10, 6),
    PRIMARY KEY (portfolio_id, account_id)
);

-- Securities & Holdings
CREATE TABLE securities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(50),
    cusip VARCHAR(9),
    isin VARCHAR(12),
    sedol VARCHAR(7),
    name VARCHAR(255) NOT NULL,
    security_type VARCHAR(50) NOT NULL,
    asset_class VARCHAR(50),
    sub_asset_class VARCHAR(50),
    currency VARCHAR(3) DEFAULT 'USD',
    exchange VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    security_id UUID REFERENCES securities(id),
    quantity DECIMAL(20, 8) NOT NULL,
    cost_basis DECIMAL(20, 4),
    acquisition_date DATE,
    lot_id VARCHAR(100),
    as_of_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(account_id, security_id, lot_id, as_of_date)
);

-- Transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    account_id UUID REFERENCES accounts(id),
    security_id UUID REFERENCES securities(id),
    transaction_type VARCHAR(50) NOT NULL,
    trade_date DATE NOT NULL,
    settlement_date DATE,
    quantity DECIMAL(20, 8),
    price DECIMAL(20, 8),
    amount DECIMAL(20, 4) NOT NULL,
    fees DECIMAL(20, 4) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    description TEXT,
    external_id VARCHAR(100),
    source VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Time Series Data (TimescaleDB)
CREATE TABLE market_prices (
    security_id UUID REFERENCES securities(id),
    price_date DATE NOT NULL,
    open_price DECIMAL(20, 8),
    high_price DECIMAL(20, 8),
    low_price DECIMAL(20, 8),
    close_price DECIMAL(20, 8),
    adjusted_close DECIMAL(20, 8),
    volume BIGINT,
    source VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (security_id, price_date)
);

SELECT create_hypertable('market_prices', 'price_date');

CREATE TABLE portfolio_valuations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    portfolio_id UUID REFERENCES portfolios(id),
    valuation_date DATE NOT NULL,
    market_value DECIMAL(20, 4) NOT NULL,
    cash_value DECIMAL(20, 4),
    accrued_income DECIMAL(20, 4),
    total_value DECIMAL(20, 4) NOT NULL,
    daily_return DECIMAL(12, 8),
    mtd_return DECIMAL(12, 8),
    ytd_return DECIMAL(12, 8),
    inception_return DECIMAL(12, 8),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(portfolio_id, valuation_date)
);

SELECT create_hypertable('portfolio_valuations', 'valuation_date');

-- Alternative Investments
CREATE TABLE alternative_investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    investment_type VARCHAR(50) NOT NULL, -- pe, vc, hedge_fund, real_estate, etc.
    manager_name VARCHAR(255),
    vintage_year INTEGER,
    commitment_amount DECIMAL(20, 4),
    called_amount DECIMAL(20, 4) DEFAULT 0,
    distributed_amount DECIMAL(20, 4) DEFAULT 0,
    current_nav DECIMAL(20, 4),
    nav_date DATE,
    currency VARCHAR(3) DEFAULT 'USD',
    documents JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE capital_calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    investment_id UUID REFERENCES alternative_investments(id),
    account_id UUID REFERENCES accounts(id),
    call_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount DECIMAL(20, 4) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    document_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Models & Rebalancing
CREATE TABLE model_portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    target_allocations JSONB NOT NULL,
    rebalance_frequency VARCHAR(50),
    drift_threshold DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE account_model_assignments (
    account_id UUID REFERENCES accounts(id),
    model_id UUID REFERENCES model_portfolios(id),
    assigned_date DATE NOT NULL,
    restrictions JSONB DEFAULT '{}',
    PRIMARY KEY (account_id)
);

-- Billing
CREATE TABLE fee_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    fee_type VARCHAR(50) NOT NULL, -- aum, flat, performance, hybrid
    tiers JSONB NOT NULL,
    billing_frequency VARCHAR(50),
    advance_arrears VARCHAR(50),
    minimum_fee DECIMAL(20, 4),
    maximum_fee DECIMAL(20, 4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    client_id UUID REFERENCES clients(id),
    invoice_number VARCHAR(100) NOT NULL,
    billing_period_start DATE NOT NULL,
    billing_period_end DATE NOT NULL,
    subtotal DECIMAL(20, 4) NOT NULL,
    adjustments DECIMAL(20, 4) DEFAULT 0,
    total DECIMAL(20, 4) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    due_date DATE,
    paid_date DATE,
    line_items JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, invoice_number)
);

-- Audit & Compliance
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID,
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('audit_log', 'timestamp');

-- Indexes for performance
CREATE INDEX idx_positions_account_date ON positions(account_id, as_of_date);
CREATE INDEX idx_transactions_account_date ON transactions(account_id, trade_date);
CREATE INDEX idx_clients_tenant ON clients(tenant_id);
CREATE INDEX idx_accounts_client ON accounts(client_id);
CREATE INDEX idx_portfolios_tenant ON portfolios(tenant_id);
CREATE INDEX idx_audit_tenant_timestamp ON audit_log(tenant_id, timestamp);
```

### Data Flow Architecture

```
Data Ingestion Pipeline
═══════════════════════

                    ┌──────────────────────────────────────────┐
                    │           External Data Sources           │
                    │  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
                    │  │Custodian│ │ Market  │ │  Alt    │    │
                    │  │  Feeds  │ │  Data   │ │ Invest  │    │
                    │  └────┬────┘ └────┬────┘ └────┬────┘    │
                    └───────┼───────────┼───────────┼─────────┘
                            │           │           │
                            ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Data Ingestion Service                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  File Handlers  │  │  API Connectors │  │  Stream Readers │         │
│  │  (SFTP, S3)     │  │  (REST, SOAP)   │  │  (WebSocket)    │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
│           │                    │                    │                   │
│           └────────────────────┼────────────────────┘                   │
│                                ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Data Transformation Layer                     │   │
│  │  • Field Mapping          • Security Master Matching            │   │
│  │  • Data Type Conversion   • Currency Normalization              │   │
│  │  • Validation Rules       • Deduplication                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                │                                        │
│                                ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Data Quality Engine                           │   │
│  │  • Completeness Checks    • Anomaly Detection (ML)              │   │
│  │  • Consistency Validation • Reconciliation                      │   │
│  │  • Business Rule Checks   • Error Flagging                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                │                                        │
└────────────────────────────────┼────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
           ┌────────────┐ ┌────────────┐ ┌────────────┐
           │ PostgreSQL │ │TimescaleDB │ │   Kafka    │
           │ (Current)  │ │(Historical)│ │  (Events)  │
           └────────────┘ └────────────┘ └────────────┘
```

---

## Frontend Architecture

### Application Structure

```
wealthnexus-web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── clients/
│   │   │   ├── portfolios/
│   │   │   ├── trading/
│   │   │   ├── reporting/
│   │   │   ├── billing/
│   │   │   └── settings/
│   │   └── api/               # API Routes
│   ├── components/
│   │   ├── ui/                # Base UI components
│   │   │   ├── Button/
│   │   │   ├── Card/
│   │   │   ├── Table/
│   │   │   ├── Modal/
│   │   │   └── Chart/
│   │   ├── features/          # Feature-specific components
│   │   │   ├── portfolio/
│   │   │   ├── client/
│   │   │   ├── trading/
│   │   │   └── reporting/
│   │   └── layouts/
│   ├── hooks/
│   │   ├── usePortfolio.ts
│   │   ├── useClient.ts
│   │   ├── useAuth.ts
│   │   └── useRealtime.ts
│   ├── lib/
│   │   ├── api/
│   │   ├── utils/
│   │   └── validators/
│   ├── stores/                # Zustand stores
│   │   ├── authStore.ts
│   │   ├── portfolioStore.ts
│   │   └── uiStore.ts
│   ├── styles/
│   └── types/
├── public/
├── tests/
└── package.json
```

### Component Architecture

```
Design System
═════════════

Tokens
├── Colors (Light/Dark themes)
├── Typography (Scale, Fonts)
├── Spacing (4px base unit)
├── Shadows
├── Borders
└── Breakpoints

Atoms
├── Button
├── Input
├── Label
├── Icon
├── Badge
├── Avatar
├── Spinner
└── Tooltip

Molecules
├── FormField
├── SearchInput
├── DataCell
├── Metric Card
├── Navigation Item
├── Alert
└── Toast

Organisms
├── DataTable
├── Chart (Line, Bar, Pie, etc.)
├── NavigationMenu
├── CommandPalette
├── FilterPanel
├── Modal
└── Sidebar

Templates
├── DashboardLayout
├── DetailLayout
├── ListLayout
├── SettingsLayout
└── AuthLayout

Pages
├── Dashboard
├── Client List/Detail
├── Portfolio List/Detail
├── Trading
├── Reporting
├── Billing
└── Settings
```

---

## Security Architecture

### Security Layers

```
Security Architecture
═════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                           Edge Security                                  │
│  • DDoS Protection (CloudFlare)                                         │
│  • Web Application Firewall                                             │
│  • Rate Limiting                                                        │
│  • Bot Detection                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Network Security                                  │
│  • TLS 1.3 Everywhere                                                   │
│  • VPC Isolation                                                        │
│  • Security Groups                                                      │
│  • Private Subnets                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      Application Security                                │
│  • OAuth 2.0 / OIDC Authentication                                      │
│  • JWT Token Management                                                 │
│  • RBAC Authorization                                                   │
│  • Input Validation                                                     │
│  • Output Encoding                                                      │
│  • CSRF Protection                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Data Security                                    │
│  • AES-256 Encryption at Rest                                           │
│  • TLS Encryption in Transit                                            │
│  • Field-Level Encryption (PII)                                         │
│  • Key Management (AWS KMS)                                             │
│  • Data Masking                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Monitoring & Response                              │
│  • SIEM Integration                                                     │
│  • Intrusion Detection                                                  │
│  • Anomaly Detection                                                    │
│  • Incident Response Automation                                         │
│  • Audit Logging                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
┌──────┐          ┌──────────┐          ┌──────────┐          ┌──────────┐
│Client│          │   Auth   │          │   Token  │          │ Resource │
│      │          │  Server  │          │ Validator│          │  Server  │
└──┬───┘          └────┬─────┘          └────┬─────┘          └────┬─────┘
   │                   │                     │                     │
   │  1. Login Request │                     │                     │
   │   (email + pwd)   │                     │                     │
   │──────────────────>│                     │                     │
   │                   │                     │                     │
   │                   │  2. Validate        │                     │
   │                   │     Credentials     │                     │
   │                   │────────────────────>│                     │
   │                   │                     │                     │
   │  3. If MFA enabled│                     │                     │
   │<──────────────────│                     │                     │
   │                   │                     │                     │
   │  4. MFA Code      │                     │                     │
   │──────────────────>│                     │                     │
   │                   │                     │                     │
   │  5. JWT Tokens    │                     │                     │
   │   (access+refresh)│                     │                     │
   │<──────────────────│                     │                     │
   │                   │                     │                     │
   │                   │                     │  6. API Request     │
   │                   │                     │     + Bearer Token  │
   │─────────────────────────────────────────────────────────────>│
   │                   │                     │                     │
   │                   │                     │  7. Validate Token  │
   │                   │                     │<────────────────────│
   │                   │                     │                     │
   │                   │                     │  8. Token Valid +   │
   │                   │                     │     Permissions     │
   │                   │                     │────────────────────>│
   │                   │                     │                     │
   │                                         │  9. API Response    │
   │<─────────────────────────────────────────────────────────────│
   │                   │                     │                     │
```

---

## Integration Layer

### API Gateway Configuration

```yaml
# Kong Gateway Configuration
services:
  - name: portfolio-service
    url: http://portfolio-service:3000
    routes:
      - name: portfolio-api
        paths:
          - /api/v1/portfolios
        plugins:
          - name: rate-limiting
            config:
              minute: 100
              policy: local
          - name: jwt
          - name: request-transformer
            config:
              add:
                headers:
                  - X-Request-ID:$(uuid)

  - name: client-service
    url: http://client-service:3000
    routes:
      - name: client-api
        paths:
          - /api/v1/clients
        plugins:
          - name: rate-limiting
          - name: jwt

plugins:
  - name: cors
    config:
      origins:
        - https://app.wealthnexus.io
        - https://*.wealthnexus.io
      methods:
        - GET
        - POST
        - PUT
        - DELETE
        - PATCH
      headers:
        - Authorization
        - Content-Type
      credentials: true
      max_age: 3600

  - name: request-termination
    config:
      status_code: 503
      message: "Service temporarily unavailable"
    enabled: false  # Circuit breaker toggle
```

### External Integration Adapters

```
Integration Architecture
════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                        Integration Service                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    Adapter Factory                              │     │
│  │  Dynamically instantiates correct adapter based on provider    │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                │                                         │
│         ┌──────────────────────┼──────────────────────┐                 │
│         │                      │                      │                 │
│         ▼                      ▼                      ▼                 │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐           │
│  │  Custodian  │       │   Market    │       │    CRM      │           │
│  │  Adapters   │       │    Data     │       │  Adapters   │           │
│  │             │       │  Adapters   │       │             │           │
│  │ • Schwab    │       │ • Refinitiv │       │ • Salesforce│           │
│  │ • Fidelity  │       │ • Bloomberg │       │ • Redtail   │           │
│  │ • Pershing  │       │ • FactSet   │       │ • Wealthbox │           │
│  │ • TD        │       │ • ICE       │       │             │           │
│  └─────────────┘       └─────────────┘       └─────────────┘           │
│                                                                          │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐           │
│  │   Alts      │       │  Planning   │       │  Compliance │           │
│  │  Adapters   │       │  Adapters   │       │  Adapters   │           │
│  │             │       │             │       │             │           │
│  │ • iCapital  │       │• MoneyGuide │       │ • Orion     │           │
│  │ • CAIS      │       │• RightCap   │       │ • Riskalyze │           │
│  │ • Artivest  │       │• eMoney     │       │             │           │
│  └─────────────┘       └─────────────┘       └─────────────┘           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## AI/ML Platform

### AI Service Architecture

```
AI/ML Platform Architecture
═══════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                           NexusAI Service                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Natural Language Interface                    │    │
│  │  • Query Understanding    • Intent Classification               │    │
│  │  • Entity Extraction      • Response Generation                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     ML Model Registry                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │   Document   │  │   Anomaly    │  │   Forecast   │          │    │
│  │  │   Extractor  │  │   Detector   │  │    Model     │          │    │
│  │  │  (GPT-4/LLM) │  │(Isolation F.)│  │   (Prophet)  │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │    Risk      │  │   Security   │  │ Rebalancing  │          │    │
│  │  │   Scoring    │  │   Matching   │  │  Optimizer   │          │    │
│  │  │   (XGBoost)  │  │(Transformer) │  │    (RL)      │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Training Pipeline                             │    │
│  │  • Data Preprocessing   • Model Training (SageMaker)            │    │
│  │  • Feature Engineering  • Model Validation                      │    │
│  │  • Hyperparameter Tuning• Model Deployment                      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### ML Use Cases

| Use Case | Model Type | Purpose |
|----------|------------|---------|
| **Document Extraction** | LLM (GPT-4) | Parse K-1s, capital calls, statements |
| **Security Master Matching** | Transformer | Match securities across data sources |
| **Anomaly Detection** | Isolation Forest | Identify unusual data patterns |
| **Cash Flow Forecasting** | Prophet/LSTM | Predict capital calls, distributions |
| **Risk Scoring** | XGBoost | Client risk assessment |
| **Rebalancing Optimization** | Reinforcement Learning | Tax-optimal trade generation |
| **Churn Prediction** | Random Forest | Identify at-risk clients |
| **Meeting Summarization** | LLM | Auto-generate meeting notes |

---

## DevOps & Observability

### CI/CD Pipeline

```
CI/CD Pipeline
══════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│                              GitHub Actions                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │      Code       │───▶│     Build       │───▶│      Test       │          │
│  │      Push       │    │                 │    │                 │          │
│  │                 │    │ • Compile       │    │ • Unit Tests    │          │
│  │ • Feature Branch│    │ • Lint          │    │ • Integration   │          │
│  │ • Main Branch   │    │ • Type Check    │    │ • E2E Tests     │          │
│  └─────────────────┘    └─────────────────┘    └────────┬────────┘          │
│                                                          │                   │
│                         ┌────────────────────────────────┘                   │
│                         │                                                    │
│                         ▼                                                    │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │    Security     │───▶│     Docker      │───▶│      ECR        │          │
│  │     Scan        │    │     Build       │    │     Push        │          │
│  │                 │    │                 │    │                 │          │
│  │ • SAST (Snyk)   │    │ • Multi-stage   │    │ • Tag: sha-xxx  │          │
│  │ • Dependency    │    │ • Optimize      │    │ • Tag: latest   │          │
│  └─────────────────┘    └─────────────────┘    └────────┬────────┘          │
│                                                          │                   │
│                         ┌────────────────────────────────┘                   │
│                         │                                                    │
│                         ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                     ArgoCD Deployment                            │        │
│  │                                                                  │        │
│  │   Staging ──────────▶ Canary (5%) ──────────▶ Production        │        │
│  │                           │                        │             │        │
│  │                     Health Checks            Health Checks       │        │
│  │                     Rollback if fail         Gradual rollout     │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Observability Stack

```
Observability Architecture
══════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                              Applications                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Service   │  │   Service   │  │   Service   │  │   Service   │   │
│  │      A      │  │      B      │  │      C      │  │      D      │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │                │          │
│         └────────────────┼────────────────┼────────────────┘          │
│                          │                │                           │
│                          ▼                ▼                           │
│         ┌────────────────────────────────────────────────┐            │
│         │              OpenTelemetry Collector            │            │
│         │  • Traces  • Metrics  • Logs                   │            │
│         └────────────────────────────────────────────────┘            │
│                          │                                            │
└──────────────────────────┼────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │   Jaeger   │  │ Prometheus │  │    Loki    │
    │  (Traces)  │  │ (Metrics)  │  │   (Logs)   │
    └────────────┘  └────────────┘  └────────────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │  Grafana   │
                    │(Dashboards)│
                    └────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │ PagerDuty  │
                    │ (Alerting) │
                    └────────────┘
```

### Key Metrics & SLOs

| Metric | SLO Target | Alert Threshold |
|--------|------------|-----------------|
| **API Latency (p99)** | < 500ms | > 800ms |
| **API Availability** | 99.9% | < 99.5% |
| **Error Rate** | < 0.1% | > 0.5% |
| **Data Freshness** | < 15 min | > 30 min |
| **Report Generation** | < 30s | > 60s |
| **Database Latency** | < 100ms | > 200ms |

---

*Document Version: 1.0*
*Last Updated: January 2026*
