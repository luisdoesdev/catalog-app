#!/usr/bin/env python
from app import app
from flask import render_template, url_for, session, \
    request, flash, redirect, jsonify
from flask import session as login_session
from functools import wraps
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item
from google.oauth2 import id_token
from google.auth.transport import requests
# I dont want to confused the  two request modules I have imported
requestGoogleAuth = requests.Request()


engine = create_engine('sqlite:///models.db?check_same_thread=False')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


# anti forgery
state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in range(32))

# Google Oath2 methods and routes


@app.route('/gconnect', methods=['POST'])
def gconnect():
    login_session['state'] = state

    if request.args.get('state') != login_session['state']:
        return 'Error state doesnt match STATE', redirect('/')

    token = request.data
    # (Receive token by HTTPS POST)
    # ...
    
    try:
      
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requestGoogleAuth,
        "682221223878-pl3rgk5qvvgme87832b2jeegjejs62og.apps.googleusercontent.com")

        data = idinfo


        login_session['username'] = data['name']
        login_session['email'] = data['email']
        createUser(login_session['username'], login_session['email'])
        return "Success"
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account
        # ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        pass


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():

    del login_session['username']
    del login_session['email']

    return "Success"


# Check if user is currenty signed in
def usernameState(state):
    login_session['state'] = state

    if "username" in login_session:
        username = True
    else:
        username = False

    return username


# App Errro Handler
@app.errorhandler(404)
def not_foud(e):
    return ' hahahah The classic<b> 404 NOT FOUND </b> click <a href="/" \
            style="border-color:#000;"> here </a> to go home'


# JSON API Route
@app.route('/catalog.json/')
def jsonCatalog():

    category = session.query(Category).all()
    items = session.query(Item).all()

    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<category>/<item>.json')
def jsonItem(category, item):
    category = session.query(Category).filter_by(name=category).one_or_none()
    item = session.query(Item).filter_by(name=item).one_or_none()
    return jsonify(item=[item.serialize])


# Route when an unathorize user tries to access CRUD operations
@app.route('/intruder')
def intruder():
    username = usernameState(state)
    return render_template('g-login.html', STATE=state, username=username)


# Catalog and / are home routes of the application


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('g-login.html', STATE=state)


@app.route('/catalog/')
def catalog():
    username = usernameState(state)
    categories = session.query(Category).all()
    items = session.query(Item).all()

    return render_template(
        'index.html',
        items=items,
        categories=categories,
        STATE=state,
        username=username)


@app.route('/')
def index():
    username = usernameState(state)
    categories = session.query(Category).all()
    items = session.query(Item).all()

    return render_template(
        'index.html',
        items=items,
        categories=categories,
        STATE=state,
        username=username)


# Detail Routes
@app.route('/catalog/<category>/items')
def catalog_items(category):
    username = usernameState(state)
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category)
    for c in category:
        categoryName = c.name
        items = session.query(Item).filter_by(category_id=c.id).all()
        itemCount = session.query(Item).filter_by(category_id=c.id).count()
        if itemCount == 1:
            itemCountString = 'Item'
        elif itemCount > 1:
            itemCountString = 'Items'

    return render_template(
        'items.html',
        categories=categories,
        items=items,
        itemCountString=itemCountString,
        itemCount=itemCount,
        categoryName=categoryName,
        STATE=state,
        username=username)


@app.route('/catalog/<category>/<item>')
def item_description(category, item):
    username = usernameState(state)
    category = session.query(Category).filter_by(name=category).one_or_none()
    item = session.query(Item).filter_by(name=item).one_or_none()
    ids = currentUser(item)

    return(render_template('item-description.html',
           item=item, STATE=state, username=username,
           category=category, id=ids))


# User Operations


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect('/intruder')
    return decorated_function


def currentUser(item):
    username = usernameState(state)
    if username:
        user = session.query(User).filter_by \
            (email=login_session['email']).one_or_none()
        ids = user.id is item.user_id
        return ids


def createUser(name, email):
    u = session.query(User).filter_by(email=email).one_or_none()
    if u is None:
        # Create and ID for the user
        id = random.randint(0, 9)
        newUser = User(id=id, name=name, email=email)
        session.add(newUser)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        newUser = session.query(User).all()
        print newUser.email + newUser.name

    else:
        print u.email + str(u.id)


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except BaseException:
        return None


# CRUD Operations
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    username = usernameState(state)
    user = session.query(User).filter_by\
        (email=login_session['email']).one_or_none()
    category = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['categories'],
            user_id=user.id
        )

        session.add(newItem)
        session.commit()
        return redirect(url_for('index'))
    return render_template(
        'add.html',
        category=category,
        username=username,
        STATE=state)


@app.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
@login_required
def edit(category, item):
    username = usernameState(state)
    category = session.query(Category).all()
    item = session.query(Item).filter_by(name=item).one_or_none()

    if currentUser(item):
        print "yes"

        if request.method == 'POST':
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['categories']:
                item.category_id = request.form['categories']

            session.add(item)
            session.commit()

            return redirect(url_for('index'))
        return render_template(
            'edit.html',
            item=item,
            category=category,
            username=username,
            STATE=state)
    else:
        return "Sorry you are not allow to edit post you have \
        not made yourself return <a href='/'>home</a>"


@app.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
@login_required
def delete(category, item):
    username = usernameState(state)
    item = session.query(Item).filter_by(name=item).one_or_none()
    category = session.query(Category).filter_by(name=category).one_or_none()
    if currentUser(item):

        if request.method == 'POST':
            session.delete(item)
            session.commit()
            return redirect('/')

        return render_template(
            'delete.html',
            item=item,
            category=category,
            STATE=state,
            username=username)
    else:
        return "sorry you are not allow to delete items \
        you have not created, return  <a href='/'> home</a>"
