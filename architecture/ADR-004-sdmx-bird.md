# ADR-004: SDMX -> BIRD Semantic Layer

**Status:** Accepted
**Context:** CBA requires BIRD/SDMX interoperability.

**Decision:** Gold view v_fact_iref_bird maps instrument_fact -> BIRD cubes. SDMX parsing in Bronze via sdmx1 lib.

**Consequence:** Regulatory reporting ready, no vendor lock-in, supports AnaCredit to IReF transition.