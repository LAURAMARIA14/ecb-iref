# ECB IReF L2 EL - LDM S4 Fig A1.2 - 0.1% Implementation
# 4 core entities per CBA Annex Fig A1.2 Table A1.2

"""
Medallion Architecture - LDM S4 to Gold:

Bronze -> Silver LDM S4 (Fig A1.2):
- party_dim (KYC-aligned, common)
- instrument_fact (core granular)
- protection_dim (common)
- instrument_protection_link (link table)
+ National Extension Scenario 2: common + da_specific (da_beaver_indicator) - DE extension replicable to FR/IT/ES

Silver -> Gold:
- fact_iref_bitemporal (bitemporal: valid_from, valid_to, system_from, system_to, is_current, hash_row)
- corrections_log (tri-temporal: reporting_time for Late Arrival T+30)
- v_fact_iref_bird (BIRD/SDMX semantic view)

Governance: WORM SEC 17a-4(f) + Iceberg V2 + Puffin bloom filter + Nessie branching + Ranger ABAC 
"""

print("LDM S4: party_dim -> instrument_fact -> protection_dim -> instrument_protection_link")
print("Gold: fact_iref_bitemporal (bitemporal) + corrections_log (tri-temporal) + v_fact_iref_bird (BIRD)")
print("Compliance: format_version=2, bloom_filter on hash_row, partitioning by country,bank_id")