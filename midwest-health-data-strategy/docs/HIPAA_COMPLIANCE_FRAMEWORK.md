# HIPAA Compliance Framework for Data Management

## Midwest Regional Health System

**Version:** 1.3
**Document Owner:** Chief Privacy Officer / Chief Compliance Officer
**Review Cycle:** Semi-annual

---

## Table of Contents

1. [Regulatory Overview](#regulatory-overview)
2. [PHI Data Inventory](#phi-data-inventory)
3. [Privacy Rule Compliance](#privacy-rule-compliance)
4. [Security Rule Compliance](#security-rule-compliance)
5. [Data Flow Mapping](#data-flow-mapping)
6. [Access Control Framework](#access-control-framework)
7. [Audit & Monitoring](#audit--monitoring)
8. [Breach Response Procedures](#breach-response-procedures)
9. [Business Associate Management](#business-associate-management)
10. [Training & Awareness](#training--awareness)

---

## Regulatory Overview

### Applicable Regulations

| Regulation | Scope | Key Requirements |
|------------|-------|------------------|
| **HIPAA Privacy Rule** (45 CFR 164.500-534) | Use & disclosure of PHI | Minimum necessary, patient rights, authorizations |
| **HIPAA Security Rule** (45 CFR 164.302-318) | Electronic PHI safeguards | Administrative, physical, technical safeguards |
| **HITECH Act** | Breach notification, penalties | Enhanced enforcement, breach notification requirements |
| **42 CFR Part 2** | Substance use disorder records | Additional consent requirements for SUD data |
| **State Laws (WI, MN, MI)** | State-specific protections | HIV, mental health, minor consent provisions |
| **CMS Interoperability Rules** | Data sharing requirements | Patient access, payer-to-payer exchange |

### Compliance Accountability

| Role | Responsibility |
|------|---------------|
| Chief Privacy Officer | Privacy Rule compliance, patient rights |
| Chief Information Security Officer | Security Rule compliance, technical controls |
| Chief Compliance Officer | Overall compliance program, risk management |
| Data Governance Council | Data handling policies, access decisions |
| Information Security Committee | Security incidents, vulnerability management |

---

## PHI Data Inventory

### PHI Data Categories

| Category | Description | Sensitivity | Systems |
|----------|-------------|-------------|---------|
| **Demographics** | Name, DOB, address, SSN, MRN | Standard PHI | Epic, MDM, Claims |
| **Clinical** | Diagnoses, procedures, notes, results | Standard PHI | Epic, PACS, Lab |
| **Financial** | Insurance, billing, payments | Standard PHI | Epic PB, Claims |
| **Substance Abuse** | 42 CFR Part 2 protected | Highly Sensitive | Epic (restricted) |
| **Mental Health** | Behavioral health, psych notes | Highly Sensitive | Epic (restricted) |
| **HIV/AIDS** | HIV status, treatment | Highly Sensitive | Epic (restricted) |
| **Genetic** | Genetic test results, counseling | Highly Sensitive | Lab, Genetics DB |
| **Reproductive** | Pregnancy, abortion services | State-dependent | Epic |

### PHI Volume Metrics

| Data Store | Records | PHI Elements | Encryption | Retention |
|------------|---------|--------------|------------|-----------|
| Epic Production | 4.2M patients | Full clinical record | AES-256 | Active +7 years |
| Data Warehouse | 4.2M patients | Structured clinical | AES-256 | 10 years |
| Data Lake (Raw) | 4.2M patients | Full dataset | AES-256 | 7 years |
| Analytics Datasets | 4.2M patients | De-identified available | AES-256 | 3 years |
| Archive/Backup | 6.1M patients | Full clinical record | AES-256 | Per policy |

---

## Privacy Rule Compliance

### Minimum Necessary Standard

**Policy:** Access to PHI is limited to the minimum necessary to accomplish the intended purpose.

**Implementation:**

| Use Case | PHI Access Level | Justification |
|----------|-----------------|---------------|
| Direct patient care | Full record | Treatment exception |
| Billing/Collections | Demographics + financial | Revenue cycle operations |
| Quality reporting | Limited dataset | Healthcare operations |
| Research | De-identified or IRB approved | Research exception |
| Analytics | De-identified or aggregated | Healthcare operations |
| IT Support | Minimum for troubleshooting | Operations with audit |

### Role-Based Access Matrix

| Role | Demographics | Clinical Summary | Full Notes | Sensitive (42CFR2) | Financial |
|------|:-----------:|:----------------:|:----------:|:-----------------:|:---------:|
| Physician (treating) | Full | Full | Full | With consent | View |
| Nurse (assigned) | Full | Full | Full | With consent | - |
| Registration | Full | - | - | - | Full |
| Billing Specialist | Full | Codes only | - | - | Full |
| Quality Analyst | Limited | Limited | - | - | - |
| Researcher | IRB approved | IRB approved | IRB approved | Special consent | - |
| IT Support | MRN only | - | - | - | - |

### Patient Rights Implementation

| Right | Implementation | Response Time |
|-------|---------------|---------------|
| **Access** | Patient portal, HIM request | 30 days (15 with extension) |
| **Amendment** | HIM process, physician review | 60 days |
| **Accounting of Disclosures** | Automated audit log query | 60 days |
| **Restriction Request** | Documented in system flags | 30 days |
| **Confidential Communications** | Alternate address/phone in system | Immediate |
| **Notice of Privacy Practices** | Website, registration, on request | Immediate |

---

## Security Rule Compliance

### Administrative Safeguards

| Standard | Requirement | MRHS Implementation |
|----------|-------------|---------------------|
| Security Management | Risk analysis, policies | Annual risk assessment, policy library |
| Assigned Responsibility | Security Officer | CISO appointed, deputies by facility |
| Workforce Security | Clearance, termination | Background checks, exit process |
| Information Access | Access management | IAM system, role-based access |
| Security Awareness | Training program | Annual training, phishing simulations |
| Security Incidents | Response procedures | Incident response plan, tabletop exercises |
| Contingency Plan | Backup, disaster recovery | Documented BCP/DR, annual testing |
| Evaluation | Periodic assessment | Internal audit, external pen testing |
| BA Contracts | Written agreements | Legal review, standard BAA template |

### Physical Safeguards

| Standard | Requirement | MRHS Implementation |
|----------|-------------|---------------------|
| Facility Access | Access controls | Badge access, visitor logs |
| Workstation Use | Appropriate use | Clean desk policy, screen positioning |
| Workstation Security | Physical safeguards | Cable locks, secured areas |
| Device Controls | Media handling | Encrypted drives, secure disposal |

### Technical Safeguards

| Standard | Requirement | MRHS Implementation |
|----------|-------------|---------------------|
| Access Control | Unique users, emergency access | AD integration, break-glass procedures |
| Audit Controls | Audit logs | Comprehensive logging, SIEM integration |
| Integrity | PHI alteration protection | Hash verification, change tracking |
| Authentication | Person or entity verification | MFA for all PHI access |
| Transmission Security | Encryption | TLS 1.3 minimum, VPN for remote |

### Technical Controls Detail

| Control | Standard | Implementation |
|---------|----------|----------------|
| Encryption at Rest | AES-256 | All PHI data stores |
| Encryption in Transit | TLS 1.3 | All PHI transmission |
| Multi-Factor Authentication | Required | All clinical applications |
| Password Policy | Complex, 90-day rotation | AD Group Policy enforced |
| Session Timeout | 15 minutes | Application-level enforcement |
| Network Segmentation | VLAN isolation | Clinical networks separated |
| Endpoint Protection | EDR + Antivirus | CrowdStrike on all endpoints |
| Data Loss Prevention | DLP policies | Email and USB monitoring |

---

## Data Flow Mapping

### PHI Data Flow Diagram

```
+------------------+     +------------------+     +------------------+
|   PATIENT        |     |   REGISTRATION   |     |   CLINICAL       |
|   INTERACTION    |---->|   SYSTEMS        |---->|   APPLICATIONS   |
|                  |     |                  |     |   (Epic/Cerner)  |
+------------------+     +------------------+     +--------+---------+
                                                          |
                                                          v
+------------------+     +------------------+     +--------+---------+
|   EXTERNAL       |<----|   INTEGRATION    |<----|   DATA           |
|   PARTNERS       |     |   ENGINE (ADF)   |     |   WAREHOUSE      |
|   (with BAA)     |     |                  |     |   (Snowflake)    |
+------------------+     +--------+---------+     +--------+---------+
                                  |                        |
                                  v                        v
                         +--------+---------+     +--------+---------+
                         |   ANALYTICS      |     |   REPORTING      |
                         |   (De-identified)|     |   (Role-based)   |
                         +------------------+     +------------------+
```

### Data Flow Inventory

| Flow ID | Source | Destination | PHI Level | Encryption | BAA Required |
|---------|--------|-------------|-----------|------------|--------------|
| DF-001 | Epic | Data Warehouse | Full PHI | TLS + AES | N/A (internal) |
| DF-002 | Warehouse | Power BI | Role-limited | TLS + AES | N/A (internal) |
| DF-003 | Epic | Health Plan | Claims data | TLS + AES | Yes |
| DF-004 | Epic | HIE | Clinical summary | TLS + AES | Yes |
| DF-005 | Warehouse | Research | De-identified | TLS + AES | IRB + DUA |
| DF-006 | Epic | Vendor Analytics | Limited | TLS + AES | Yes |
| DF-007 | Claims | CMS | Required elements | SFTP + PGP | Regulation |

---

## Access Control Framework

### Identity & Access Management

```
+------------------------------------------------------------------+
|                    IDENTITY MANAGEMENT                            |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+     +------------------+                    |
|  |  Active          |     |   IAM Platform   |                    |
|  |  Directory       |<--->|   (SailPoint)    |                    |
|  +------------------+     +--------+---------+                    |
|                                    |                              |
|         +-------------+------------+------------+                 |
|         |             |            |            |                 |
|  +------v-----+ +-----v------+ +---v--------+ +-v--------------+ |
|  | Epic       | | Snowflake  | | Power BI   | | Other Apps     | |
|  | Security   | | RBAC       | | Workspace  | | SSO + RBAC     | |
|  +------------+ +------------+ +------------+ +----------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

### Access Request & Approval Workflow

| Step | Action | Responsible | SLA |
|------|--------|-------------|-----|
| 1 | Submit access request | Requestor | N/A |
| 2 | Manager approval | Direct supervisor | 24 hours |
| 3 | Data Owner approval | Domain data owner | 48 hours |
| 4 | Security review (PHI bulk) | ISO team | 72 hours |
| 5 | Compliance review (sensitive) | Privacy Office | 72 hours |
| 6 | Provisioning | IAM team | 24 hours |
| 7 | Confirmation & training | Requestor | 48 hours |

### Break-Glass Procedures

**Purpose:** Emergency access to PHI when normal access is unavailable and patient safety is at risk.

| Scenario | Authorization | Access Level | Monitoring |
|----------|--------------|--------------|------------|
| System outage (clinical) | Charge nurse | Full patient record | Real-time alert |
| Cross-facility emergency | ED physician | Full patient record | Real-time alert |
| Disaster/mass casualty | Incident commander | Full access | Post-event audit |

**Break-Glass Controls:**
- Separate credentials stored securely
- MFA still required
- Immediate alert to Security and Privacy
- Mandatory justification within 24 hours
- Full audit review within 48 hours

---

## Audit & Monitoring

### Audit Log Requirements

| System | Events Logged | Retention | Review Frequency |
|--------|--------------|-----------|------------------|
| Epic (EMR) | All PHI access, modifications | 6 years | Real-time + monthly |
| Snowflake | All queries, exports | 6 years | Weekly sampling |
| Power BI | Report access, downloads | 6 years | Monthly |
| Active Directory | Authentication, privilege changes | 6 years | Real-time |
| VPN | All connections | 2 years | Weekly |

### Audit Log Contents

| Field | Description | Example |
|-------|-------------|---------|
| Timestamp | Date/time of event | 2026-01-15 14:23:45 UTC |
| User ID | Unique identifier | john.smith@mrhs.org |
| Patient ID | MRN if applicable | 12345678 |
| Action | Event type | VIEW, PRINT, EXPORT, MODIFY |
| Data Elements | Fields accessed | Demographics, Lab Results |
| Source IP | Network location | 10.50.25.100 |
| Application | System used | Epic, Power BI |
| Reason | Justification (if required) | Direct care |

### Monitoring & Alerting

| Alert Type | Trigger | Response | Escalation |
|------------|---------|----------|------------|
| High-volume access | >100 records/hour | Automated lockout | Security team |
| After-hours access | PHI access 10PM-6AM | Alert to manager | Review within 24hr |
| VIP patient access | Access to flagged patients | Alert to Privacy | Immediate review |
| Peer access | Accessing coworker records | Alert to Privacy | Investigation |
| Break-glass activation | Any emergency access | Real-time alert | 24-hour review |
| Export/download | Large data export | Manager notification | Weekly review |

### Proactive Audit Program

| Audit Type | Scope | Frequency | Owner |
|------------|-------|-----------|-------|
| Random access review | 50 users sampled | Monthly | Privacy Office |
| Terminated employee audit | All recent terminations | Weekly | IAM + Privacy |
| Vendor access audit | All BA system access | Quarterly | Compliance |
| PHI export audit | All bulk downloads | Weekly | Security |
| Break-glass review | All emergency access | Per occurrence | Privacy + CISO |

---

## Breach Response Procedures

### Breach Definition

A breach is the unauthorized acquisition, access, use, or disclosure of PHI that compromises its security or privacy, unless an exception applies:

1. Unintentional acquisition by workforce member acting in good faith
2. Inadvertent disclosure between authorized persons
3. Good faith belief that unauthorized person could not retain information

### Risk Assessment Factors

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| Data Type | Demographics only | Clinical data | Financial + SSN |
| Volume | <10 individuals | 10-500 individuals | >500 individuals |
| Recipient | Known, trustworthy | Unknown but limited | Malicious actor |
| Mitigation | Immediate return/destroy | Partial mitigation | No mitigation |
| Re-identification | Not possible | Difficult | Easy |

### Breach Response Timeline

| Timeframe | Action | Responsible |
|-----------|--------|-------------|
| Immediate | Contain breach, preserve evidence | First responder |
| <24 hours | Initial assessment, activate IRT | ISO + Privacy |
| <72 hours | Complete risk assessment | Privacy Officer |
| <15 days | Notify individuals (if >500 in state) | Compliance |
| <60 days | Notify individuals (all others) | Compliance |
| <60 days | Notify HHS (if >500) | Compliance |
| Annual | Notify HHS (if <500) | Compliance |
| Ongoing | Media notification (if >500 in state) | Communications |

### Incident Response Team

| Role | Primary | Backup |
|------|---------|--------|
| Incident Commander | CISO | Privacy Officer |
| Legal Counsel | General Counsel | Outside counsel |
| Communications | VP Communications | PR agency |
| IT Lead | VP IT Operations | Security architect |
| Clinical Lead | CMO | CMIO |
| HR Lead | CHRO | HR Director |
| Compliance Lead | CCO | Compliance Director |

---

## Business Associate Management

### BA Categories

| Category | Examples | Risk Level | Review Frequency |
|----------|----------|------------|------------------|
| Cloud Infrastructure | Azure, AWS, Snowflake | High | Annual + continuous |
| Software Vendors | Epic, Power BI | High | Annual |
| Analytics Partners | Consulting firms | Medium | Per engagement |
| IT Services | MSPs, contractors | Medium | Annual |
| Research Partners | Universities, CROs | Medium | Per study |
| Collection Agencies | Third-party collections | Medium | Annual |

### BAA Requirements

Every Business Associate Agreement must include:

1. **Permitted uses and disclosures** of PHI
2. **Safeguards** required to protect PHI
3. **Reporting requirements** for security incidents
4. **Subcontractor requirements** (downstream BAs)
5. **Individual rights** obligations
6. **HHS access** for compliance review
7. **Termination provisions** and data return/destruction
8. **Breach notification** requirements

### BA Risk Assessment

| Assessment Area | Questions | Scoring |
|-----------------|-----------|---------|
| Data Handling | What PHI is accessed? How is it stored? | 1-5 scale |
| Security Controls | Encryption, access controls, auditing? | 1-5 scale |
| Compliance History | Prior breaches? Audit findings? | 1-5 scale |
| Subcontractors | Who else has access? | 1-5 scale |
| Incident Response | Notification procedures? | 1-5 scale |

**Risk Tiers:**
- Low (5-10): Annual review
- Medium (11-18): Semi-annual review
- High (19-25): Quarterly review + enhanced monitoring

---

## Training & Awareness

### Training Requirements

| Audience | Training | Frequency | Method |
|----------|----------|-----------|--------|
| All Workforce | HIPAA Basics | Annual | Online (30 min) |
| Clinical Staff | HIPAA + Privacy | Annual | Online (45 min) |
| IT Staff | Security Awareness | Annual | Online (60 min) |
| Data Analysts | PHI Handling | Annual | In-person (2 hr) |
| Managers | Privacy Accountability | Annual | Online (30 min) |
| Executives | Compliance Overview | Annual | In-person (1 hr) |
| New Hires | HIPAA Orientation | Day 1 | Online + in-person |

### Training Content

| Module | Topics Covered |
|--------|----------------|
| HIPAA Fundamentals | Privacy Rule basics, patient rights, penalties |
| PHI Handling | Minimum necessary, de-identification, disposal |
| Security Essentials | Password hygiene, phishing, physical security |
| Incident Reporting | What to report, how to report, timelines |
| Role-Specific | Department-specific scenarios and procedures |

### Compliance Metrics

| Metric | Target | Current | Measurement |
|--------|--------|---------|-------------|
| Training completion rate | 100% | 98.5% | LMS tracking |
| Phishing test pass rate | >90% | 87% | Simulation results |
| Policy acknowledgment | 100% | 99.2% | HR system |
| Incident reporting rate | 100% | N/A | Near-miss capture |
| Audit finding closure | <30 days | 22 days avg | Issue tracking |

---

## Appendix A: Compliance Checklist

### Annual Compliance Tasks

- [ ] Complete HIPAA risk assessment
- [ ] Review and update policies
- [ ] Verify BA agreements current
- [ ] Complete workforce training
- [ ] Test incident response plan
- [ ] Review access controls
- [ ] Audit break-glass usage
- [ ] Update PHI inventory
- [ ] Review vendor compliance
- [ ] Report to Board

### Monthly Compliance Tasks

- [ ] Review audit logs (sampling)
- [ ] Monitor access anomalies
- [ ] Track training completion
- [ ] Review breach reports
- [ ] Verify terminated access removal
- [ ] Update data flow documentation
- [ ] Review open compliance issues

---

## Appendix B: Key Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Chief Privacy Officer | [Name] | [Phone] | privacy@mrhs.org |
| Chief Information Security Officer | [Name] | [Phone] | security@mrhs.org |
| Chief Compliance Officer | [Name] | [Phone] | compliance@mrhs.org |
| HIPAA Hotline | N/A | 1-800-XXX-XXXX | hipaa@mrhs.org |
| Security Incident | N/A | 1-800-XXX-XXXX | incident@mrhs.org |

---

*This document is reviewed semi-annually by the Privacy and Compliance offices. Last review: January 2026.*
