# Source: ECB CBA Annex 1 - Fig A1.2 Applying normalisation (p14/25)

Flat Table (Bronze) -> Instrument + Counterparty (Silver LDM S4)

Implementation mapping:
- FLAT TABLE (Observed agent, Reference period, Instrument ID, Counterparty ID, Outstanding amount, ESA sector, Country) = bronze/DE_A20_S11 CSV
- TABLE Instrument (Observed agent, Instrument ID, Outstanding amount) = silver/instrument_fact
- TABLE Counterparty (Counterparty ID, ESA sector, Country) = silver/party_dim (KYC-aligned)

Plus National Extension Scenario 2: common + da_specific (DE)
Source: https://www.ecb.europa.eu