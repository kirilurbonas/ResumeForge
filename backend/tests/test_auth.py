import uuid


def test_register_login_me(client):
    suffix = uuid.uuid4().hex[:12]
    email = f"reg_{suffix}@example.com"
    username = f"reguser{suffix}"
    password = "Testpw11a"

    r = client.post(
        "/api/auth/register",
        json={"email": email, "username": username, "password": password},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == email
    assert "id" in body

    r2 = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert r2.status_code == 200
    token = r2.json()["access_token"]

    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["username"] == username


def test_upload_without_auth_returns_401(client):
    r = client.post("/api/resume/upload", files={"file": ("x.pdf", b"%PDF-1.4", "application/pdf")})
    assert r.status_code == 401
