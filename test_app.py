from app import app
from db import get_db_connection

def test_home(monkeypatch):
	client = app.test_client()
	response = client.get("/")
	assert response.status_code == 200

def test_add_user_empty_name():
	client = app.test_client()

	response = client.post(
		"/add", data={"name":""}
		)

	assert response.status_code == 302

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"SELECT COUNT(*) FROM users"
			)
			count = cur.fetchone()[0]
	assert count == 0

def test_add_user():
	client = app.test_client()
	response = client.post(
		"/add",
		data={"name" : "Test User"}
	)

	assert response.status_code == 302

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"SELECT name FROM users WHERE name = %s",
				("Test User",)
			)
			user = cur.fetchone()
	assert user is not None
	assert user[0] == "Test User"

def test_update_user(user):
	user_id = user[0]
	client = app.test_client()

	response = client.post(
		f"/update/{user_id}", data={"name":"Mario Updated"}
	)

	assert response.status_code == 302

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"SELECT name FROM users WHERE id = %s", (user_id,)
			)
			user = cur.fetchone()

	assert user is not None
	assert user[0] == "Mario Updated"

def test_update_user_empty_name(user):
	user_id = user[0]
	client = app.test_client()
	response = client.post(
		f"/update/{user_id}", data={"name": ""}
		)
	assert response.status_code == 302

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"SELECT name FROM users WHERE id = %s", (user_id,)
			)
			result = cur.fetchone()
	assert result == ("Mario",)

def test_delete_user(user):
	user_id = user[0]
	client = app.test_client()
	response = client.post(f"/delete/{user_id}")

	assert response.status_code == 302

	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(
				"SELECT id FROM users WHERE id = %s", (user_id,)
			)
			user = cur.fetchone()

	assert user is None

def test_delete_user_not_found():
	client = app.test_client()
	response = client.post("/delete/9999")
	assert response.status_code == 302

