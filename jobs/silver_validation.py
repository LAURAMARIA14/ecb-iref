from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
INT_FILE = BASE / "data" / "minio" / "bronze" / "internal" / "internal_loans_DE_S11_2023-12.csv"
SILVER_DIR = BASE / "data" / "minio" / "silver" / "reconciled"
SILVER_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INT_FILE)
assert not df.empty, "Fisier intern gol"
assert df.loc[0, "ref_period"] == "2023-12"
assert float(df.loc[0, "amount"]) > 0

out = SILVER_DIR / "loans_2023-12.parquet"
df.to_parquet(out, index=False)
print(f"OK Silver: {out} cu {len(df)} randuri")