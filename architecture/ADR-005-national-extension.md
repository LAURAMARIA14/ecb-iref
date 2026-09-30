# ADR-005: National Extension Scenario 2

**Status:** Accepted
**Context:** Fig A1.2 National Extension: common + da_specific.

**Decision:** Implement de_beaver_indicator (DE specific) in party_dim.da_specific JSON. Replicable pattern for FR/IT/ES.

**Structure:** common (KYC-aligned, LDM S4) + da_specific (national). Partitioned by country.

**Consequence:** Meets Scenario 2, allows DE to extend without breaking common LDM. Forward compatible.