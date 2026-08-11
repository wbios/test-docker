from flask import Flask, render_template, request, redirect, flash
from db import get_users, add_user, update_user, delete_user

app =  Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
	users = get_users()
	return render_template("users.html", users=users)

@app.route("/add", methods=["POST"])
def add_user_route():
	name = request.form["name"].strip()
	if not name:
		flash("Il nome è obbligatorio")
		return redirect("/")

	add_user(name)

	return redirect("/")

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user_route(user_id):
	deleted = delete_user(user_id)
	if deleted ==0:
		flash("Utente non trovato")
	else:
		flash("Utente eliminato")
	return redirect("/")

@app.route("/edit/<int:user_id>")
def edit_user(user_id):
	conn = get_db_connection()
	cur = conn.cursor()

	cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))

	user = cur.fetchone()
	if user is None:
		flash("Utente non trovato")
		return redirect("/")

	cur.close()
	conn.close()

	return render_template("edit.html", user=user)

@app.route("/update/<int:user_id>", methods=["POST"])
def update_user_route(user_id):
	name = request.form["name"].strip()
	if not name:
		flash("Il nome è obbligatorio")
		return redirect(f"/edit/{user_id}")

	update_user(user_id, name)
	return redirect("/")


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)
