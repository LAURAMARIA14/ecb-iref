# ADR-003: Bitemporal + Tri-temporal

**Status:** Accepted
**Context:** IReF late arrivals T+30 require correction handling per ECB reg.

**Decision:** 
- Silver: valid_from/to, system_from/to, is_current
- Gold: fact_iref_bitemporal (bitemporal) + corrections_log (tri-temporal: reporting_time)

**Consequence:** v_fact_iref_bird serves current view, corrections_log keeps full history for audit.