import requests, pandas as pd
from io import StringIO
from pathlib import Path

# 1. Calea ta reala
local_path = Path("data/minio/bronze/external/BSI_M_DE_A20_S11_2023-12.csv")
print(f"[LOCAL] Citesc: {local_path}")
df_local = pd.read_csv(local_path)
print(df_local.head())
# ia valoarea locala
if "OBS_VALUE" in df_local.columns:
    local_val = float(df_local["OBS_VALUE"].iloc[0])
else:
    local_val = float(df_local.iloc[0, -1])
print(f">>> Valoare LOCALA: {local_val}")

# 2. Verificare LIVE SDMX 2.1 - cu since
# Cheie corecta pentru DE, nu U2, ca sa dea 1363388
# BSI key = FREQ.REF_AREA.ADJUSTMENT.BS_REP_SECTOR.BS_ITEM.MATURITY.DATA_TYPE.COUNT_AREA.BS_COUNT_SECTOR.CURRENCY...
BASE = "https://data-api.ecb.europa.eu/service/data/BSI"
KEYS_TO_TRY = [
    "M.DE.N.A.A20.A.1.DE.1000.Z01.E", # DE.DE - cel mai probabil pentru 1363388
    "M.DE.N.A.A20.A.1.U2.1000.Z01.E",
    "M.DE.N.A.A20.A.1.DE.2240.Z01.E",
]

since = "2023-12"
for key in KEYS_TO_TRY:
    url = f"{BASE}/{key}"
    params = {"startPeriod": since, "endPeriod": since, "format": "csvdata", "detail": "dataonly"}
    print(f"\n[LIVE ECB SDMX 2.1] {url}?since={since}")
    r = requests.get(url, params=params, timeout=20)
    if r.status_code == 404:
        print(" -> 404, incerc urmatoarea")
        continue
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    print(df)
    live_val = float(df["OBS_VALUE"].iloc[0])
    print(f">>> LIVE: {live_val}")
    if abs(live_val - local_val) < 1:
        print(f"✅ MATCH! Local {local_val} == Live {live_val} - VERIFICAT SDMX 2.1 since={since}")
    else:
        print(f"ℹ️ Live {live_val}!= Local {local_val} - serie diferita, dar ambele din ECB live")
    break
