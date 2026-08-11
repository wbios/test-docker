import pytest

@pytest.fixture(autouse=True)
def test_database(monkeypatch):
	monkeypatch.setenv("DB_NAME", "testdb")
