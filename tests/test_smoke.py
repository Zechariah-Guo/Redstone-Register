import importlib

import pytest


@pytest.fixture()
def client():
    import main

    return main.app.test_client()


@pytest.mark.parametrize("path", ["/", "/catalogue", "/about", "/offline", "/static/manifest.json"])
def test_pages_load(client, path):
    assert client.get(path).status_code == 200


def test_catalogue_search_returns_page(client):
    assert client.get("/catalogue?q=piston").status_code == 200


def test_security_headers(client):
    response = client.get("/")
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" not in response.headers


def test_service_worker_scope_header(client):
    response = client.get("/static/js/serviceworker.js")
    assert response.headers["Service-Worker-Allowed"] == "/"


def test_hsts_sent_behind_trusted_proxy(monkeypatch):
    monkeypatch.setenv("REDSTONE_TRUST_PROXY", "1")
    import main

    main = importlib.reload(main)
    try:
        response = main.app.test_client().get("/", headers={"X-Forwarded-Proto": "https"})
        assert "Strict-Transport-Security" in response.headers
    finally:
        monkeypatch.delenv("REDSTONE_TRUST_PROXY")
        importlib.reload(main)
