from flask import Flask
import psycopg2

app =  Flask(__name__)
def get_db_connection():
	return psycopg2.connect(
		host="database", database="testdb", user="app", password="password"
		)

@app.route("/")
def home():
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("SELECT * FROM users;")
	users = cur.fetchall()

	cur.close()
	conn.close()
	
	return str(users)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)
