# ../home/views.py


from flask import render_template, url_for, session, \
    request, flash, redirect, jsonify, Blueprint
from flask import session as login_session
from project import state, session
from project.models import Base, User, Category, Item
from functools import wraps

home_blueprint = Blueprint(
    'home',
    __name__,
    template_folder='templates'
)


@home_blueprint.route('/')
def index():
    '''
        User Initial Route
    '''
    username = usernameState(state)
    categories = session.query(Category).all()
    items = session.query(Item).all()

    return render_template(
        'index.html',
        items=items,
        categories=categories,
        STATE=state,
        username=username)

@home_blueprint.route('/')
def test():
    return 'hello'


@home_blueprint.route('/catalog/')
def catalog():
    '''
    /catalog route will show everything in the database
    username: will be analyze as a boolean in the template
              to see if an user is logged in

    cataegories: all the Categories on the in the database,
                 is organizing the items in the template

    items: all items in the database wich are organize with
           the help of the cataegories

    '''
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
@home_blueprint.route('/catalog/<category>/items')
def catalog_items(category):
    '''
        Details holds all the details of an items
        A specific category will be called from the database


    '''
    username = usernameState(state)
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category)
    for c in category:
        '''
        loops all the items localize on the specific category
        '''

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


@home_blueprint.route('/catalog/<category>/<item>')
def item_description(category, item):
    username = usernameState(state)
    category = session.query(Category).filter_by(name=category).one_or_none()
    item = session.query(Item).filter_by(name=item).one_or_none()
    ids = currentUser(item)

    return(render_template('item-description.html',
                           item=item, STATE=state, username=username,
                           category=category, id=ids))


def usernameState(state):
    '''
     Check if user is currenty signed in
    '''

    login_session['state'] = state

    if "username" in login_session:
        username = True
    else:
        username = False

    return username


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
        user = session.query(User).filter_by(
            email=login_session['email']).one_or_none()
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
        except BaseException:
            session.rollback()
            raise
        finally:
            session.close()

        newUser = session.query(User).all()
        print(newUser)

    else:
        print(u)


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
@home_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    username = usernameState(state)
    user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
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
        return redirect(url_for('home.index'))
    return render_template(
        'add.html',
        category=category,
        username=username,
        STATE=state)


@home_blueprint.route(
    '/catalog/<category>/<item>/edit',
    methods=[
        'GET',
        'POST'])
@login_required
def edit(category, item):
    username = usernameState(state)
    category = session.query(Category).all()
    item = session.query(Item).filter_by(name=item).one_or_none()
    
    if currentUser(item):
        

        if request.method == 'POST':
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['categories']:
                item.category_id = request.form['categories']

            session.add(item)
            session.commit()

            return redirect(url_for('home.index'))
        return render_template(
            'edit.html',
            item=item,
            category=category,
            username=username,
            STATE=state)
    else:
        return "Sorry you are not allow to edit post you have \
        not made yourself return <a href='/'>home</a>"


@home_blueprint.route(
    '/catalog/<category>/<item>/delete',
    methods=[
        'GET',
        'POST'])
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


# ERROR handlers and misalenious routes
@home_blueprint.errorhandler(404)
def not_foud(e):
    '''  App Errro Handler '''
    return ' hahahah The classic<b> 404 NOT FOUND </b> click <a href="/" \
            style="border-color:#000;"> here </a> to go home'


@home_blueprint.route('/intruder')
def intruder():
    '''
        Route when an unathorize user tries to access CRUD operations
    '''
    username = usernameState(state)
    return render_template('g-login.html', STATE=state, username=username)
