
from airflow import DAG
from datetime import datetime
import hashlib
# ECB Revision Policy Art 12 - prevent duplicate reporting
# source_hash=9333a436ff7cd7bc
# idempotency_key=f26e36808194d152bdeda7acdc3ad30697a2fc321304552d566f28947ea55b4c
def get_idempotency_key(ref_area, ref_period, source_hash):
    return hashlib.sha256(f"{ref_area}_{ref_period}_{source_hash}".encode()).hexdigest()
with DAG(dag_id="iref_bsi_medallion", start_date=datetime(2023,12,1), schedule_interval=None) as dag:
    pass
