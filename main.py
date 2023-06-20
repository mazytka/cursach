from flask import Flask, render_template, request, jsonify
import database as db


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
    return render_template('application_submitted.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
