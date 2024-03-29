from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from cloudipsp import Api, Checkout
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    IsActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


@app.route('/')
def home():
    items = Item.query.order_by(Item.price).all()
    return render_template('home.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>/delete')
def item_delete(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении возникла ошибка"


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/buy/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    item = Item.query.get(id)
    if request.method == "POST":
        item.title = request.form['title']
        item.price = request.form['price']


        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибочка вышла :("
    else:
        return render_template('item_update.html', item=item)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибочка вышла :("
    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)

