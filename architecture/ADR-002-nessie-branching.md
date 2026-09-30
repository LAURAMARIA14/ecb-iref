# ADR-002: Nessie + Ranger ABAC

**Status:** Accepted
**Context:** Need isolated testing for National Extensions (DE/FR) without affecting main.

**Decision:** Nessie branching: main -> dev/de_extension, dev/fr_extension. Merge via merge API.

**Security:** Ranger ABAC on party_dim (KYC), row-filter country=DE, column-mask counterparty_id.

**Consequence:** Zero-copy branching, audit per branch, compliance with DG-IS.