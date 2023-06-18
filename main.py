from flask import Flask, render_template
import database as db


app = Flask(__name__)


@app.route("/")
def hello():
    services = db.load_services_from_db()  # Берет функции из модуля database.py
    return render_template('home.html', services=services)


if __name__ == "__main__":
    app.run(debug=True)
