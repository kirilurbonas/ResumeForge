def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["service"] == "resume-forge"
    assert data.get("checks", {}).get("database") is True
    assert "X-Request-ID" in r.headers


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "ResumeForge" in r.json().get("message", "")
