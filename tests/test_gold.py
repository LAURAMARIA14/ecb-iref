def test_ranger_policy_exists():
    import json, pathlib
    p = pathlib.Path("governance/ranger-policies.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert "policies" in data

def test_audit_trail_exists():
    import pathlib
    assert pathlib.Path("docs/GOLD_S4_AUDIT_TRAIL_DIFF_0.0_NESSIE_20b2c9a_PASS.csv").exists()

def test_adrs_count():
    import pathlib
    adrs = list(pathlib.Path("architecture").glob("ADR-*.md"))
    assert len(adrs) >= 5, "Trebuie 5 ADRs pentru L2"