from datetime import datetime, date

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tatoodb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tatoo(db.Model):
    tatoo_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    date_added = db.Column(db.Date, default = datetime.utcnow)


@app.route('/')
def index():
    data = Tatoo.query.all()
    return render_template('index.html', data = data)

@app.route('/update')
def update():
    pk = request.args.get('pk')
    data = Tatoo.query.filter_by(tatoo_id = int(pk))
    return render_template('update.html', data = data)
    
@app.route('/process', methods=['POST', 'GET'])
def process():
    
    # Request steps:
        # request.form['action'] ამოწმებს რას უდრის request.form['action']. ეს რექვესტი უტოლდება value-ს, რის შედეგადაც
        # ვარჩევ რომელი ღილაკიდან მოდის რექვესტი. ამიტომ ყველა ღილაკს აქვს ერთნაირი სახელი, მაგრამ value სხვა
        
    if request.form['action'] == "Add": # Add request from index page
        tatoo_name = request.form['tatoo_name'].strip()
        price = request.form['price'].strip()
        tatoo = Tatoo(name=tatoo_name, price=price)
        db.session.add(tatoo)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    elif request.form['action'] == 'Delete': # Delete request from index page
        pk = int(request.form['primary_key'])
        tatoo = Tatoo.query.filter_by(tatoo_id = pk).first() # first() მეთოდით ლისტს ვაშორებ, თორემ ამის გარეშე [0]-ით მოვაშორებდი. როცა list-ით გამოაქვს არ იშლება
        db.session.delete(tatoo)
        db.session.commit()
        return redirect(url_for('index'))
    
    elif request.form['action'] == "Edit": # Edit request from index page        
        pk = int(request.form['primary_key'])
        return redirect(url_for('update', pk = pk))
    
    elif request.form['action'] == 'Back': # Back request from update page
        return redirect(url_for('index'))
    
    elif request.form['action'] == "Save changes": # Save changes request from edit page
        primary_key = int(request.form['primary_key'])
        tatoo_name = request.form['tatoo_name'].strip()
        price = request.form['price'].strip()
        yyyy, mm, dd = request.form['date_added'].split('-')
        
        tatoo = Tatoo.query.filter_by(tatoo_id = primary_key).first()
        tatoo.name = tatoo_name
        tatoo.price = price
        tatoo.date_added = date(int(yyyy), int(mm), int(dd))
        db.session.commit()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


