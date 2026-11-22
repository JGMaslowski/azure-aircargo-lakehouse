# Air Cargo Lakehouse – Project State

## Repository
- **GitHub:** https://github.com/JGMaslowski/azure-aircargo-lakehouse

## Azure Infrastructure (`rg-aircargo-dev`, region: `Sweden Central`)
- **ADLS Gen2 (Storage):** `staircargodevjm` (containers: `landing`, `bronze`, `silver`, `gold`)
- **Event Hubs:** `evhns-aircargo-dev-jm` → event hub: `flight-telemetry`
- **Key Vault:** `kv-aircargo-dev-jm` (SAS secrets: `eh-flight-telemetry-listen-conn`, `eh-flight-telemetry-send-conn`)
- **Access Connector:** `ac-aircargo-dev-jm` (role: `Storage Blob Data Contributor` on ADLS Gen2)
- **Databricks Workspace:** `dbw-aircargo-dev-jm` (Hybrid, Premium)

## Databricks & Unity Catalog Configuration
- **Secret Scope:** `kv-aircargo-scope` (backed by `kv-aircargo-dev-jm`)
- **Compute (FinOps):** `cluster-aircargo-dev` (`Standard_D4ds_v5`, 4 cores / 16 GB RAM, Single Node, Photon off, auto-termination: 15 min)
- **Storage Credential:** `sc_aircargo_dev`
- **External Locations:** `ext_aircargo_landing`, `ext_aircargo_bronze`, `ext_aircargo_silver`, `ext_aircargo_gold`
- **Catalog:** `aircargo_dev`
  - Schemas: `landing`, `bronze`, `silver`, `gold`
  - External Volume: `/Volumes/aircargo_dev/landing/raw_files/`

---

## Production Roadmap (8 End-to-End Phases)

### Phase 0: Foundations, Git & Budget Guardrails
- [x] Create GitHub repository and initialize branching strategy (`main` + feature branches)
- [x] Configure Azure subscription, region (`Sweden Central`), and budget alerts
- [x] Establish FinOps baseline (cost tracking, auto-shutdown policies)

### Phase 1: Core Azure Infrastructure & Ingestion Backbone
- [x] Deploy ADLS Gen2 storage accounts (`landing`, `bronze`, `silver`, `gold`)
- [x] Configure Azure Key Vault and store Event Hubs SAS policies
- [x] Provision Event Hubs namespace & `flight-telemetry` event hub
- [x] Deploy Azure Databricks Premium workspace and configure Azure Access Connector (managed identity)
- [x] Configure OpenSky API producer / telemetry simulation pipeline to Event Hubs (`01_flight_telemetry_producer`)

### Phase 2: Bronze Layer (Streaming, Batch & Data Quarantine)
- [x] Configure Unity Catalog 3-level namespace (`aircargo_dev`), external locations & volumes
- [x] Provision FinOps-optimized compute (`cluster-aircargo-dev`, Single Node, 15m idle shutdown)
- [x] Validate end-to-end connectivity (Key Vault secrets scope + Volume read/write)
- [x] Implement Spark Structured Streaming from Event Hubs using `Trigger.AvailableNow` (cost-optimized micro-batch)
- [ ] Ingest static/batch reference datasets into `/Volumes/aircargo_dev/landing/raw_files/` (airports, weather, synthetic cargo manifests)
- [x] Persist append-only Delta tables in `aircargo_dev.bronze` with ingestion audit metadata (`_ingest_timestamp`, `_source_file`)
- [x] Build Quarantine table pattern for malformed JSON payloads and schema drift

### Phase 3: Silver Layer (Cleansing, H3 Indexing, SCD & PII Governance)
- [ ] Parse and unpack nested JSON payloads (`from_json`, array exploding, schema enforcement)
- [ ] Implement spatial indexing using Uber H3 grid for real-time flight position mapping
- [ ] Implement Slowly Changing Dimensions (SCD Type 1 for cargo status, SCD Type 2 for flight legs) using `MERGE INTO`
- [ ] Configure Unity Catalog data governance: column-level masking and tag-based policies for sensitive client PII
- [ ] Enrich streaming telemetry with reference airport coordinates and ambient weather dimensions

### Phase 4: Code Modularization, Unit Testing & CI/CD
- [ ] Establish secure CI/CD service principal or GitHub Actions OIDC connection to Azure
- [ ] Refactor PySpark transformation logic from notebooks into modular Python packages (`src/`)
- [ ] Write unit tests using `pytest` and `chispa` (DataFrame assertions)
- [ ] Configure GitHub Actions workflow: automated linting (`black`, `flake8`), static checks, and unit test runner
- [ ] Enforce Pull Request (PR) review workflow before merging into `main`

### Phase 5: Gold Layer (Star Schema, Business Metrics & Performance Tuning)
- [ ] Design Dimensional Model (Fact tables: `fact_cargo_tracking`, `fact_flight_delays`; Dimension tables: `dim_aircraft`, `dim_airport`)
- [ ] Calculate core KPIs: cargo transit delays, fuel burn proxies, SLA breaches, high-risk corridor analytics
- [ ] Performance Tuning & Storage Optimization:
  - Benchmark query plans using `EXPLAIN EXTENDED`
  - Evaluate and implement Liquid Clustering (`CLUSTER BY`) vs. traditional Z-ORDER
  - Schedule table maintenance routines (`OPTIMIZE`, `VACUUM`)

### Phase 6: Orchestration & Production Workflows
- [ ] Define production DAG in Databricks Workflows (ingestion → bronze → silver → gold)
- [ ] Configure cost-effective ephemeral Job Clusters (auto-provision and terminate per run)
- [ ] Set up retry policies, task dependencies, and alert notifications (email/webhook on failure)
- [ ] Parameterize pipeline runs for backfilling and scheduled incremental loads

### Phase 7: Analytics Serving, Power BI & Portfolio Documentation
- [ ] Expose Gold Delta tables via Databricks SQL Serverless Warehouse
- [ ] Connect Power BI (or build Databricks native SQL Dashboards) for executive & operational tracking
- [ ] Generate architectural diagrams (data flow, network boundaries, medallion transitions)
- [ ] Complete comprehensive technical `README.md` highlighting architecture decisions, FinOps savings, and engineering tradeoffs