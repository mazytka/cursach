from flask import Flask, render_template, request, jsonify, flash, g, abort, redirect, url_for, session
import database as db
import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                     port='3306',
                                     database='парикмахерская',
                                     user='root',
                                     password='1234')
cursor = connection.cursor()

app = Flask(__name__)





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
        username = request.form['username']
        password = request.form['psw']
        cursor.execute(f"SELECT * from user where useraname='{username}' and password='{password}'")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('hello'))
        else:
            flash('Пароль или email не совпадает', 'error')
    return render_template('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['psw'] == request.form['psw2']:
            print(2)
            res = db.add_user(request.form['email'], request.form['psw'])
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
