import os
import psycopg2

def get_db_connection():
	return psycopg2.connect(
		host=os.getenv("DB_HOST", "database"), 
		database=os.getenv("DB_NAME", "testdb"), 
		user=os.getenv("DB_USER", "app"), 
		password=os.getenv("DB_PASSWORD", "password")
	)

def get_users():
	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("SELECT * FROM users")
			users = cur.fetchall()

			return users

def add_user(name):
	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("""INSERT INTO users (name) VALUES (%s) RETURNING id """, (name,))

def update_user(user_id, name):
	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("UPDATE users SET name = %s WHERE id = %s", (name, user_id))

def delete_user(user_id):
	with get_db_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
			return cur.rowcount
