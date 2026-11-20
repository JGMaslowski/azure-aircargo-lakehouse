Markdown
# Air Cargo Lakehouse – Stan Projektu

## Repozytorium
- **GitHub:** https://github.com/JGMaslowski/azure-aircargo-lakehouse

## Infrastruktura Azure (`rg-aircargo-dev`, region: `Sweden Central`)
- **ADLS Gen2 (Storage):** `staircargodevjm` (kontenery: `landing`, `bronze`, `silver`, `gold`)
- **Event Hubs:** `evhns-aircargo-dev-jm` → strumień: `flight-telemetry`
- **Key Vault:** `kv-aircargo-dev-jm` (sekrety SAS dla Event Hubs)
- **Access Connector:** `ac-aircargo-dev-jm` (rola: `Storage Blob Data Contributor` na ADLS)
- **Databricks Workspace:** `dbw-aircargo-dev-jm` (Hybrid, Premium)

## Konfiguracja Databricks & Unity Catalog
- **Secret Scope:** `kv-aircargo-scope` (podpięty do `kv-aircargo-dev-jm`)
- **Storage Credential:** `sc_aircargo_dev`
- **External Locations:** `ext_aircargo_landing`, `ext_aircargo_bronze`, `ext_aircargo_silver`, `ext_aircargo_gold`
- **Catalog:** `aircargo_dev`
  - Schematy: `landing`, `bronze`, `silver`, `gold`
  - External Volume: `/Volumes/aircargo_dev/landing/raw_files/`

## Postęp
- [x] Faza 1: Infrastruktura Azure + Unity Catalog + Key Vault
- [x] Faza 2a: Integracja GitHub (Git Folders)
- [ ] Faza 2b: Klaster obliczeniowy (FinOps) i test połączeń
- [ ] Faza 3: Pipeline'y (Ingestion → Bronze → Silver → Gold)