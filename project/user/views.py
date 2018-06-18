# ...user/views.py

# IMPORTS
from flask import redirect, render_template, request, url_for, Blueprint
from project.models import db, User
from project.user.forms import UserForm

# Blueprints
user_blueprint = Blueprint(
    'user',
    __name__,
    template_folder='templates'
)

@user_blueprint.route('/', methods=['GET', 'POST'])
def index():
    '''
        If The Method is a post add it tod DB
        ELSE Go Back home
    '''
    if request.method == "POST":
       form = UserForm(request.form)
       if form.validate():
           new_user = User(request.form['email'], request.form['name'])
           db.session.add(new_user)
           db.session.commit()
           print '!DONE'
           return redirect(url_for('user.index'))
       return render_template('new.html', form=form)
    return render_template('index.html', user=User.query.all())
  

@user_blueprint.route('/new')
def new():
    form = UserForm()
    return render_template('new.html', form=form)    
