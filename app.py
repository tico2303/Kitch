from flask import Flask,render_template, redirect, url_for, request
from models import *
from forms import *
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

@login_required
@app.route('/kitch', methods=["GET","POST"])
def kitch():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("kitch.html", chef=chef)

@login_required
@app.route('/cart', methods=["GET","POST"])
def cart():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    cart = session.query(Cart).filter_by(chef_id=current_user.id).first()
    if cart == None: plates = None
    else: plates = cart.plates
    return render_template("cart.html", chef=chef, plates=plates)

@login_required
@app.route('/plates')
def plates():
    user = session.query(Chef).filter_by(id=current_user.id).first()
    kitch = session.query(Kitch).filter_by(chef_id = user.id).first()
    plates = session.query(Plate).filter_by(kitch_id = kitch).all()
    return render_template("plates.html", chef=user,plates=plates)


@login_required
@app.route('/create_plate', methods = ["GET", "POST"])
def create_plate():
    user = session.query(Chef).filter_by(id=current_user.id).first()
    kitch = session.query(Kitch).filter_by(chef_id = user.id).first()
    plates = session.query(Plate).filter_by(kitch_id = kitch).all()
    form = CreatePlateForm()
    if form.validate_on_submit():
        plate = Plate(kitch_id=kitch, name=form.plate_name.data, is_public=True) 
        plate.items.append(Item(name=form.item_one.data, price=form.price_one.data))
        plate.items.append(Item(name=form.item_two.data, price=form.price_two.data))
        plate.items.append(Item(name=form.item_three.data, price=form.price_three.data))
        session.add(plate)
        session.commit()
        return redirect(url_for('plates'))
    return render_template("create_plate.html", form = form)

@login_required
@app.route('/menus')
def menus():
    user = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("menus.html", chef=user)

@login_required
@app.route('/patron-orders')
def patron_orders():
    user = session.query(Chef).filter_by(id=current_user.id).first()
    #plates = session.query(Order).filter_by(plate.kitch_id=user.kitch).all()
    print plates
    return render_template("patron_orders.html", chef=user, plates=plates)

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

@app.route("/account")
@login_required
def account():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("account.html", chef = chef)

@app.route("/order-history")
@login_required
def orders():
    orders = session.query(Order).all()
    return render_template("order_history.html", orders=orders)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",var="Yes")

@app.route("/edit_address")
def edit_address():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("edit_address.html", chef=chef)

@app.route("/edit_login")
def edit_login():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("edit_login.html", chef=chef)

@app.route("/edit_payment_options")
def edit_payment_options():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    return render_template("edit_payment_options.html", chef=chef)

@app.route("/search/<filter>", methods=["GET", "POST"])
def search(filter=None):
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    print("filter: ", filter)
    if request.method == "POST":
        search_input = request.form["search_input"] 
        print("search input: ", search_input)

        results = {}
        results["names"] = None
        results["plates"] = None
        results["city"] = None

        if filter == "Chef":
            names = session.query(Chef).filter_by(name=search_input).first()
            results["names"] = names
        elif filter == "Location":
            cities = session.query(Chef).filter_by(city=search_input).first()
        elif filter == "Food":
            results = session.query(Chef).filter_by(name=search_input).first()
        else:
            names = session.query(Chef).filter_by(name=search_input).all() 
            cities = session.query(Chef).filter_by(city=search_input).all() 
            plates = session.query(Plate).all()

            results["names"] = names
            results["plates"] = plates
            results["cities"] = cities

        return render_template("search_results.html",chef = chef, results=results)
    return "NO POST"

@app.route("/add_plate_to_cart/<plate_id>", methods=["POST"])
def add_plate_to_cart(plate_id):
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    print "Plate id:", plate_id
    plate = session.query(Plate).filter_by(id=plate_id).first()
    print plate
    cart = Cart(chef_id=chef.id)
    cart.plates.append(plate)
    session.add(cart)
    session.commit()
    return render_template("plate_added_successfully.html", plate=plate)

def get_price(plates):
    total = 0.0
    for plate in plates:
        total = plate.price + total
    return total

@app.route("/checkout", methods=["POST"])
def checkout():
    chef = session.query(Chef).filter_by(id=current_user.id).first()
    print chef.carts[0].plates
    order = Order(
    total = get_price(chef.carts[0].plates[0].items),
    delivery_option = "delivery",
    buyer_id = chef.id,
    is_delivered = False 
    )
    for plate in chef.carts[0].plates:
        order.plates.append(plate)

    session.add(order)
    session.delete(session.query(Cart).filter_by(chef_id=current_user.id).first())
    session.commit()
    return render_template("order_placed_successfully.html")


if __name__ == "__main__":
    app.run(debug=True)
