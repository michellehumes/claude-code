"""
Healthcare Data Quality Monitoring Framework
=============================================
Enterprise data quality monitoring for healthcare data warehouse.

This module provides automated data quality checks for:
- Patient demographics completeness
- Clinical data integrity
- Cross-system consistency
- Regulatory compliance validation

Author: Data Strategy Consultant
Version: 2.1
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# Note: In production, these would use actual database connections
# Snowflake: snowflake-connector-python
# Great Expectations for advanced profiling

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityDimension(Enum):
    """Data quality dimensions based on DAMA-DMBOK framework."""
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"


class Severity(Enum):
    """Alert severity levels."""
    CRITICAL = "critical"  # Patient safety or compliance risk
    HIGH = "high"          # Significant business impact
    MEDIUM = "medium"      # Moderate operational impact
    LOW = "low"            # Minor issue, workaround available


@dataclass
class QualityRule:
    """Definition of a data quality rule."""
    rule_id: str
    name: str
    description: str
    dimension: QualityDimension
    domain: str  # Patient, Clinical, Financial, etc.
    severity: Severity
    threshold: float  # Acceptable threshold (e.g., 0.95 for 95%)
    sql_check: str
    remediation: str


@dataclass
class QualityResult:
    """Result of a quality rule execution."""
    rule_id: str
    execution_time: datetime
    total_records: int
    passing_records: int
    failing_records: int
    score: float
    passed: bool
    details: Optional[str] = None


# ============================================================================
# PATIENT DEMOGRAPHICS QUALITY RULES
# ============================================================================

PATIENT_QUALITY_RULES = [
    QualityRule(
        rule_id="PAT-001",
        name="Patient Name Completeness",
        description="All patients must have first and last name populated",
        dimension=QualityDimension.COMPLETENESS,
        domain="Patient",
        severity=Severity.HIGH,
        threshold=0.99,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN PAT_FIRST_NAME IS NOT NULL
                         AND PAT_LAST_NAME IS NOT NULL
                         AND TRIM(PAT_FIRST_NAME) != ''
                         AND TRIM(PAT_LAST_NAME) != ''
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.DIM_PATIENT
            WHERE ACTIVE_IND = 'Y'
        """,
        remediation="Review registration workflow; check interface mappings from source EMR"
    ),

    QualityRule(
        rule_id="PAT-002",
        name="Date of Birth Validity",
        description="DOB must be valid date, not in future, and patient not >120 years old",
        dimension=QualityDimension.VALIDITY,
        domain="Patient",
        severity=Severity.HIGH,
        threshold=0.99,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN PAT_BIRTH_DT IS NOT NULL
                         AND PAT_BIRTH_DT <= CURRENT_DATE
                         AND PAT_BIRTH_DT >= DATEADD(year, -120, CURRENT_DATE)
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.DIM_PATIENT
            WHERE ACTIVE_IND = 'Y'
        """,
        remediation="Investigate source system data entry; implement DOB validation at registration"
    ),

    QualityRule(
        rule_id="PAT-003",
        name="SSN Format Validity",
        description="If SSN populated, must be valid 9-digit format (not all zeros or 9s)",
        dimension=QualityDimension.VALIDITY,
        domain="Patient",
        severity=Severity.MEDIUM,
        threshold=0.95,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN PAT_SSN IS NULL
                         OR (REGEXP_LIKE(PAT_SSN, '^[0-9]{9}$')
                             AND PAT_SSN NOT IN ('000000000', '999999999', '123456789'))
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.DIM_PATIENT
            WHERE ACTIVE_IND = 'Y'
        """,
        remediation="Review SSN collection process; may indicate test data in production"
    ),

    QualityRule(
        rule_id="PAT-004",
        name="Address Completeness",
        description="Active patients should have complete address (street, city, state, zip)",
        dimension=QualityDimension.COMPLETENESS,
        domain="Patient",
        severity=Severity.MEDIUM,
        threshold=0.90,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN PAT_STREET_ADDR IS NOT NULL
                         AND PAT_CITY IS NOT NULL
                         AND PAT_STATE IS NOT NULL
                         AND PAT_ZIP IS NOT NULL
                         AND TRIM(PAT_STREET_ADDR) != ''
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.DIM_PATIENT
            WHERE ACTIVE_IND = 'Y'
              AND LAST_ENCOUNTER_DT >= DATEADD(year, -2, CURRENT_DATE)
        """,
        remediation="Update registration address requirements; consider address verification service"
    ),

    QualityRule(
        rule_id="PAT-005",
        name="MRN Uniqueness",
        description="Medical Record Numbers must be unique across the enterprise",
        dimension=QualityDimension.UNIQUENESS,
        domain="Patient",
        severity=Severity.CRITICAL,
        threshold=1.0,
        sql_check="""
            WITH DuplicateMRNs AS (
                SELECT MRN, COUNT(*) as cnt
                FROM DW.DIM_PATIENT
                WHERE ACTIVE_IND = 'Y'
                GROUP BY MRN
                HAVING COUNT(*) > 1
            )
            SELECT
                (SELECT COUNT(*) FROM DW.DIM_PATIENT WHERE ACTIVE_IND = 'Y') as total_records,
                (SELECT COUNT(*) FROM DW.DIM_PATIENT WHERE ACTIVE_IND = 'Y')
                    - COALESCE((SELECT SUM(cnt) FROM DuplicateMRNs), 0) as passing_records
        """,
        remediation="CRITICAL: Investigate MPI matching algorithm; manual review of duplicates required"
    ),
]


# ============================================================================
# CLINICAL DATA QUALITY RULES
# ============================================================================

CLINICAL_QUALITY_RULES = [
    QualityRule(
        rule_id="CLN-001",
        name="Encounter Diagnosis Presence",
        description="Inpatient encounters should have at least one diagnosis code",
        dimension=QualityDimension.COMPLETENESS,
        domain="Clinical",
        severity=Severity.HIGH,
        threshold=0.98,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN dx.ENCOUNTER_ID IS NOT NULL THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_ENCOUNTER enc
            LEFT JOIN (
                SELECT DISTINCT ENCOUNTER_ID
                FROM DW.FACT_DIAGNOSIS
            ) dx ON enc.ENCOUNTER_ID = dx.ENCOUNTER_ID
            WHERE enc.ENCOUNTER_TYPE = 'INPATIENT'
              AND enc.DISCHARGE_DT IS NOT NULL
              AND enc.DISCHARGE_DT >= DATEADD(day, -90, CURRENT_DATE)
        """,
        remediation="Review clinical documentation workflows; coordinate with HIM for coding backlog"
    ),

    QualityRule(
        rule_id="CLN-002",
        name="Admission/Discharge Date Logic",
        description="Discharge date must be >= admission date",
        dimension=QualityDimension.VALIDITY,
        domain="Clinical",
        severity=Severity.CRITICAL,
        threshold=1.0,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN DISCHARGE_DT >= ADMIT_DT OR DISCHARGE_DT IS NULL
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_ENCOUNTER
            WHERE ENCOUNTER_TYPE = 'INPATIENT'
              AND ADMIT_DT >= DATEADD(year, -1, CURRENT_DATE)
        """,
        remediation="CRITICAL: Data integrity issue; investigate ETL date handling logic"
    ),

    QualityRule(
        rule_id="CLN-003",
        name="Provider Attribution",
        description="Encounters should have an attending provider assigned",
        dimension=QualityDimension.COMPLETENESS,
        domain="Clinical",
        severity=Severity.MEDIUM,
        threshold=0.95,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN ATTENDING_PROVIDER_ID IS NOT NULL THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_ENCOUNTER
            WHERE ENCOUNTER_TYPE IN ('INPATIENT', 'OUTPATIENT')
              AND ADMIT_DT >= DATEADD(day, -30, CURRENT_DATE)
        """,
        remediation="Review provider assignment workflow in source EMR; check interface mappings"
    ),

    QualityRule(
        rule_id="CLN-004",
        name="Lab Result Timeliness",
        description="Lab results should load within 4 hours of finalization",
        dimension=QualityDimension.TIMELINESS,
        domain="Clinical",
        severity=Severity.HIGH,
        threshold=0.95,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN TIMESTAMPDIFF(hour, RESULT_FINAL_DT, DW_LOAD_DT) <= 4
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_LAB_RESULT
            WHERE RESULT_FINAL_DT >= DATEADD(day, -7, CURRENT_DATE)
        """,
        remediation="Review lab interface performance; check ETL job schedules"
    ),
]


# ============================================================================
# FINANCIAL DATA QUALITY RULES
# ============================================================================

FINANCIAL_QUALITY_RULES = [
    QualityRule(
        rule_id="FIN-001",
        name="Charge Amount Validity",
        description="Charge amounts should be positive and within reasonable range",
        dimension=QualityDimension.VALIDITY,
        domain="Financial",
        severity=Severity.HIGH,
        threshold=0.99,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN CHARGE_AMT > 0 AND CHARGE_AMT < 1000000
                    THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_CHARGE
            WHERE SERVICE_DT >= DATEADD(day, -30, CURRENT_DATE)
        """,
        remediation="Review charge master entries; investigate outlier charges"
    ),

    QualityRule(
        rule_id="FIN-002",
        name="Insurance Eligibility",
        description="Encounters should have insurance coverage verified",
        dimension=QualityDimension.COMPLETENESS,
        domain="Financial",
        severity=Severity.MEDIUM,
        threshold=0.90,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN cov.ENCOUNTER_ID IS NOT NULL THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_ENCOUNTER enc
            LEFT JOIN DW.FACT_COVERAGE cov ON enc.ENCOUNTER_ID = cov.ENCOUNTER_ID
            WHERE enc.ADMIT_DT >= DATEADD(day, -30, CURRENT_DATE)
              AND enc.ENCOUNTER_TYPE IN ('INPATIENT', 'OUTPATIENT', 'EMERGENCY')
        """,
        remediation="Review eligibility verification workflow; check payer connection status"
    ),

    QualityRule(
        rule_id="FIN-003",
        name="Claim-Encounter Linkage",
        description="Claims should link to valid encounters",
        dimension=QualityDimension.CONSISTENCY,
        domain="Financial",
        severity=Severity.HIGH,
        threshold=0.99,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN enc.ENCOUNTER_ID IS NOT NULL THEN 1 ELSE 0 END) as passing_records
            FROM DW.FACT_CLAIM clm
            LEFT JOIN DW.FACT_ENCOUNTER enc ON clm.ENCOUNTER_ID = enc.ENCOUNTER_ID
            WHERE clm.CLAIM_CREATE_DT >= DATEADD(day, -30, CURRENT_DATE)
        """,
        remediation="Investigate orphan claims; review claim generation logic"
    ),
]


