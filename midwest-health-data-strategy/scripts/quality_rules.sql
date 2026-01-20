/*
================================================================================
HEALTHCARE DATA QUALITY MONITORING - SQL RULE LIBRARY
================================================================================
Enterprise data quality rules for healthcare data warehouse
Designed for Snowflake execution with daily monitoring

Author: Data Strategy Consultant
Version: 2.1
================================================================================
*/

-- ============================================================================
-- QUALITY RESULTS TRACKING TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS DW_ADMIN.DQ_RULE_RESULTS (
    RESULT_ID               NUMBER AUTOINCREMENT PRIMARY KEY,
    RULE_ID                 VARCHAR(20) NOT NULL,
    RULE_NAME               VARCHAR(200),
    DIMENSION               VARCHAR(50),
    DOMAIN                  VARCHAR(50),
    EXECUTION_DT            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    TOTAL_RECORDS           NUMBER,
    PASSING_RECORDS         NUMBER,
    FAILING_RECORDS         NUMBER,
    QUALITY_SCORE           FLOAT,
    THRESHOLD               FLOAT,
    PASSED_IND              BOOLEAN,
    EXECUTION_TIME_MS       NUMBER,
    ERROR_MESSAGE           VARCHAR(4000)
);

CREATE TABLE IF NOT EXISTS DW_ADMIN.DQ_FAILED_RECORDS (
    FAILED_RECORD_ID        NUMBER AUTOINCREMENT PRIMARY KEY,
    RESULT_ID               NUMBER REFERENCES DW_ADMIN.DQ_RULE_RESULTS(RESULT_ID),
    RULE_ID                 VARCHAR(20),
    RECORD_KEY              VARCHAR(100),  -- MRN, Encounter ID, etc.
    FAILURE_REASON          VARCHAR(500),
    FIELD_NAME              VARCHAR(100),
    FIELD_VALUE             VARCHAR(500),
    CAPTURED_DT             TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================================
-- PATIENT DEMOGRAPHICS QUALITY CHECKS
-- ============================================================================

-- PAT-001: Patient Name Completeness
-- Business Rule: All active patients must have first and last name populated
-- Threshold: 99%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'PAT-001' AS rule_id,
        'Patient Name Completeness' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN PAT_FIRST_NAME IS NOT NULL
                AND PAT_LAST_NAME IS NOT NULL
                AND TRIM(PAT_FIRST_NAME) != ''
                AND TRIM(PAT_LAST_NAME) != ''
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW.DIM_PATIENT
    WHERE ACTIVE_IND = 'Y'
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.99 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.99
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- PAT-002: Date of Birth Validity
-- Business Rule: DOB must be valid, not in future, patient not >120 years old
-- Threshold: 99%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'PAT-002' AS rule_id,
        'Date of Birth Validity' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN PAT_BIRTH_DT IS NOT NULL
                AND PAT_BIRTH_DT <= CURRENT_DATE
                AND PAT_BIRTH_DT >= DATEADD(year, -120, CURRENT_DATE)
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW.DIM_PATIENT
    WHERE ACTIVE_IND = 'Y'
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.99 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.99
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- PAT-005: MRN Uniqueness (Critical - Patient Safety)
-- Business Rule: Medical Record Numbers must be unique enterprise-wide
-- Threshold: 100%
-- Severity: CRITICAL

WITH DuplicateMRNs AS (
    SELECT
        MRN,
        COUNT(*) AS duplicate_count
    FROM DW.DIM_PATIENT
    WHERE ACTIVE_IND = 'Y'
      AND MRN IS NOT NULL
    GROUP BY MRN
    HAVING COUNT(*) > 1
),
RuleExecution AS (
    SELECT
        'PAT-005' AS rule_id,
        'MRN Uniqueness' AS rule_name,
        (SELECT COUNT(*) FROM DW.DIM_PATIENT WHERE ACTIVE_IND = 'Y') AS total_records,
        (SELECT COUNT(*) FROM DW.DIM_PATIENT WHERE ACTIVE_IND = 'Y')
            - COALESCE((SELECT SUM(duplicate_count) FROM DuplicateMRNs), 0) AS passing_records
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 6) AS quality_score,
    1.0 AS threshold,
    CASE WHEN passing_records = total_records THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- Capture duplicate MRNs for investigation
INSERT INTO DW_ADMIN.DQ_FAILED_RECORDS (RULE_ID, RECORD_KEY, FAILURE_REASON, FIELD_NAME, FIELD_VALUE)
SELECT
    'PAT-005',
    p.MRN,
    'Duplicate MRN found - ' || d.duplicate_count || ' occurrences',
    'MRN',
    p.MRN
FROM DW.DIM_PATIENT p
JOIN (
    SELECT MRN, COUNT(*) AS duplicate_count
    FROM DW.DIM_PATIENT
    WHERE ACTIVE_IND = 'Y'
    GROUP BY MRN
    HAVING COUNT(*) > 1
) d ON p.MRN = d.MRN
WHERE p.ACTIVE_IND = 'Y';


-- ============================================================================
-- CLINICAL DATA QUALITY CHECKS
-- ============================================================================

-- CLN-001: Inpatient Diagnosis Presence
-- Business Rule: All discharged inpatients should have at least one diagnosis
-- Threshold: 98%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'CLN-001' AS rule_id,
        'Inpatient Diagnosis Presence' AS rule_name,
        COUNT(DISTINCT enc.ENCOUNTER_ID) AS total_records,
        COUNT(DISTINCT CASE WHEN dx.ENCOUNTER_ID IS NOT NULL
                           THEN enc.ENCOUNTER_ID END) AS passing_records
    FROM DW.FACT_ENCOUNTER enc
    LEFT JOIN DW.FACT_DIAGNOSIS dx ON enc.ENCOUNTER_ID = dx.ENCOUNTER_ID
    WHERE enc.ENCOUNTER_TYPE = 'INPATIENT'
      AND enc.DISCHARGE_DT IS NOT NULL
      AND enc.DISCHARGE_DT >= DATEADD(day, -90, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.98 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.98
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- CLN-002: Admission/Discharge Date Logic (Critical - Data Integrity)
-- Business Rule: Discharge date must be >= admission date
-- Threshold: 100%
-- Severity: CRITICAL

WITH RuleExecution AS (
    SELECT
        'CLN-002' AS rule_id,
        'Admission/Discharge Date Logic' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN DISCHARGE_DT IS NULL OR DISCHARGE_DT >= ADMIT_DT
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW.FACT_ENCOUNTER
    WHERE ENCOUNTER_TYPE = 'INPATIENT'
      AND ADMIT_DT >= DATEADD(year, -1, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 6) AS quality_score,
    1.0 AS threshold,
    CASE WHEN passing_records = total_records THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- CLN-004: Lab Result Timeliness
-- Business Rule: Lab results should load within 4 hours of finalization
-- Threshold: 95%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'CLN-004' AS rule_id,
        'Lab Result Timeliness' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN TIMESTAMPDIFF(hour, RESULT_FINAL_DT, DW_LOAD_DT) <= 4
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW.FACT_LAB_RESULT
    WHERE RESULT_FINAL_DT >= DATEADD(day, -7, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.95 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.95
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- ============================================================================
-- FINANCIAL DATA QUALITY CHECKS
-- ============================================================================

-- FIN-001: Charge Amount Validity
-- Business Rule: Charges should be positive and within reasonable range
-- Threshold: 99%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'FIN-001' AS rule_id,
        'Charge Amount Validity' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN CHARGE_AMT > 0 AND CHARGE_AMT < 1000000
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW.FACT_CHARGE
    WHERE SERVICE_DT >= DATEADD(day, -30, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.99 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.99
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- FIN-003: Claim-Encounter Linkage
-- Business Rule: Claims should link to valid encounters
-- Threshold: 99%
-- Severity: HIGH

WITH RuleExecution AS (
    SELECT
        'FIN-003' AS rule_id,
        'Claim-Encounter Linkage' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE WHEN enc.ENCOUNTER_ID IS NOT NULL THEN 1 ELSE 0 END) AS passing_records
    FROM DW.FACT_CLAIM clm
    LEFT JOIN DW.FACT_ENCOUNTER enc ON clm.ENCOUNTER_ID = enc.ENCOUNTER_ID
    WHERE clm.CLAIM_CREATE_DT >= DATEADD(day, -30, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 4) AS quality_score,
    0.99 AS threshold,
    CASE WHEN passing_records / NULLIF(total_records, 0) >= 0.99
         THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- ============================================================================
-- HIPAA COMPLIANCE CHECKS
-- ============================================================================

-- HIPAA-001: PHI Access Logging
-- Business Rule: All PHI access should be logged
-- Threshold: 100%
-- Severity: CRITICAL (Regulatory)

WITH RuleExecution AS (
    SELECT
        'HIPAA-001' AS rule_id,
        'PHI Access Logging' AS rule_name,
        COUNT(*) AS total_records,
        SUM(CASE
            WHEN ACCESS_LOG_ID IS NOT NULL
            THEN 1 ELSE 0
        END) AS passing_records
    FROM DW_ADMIN.AUDIT_PHI_ACCESS
    WHERE ACCESS_DT >= DATEADD(day, -1, CURRENT_DATE)
)
SELECT
    rule_id,
    rule_name,
    total_records,
    passing_records,
    total_records - passing_records AS failing_records,
    ROUND(passing_records / NULLIF(total_records, 0), 6) AS quality_score,
    1.0 AS threshold,
    CASE WHEN passing_records = total_records THEN TRUE ELSE FALSE END AS passed
FROM RuleExecution;


-- ============================================================================
-- QUALITY SCORECARD GENERATION
-- ============================================================================

-- Daily Quality Scorecard by Domain
CREATE OR REPLACE VIEW DW_ADMIN.V_DQ_SCORECARD_BY_DOMAIN AS
SELECT
    DATE_TRUNC('day', EXECUTION_DT) AS REPORT_DT,
    DOMAIN,
    COUNT(*) AS RULE_COUNT,
    SUM(CASE WHEN PASSED_IND THEN 1 ELSE 0 END) AS RULES_PASSED,
    SUM(CASE WHEN NOT PASSED_IND THEN 1 ELSE 0 END) AS RULES_FAILED,
    ROUND(AVG(QUALITY_SCORE), 4) AS AVG_QUALITY_SCORE,
    MIN(QUALITY_SCORE) AS MIN_QUALITY_SCORE
FROM DW_ADMIN.DQ_RULE_RESULTS
WHERE EXECUTION_DT >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY DATE_TRUNC('day', EXECUTION_DT), DOMAIN
ORDER BY REPORT_DT DESC, DOMAIN;


-- Daily Quality Scorecard by Dimension
CREATE OR REPLACE VIEW DW_ADMIN.V_DQ_SCORECARD_BY_DIMENSION AS
SELECT
    DATE_TRUNC('day', EXECUTION_DT) AS REPORT_DT,
    DIMENSION,
    COUNT(*) AS RULE_COUNT,
    SUM(CASE WHEN PASSED_IND THEN 1 ELSE 0 END) AS RULES_PASSED,
    ROUND(AVG(QUALITY_SCORE), 4) AS AVG_QUALITY_SCORE
FROM DW_ADMIN.DQ_RULE_RESULTS
WHERE EXECUTION_DT >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY DATE_TRUNC('day', EXECUTION_DT), DIMENSION
ORDER BY REPORT_DT DESC, DIMENSION;


-- Overall Enterprise Quality Score Trend
CREATE OR REPLACE VIEW DW_ADMIN.V_DQ_ENTERPRISE_TREND AS
SELECT
    DATE_TRUNC('day', EXECUTION_DT) AS REPORT_DT,
    COUNT(*) AS TOTAL_RULES,
    SUM(CASE WHEN PASSED_IND THEN 1 ELSE 0 END) AS RULES_PASSED,
    ROUND(AVG(QUALITY_SCORE), 4) AS ENTERPRISE_QUALITY_SCORE,
    SUM(FAILING_RECORDS) AS TOTAL_FAILING_RECORDS
FROM DW_ADMIN.DQ_RULE_RESULTS
WHERE EXECUTION_DT >= DATEADD(day, -90, CURRENT_DATE)
GROUP BY DATE_TRUNC('day', EXECUTION_DT)
ORDER BY REPORT_DT DESC;


-- ============================================================================
-- ALERT GENERATION FOR FAILED RULES
-- ============================================================================

-- Critical Alerts (for immediate notification)
CREATE OR REPLACE VIEW DW_ADMIN.V_DQ_CRITICAL_ALERTS AS
SELECT
    r.RULE_ID,
    r.RULE_NAME,
    r.DOMAIN,
    r.DIMENSION,
    r.QUALITY_SCORE,
    r.THRESHOLD,
    r.FAILING_RECORDS,
    r.EXECUTION_DT,
    'CRITICAL: ' || r.RULE_NAME || ' failed with score ' ||
        ROUND(r.QUALITY_SCORE * 100, 2) || '% (threshold: ' ||
        ROUND(r.THRESHOLD * 100, 2) || '%)' AS ALERT_MESSAGE
FROM DW_ADMIN.DQ_RULE_RESULTS r
WHERE r.PASSED_IND = FALSE
  AND r.EXECUTION_DT >= DATEADD(hour, -24, CURRENT_TIMESTAMP)
  AND r.RULE_ID IN ('PAT-005', 'CLN-002', 'HIPAA-001')  -- Critical rules
ORDER BY r.EXECUTION_DT DESC;


-- End of quality rules SQL
