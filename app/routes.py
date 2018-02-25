#!/usr/bin/env python
from app import app
from flask import render_template, url_for, session, \
request, flash, redirect, jsonify

from flask import session as login_session
import random
import string


from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Load Clients Secrets Id
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

# Impor Models and SQLAlchemy library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item

engine = create_engine('sqlite:///models.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


'''
* Pep8(Module Problems Solution Pending...)
* ADD USERS TO DATABASE
* an endpoint that serves an arbitrary item in the catalog.
* Refers to the createUser method
* Get Rid of Code Repition using decorators
* Make sure the actual user can Perform the actions
* Checks one_or_none function
'''


@app.route('/login', methods=['GET','POST'])
def login():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter id'), 401)
        response.headers['Content-Type'] = 'aplication/json'
        print response
        return redirect('/') 
    code = request.data
    data_r = request.form['user']

    print data_r
    return redirect('/')


# Google Oath2 methods and routes
@app.route('/gconnect', methods=['POST'])
def gconnect():

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter id'), 401)
        response.headers['Content-Type'] = 'aplication/json'
        return response
    code = request.data

    try:
        # Updgrade the  auth code to a creddential object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to Upgrade the autho code'), 401)
        response.headers['Content-Type'] = 'aplication/json'
        return response

    # check the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # verification for access token
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'aplication/json'
        return response

    # Verification for the access toke is used for the  intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID does not match giver user ID"), 401
        )
        response.headers['Content-Type'] = 'aplication/json'
        return response

    # Verification for the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app"), 401)
        print"Token's client id does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the acccess token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    output = login_session['username']
    createUser()
    

    print "done!"
    return output


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():

    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
    % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result

    # If th status is 200 logout the user no problem
    if result['status'] == '200':
        print('yeah')
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If the status is 400 logout the user regardless but printout the proble
    # to be solve later withou ruining the users experience
    elif result['status'] == '400':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Check if user is currenty signed in
def usernameState(state):
    login_session['state'] = state

    if "username" in login_session:
        username = True
    else:
        username = False

    return username

# creates anti forgery token state


def currentState():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))

    print(login_session)

    return state


# App Errro Handler
@app.errorhandler(404)
def not_foud(e):
    return '404 NOT FOUND'


# JSON API Route
@app.route('/catalog.json/')
def jsonCatalog():

    category = session.query(Category).all()
    items = session.query(Item).all()

    return jsonify(items=[i.serialize for i in items])


# Route when an unathorize user tries to access CRUD operations
@app.route('/intruder')
def intruder():

    state = currentState()
    username = usernameState(state)

    return render_template('g-login.html', STATE=state, username=username)


# Catalog and / are home routes of the application

@app.route('/catalog/')
def catalog():

    state = currentState()
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

    state = currentState()
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

    state = currentState()
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

    state = currentState()
    username = usernameState(state)

    category = session.query(Category).filter_by(name=category).one_or_none()
    item = session.query(Item).filter_by(name=item).one_or_none()

    return(render_template('item-description.html',
           item=item, STATE=state, username=username, category=category))


# User Operations
def createUser(login_session):

    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
    return user.id


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
def add():
    state = currentState()
    username = usernameState(state)
    state = currentState()
    username = usernameState(state)
    if not username:
        return redirect('/intruder')

    category = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['categories'],
        )

        session.add(newItem)
        session.commit
        return redirect(url_for('index'))
    return render_template(
        'add.html',
        category=category,
        username=username,
        STATE=state)


@app.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
def edit(category, item):

    state = currentState()
    username = usernameState(state)
    if not username:
        return redirect('/intruder')

    category = session.query(Category).all()
    item = session.query(Item).filter_by(name=item).one_or_none()

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


@app.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
def delete(category, item):
    state = currentState()
    username = usernameState(state)
    if not username:
        return redirect('/intruder')

    item = session.query(Item).filter_by(name=item).one_or_none()
    category = session.query(Category).filter_by(name=category).one_or_none()

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
