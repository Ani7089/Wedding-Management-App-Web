from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Guest, Task, Vendor, Expense
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/guests')
@login_required
def guests():
    guests = Guest.query.filter_by(user_id=current_user.id).all()
    return render_template('guests.html', title='Guests', guests=guests)

@app.route('/guest/new', methods=['GET', 'POST'])
@login_required
def new_guest():
    form = GuestForm()
    if form.validate_on_submit():
        guest = Guest(name=form.name.data, email=form.email.data, category=form.category.data, author=current_user)
        db.session.add(guest)
        db.session.commit()
        flash('Guest has been added!', 'success')
        return redirect(url_for('guests'))
    return render_template('create_guest.html', title='New Guest', form=form)

@app.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', title='Tasks', tasks=tasks)

@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, deadline=form.deadline.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task has been created!', 'success')
        return redirect(url_for('tasks'))
    return render_template('create_task.html', title='New Task', form=form)


@app.route('/vendors')
@login_required
def vendors():
    vendors = Vendor.query.filter_by(user_id=current_user.id).all()
    return render_template('vendors.html', title='Vendors', vendors=vendors)

@app.route('/vendor/new', methods=['GET', 'POST'])
@login_required
def new_vendor():
    form = VendorForm()
    if form.validate_on_submit():
        vendor = Vendor(name=form.name.data, contact_info=form.contact_info.data, service_type=form.service_type.data, author=current_user)
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor has been added!', 'success')
        return redirect(url_for('vendors'))
    return render_template('create_vendor.html', title='New Vendor', form=form)


@app.route('/expenses')
@login_required
def expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('expenses.html', title='Expenses', expenses=expenses)

@app.route('/expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, amount=form.amount.data, category=form.category.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Expense has been added!', 'success')
        return redirect(url_for('expenses'))
    return render_template('create_expense.html', title='New Expense', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
