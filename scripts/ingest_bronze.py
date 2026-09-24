import pandas as pd
from pathlib import Path
import shutil
import glob

# CAI ABSOLUTE DIN PROIECTUL TAU
BASE = Path(__file__).resolve().parent.parent
BRONZE_EXT = BASE / "data" / "minio" / "bronze" / "external"
BRONZE_INT = BASE / "data" / "minio" / "bronze" / "internal"
BRONZE_EXT.mkdir(parents=True, exist_ok=True)
BRONZE_INT.mkdir(parents=True, exist_ok=True)

src = BRONZE_EXT /"BSI_M_DE_A20_S11_2023-12.csv"
dst_ext = src 
if not src.exists():
      raise FileNotFoundError(f"Nu exista fisierul sursa bun: {src}")
    
print(f"[1/2] Copiat extern: {src.name} -> {dst_ext}")

# CITIRE ROBUSTA - ia ultima valoare numerica din fisier, indiferent de header
df_ext = pd.read_csv(dst_ext, header=0)
# ultima coloana, ultimul rand, curatat de ghilimele si virgula
raw_val = str(df_ext.iloc[-1, -1])
real_value = float(raw_val.replace('"','').replace(',','').strip())
print(f"Valoare REALA Dec 2023 (ECB): {real_value}")

# FAKE intern +1.8% ca sa iasa FAIL la reconciliere
fake_value = round(real_value * 1.018, 2)
df_fake = pd.DataFrame([{
    "ref_period": "2023-12",
    "counterparty": "S11",
    "country": "DE",
    "indicator": "A20",
    "amount": fake_value
}])
dst_int = BRONZE_INT / "internal_loans_DE_S11_2023-12.csv"
df_fake.to_csv(dst_int, index=False)
print(f"[2/2] Creat intern fake: {fake_value} -> {dst_int}")
print("OK Bronze - ready")

real_internal_value = round(real_value * 1.0000008,2)

df_real = pd.DataFrame([{
    "ref_period": "2023-12",
    "counterparty": "S11",
    "country": "DE",
    "indicator": "A20",
    "amount": real_internal_value
}])

dst_int_real= BRONZE_INT / "internal_loans_DE_S11_2023-12_REAL.csv"
df_real.to_csv(dst_int_real, index=False)
print(f"Creat intern REAL PASS: {real_internal_value}")
