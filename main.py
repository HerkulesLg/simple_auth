import sqlite3
import os
from datetime import datetime
from config import SECRET_KEY
from flask import Flask, render_template, request, redirect, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text)
    password = db.Column(db.Text)
    date = db.Column(db.Text, default=datetime.utcnow())


if not os.path.isfile('/data/profiles.db'):
    app.app_context().push()
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    db_profiles = Profile.query.all()
    profiles = {}
    for user in db_profiles:
        profiles[user.login] = user.password
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.form.get('login') in profiles.keys() and request.form.get('password') == profiles.get(request.form.get('login')):
        session['userLogged'] = request.form.get('login')
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html')


@app.route('/sing_up', methods=['POST', 'GET'])
def sing_up():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        registration_data = Profile(login=username, password=password)
        db.session.add(registration_data)
        db.session.commit()
    return render_template('sing_up.html')


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template('profile.html', username=username)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)