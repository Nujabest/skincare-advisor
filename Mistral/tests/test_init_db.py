# tests/test_init_db.py
import os
from backend.init_db import init_db

def test_init_db_creates_file(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{test_db_path}")

    init_db()

    # Le fichier SQLite doit exister après la création des tables
    assert test_db_path.is_file()
