from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    IsActive = db.Column(db.Boolean, default = True)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about_us")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)