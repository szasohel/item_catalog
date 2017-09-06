from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from model import Base, Catagory, User, Item
from flask import Flask, render_template, url_for	
from flask import request, redirect


app = Flask(__name__)

# connect to database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# create database session
DBSession = sessionmaker(bind = engine)
session = DBSession()

# show all catagory
@app.route('/')
@app.route('/catagory/')
def show_catagory():
	catagories = session.query(Catagory).order_by(asc(Catagory.name))
	return render_template('catagory.html', catagories = catagories)

# add new catagory
@app.route('/catagory/new', methods=['GET','POST'])
def new_catagory():
	if request.method == 'POST':
		new_name = request.form['name']
		new_catagory = Catagory(name = new_name)
		session.add(new_catagory)
		session.commit()
		return redirect(url_for('show_catagory'))

	else:
		return render_template('new_catagory.html')

# delete existing catagory
@app.route('/catagory/<int:catagory_id>/delete/', methods=['GET','POST'])
def delete_catagory(catagory_id):
	catagory_delete = session.query(Catagory).filter_by(id = catagory_id).one()
	if request.method == 'POST':
		session.delete(catagory_delete)
		session.commit()
		return redirect(url_for('show_catagory'))
	else:
		return render_template('delete_catagory.html', catagory= catagory_delete)

# edit existing catagory
@app.route('/catagory/<int:catagory_id>/edit/', methods=['GET','POST'])
def edit_catagory(catagory_id):
	catagory_edit = session.query(Catagory).filter_by(id = catagory_id).one()
	if request.method == 'POST':
		if request.form['name']:
			catagory_edit.name = request.form['name']
			return redirect(url_for('show_catagory'))
	else:
		return render_template('edit_catagory.html', catagory = catagory_edit)

@app.route('/catagory/<int:catagory_id>/items/')
def show_item(catagory_id):
	catagory = session.query(Catagory).filter_by(id = catagory_id).one()
	items = session.query(Item).filter_by(catagory_id = catagory_id).all()
	return render_template('items.html', catagory = catagory, items = items)

@app.route('/catagory/<int:catagory_id>/new/')
def new_item(catagory_id):
	return 'new item'

@app.route('/catagory/<int:catagory_id>/<int:item_id>/edit/')
def edit_item(catagory_id,item_id):
	return 'edit item'

@app.route('/catagory/<int:catagory_id>/<int:item_id>/delete/')
def delete_item(catagory_id,item_id):
	return 'delete item'




if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
