#.../api/views.py

# IMPORTS
from flask import Blueprint, jsonify
from project import session
from project.models import Base, User, Category, Item

# BLuprint Route SETUP
api_blueprint = Blueprint(
    'api',
    __name__
)

@api_blueprint.route('/items.json/')
def jsonCatalog():
    ''' JSON API Route for the whole catalog collection'''

    category = session.query(Category).all()
    items = session.query(Item).all()

    return jsonify(items=[i.serialize for i in items])


@api_blueprint.route('/catalog/<category>/<item>.json')
def jsonItem(category, item):
    ''' JSON API Route for a specific Item '''
    category = session.query(Category).filter_by(name=category).one_or_none()
    item = session.query(Item).filter_by(name=item).one_or_none()
    return jsonify(item=[item.serialize])    