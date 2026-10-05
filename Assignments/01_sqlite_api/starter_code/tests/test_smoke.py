"""
Smoke tests -- prove the wiring works. Extend these as you implement routes.

A tiny database is generated once per test session into a temp data/ folder
(as idx_10k.db), and app.experiment.DATA_DIR is pointed at it before the app
is imported, so tests never touch your real data/ folder.
"""

from __future__ import annotations

import importlib
import os

import pytest


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    data = tmp_path_factory.mktemp("data")

    import scale_data
    scale_data.build(str(data / "idx_10k.db"), customers=200, products=150,
                     zipcodes=60, purchases=3_000, skew=True, seed=7)

    os.environ["DATA_DIR"] = str(data)
    os.environ.pop("API_KEYS", None)          # dev mode -> no key needed

    from fastapi.testclient import TestClient
    import app.experiment
    importlib.reload(app.experiment)          # pick up DATA_DIR
    import app.main
    importlib.reload(app.main)

    with TestClient(app.main.app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json() == {"ok": True}


def test_q01_envelope(client):
    r = client.get("/customers/1", params={"db": "idx_10k"})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"elapsed_ms", "row_count", "plan", "rows"}
    assert body["row_count"] == 1
    assert body["rows"][0]["customer_id"] == 1
    assert any("PRIMARY KEY" in line for line in body["plan"])


def test_q01_missing_customer_is_empty(client):
    r = client.get("/customers/999999", params={"db": "idx_10k"})
    assert r.status_code == 200
    assert r.json()["row_count"] == 0


def test_unknown_db_name_rejected(client):
    assert client.get("/customers/1", params={"db": "store"}).status_code == 422


def test_db_file_not_built(client):
    # valid name, but make_dbs.py hasn't built it in the temp data/ folder
    assert client.get("/customers/1", params={"db": "noidx_1m"}).status_code == 404
