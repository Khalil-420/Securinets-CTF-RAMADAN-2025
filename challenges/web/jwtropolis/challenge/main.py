from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, verify_jwt_in_request, set_access_cookies, unset_jwt_cookies, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

import os, time, random, string, math

up = math.floor(time.time())
random.seed(up + os.getpid())

print("Starting server at", up)
print("Process ID:", os.getpid())

strongpassword = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

app = Flask(__name__)
app.config['SECRET_KEY'] = "".join(random.choice(string.printable) for _ in range(32))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/data/site.db'
app.config['JWT_SECRET_KEY'] = "".join(random.choice(string.printable) for _ in range(32))
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 

db = SQLAlchemy(app)
jwt = JWTManager(app)

FLAG = os.getenv("FLAG", "flag{this_is_a_fake_flag}")

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	avatar = db.Column(db.String(80), nullable=True)
	role = db.Column(db.Integer, nullable=False) # 0 = student, 1 = teacher, 2 = admin
	totp_secret = db.Column(db.Integer, nullable=True) # Only for admin users / 4 digits
 
@app.route("/status")
def status():
	return jsonify(status="OK", uptime=time.time() - up)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		totp_code = request.form.get("totp")

		u = User.query.filter_by(username=username).first()

		if not u or not check_password_hash(u.password, password):
			return render_template("login.html", error="Invalid username or password"), 400

		if u.role == 2:
			if not totp_code:
				return render_template("login.html", error="TOTP is required for admin users."), 400
			if totp_code != str(u.totp_secret):
				return render_template("login.html", error="Invalid TOTP code."), 400
		access_token = create_access_token(identity=username, additional_claims={'role': u.role, 'avatar': u.avatar, 'totp': u.totp_secret})
		resp = make_response(redirect(url_for('dashboard')))
		set_access_cookies(resp, access_token)
		return resp

	return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		existing_user = User.query.filter_by(username=username).first()
		if existing_user:
			return render_template('register.html', error="Username already taken"), 400
		hashed_password = generate_password_hash(password)
		new_user = User(username=username, password=hashed_password, role=0)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html')

def random_string(length):
	return "".join(random.choice(string.printable) for _ in range(length))

@app.route("/logout")
def logout():
	resp = make_response(redirect(url_for("login")))
	unset_jwt_cookies(resp)
	return resp

@app.route("/")
def index():
	if verify_jwt_in_request():
		return redirect(url_for("dashboard"))
	return redirect(url_for("login"))

@app.route("/dashboard")
@jwt_required()
def dashboard():
    username = get_jwt()["sub"]
    
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "User not found", 404
    
    if user.role == 2 and get_jwt()["totp"] == user.totp_secret:
        return render_template("dashboard.html", user=user, flag=FLAG)

    return render_template("dashboard.html", user=user, flag="are u admin? cuz i'm not :p")

@app.route("/fetchstaff")
@jwt_required()
def staff():
	if get_jwt()["role"] < 1:
		return "Unauthorized", 403
	staff = User.query.filter(User.role > 0).all()
	return jsonify([{"username": s.username, "avatar": s.avatar} for s in staff])


@app.errorhandler(Exception)
def handle_exception(error):
    return jsonify(error="Internal Server Error", message=str(error)), 500

if __name__ == "__main__":
	import redacted 
	app.run(host="0.0.0.0", port=5000)
