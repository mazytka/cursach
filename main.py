from flask import Flask, render_template


app = Flask(__name__)


SERVICES = [{
    'id': 1,
    'title': 'Стрижка',
    'price': '15000 рублей'
},
           {
    'id': 2,
    'title': 'Педикюр',
    'price': '1500 рублей'
},
{
    'id': 3,
    'title': 'Солярий',
    'price': '25000 рублей'
},
{
    'id': 4,
    'title': 'Маникюр',
    'price': '2000 рублей'
}
]

@app.route("/")
def hello():
    return render_template('home.html', services=SERVICES)


if __name__ == "__main__":
    app.run(debug=True)