# ============================================================================
# CROSS-SYSTEM CONSISTENCY RULES
# ============================================================================

CONSISTENCY_RULES = [
    QualityRule(
        rule_id="XSY-001",
        name="Patient Count Reconciliation",
        description="Patient counts should match between source EMR and warehouse",
        dimension=QualityDimension.CONSISTENCY,
        domain="Cross-System",
        severity=Severity.HIGH,
        threshold=0.999,
        sql_check="""
            -- This would compare against a staging table with source counts
            SELECT
                src.PATIENT_CNT as total_records,
                CASE WHEN ABS(src.PATIENT_CNT - dw.PATIENT_CNT) / src.PATIENT_CNT <= 0.001
                     THEN src.PATIENT_CNT ELSE 0 END as passing_records
            FROM DW.RECON_SOURCE_COUNTS src
            CROSS JOIN (SELECT COUNT(*) as PATIENT_CNT FROM DW.DIM_PATIENT WHERE ACTIVE_IND='Y') dw
            WHERE src.SOURCE_SYSTEM = 'EPIC'
              AND src.ENTITY = 'PATIENT'
              AND src.RECON_DT = CURRENT_DATE
        """,
        remediation="Investigate ETL load process; check for failed incremental loads"
    ),

    QualityRule(
        rule_id="XSY-002",
        name="Provider Master Sync",
        description="Active providers should exist in both credentialing and clinical systems",
        dimension=QualityDimension.CONSISTENCY,
        domain="Cross-System",
        severity=Severity.MEDIUM,
        threshold=0.98,
        sql_check="""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN cred.PROVIDER_ID IS NOT NULL THEN 1 ELSE 0 END) as passing_records
            FROM DW.DIM_PROVIDER prov
            LEFT JOIN DW.DIM_PROVIDER_CREDENTIALING cred
                ON prov.NPI = cred.NPI
            WHERE prov.ACTIVE_IND = 'Y'
              AND prov.PROVIDER_TYPE IN ('PHYSICIAN', 'APP')
        """,
        remediation="Review provider master data management process; sync credentialing system"
    ),
]


