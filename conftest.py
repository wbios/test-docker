import pytest
from db import get_db_connection

@pytest.fixture(autouse=True)
def test_database(monkeypatch):
	monkeypatch.setenv("DB_NAME", "testdb")

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")

