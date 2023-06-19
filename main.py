from flask import Flask, render_template, jsonify
import database as db


app = Flask(__name__)


@app.route("/")
def hello():
    services = db.load_services_from_db()  # Берет функции из модуля database.py
    # min_price = db.load_min_price_from_service()
    return render_template('home.html', services=services)
@app.route("/<id>")
def show_service(id):
    service = db.load_service_from_db(id)
    servicec = db.load_service_price_from_db(id)
    if not service:
        return "Not Found", 404
    return render_template('servicepage.html', service=service, servicec = servicec)


if __name__ == "__main__":
    app.run(debug=True)
