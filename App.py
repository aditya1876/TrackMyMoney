from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Name of the app
app=Flask(__name__)

#Database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  #initialize db by passing the app

#Add class for the items on the page.
class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)                #primary key given to each entry.
    tr_date = db.Column(db.DateTime, default=datetime.utcnow)   #date of the transaction
    desc = db.Column(db.String(200), nullable=False)            #Description of the expense - user entered
    amt = db.Column(db.Float(10,2), nullable=False)                   #Amount of the transacton - user entered

    def __repr__(self):
        return '<Task %r>' %self.id                             #returns the Id after every row is created.
"""
    To set up the DB, do the following:
    1. Activate the environemnt -- source env/bin/activate
    2. Goto interactive python3 shell -- python3
    3. from App import db
    4. db.create_all()
    you should now see a test.db file created.
"""                        

#Page locations
@app.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        expense_item = request.form['Mylist']                   #getting the item form home.html
        new_expense = Tracker(desc=expense_item)                #creating a Tracker object.

        try:
            db.session.add(new_expense)                         #adding data to the database.
            db.session.commit()
            return redirect('/')
        except:
            return "Error in adding expense."
    else:
        expenses = Tracker.query.order_by(Tracker.tr_date).all()
        return render_template('Home.html', expenses=expenses)

@app.route('/about')
def about():
    return "<h1>About Page</h1>"

if __name__=="__main__":
    app.run(debug=True)