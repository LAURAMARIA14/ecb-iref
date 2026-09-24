import requests, json
base = "http://localhost:19120/api/v2"
# iau hash-ul
r = requests.get(f"{base}/trees/branch/main", headers={"Accept":"application/json"})
print("BRANCH:", r.status_code)
print(r.text[:600])
h = r.json().get("hash") or r.json().get("reference",{}).get("hash") or r.headers.get("ETag")
print("HASH:", h)

new_loc = "s3://gold/fact_iref_bitemporal-033258327a6241c38181a9f4984b49df/metadata/00009-c1827d75-eb41-46dc-bed4-1959be2e15f2.metadata.json"

payload = {
 "parentHash": h,
 "commitMeta": {"message": "WORM+PUFFIN FINAL 00009"},
 "operations": [{
   "type": "PUT",
   "key": {"elements": ["gold","fact_iref_bitemporal"]},
   "contents": {"type": "ICEBERG_TABLE", "metadataLocation": new_loc}
 }]
}
r2 = requests.post(f"{base}/trees/branch/main/history/commit", json=payload, headers={"Accept":"application/json"})
print("COMMIT:", r2.status_code)
print(r2.text[:1000])