class DataQualityMonitor:
    """
    Enterprise data quality monitoring engine.

    Executes quality rules against Snowflake data warehouse and
    generates compliance reports for healthcare data governance.
    """

    def __init__(self, connection_params: dict):
        """
        Initialize the monitor with database connection parameters.

        Args:
            connection_params: Dict with Snowflake connection details
                - account, user, password, warehouse, database, schema
        """
        self.connection_params = connection_params
        self.rules = []
        self.results = []

    def register_rules(self, rules: list[QualityRule]):
        """Register quality rules for monitoring."""
        self.rules.extend(rules)
        logger.info(f"Registered {len(rules)} quality rules")

    def execute_rule(self, rule: QualityRule) -> QualityResult:
        """
        Execute a single quality rule and return results.

        In production, this would execute against Snowflake.
        """
        logger.info(f"Executing rule {rule.rule_id}: {rule.name}")

        # Placeholder for actual database execution
        # In production:
        # with snowflake.connector.connect(**self.connection_params) as conn:
        #     cursor = conn.cursor()
        #     cursor.execute(rule.sql_check)
        #     row = cursor.fetchone()
        #     total_records = row[0]
        #     passing_records = row[1]

        # Simulated results for demonstration
        total_records = 1000000
        passing_records = int(total_records * (rule.threshold + 0.01))  # Slightly above threshold

        score = passing_records / total_records if total_records > 0 else 0
        passed = score >= rule.threshold

        result = QualityResult(
            rule_id=rule.rule_id,
            execution_time=datetime.now(),
            total_records=total_records,
            passing_records=passing_records,
            failing_records=total_records - passing_records,
            score=score,
            passed=passed
        )

        if not passed:
            logger.warning(
                f"Rule {rule.rule_id} FAILED: {score:.2%} < {rule.threshold:.2%} threshold"
            )
        else:
            logger.info(f"Rule {rule.rule_id} PASSED: {score:.2%}")

        return result

    def run_all_rules(self) -> list[QualityResult]:
        """Execute all registered rules and return results."""
        self.results = []

        for rule in self.rules:
            result = self.execute_rule(rule)
            self.results.append(result)

        return self.results

    def generate_scorecard(self) -> dict:
        """
        Generate a quality scorecard summary.

        Returns:
            Dict with overall scores by dimension and domain
        """
        if not self.results:
            return {}

        # Calculate scores by dimension
        dimension_scores = {}
        for dim in QualityDimension:
            dim_rules = [r for r in self.rules if r.dimension == dim]
            dim_results = [res for res in self.results
                         if res.rule_id in [r.rule_id for r in dim_rules]]
            if dim_results:
                avg_score = sum(r.score for r in dim_results) / len(dim_results)
                dimension_scores[dim.value] = round(avg_score, 4)

        # Calculate scores by domain
        domain_scores = {}
        domains = set(r.domain for r in self.rules)
        for domain in domains:
            domain_rules = [r for r in self.rules if r.domain == domain]
            domain_results = [res for res in self.results
                            if res.rule_id in [r.rule_id for r in domain_rules]]
            if domain_results:
                avg_score = sum(r.score for r in domain_results) / len(domain_results)
                domain_scores[domain] = round(avg_score, 4)

        # Overall score
        overall_score = sum(r.score for r in self.results) / len(self.results)

        return {
            "execution_time": datetime.now().isoformat(),
            "total_rules": len(self.rules),
            "rules_passed": sum(1 for r in self.results if r.passed),
            "rules_failed": sum(1 for r in self.results if not r.passed),
            "overall_score": round(overall_score, 4),
            "dimension_scores": dimension_scores,
            "domain_scores": domain_scores
        }

    def get_failed_rules(self) -> list[tuple[QualityRule, QualityResult]]:
        """Return list of failed rules with their results."""
        failed = []
        for result in self.results:
            if not result.passed:
                rule = next(r for r in self.rules if r.rule_id == result.rule_id)
                failed.append((rule, result))
        return failed

    def generate_alert(self, rule: QualityRule, result: QualityResult) -> dict:
        """Generate an alert for a failed rule."""
        return {
            "alert_time": datetime.now().isoformat(),
            "rule_id": rule.rule_id,
            "rule_name": rule.name,
            "severity": rule.severity.value,
            "dimension": rule.dimension.value,
            "domain": rule.domain,
            "score": result.score,
            "threshold": rule.threshold,
            "failing_records": result.failing_records,
            "remediation": rule.remediation
        }


