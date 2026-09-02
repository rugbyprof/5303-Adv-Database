"""
Smoke tests -- prove the wiring works. Extend these as you implement phases.

A tiny database is generated once per test session into a temp file, and
app.db.DB_PATH is pointed at it before the app is imported.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest

STARTER = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    db = tmp_path_factory.mktemp("data") / "test.db"

    import scale_data
    scale_data.build(str(db), customers=200, products=150, zipcodes=60,
                     purchases=3_000, skew=True, seed=7)

    os.environ["DB_PATH"] = str(db)
    os.environ.pop("API_KEYS", None)          # dev mode -> no key needed

    from fastapi.testclient import TestClient
    import app.db
    importlib.reload(app.db)                  # pick up DB_PATH
    import app.main
    importlib.reload(app.main)

    with TestClient(app.main.app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json() == {"ok": True}


def test_get_customer_ok(client):
    r = client.get("/customers/1")
    assert r.status_code == 200
    body = r.json()
    assert body["customer_id"] == 1
    assert "@" in body["email"]
    assert len(body["state_code"]) == 2


def test_get_customer_404(client):
    assert client.get("/customers/999999").status_code == 404


def test_products_pagination(client):
    r = client.get("/products", params={"limit": 10, "offset": 5})
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_purchases_date_range(client):
    r = client.get("/purchases", params={"start": "2024-01-01", "end": "2027-01-01", "limit": 5})
    assert r.status_code == 200
    assert 1 <= len(r.json()) <= 5


def test_phase2_still_stubbed(client):
    # delete this test once you implement Phase 2
    assert client.get("/stats/revenue-by-state").status_code == 501
