from flask import render_template, url_for, flash, redirect, request
from hello import app, bcrypt
from hello.forms import RegistrationForm, LoginForm
from hello.models import User, Post
import pypyodbc




posts = [

]

connection = pypyodbc.connect('Driver={SQL Server}; Server=LAPTOP-RUUC0E0L; Database=Users; trusted_connection=yes')
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/home2")
def home2():
    return render_template('home2.html', posts=posts)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST':
            result = request.form
            cursor1 = connection.cursor()
            insert = ("INSERT INTO details "
                      "(email, password, username) "
                      "VALUES(?,?,?)")
            values = list(result.values())
            values = [values[2], values[3], values[1]]
            cursor1.execute(insert, values)
            connection.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = connection.cursor()
            username_form = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT email,password "
                      "FROM details "
                      "WHERE email= ?")
            cu.execute(select, [username_form])
            results = cu.fetchone()
            print(results)
            if username_form and password_form in results:
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('home2'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminlogin", methods=['GET', 'POST'])
def Adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        cursor2 = connection.cursor()
        SQLCommand = ("SELECT email "
                      "FROM adminlogin")
        cursor2.execute(SQLCommand)
        results = cursor2.fetchall()
        print(results)
        connection.commit()

        for lis in results:
            if str(form.email.data) in lis[0][0]:
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)
