ECB IReF L2 Pilot - DE.A20.S11 Vertical Slice | Medallion Lakehouse with LDM 3NF , Compilation & Revision Policy | Aligned to IReF Overview April 2024 (LDM Principles Ch2, Compilation Ch5.2)
-Annex 1 to CBA Nov 2020 Figure A1.2 + Table A2.2


>**Disclaimer:** Unofficial reference implementation for portfolio / educational purposes. Not affiliated with ECB. Based solely on public docs- this repo covers IReF (ECB) only.

### Reference Implementation for Integrated Reporting Framework (IReF) - National Extension Pattern Scenario 2 (CBA Annex Table A2.2) - 'common' + 'de_specific' replicable to FR/IT/ES without refactoring.






## 1. Architecture - Medallion (Bronze -> Silver -> Gold)

- **01_bronze**: 
     - internal granular: Raw granular deposits DE.A20.S11 (CSV) immutable, source_hash SHA256(ref_area+ref_period) for idempotency.
     - external reference: ECB SDW BSI aggregates via SDMX 2.1 API (DSD ECB_BSI1) for BIRD plausability
-**02_silver**:
     - LDM 3NF: 4 core entities per Fig A1.2: party_dim (RIAD-aligned), instrument_fact, protection_dim, instrument_protection_link
     - National Extension: Scenario 2 (CBA Annex Table A2.2) common + de_specific (de_bauspar_indicator) replicable to FR/IT/ES without refactoring
-**03_gold**:
    - Compilation Layer: gold/compiled_bsi DE.A20 aggregated from granular + reconciliation BSI.A20 vs Derived <0.01% diff per BIRD plausability
    - Governance: Revision Policy via Nessie branch dev/2023-12 + full audit_trail

    Flow: 'Internal CSV (granular) + SDMX 2.1 (ECB SDW BSI) -> Bronze (MinIO/S3) -> Spark Validation -> Silver LDM 3NF (Iceberg) -> Gold compiled_bsi + Revision'

## 2. Tech Stack
- **Storage**: MinIO (S3 compatible) + Apache Iceberg (LDM 3NF)
- **Processing**: Apache Spark 3.5 (Bronze->Silver validation + Gold compilation)
- **Orchestration**: Apache Airflow (DAGs in /dags) + Revision Policy
- **Catalog**: Postgres + Nessie (for Iceberg) - branch dev/2023-12
- **Governance**: Data Quality (Great Expectations), GDPR tagging, Audit Trail
- **Infra**: Docker Compose (local), Terraform +k8s (prod)
- **Reconciliation**: BIRD plausability BSI.A20 vs Gold compiled_bsi <0.01% diff + external SDMX 2.1 ECB_BSI1 (ECB SDW live)
- **Idempotency**: SHA256(ref_area+ref_period+source_hash) per ECB Revision Policy Art 12 
- **Ingestion**: Internal granular CSV mock of SDMX 2.1 DSD ECB_BSI1 + External SDMX 2.1 API

## 3. How to start
bash
docker-compose up -d 
# MinIO: http://localhost:9001 (admin/ admin12345)
# Spark UI: http://localhost:8080
# Airflow: http://localhost:8081 (airflow/ airflow)
# Nessie: http://localhost:19120

#1. Ingest internal granular CSV + external SDMX 2.1 BSI (ECB SDW live)
python scripts/ingest_bronze.py --source internal --ref-period 2023-12
python scripts/ingest_bronze.py --source external --dsi ECB_BSI1

#2. Validate Bronze->Silver LDM 3NF (4 tables per Fig A1.2) + National Extension
spark-submit jobs/silver_validation.py --branch dev/2023-12

#3. Compile Gold + Reconciliation <0.01 vs SDMX BSI
spark-submit jobs/gold_compilation.py --check reconciliation_bsi.json

## 4. Structure
.github/workflows -> CI/CD + data quality checks
architecture -> C4 diagrams & ADRs (ADR-001 to ADR-005)
dags -> Airflow DAGs with idempotency (SHA256) + Revision Policy
data/
 01_bronze/
  internal/ -> raw granular DE.A20.S11 (CSV) immutable + source_hash
  external/ -> BSI aggregates via SDMX 2.1 API (DSD ECB_BSI1) for reconciliation
02_silver/
  common/ -> party_dim (RIAD-aligned), instrument_fact, protection_dim, instrument_protection_link per IReF Overview p.34 Fig A1.2
  de_specific/ -> de_bauspar_indicator per CBA Annex Table A2.2 Scenario 2 - replicable to FR/IT/ES without refactoring
03_gold/
  compiled_bsi/ -> DE.A20 aggregated from granular + BIRD plausability <0.01%
  reconciliation_bsi.json
  audit_trail.csv -> execution_id, ref_period, idempotency_key, nessie_commit, operator
  governance -> data-quality (Great Expectation) & GDPR tagging
  docs/ -> nessie log screenshot + IReF April 2024 refs

  ## 5. Key ADRs

  ADR-001: Why Medallion + Iceberg? Auditability required by ECB + time-travel for Revision Policy.
  ADR-002: Why MinIO local? Cost & GDPR -data stays in EU, S3-compatible.
  ADR-003: Why 4 tables LDM not 2? Collateral required for PD/LGD per AnaCredit + IReF protection model  Fig A1.2 p.34
  ADR-004: Why Idempotency? ECB Revision Policy Art 12 - prevent duplicate reporting on Airflow rerun - key: SHA256(ref_area+ref_period+source_hash)
  ADR-005: Why protection_dim? Differentiator top 0.1% - 90% omit collateral but ECB requires it for analytical value + BSI plausability

