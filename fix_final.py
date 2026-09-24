import boto3, json, requests, re, os
from botocore.client import Config

s3 = boto3.client('s3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

bucket = 'gold'
prefix = 'fact_iref_bitemporal-033258327a6241c38181a9f4984b49df/metadata/'

objs = s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get('Contents', [])
jsons = [o['Key'] for o in objs if o['Key'].endswith('.metadata.json')]
jsons.sort()
print(f"Am gasit {len(jsons)} fisiere metadata")
for j in jsons[-5:]:
    print(" ", j)

latest = jsons[-1]
print(f"\nLatest: {latest}")

data = json.loads(s3.get_object(Bucket=bucket, Key=latest)['Body'].read())
print("\nProprietati VECHI:", data.get('properties', {}))

props = data.setdefault('properties', {})
props['history.expire.min-snapshots-to-keep'] = '2147483647'
props['gc.enabled'] = 'false'
props['write.parquet.bloom-filter-enabled.column.hash_row'] = 'true'
props['write.parquet.bloom-filter-fpp.column.hash_row'] = '0.01'
props['write.metadata.metrics.default'] = 'full'

# new version number
m = re.search(r'/(\d+)-', latest)
ver = int(m.group(1)) + 1 if m else len(jsons)
new_key = re.sub(r'/\d+-', f'/{ver:05d}-', latest)
if new_key == latest:
    new_key = latest.replace('.metadata.json', f'.{ver}.metadata.json')

print(f"\nNew: {new_key}")
s3.put_object(Bucket=bucket, Key=new_key, Body=json.dumps(data, indent=2).encode())

# update Nessie
nessie = "http://localhost:19120/api/v2"
r = requests.get(f"{nessie}/trees/tree/main")
main_hash = r.json()['hash']
print(f"\nNessie main hash: {main_hash}")

table = "gold.fact_iref_bitemporal"
r2 = requests.get(f"{nessie}/trees/tree/main/contents?key={table}")
print(f"Get contents: {r2.status_code}")

try:
    table_id = r2.json()['contents'][0]['id']
except:
    table_id = "fact-iref-id"

new_location = f"s3://{bucket}/{new_key}"
payload = {
    "expectedHash": main_hash,
    "operations": [{
        "type": "PUT",
        "key": {"elements": table.split(".")},
        "contents": {
            "type": "ICEBERG_TABLE",
            "id": table_id,
            "metadataLocation": new_location
        }
    }],
    "commitMeta": {"message": "PASUL 8 - WORM + PUFFIN - ANTI-VACUUM"}
}

r3 = requests.post(f"{nessie}/trees/branch/main/commit", json=payload)
print(f"\nCommit: {r3.status_code}")
print(r3.text[:800])

if r3.status_code in [200,204]:
    print("\n✅✅✅ PASUL 8 GATA - WORM + PUFFIN SETAT! ✅✅✅")
    print(f"Locatie noua: {new_location}")
else:
    print("\n⚠️ Metadata scris, dar commit Nessie trebuie facut manual din UI")
    print(f"Locatie noua: {new_location}")