# ADR-001: Medallion + Iceberg V2

**Status:** Accepted
**Context:** ECB IReF L2 EL requires WORM audit + time travel per CBA Annex. Parquet fails SEC 17a-4(f).

**Decision:** Bronze (raw SDMX CSV) -> Silver LDM S4 (party_dim, instrument_fact, protection_dim, instrument_protection_link) -> Gold (fact_iref_bitemporal)

**Format:** Iceberg V2, format_version=2, Puffin bloom_filter on hash_row, partitioning by country,bank_id.

**Consequence:** ACID, time travel for corrections, GDPR delete via DML not rewrite.
