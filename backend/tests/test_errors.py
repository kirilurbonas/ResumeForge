def test_not_found_returns_404_not_500(client, auth_headers):
    """HTTPException must not be converted to 500 by the global handler."""
    r = client.get(
        "/api/resume/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert r.status_code == 404
    assert r.json().get("detail")