def main():
    """Main execution for data quality monitoring."""

    # Initialize monitor (connection params would come from secure config)
    monitor = DataQualityMonitor(
        connection_params={
            "account": "mrhs_snowflake",
            "warehouse": "ANALYTICS_WH",
            "database": "ENTERPRISE_DW",
            "schema": "DW"
        }
    )

    # Register all rule sets
    monitor.register_rules(PATIENT_QUALITY_RULES)
    monitor.register_rules(CLINICAL_QUALITY_RULES)
    monitor.register_rules(FINANCIAL_QUALITY_RULES)
    monitor.register_rules(CONSISTENCY_RULES)

    # Execute all rules
    logger.info("Starting data quality monitoring run...")
    results = monitor.run_all_rules()

    # Generate scorecard
    scorecard = monitor.generate_scorecard()
    logger.info(f"Quality Scorecard: {scorecard}")

    # Handle failures
    failed_rules = monitor.get_failed_rules()
    if failed_rules:
        logger.warning(f"{len(failed_rules)} rules failed quality checks")
        for rule, result in failed_rules:
            alert = monitor.generate_alert(rule, result)
            logger.warning(f"ALERT: {alert}")
            # In production: send to alerting system (PagerDuty, ServiceNow, etc.)

    return scorecard


if __name__ == "__main__":
    main()
