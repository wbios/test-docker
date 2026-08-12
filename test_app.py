from app import app
from db import get_db_connection

def test_home(monkeypatch):
	client = app.test_client()
	response = client.get("/")
	assert response.status_code == 200

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
