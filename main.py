from flask import Flask, render_template, request, jsonify, flash, g, abort, redirect, url_for
import database as db
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user

app = Flask(__name__)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, app)


@app.route("/")
def hello():
    services = db.load_services_from_db()  # Берет функции из модуля database.py
    return render_template('home.html', services=services)


@app.route("/<id>")
def show_service(id):
    service = db.load_service_from_db(id)
    servicec = db.load_service_price_from_db(id)
    master = db.load_master_from_db(id)
    if not service:
        return "Not Found", 404
    return render_template('servicepage.html', service=service, servicec=servicec, master=master)


@app.route("/<id>/apply", methods=['post'])
def apply(id):
    data = request.form
    service = db.load_service_from_db(id)
    master = db.load_master_from_db(id)
    db.add_application_to_db(id, id, data)
    db.add_client_to_db(data)
    return render_template('application_submitted.html', data=data, master=master, service=service)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.get_user_by_email(request.form['email'])
        print(user.psw)
        if user and check_password_hash(user.psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            print(userlogin.get_id())
            login_user(userlogin)
            print(3)
            return redirect(url_for('home'))
        else:
            flash('Неверная пара логин/пароль', 'error')

    return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = db.add_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("Регистрация прошла успешно")
                return redirect(url_for('login'))

            else:
                flash("Почтовый адрес уже зарегистрирован", 'error')
        else:
            flash('Пароли не совпадают', 'error')

    return render_template('register.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'static'
    app.run(debug=True)
