from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Database
db = mysql.connector.connect(
	host="easy-table.cqungzqiodei.ap-southeast-1.rds.amazonaws.com",
	user="admin",
	passwd="9X4&34exf$5Q#",
	database="easytabledatabase"
	)

mycursor = db.cursor(buffered=True)

@app.route("/", methods=["GET", "POST"])
def index():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")

	# if method is POST
	if request.method == "POST":
		user_id = str(session["user_id"])
		if "search_column" in request.form:			
			query = "SELECT * FROM items WHERE user_id=" + user_id + " AND " + request.form['search_column'] + " LIKE '%" + request.form["search_input"] + "%'"
			mycursor.execute(query)

		if "sort_column" in request.form:
			query = "SELECT * FROM items WHERE user_id=" + user_id + " ORDER BY " + request.form['sort_column'] + " " + request.form["sort_type"]
			mycursor.execute(query)
	# if method is GET
	else:
		mycursor.execute("SELECT * FROM items WHERE user_id=%s", [session["user_id"]])
	column_names = mycursor.column_names
	items = mycursor.fetchall()
	return render_template("index.html", 
		column_names = column_names, 
		items = items, 
		plusitem = session["plusitem"], 
		item_id = session["item_id"], 
		pluscolumn = session["pluscolumn"],
		edit_column = session["edit_column"])

@app.route("/addnewcolumn", methods=["GET", "POST"])
def addnewcolumn():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")

	if request.method == "POST":
		query = "ALTER TABLE items ADD " + request.form["new_column_name"] + " TEXT NOT NULL"
		mycursor.execute(query)
		db.commit()
		session["pluscolumn"] = False
		return redirect("/")

	session["pluscolumn"] = True
	return redirect("/")

@app.route("/deletecolumn", methods=["GET", "POST"])
def deletecolumn():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")
	query = "ALTER TABLE items DROP COLUMN " + request.form["delete_column"]
	mycursor.execute(query)
	db.commit()
	return redirect("/")

@app.route("/editcolumn", methods=["GET", "POST"])
def editcolumn():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")
	if "change_column_name" in request.form:
		query = "ALTER TABLE items RENAME COLUMN " + session["edit_column"] + " TO " + request.form["change_column_name"]
		mycursor.execute(query)
		db.commit()
		session["edit_column"] = None
		return redirect("/")
	session["edit_column"] = request.form["edit_column"]
	return redirect("/")

@app.route("/addnewitem", methods=["GET", "POST"])	
def addnewitem():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")

	# if method is POST
	if request.method == "POST":
		columnnames = "user_id,"
		columns = "%s,"
		columnvalues = [session["user_id"]]
		for column in request.form:
			columnnames += column + ","
			columns += "%s,"
			columnvalues.append(request.form[column])
		query = "INSERT INTO items (" + columnnames[:-1] + ") VALUES(" + columns[:-1] + ")"
		mycursor.execute(query, columnvalues)
		db.commit()
		session["plusitem"] = False
		return redirect("/")

	# if method is GET
	session["plusitem"] = True
	return redirect("/")

@app.route("/deleteitem", methods=["GET", "POST"])
def deleteitem():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")

	item_id = request.form["item_id"]
	mycursor.execute("DELETE FROM items WHERE item_id=%s", [item_id])
	db.commit()
	return redirect("/")

@app.route("/edititem", methods=["GET", "POST"])
def edititem():
	# if not logged in, redirect to registration
	if "user_id" not in session:
		return redirect("/register")

	if "Name" in request.form:
		data = ""
		for column in request.form:
			if column == "item_id":
				item_id = [request.form["item_id"]]
			else:
				data += column + "= '" + request.form[column] + "' ,"
		query = "UPDATE items SET " + data[:-1] + " WHERE item_id=%s"
		# return f"{query}"
		mycursor.execute(query, item_id)
		db.commit()
		session["item_id"] = None
		return redirect("/")
	session["item_id"] = int(request.form["item_id"])
	return redirect("/")


@app.route("/admin")
def admin():
	mycursor.execute("SELECT * FROM users")
	users = mycursor.column_names
	fusers = mycursor.fetchall()
	mycursor.execute("SELECT * FROM items")
	items = mycursor.fetchall()
	return f"{users} \n{fusers} \n{items}"

@app.route("/register", methods=["GET", "POST"])
def register():

	# clear previous session
	session.clear()

	# check method
	if request.method == "POST":

		# check user submit errors
		# check if username is submitted
		if not request.form["username"]:
			return render_template("register.html", alert_type="alert alert-danger", message="Please submit Username.")
		# check if password is submitted
		elif not request.form["password"]:
			return render_template("register.html", alert_type="alert alert-danger", message="Please submit Password.")
		# check if password confirmation is correct
		elif request.form["password"] != request.form["confirmation"]:
			return render_template("register.html", alert_type="alert alert-danger", message="Confirm Password is not the same with Password")

		# if user submits are correct, check with database
		mycursor.execute("SELECT * FROM users WHERE username=%s", [request.form["username"]])
		row = mycursor.fetchall()
		# check if username already exists
		if row:
			return render_template("register.html", alert_type="alert alert-danger", message="Username already exists.")

		# if all submits are valid, create new account for the user
		# create hash for the password
		new_hash = generate_password_hash(request.form["password"])
		# create new account
		mycursor.execute("INSERT INTO users (username, hash) VALUES(%s, %s)", [request.form["username"], new_hash])
		db.commit()

		# Log user into the session
		mycursor.execute("SELECT * FROM users WHERE username=%s", [request.form["username"]])
		row = mycursor.fetchall()
		session["user_id"] = row[0][0]
		session["plusitem"] = False
		session["item_id"] = None
		session["pluscolumn"] = False
		session["edit_column"] = None
		return redirect("/")

	else:
		return render_template("register.html", alert_type="alert alert-secondary", message="If you already have an accout, please click Login.")

@app.route("/login", methods=["GET", "POST"])
def login():

	# clear previous session
	session.clear()

	# check method
	if request.method == "POST":

		# check user submit errors
		# check if username is submitted
		if not request.form["username"]:
			return render_template("login.html", alert_type="alert alert-danger", message="Please submit Username.")
		# check if password is submitted
		elif not request.form["password"]:
			return render_template("login.html", alert_type="alert alert-danger", message="Please submit Password.")

		# if user submits are correct, check with database
		mycursor.execute("SELECT * FROM users WHERE username=%s", [request.form["username"]])
		row = mycursor.fetchall()
		# check if username already exists
		if not row or not check_password_hash(row[0][2], request.form["password"]):
			return render_template("login.html", alert_type="alert alert-danger", message="Invalid Username/Password.")

		# if all submits are valid, Log user into the session
		else:
			session["user_id"] = row[0][0]
			session["plusitem"] = False
			session["item_id"] = None
			session["pluscolumn"] = False
			session["edit_column"] = None
			return redirect("/")

	else:
		return render_template("login.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/register")

if __name__=="__main__":
	app.run(debug=True)

"""
	Bugs:
	- creating new columns with already existed names
"""