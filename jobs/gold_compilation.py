from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
EXT_FILE = BASE / "data" / "minio" / "bronze" / "external" / "BSI_M_DE_A20_S11_2023-12.csv"
INT_FILE = BASE / "data" / "minio" / "silver" / "reconciled" / "loans_2023-12.parquet"
GOLD_DIR = BASE / "data" / "minio" / "gold" / "report"
GOLD_DIR.mkdir(parents=True, exist_ok=True)

df_ext = pd.read_csv(EXT_FILE)
raw_val = str(df_ext.iloc[-1, -1])
real_value = float(raw_val.replace('"','').replace(',','').strip())

df_int = pd.read_parquet(INT_FILE)
fake_value = float(df_int.loc[0, "amount"])

diff_pct = abs(fake_value - real_value) / real_value * 100
status = "PASS" if diff_pct <= 1.0 else "FAIL"

report = pd.DataFrame([{
    "ref_period": "2023-12",
    "indicator": "BSI.M.DE.N.A.A20T.A.1.U2.2240.Z01.E",
    "external_ECB": real_value,
    "internal_fake": fake_value,
    "diff_pct": round(diff_pct, 4),
    "status": status
}])

out = GOLD_DIR / "reconciliation_2023-12.csv"
report.to_csv(out, index=False)
print(report.to_string(index=False))
print(f"\nOK Gold -> {out} | Status: {status} ({diff_pct:.2f}%)")