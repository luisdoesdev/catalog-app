from app import app
from flask import render_template, url_for, session, request
from flask_oauthlib.client import OAuth

from flask import session as login_session
import random, string


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item

engine = create_engine('sqlite:///models.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()



@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in range(32))
    login_session['state'] = state
    return render_template('g-login.html')



@app.errorhandler(404)
def not_foud(e):
    return '404 NOT FOUND'


@app.route('/')
def index():
    categories = session.query(Category).all()
    item = session.query(Item).all()
    for i in item:
        print(i.category_id)
    
    return render_template('index.html', item=item, categories=categories)

@app.route('/catalog/<category>/items')
def catalog_item(category):
    categories = session.query(Category).all()
    category= session.query(Category).filter_by(name=category)
    for c in category:
        categoryName = c.name
        item = session.query(Item).filter_by(category_id=c.id)
        itemCount = session.query(Item).filter_by(category_id=c.id).count()
        if itemCount == 1:
            itemCountString = 'Item'
        elif itemCount > 1:
            itemCountString = 'Items'     

    return render_template('index.html',categories=categories, category=category, item=item, itemCount = itemCount, itemCountString=itemCountString, categoryName=categoryName)   

@app.route('/catalog/<category>/<item>')
def item_description(category, item):
    category = session.query(Category).filter_by(name=category)
    item = session.query(Item).filter_by(name=item)
    for i in item:
        item_name = i.name
        item_description = i.description


    return(render_template('product.html', item_name=item_name, item_description=item_description))