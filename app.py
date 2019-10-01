from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import reduce
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/my_app_db')
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()

candies_collection = db.candies

@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html', candies=candies_collection.find())

@app.route('/new')
def new_candy():
    """Return new candy creation page."""
    return render_template('new_candy.html')

@app.route('/new', methods=['POST'])
def create_candy():
    """Make a new candy according to user's specifications."""
    candy = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    candy_id = candies_collection.insert_one(candy).inserted_id
    return redirect(url_for('show_candy', candy_id=candy_id))

@app.route('/candy/<candy_id>')
def show_candy(candy_id):
    """Show a single candy."""
    candy = candies_collection.find_one({'_id': ObjectId(candy_id)})
    return render_template('show_candy.html', candy=candy)

@app.route('/edit/<candy_id>', methods=['POST'])
def update_candy(candy_id):
    """Edit page for a candy."""
    new_candy = {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'img_url': request.form.get('img_url')
    }
    candies_collection.update_one(
        {'_id': ObjectId(candy_id)},
        {'$set': new_candy}
    )
    return redirect(url_for('show_candy', candy_id=candy_id))

@app.route('/edit/<candy_id>', methods=['GET'])
def edit_candy(candy_id):
    """Page to submit an edit on a candy."""
    candy = candies_collection.find_one({'_id': ObjectId(candy_id)})
    return render_template('edit_candy.html', candy=candy)

@app.route('/delete/<candy_id>', methods=['POST'])
def delete_candy(candy_id):
    """Delete a candy."""
    candies_collection.delete_one({'_id': ObjectId(candy_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))