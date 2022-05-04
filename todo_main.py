import os

from flask import Flask, render_template, redirect, url_for, flash, request
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import desc
from forms import *
from flask_bootstrap import Bootstrap


#--------------SetUp App----------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('sk')
Bootstrap(app)

#-------------Connect DB-----------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#-------------Configure Databases-----------------------------------------------------------------
class Todolist(db.Model):
    __tablename__ = "To_Do"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),unique=True, nullable=False)
    date = db.Column(db.String(250),nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    completion=db.Column(db.Integer,nullable=False)
    body = db.Column(db.Text,nullable=False)

# class Task (db.Model):
#     __tablename__ = "Task"
#     title = db.Column(db.String(250),primary_key=True)
# #
#
# db.create_all()
#-------------Create Record-----------------------------------------------------------------


# db.session.add(new_task)
# db.session.commit()



#-------------Index Home-----------------------------------------------------------------
@app.route('/', methods=['GET','POST'])
def home():
  #--------Search Form------------
    form = SearchForm()
    if form.validate_on_submit():
        id = form.id.data
        task_ = Todolist.query.filter_by(id=id).first()
        # ID doesn't exist or password incorrect.
        if not task_:
            flash('That ID doesnt exist, please try again.')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('search', task_id=id))
    #-------To do listings--------------
    lists = Todolist.query.order_by(desc(Todolist.weight)).all()

    return render_template('index.html', form=form, all_task = lists)
#-------------Add-----------------------------------------------------------------

@app.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()
    #------------Retrieve new ID----------
    id_prev = Todolist.query.order_by(Todolist.id).all()
    id_new = len(id_prev)+1
    if form.validate_on_submit():
        #-----------New Task-----------
        new_task = Todolist(
            id=id_new,
            title=request.form['title'],
            date=request.form['date'],
            weight=int(request.form['weight']),
            body=request.form['body'],
            completion=int(request.form['completion'])
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


#------------------Edit ----------------------------------------------------------
@app.route('/edit/<int:task_id>', methods=['GET','POST'])
def update(task_id):
    task = Todolist.query.get(f'{task_id}')
    form = EditForm(

    )
    if form.validate_on_submit():
        task.completion= form.completion.data
        task.body= form.body.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",form=form)


#------------------Search----------------------------------------------------------

@app.route('/search/<int:task_id>', methods=['GET','POST'])
def search(task_id):
    print(task_id)
    task_ = Todolist.query.get(f'{task_id}')
    print(task_)
    return render_template("task-info.html", task= task_)


#---------Run App---------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)