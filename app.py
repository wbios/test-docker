from flask import Flask, render_template, request, redirect, flash
import psycopg2

app =  Flask(__name__)
app.secret_key = "dev-secret-key"

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
	
	return render_template("users.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
	name = request.form["name"].strip()
	if not name:
		flash("Il nome è obbligatorio")
		return redirect("/")

	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
	
	conn.commit()

	cur.close()
	conn.close()

	return redirect("/")

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

	conn.commit()

	cur.close()
	conn.close()

	return redirect("/")

@app.route("/edit/<int:user_id>")
def edit_user(user_id):
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))

	user = cur.fetchone()

	cur.close()
	conn.close()

	return render_template("edit.html", user=user)

@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
	name = request.form["name"].strip()
	if not name:
		flash("Il nome è obbligatorio")
		return redirect(f"/edit/{user_id}")
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("UPDATE users SET name = %s WHERE id = %s;", (name, user_id))

	conn.commit()

	cur.close()
	conn.close()

	return redirect("/")


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)
