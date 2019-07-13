# imports
from flask import render_template, url_for, flash, redirect, request, session
from hello import app
from hello.forms import RegistrationForm, LoginForm, CandidateForm, SearchForm
import pypyodbc
import secrets
import os

connection = pypyodbc.connect('Driver={SQL Server}; Server=LAPTOP-RUUC0E0L; Database=Users; trusted_connection=yes')


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    print(form.s.data)
    result = None
    if form.validate_on_submit():
        print(form.s.data)
        cursor4 = connection.cursor()
        choice = form.s.data
        sch = form.s.data
        if choice == 'Skill':
            select = ("SELECT candidatename, skill"
                      "FROM candidatedel"
                      "WHERE skill = ?")
            print(choice)
        elif choice == 'Job Id':
            select = ("SELECT job_id "
                      "FROM candidatedel "
                      "WHERE job_id= ?")
        else:
            select = ("SELECT candidatename ,notice "
                      "FROM candidatedel "
                      "WHERE notice = ?")
        cursor4.execute(select, [sch])
        result = cursor4.fetchone()
        if not result:
            flash('No Result Found!', 'danger')
        else:
            flash('Filter Applied!', 'success')

    return render_template('Search.html', form=form, result=result)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('Search.html', form=form)


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
                session['loggedin'] = True
                session['username'] = username_form
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminlogin", methods=['GET', 'POST'])
def Adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cu = connection.cursor()
            username_form = str(form.email.data)
            password_form = str(form.password.data)
            select = ("SELECT email,password "
                      "FROM adminlogin "
                      "WHERE email= ?")
            cu.execute(select, [username_form])
            results = cu.fetchone()
            print(results)
            if username_form and password_form in results:
                session['loggedin'] = True
                session['username'] = username_form
                flash('You have been logged in!', 'success')
                print(results)
                return redirect(url_for('candidateprofile'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('username', None)
        return redirect(url_for('login'))


def save_picture(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/profile_pics', file_fn)
    file.save(file_path)
    return file_fn


@app.route('/candidateprofile', methods=['GET', 'POST'])
def candidateprofile():
    form = CandidateForm()
    flash(f'Candidate Profile created for {form.candidatename.data}!', 'success')
    if form.validate_on_submit():
        if form.cv.data:
            resume_file = save_picture(form.cv.data)
            session['photo'] = resume_file
            print(session['photo'])
            cursor3 = connection.cursor()
            print(form.cv.data)
            result = request.form
            insert = ("INSERT INTO candidatedel "
                      "(email, candidatename, contact, notice, skill, source, job_id, cv) "
                      "VALUES(?,?,?,?,?,?,?,?)")
            values = list(result.values())
            print(values)
            ind = [resume_file, values[2], values[3], values[4], values[5], values[6], values[7], values[1]]
            cursor3.execute(insert, ind)
            connection.commit()
            flash('Your changes have been saved', 'success')
            return redirect(url_for('candidateprofile'))

    return render_template('candidate.html', title='Register', form=form)
