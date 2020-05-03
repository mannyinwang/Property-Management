from flask import Flask, redirect, request, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy import func
import re

app = Flask(__name__)
app.secret_key = 'burrito'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# The Admin creates the apartments in the apartment table and creates the employees.
# The admin determines the access level of the employees
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'Name: {self.first_name} {self.last_name} | email:{self.email} | <admin id: {self.id}>'


# Table for Employees with the column type specifying the employee
# Specifies if the employee is  admin side or in the maintenance side.
# If the type is '0' the employee is admin and if '1' the employee is in maintenance
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    type = db.Column(db.Integer)
    position = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Name: {self.first_name} {self.last_name}> <Email: {self.email} > <ID: {self.id}>'


# Table for the Apartments
# Number is for apartment number, Room is number of rooms
class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    apartment_number = db.Column(db.String(20))
    number_of_room = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('apt_categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    apartment_tenant = db.relationship('Tenant', backref='apartments')

    def __repr__(self):
        return f'<Apartment Number: {self.number}> <Number of Rooms: {self.room} > <ID: {self.id}>'


# category for the type of apartment, price for the cost of the apartment
class ApartmentCategory(db.Model):
    __tablename__ = 'apt_categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(45))
    price = db.Column(db.Integer)  # Change the datatype to float
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    category_apartment = db.relationship('Apartment', backref='apt_categories')

    def __repr__(self):
        return f'<Apartment category: {self.category}> <NPrice to Rent Room: {self.price} > <ID: {self.id}>'


# Table for the Tenants
class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(45))
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)

    def __repr__(self):
        return f'<Name: {self.first_name} {self.last_name}> <Email: {self.email} > <ID: {self.id}>'


@app.route('/')
def landing():
    return render_template('landing.html')


# *******************************************************************************************
# All routes that have to do with Admin
# *******************************************************************************************
@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/admin_login', methods=['post'])
def admin_login():
    admin = Admin.query.filter_by(email=request.form['email']).all()
    valid = True if len(admin) == 1 and admin[0].password == request.form['password'] else False
    if valid:
        session['cur_user'] = admin[0].id
        print(session['cur_user'])
        print(admin)
        return redirect('/admin_view')
    else:
        flash('Invalid User credentials')
        return redirect('/admin')


@app.route('/admin_view')
def ad_view():
    if 'cur_user' not in session:
        flash('Please Log In')
        return redirect('/admin')
    get_category = ApartmentCategory.query.all()
    get_apartment = Apartment.query.all()
    get_employee = Employee.query.all()
    print(session['cur_user'])
    print('current session')
    admin = Admin.query.get(session['cur_user'])
    print('I am waiting')
    print(admin.last_name)
    return render_template('admin_view.html', admin=admin,
                           categories=get_category,
                           apartments=get_apartment,
                           employees=get_employee)


@app.route('/add_category', methods=['post'])
def cat():
    add_category = ApartmentCategory(category=request.form['category'],
                                     price=request.form['price'])
    db.session.add(add_category)
    db.session.commit()
    return redirect('/admin_view')


@app.route('/add_employee', methods=['post'])
def emp_add():
    employee_add = Employee(first_name=request.form['fname'],
                            last_name=request.form['lname'],
                            email=request.form['email'],
                            password=request.form['pwd'],
                            position=request.form['position'],
                            type=request.form['access'])
    db.session.add(employee_add)
    db.session.commit()
    return redirect('/admin_view')


@app.route('/add_apartment', methods=['post'])
def add_apt():
    apt_add = Apartment(apartment_number=request.form['apt_no'],
                        number_of_room=request.form['no_room'],
                        category_id=request.form['category'])
    db.session.add(apt_add)
    db.session.commit()
    return redirect('/admin_view')


@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect("admin")


# *******************************************************************************************
# All routes that have to do with the Employees
# *******************************************************************************************


# **********************************************************************************************
# All Routes that have to do with Tenants
# **********************************************************************************************
@app.route('/new_tenant')
def new():
    return render_template('create_tenant.html')


@app.route('/register', methods=['post'])
def new_user():
    is_valid = True
    if len(request.form['fname']) < 2:
        is_valid = False
        flash("First name must be at least 3 characters long")
    if len(request.form['lname']) < 2:
        is_valid = False
        flash("Last name must be at least 3 characters long")
    if len(request.form['pwd']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long")
    if request.form['cpwd'] != request.form['pwd']:
        is_valid = False
        flash("Passwords must match")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address")

    if not is_valid:
        return redirect('/')
    if is_valid:
        add_user = Tenant(first_name=request.form['fname'],
                          last_name=request.form['lname'],
                          email=request.form['email'],
                          password=request.form['pwd'])
        db.session.add(add_user)
        db.session.commit()
        print('Added a New User')
        print(add_user)
        return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == ' __main__':
    app.run(debug=True)
