from flask import Flask, render_template, jsonify
import database as db


app = Flask(__name__)


@app.route("/")
def hello():
    services = db.load_services_from_db()  # Берет функции из модуля database.py
    return render_template('home.html', services=services)

@app.route("/<id>")
def show_service(id):
    service = db.load_service_from_db(id)
    return render_template('servicepage.html', service=service)


if __name__ == "__main__":
    app.run(debug=True)
