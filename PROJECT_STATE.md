# Air Cargo Lakehouse – Project State

## Repository
- **GitHub:** https://github.com/JGMaslowski/azure-aircargo-lakehouse

## Azure Infrastructure (`rg-aircargo-dev`, region: `Sweden Central`)
- **ADLS Gen2 (Storage):** `staircargodevjm` (containers: `landing`, `bronze`, `silver`, `gold`)
- **Event Hubs:** `evhns-aircargo-dev-jm` → event hub: `flight-telemetry`
- **Key Vault:** `kv-aircargo-dev-jm` (SAS secrets for Event Hubs)
- **Access Connector:** `ac-aircargo-dev-jm` (role: `Storage Blob Data Contributor` on ADLS Gen2)
- **Databricks Workspace:** `dbw-aircargo-dev-jm` (Hybrid, Premium)

## Databricks & Unity Catalog Configuration
- **Secret Scope:** `kv-aircargo-scope` (backed by `kv-aircargo-dev-jm`)
- **Storage Credential:** `sc_aircargo_dev`
- **External Locations:** `ext_aircargo_landing`, `ext_aircargo_bronze`, `ext_aircargo_silver`, `ext_aircargo_gold`
- **Catalog:** `aircargo_dev`
  - Schemas: `landing`, `bronze`, `silver`, `gold`
  - External Volume: `/Volumes/aircargo_dev/landing/raw_files/`

## Roadmap & Progress
- [x] Phase 1: Azure Infrastructure + Unity Catalog + Key Vault
- [x] Phase 2a: GitHub Integration (Databricks Git Folders)
- [ ] Phase 2b: Compute Cluster (FinOps) & Connectivity Validation
- [ ] Phase 3: Data Pipelines (Ingestion → Bronze → Silver → Gold)