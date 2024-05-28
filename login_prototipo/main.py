from flask import render_template , request, redirect, url_for
from flask_login import *
from app import app, db, login_manager
from app.models import User


@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get['name']
        email = request.form.get['email']
        pwd= request.form.get['password']

        if name and email and pwd:
            user = User(name=name,email=email,password=pwd)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(pwd):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


app.run(debug=True)