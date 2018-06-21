# ../auth/views.py


from flask import redirect, render_template, request, url_for, Blueprint
from project import state, session
import random
import string
from flask import session as login_session
from project.models import Base, User
from google.oauth2 import id_token
from google.auth.transport import requests

# I dont want to confused the  two request modules I have imported
requestGoogleAuth = requests.Request()


auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''
    the login page method,  STATE crated
    with the anti forgery key method
    '''
    return render_template('g-login.html', STATE=state)


# Google Oath2 methods and routes
@auth_blueprint.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    Logs In User using the Google Sign In API
    '''
    login_session['state'] = state

    if request.args.get('state') != login_session['state']:
        return 'Error state doesnt match STATE', redirect('/')

    token = request.data
    # (Receive token by HTTPS POST)

    try:

        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token,
            requestGoogleAuth,
            "682221223878-pl3rgk5qvvgme87832b2jeegjejs62og.apps.googleusercontent.com")

        data = idinfo

        """
        Reasing the data receieved into the loggin_sesson
        """

        login_session['username'] = data['name']
        login_session['email'] = data['email']

        # Create the user if User is not part of the db
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


@auth_blueprint.route('/gdisconnect', methods=['POST'])
def gdisconnect():

    # delete the loggin_session state

    del login_session['username']
    del login_session['email']

    return "Success"


def createUser(name, email):
    '''
    Check if User is in datbase
    if not
    It will add him/her
    '''
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
        print newUser

    else:
        print u


