from flask import Flask,render_template, redirect, url_for, request
from models import *
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
session = setUpSession()

@login_manager.user_loader
def load_user(user_id):
    return session.query(Chef).filter_by(id=user_id).first()

@app.route('/kitch', methods=["GET","POST"])
def kitch():
    user = session.query(Chef).filter_by(id=current_user.id).first()
    return "<h1> %s's Kitch Called Successfully. </h1> "%(user.name)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #return '<h1>' + form.username.data  + " " + form.password.data + "</h1>"
        #get first user in query because usernames are unique
        user = session.query(Chef).filter_by(name=form.username.data).first()
        if user:
            # checking password in db against what user entered in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.password.data)
                return redirect(url_for('home'))
        return "<h1>Invalid Username or Password</h1>"
    return render_template("login.html", form=form)


@app.route('/signup',methods=["GET","POST"])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = Chef(name=form.username.data, 
                                email=form.email.data, 
                                password=hashed_password,
                                street=form.street.data,
                                city=form.city.data,
                                state=form.state.data,
                                zip_code=form.zip_code.data,
                                apt_number=form.apt_number.data,
                                phone_number=form.phone_number.data
                                )
		session.add(new_user)
		session.commit()
		return "<h1> New user has been created </h1>"
	return render_template("signup.html", form=form)

@app.route("/home")
@login_required
def home():
    chefs = session.query(Chef).all()
    return render_template("home.html",chefs=chefs)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",var="Yes")

@app.route("/search/<filter>", methods=["GET", "POST"])
def search(filter=None):
    #print("Search param: ", search_term)
    print("filter: ", filter)
    if request.method == "POST":
        search_input = request.form["search_input"] 
        print("search input: ", search_input)
        results = []
        if filter == "Chef":
            results = session.query(Chef).filter_by(name=search_input).first()
        elif filter == "Location":
            results = session.query(Chef).filter_by(address=search_input).first()
        elif filter == "Food":
            results = session.query(Chef).filter_by(name=search_input).first()
        else:
            results = session.query(Chef).filter_by(name=search_input).first()
        return "<h1> %s </h1>"%(results.address)
    return "NO POST"


if __name__ == "__main__":
    app.run(debug=True)
