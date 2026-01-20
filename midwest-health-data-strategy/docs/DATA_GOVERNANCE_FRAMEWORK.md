# Enterprise Data Governance Framework

## Midwest Regional Health System

**Version:** 2.1
**Effective Date:** January 2026
**Document Owner:** Enterprise Data Governance Council

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Governance Vision & Objectives](#governance-vision--objectives)
3. [Organizational Structure](#organizational-structure)
4. [Roles & Responsibilities](#roles--responsibilities)
5. [Decision Rights Matrix](#decision-rights-matrix)
6. [Data Domains & Stewardship](#data-domains--stewardship)
7. [Data Classification Standards](#data-classification-standards)
8. [Policies & Standards](#policies--standards)
9. [Issue Management & Escalation](#issue-management--escalation)
10. [Metrics & Performance Monitoring](#metrics--performance-monitoring)

---

## Executive Summary

This Data Governance Framework establishes the organizational structures, policies, and processes necessary to manage MRHS's data as a strategic enterprise asset. The framework ensures data quality, security, and compliance while enabling data-driven decision making across clinical, operational, and financial functions.

### Framework Principles

| Principle | Description |
|-----------|-------------|
| **Data as an Asset** | Data is a strategic enterprise resource requiring active management |
| **Accountability** | All data has clearly defined ownership and stewardship |
| **Quality at Source** | Data quality is enforced at the point of creation |
| **Fit for Purpose** | Data meets the needs of its intended business use |
| **Compliance by Design** | Regulatory requirements are embedded in data processes |
| **Transparency** | Data definitions, lineage, and quality are documented and accessible |

---

## Governance Vision & Objectives

### Vision Statement

> Enable MRHS to deliver exceptional patient care and operational excellence through trusted, accessible, and well-governed data.

### Strategic Objectives

1. **Improve Patient Outcomes**
   - Ensure complete and accurate patient data for clinical decision support
   - Enable population health analytics for proactive care management
   - Support quality measure reporting (HEDIS, CMS Stars, MIPS)

2. **Optimize Financial Performance**
   - Reduce revenue cycle delays from data quality issues
   - Enable accurate cost accounting and margin analysis
   - Support value-based care contract performance

3. **Ensure Regulatory Compliance**
   - Maintain HIPAA Privacy and Security Rule compliance
   - Meet state health information exchange requirements
   - Support CMS Interoperability mandates

4. **Enable Analytics & Innovation**
   - Provide self-service access to trusted data
   - Support AI/ML initiatives with quality training data
   - Enable real-time operational dashboards

---

## Organizational Structure

### Governance Hierarchy

```
                    +------------------------+
                    |    Board of Directors  |
                    |   (Oversight & Policy) |
                    +-----------+------------+
                                |
                    +-----------v------------+
                    |  Executive Steering    |
                    |      Committee         |
                    |  (CDO, CMO, CFO, CIO)  |
                    +-----------+------------+
                                |
                    +-----------v------------+
                    |   Data Governance      |
                    |       Council          |
                    +-----------+------------+
                                |
          +---------------------+---------------------+
          |                     |                     |
+---------v---------+ +---------v---------+ +---------v---------+
|  Clinical Data    | |  Financial Data   | |  Operational Data |
|  Domain Council   | |  Domain Council   | |  Domain Council   |
+---------+---------+ +---------+---------+ +---------+---------+
          |                     |                     |
+---------v---------+ +---------v---------+ +---------v---------+
|  Data Stewards    | |  Data Stewards    | |  Data Stewards    |
|  (By Department)  | |  (By Department)  | |  (By Department)  |
+-------------------+ +-------------------+ +-------------------+
```

### Data Governance Council

**Charter:** The Data Governance Council (DGC) is the primary decision-making body for enterprise data management policies, standards, and priorities.

**Membership:**

| Role | Representative | Responsibility |
|------|---------------|----------------|
| Chair | Chief Data Officer | Overall governance leadership |
| Vice Chair | VP of Clinical Informatics | Clinical data strategy |
| Member | VP of Revenue Cycle | Financial data oversight |
| Member | VP of IT Operations | Technical implementation |
| Member | Chief Compliance Officer | Regulatory compliance |
| Member | Chief Medical Information Officer | Physician engagement |
| Member | VP of Quality | Clinical quality measures |
| Member | Director of Analytics | BI/Analytics requirements |

**Meeting Cadence:** Monthly (2nd Tuesday, 2:00 PM - 4:00 PM)

**Quorum Requirements:** 5 of 8 members or designated alternates

---

## Roles & Responsibilities

### Executive Sponsor (CDO)

| Responsibility | Activities |
|---------------|------------|
| Strategic Direction | Set data strategy aligned with organizational goals |
| Resource Allocation | Secure funding and staffing for governance initiatives |
| Issue Escalation | Resolve cross-functional governance conflicts |
| Executive Communication | Report governance status to Board and C-suite |

### Data Owner

**Definition:** Senior business leader accountable for a specific data domain

| Responsibility | Activities |
|---------------|------------|
| Domain Accountability | Final authority for data definitions and quality standards |
| Policy Approval | Approve domain-specific data policies |
| Access Authorization | Approve data access requests for their domain |
| Quality Targets | Set and monitor data quality thresholds |
| Issue Resolution | Resolve data quality issues within their domain |

**Current Data Owners:**

| Domain | Data Owner | Title |
|--------|-----------|-------|
| Patient Demographics | Dr. Sarah Chen | CMIO |
| Clinical/EHR | Dr. Michael Torres | VP Clinical Informatics |
| Financial/Claims | Jennifer Walsh | VP Revenue Cycle |
| Provider/Credentialing | David Kim | VP Medical Staff Services |
| Supply Chain | Robert Martinez | VP Supply Chain |
| Human Resources | Lisa Thompson | CHRO |
| Facilities/Assets | James Wilson | VP Facilities |

### Data Steward

**Definition:** Business subject matter expert responsible for day-to-day data quality management

| Responsibility | Activities |
|---------------|------------|
| Data Quality Monitoring | Review daily/weekly quality dashboards |
| Issue Triage | Investigate and resolve data quality issues |
| Business Rules | Define and document data validation rules |
| Metadata Management | Maintain data definitions in catalog |
| User Support | Assist users with data interpretation |
| Change Management | Review and approve data element changes |

**Stewardship Program:**

- 35 trained data stewards across all facilities
- 8-hour certification training program
- Monthly steward community of practice meetings
- Annual recertification requirement

### Data Custodian

**Definition:** IT professional responsible for technical data management

| Responsibility | Activities |
|---------------|------------|
| Technical Implementation | Implement data quality rules in systems |
| Security Controls | Enforce access controls and encryption |
| Data Integration | Manage ETL/ELT processes |
| Performance Monitoring | Ensure system availability and performance |
| Backup & Recovery | Maintain data backup and disaster recovery |

---

## Decision Rights Matrix

### RACI Model for Key Data Decisions

| Decision | Data Owner | Data Steward | Data Custodian | DGC | Compliance |
|----------|:----------:|:------------:|:--------------:|:---:|:----------:|
| New data element creation | A | R | C | I | C |
| Data definition changes | A | R | C | I | C |
| Quality threshold setting | A | R | I | I | C |
| Access grant (standard) | A | R | I | I | C |
| Access grant (PHI bulk) | A | R | I | C | A |
| Data retention changes | C | I | R | A | A |
| Cross-domain integration | C | R | R | A | C |
| Vendor data sharing | A | C | R | A | A |
| Policy exceptions | I | C | I | A | A |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## Data Domains & Stewardship

### Enterprise Data Domain Model

```
+------------------------------------------------------------------+
|                    ENTERPRISE DATA DOMAINS                        |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |     PATIENT      |  |    PROVIDER      |  |    LOCATION      | |
|  |  Master Data     |  |  Master Data     |  |  Master Data     | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |    CLINICAL      |  |   FINANCIAL      |  |   OPERATIONAL    | |
|  |  Encounters      |  |  Charges/Claims  |  |  Scheduling      | |
|  |  Orders/Results  |  |  Payments        |  |  Bed Management  | |
|  |  Medications     |  |  Contracts       |  |  Supply Chain    | |
|  |  Documents       |  |  Cost Accounting |  |  HR/Staffing     | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |    QUALITY       |  |   RESEARCH       |  |    REFERENCE     | |
|  |  Measures        |  |  Studies         |  |  Code Sets       | |
|  |  Outcomes        |  |  Consents        |  |  Vocabularies    | |
|  |  Safety Events   |  |  Biospecimens    |  |  Hierarchies     | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

### Domain Stewardship Matrix

| Domain | Primary Steward | Backup Steward | Source System | Data Owner |
|--------|----------------|----------------|---------------|------------|
| Patient Master | Maria Garcia | Tom Anderson | Epic MPI | Dr. Chen |
| Provider Master | Kevin Lee | Susan Park | Cactus/NPI | D. Kim |
| Location Master | Amy Johnson | Chris Davis | Facilities DB | J. Wilson |
| Clinical - Encounters | Dr. Emily White | RN Jane Foster | Epic/Cerner | Dr. Torres |
| Clinical - Orders | Pharm. John Smith | Lab Dir. K. Brown | Epic/Cerner | Dr. Torres |
| Financial - Charges | Bill Thompson | Rachel Green | Epic PB | J. Walsh |
| Financial - Claims | Mike Wilson | Sarah Davis | Claim System | J. Walsh |
| Quality Measures | QA Dir. Nancy Lee | Analyst P. Chen | Quality DB | VP Quality |

---

## Data Classification Standards

### Classification Levels

| Level | Classification | Description | Examples |
|-------|---------------|-------------|----------|
| 1 | **Public** | Information approved for public release | Press releases, public quality ratings |
| 2 | **Internal** | General business information for employees | Org charts, policies, aggregate statistics |
| 3 | **Confidential** | Sensitive business data requiring protection | Financial reports, contracts, strategic plans |
| 4 | **PHI** | Protected Health Information under HIPAA | Patient records, diagnoses, treatment data |
| 5 | **Restricted PHI** | Highly sensitive PHI with additional protections | Substance abuse, HIV, mental health, genetics |

### Classification Controls Matrix

| Control | Public | Internal | Confidential | PHI | Restricted PHI |
|---------|:------:|:--------:|:------------:|:---:|:--------------:|
| Encryption at Rest | - | - | Required | Required | Required (AES-256) |
| Encryption in Transit | - | TLS 1.2+ | TLS 1.2+ | TLS 1.3 | TLS 1.3 |
| Access Logging | - | Basic | Detailed | Full Audit | Full Audit + Alert |
| Access Review Frequency | N/A | Annual | Quarterly | Monthly | Weekly |
| Data Masking (non-prod) | No | No | Yes | Required | Required + Token |
| Retention Period | Indefinite | 3 years | 7 years | Per regulation | Per regulation |
| Disposal Method | Delete | Delete | Secure delete | Certified destroy | Certified destroy |

### PHI Data Elements

The following data elements are classified as PHI and subject to HIPAA protections:

1. Names
2. Geographic data smaller than state
3. Dates (except year) related to individual
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying characteristic

---

## Policies & Standards

### Core Data Policies

| Policy | Description | Review Cycle |
|--------|-------------|--------------|
| DG-001 | Data Governance Charter | Annual |
| DG-002 | Data Classification Policy | Annual |
| DG-003 | Data Quality Policy | Annual |
| DG-004 | Data Access Policy | Semi-annual |
| DG-005 | Data Retention Policy | Annual |
| DG-006 | Data Privacy Policy | Semi-annual |
| DG-007 | Metadata Management Policy | Annual |
| DG-008 | Master Data Management Policy | Annual |
| DG-009 | Data Integration Standards | Semi-annual |
| DG-010 | BI & Analytics Standards | Annual |

### Data Quality Standards

**Dimensions Measured:**

| Dimension | Definition | Target | Measurement Method |
|-----------|-----------|--------|-------------------|
| **Completeness** | Required fields populated | ≥95% | Null/blank analysis |
| **Accuracy** | Data reflects real-world truth | ≥98% | Audit sampling |
| **Consistency** | Data agrees across systems | ≥99% | Cross-system reconciliation |
| **Timeliness** | Data available when needed | <4 hours | Load timestamp analysis |
| **Validity** | Data conforms to business rules | ≥99% | Rule engine validation |
| **Uniqueness** | No unintended duplicates | ≥99.5% | Duplicate detection |

### Naming Standards

**Database Objects:**
- Tables: `[Domain]_[Entity]_[Type]` (e.g., `CLN_PATIENT_DIM`)
- Columns: `[Entity]_[Attribute]_[Suffix]` (e.g., `PAT_BIRTH_DT`)
- Views: `VW_[Domain]_[Purpose]` (e.g., `VW_CLN_ACTIVE_PATIENTS`)

**Reports & Dashboards:**
- Format: `[Domain]-[Audience]-[Purpose]-[Version]`
- Example: `FIN-EXEC-Revenue_Dashboard-v2.1`

---

## Issue Management & Escalation

### Issue Classification

| Severity | Definition | Response Time | Resolution Target |
|----------|-----------|---------------|-------------------|
| **Critical** | Patient safety or major compliance risk | 1 hour | 4 hours |
| **High** | Significant business impact or revenue loss | 4 hours | 24 hours |
| **Medium** | Moderate impact to operations | 24 hours | 5 business days |
| **Low** | Minor inconvenience, workaround available | 48 hours | 10 business days |

### Escalation Path

```
Level 1: Data Steward
    ↓ (4 hours no resolution)
Level 2: Data Owner
    ↓ (24 hours no resolution)
Level 3: Data Governance Council
    ↓ (Cross-domain or policy conflict)
Level 4: Executive Steering Committee
```

### Issue Tracking

All data governance issues tracked in ServiceNow with:
- Issue ID and classification
- Affected data domain(s)
- Business impact assessment
- Root cause analysis
- Remediation plan
- Resolution verification

---

## Metrics & Performance Monitoring

### Governance Program KPIs

| KPI | Target | Current | Trend |
|-----|--------|---------|-------|
| Data Quality Score (Overall) | ≥95% | 94.2% | ↑ |
| Stewardship Coverage | 100% | 100% | → |
| Policy Compliance Rate | ≥98% | 97.5% | ↑ |
| Issue Resolution (on-time) | ≥90% | 92% | ↑ |
| Metadata Completeness | ≥95% | 89% | ↑ |
| User Satisfaction (survey) | ≥4.0/5 | 4.2/5 | ↑ |
| Training Completion | 100% | 98% | → |

### Data Quality Scorecard by Domain

| Domain | Completeness | Accuracy | Consistency | Timeliness | Overall |
|--------|:-----------:|:--------:|:-----------:|:----------:|:-------:|
| Patient Master | 97% | 99% | 98% | 99% | **98%** |
| Provider Master | 95% | 98% | 96% | 97% | **97%** |
| Clinical | 93% | 97% | 94% | 96% | **95%** |
| Financial | 96% | 98% | 97% | 94% | **96%** |
| Operational | 91% | 95% | 93% | 98% | **94%** |

### Reporting Cadence

| Report | Audience | Frequency | Delivery |
|--------|----------|-----------|----------|
| Data Quality Dashboard | All Stewards | Real-time | Power BI |
| Weekly Governance Summary | DGC Members | Weekly | Email |
| Monthly Scorecard | Executive Steering | Monthly | Meeting |
| Quarterly Business Review | Board | Quarterly | Presentation |
| Annual Governance Report | All Stakeholders | Annual | Published |

---

## Appendices

### Appendix A: Glossary of Terms

| Term | Definition |
|------|------------|
| **Data Asset** | Any collection of data that has value to the organization |
| **Data Domain** | A logical grouping of related data elements |
| **Data Element** | The smallest unit of data that has meaning |
| **Data Lineage** | The lifecycle of data including its origins and transformations |
| **Master Data** | Core business entities shared across the organization |
| **Metadata** | Data that describes other data |
| **PHI** | Protected Health Information as defined by HIPAA |

### Appendix B: Related Documents

- HIPAA Compliance Framework
- Information Security Policy
- Business Continuity Plan
- Disaster Recovery Plan
- Vendor Management Policy

### Appendix C: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jun 2025 | Data Strategy Team | Initial framework |
| 1.1 | Aug 2025 | DGC | Added stewardship matrix |
| 2.0 | Nov 2025 | DGC | Major update - added metrics |
| 2.1 | Jan 2026 | DGC | Annual review updates |

---

*This document is reviewed and approved by the Data Governance Council on an annual basis.*
