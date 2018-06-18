# ...user/views.py

# IMPORTS
from flask import redirect, render_template, request, url_for, Blueprint
from project.models import db, User
from project.user.forms import UserForm, DeleteForm

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


@user_blueprint.route('/<int:id>/edit')
def edit(id):
    user=User.query.get(id)
    form=UserForm(obj=user)
    return render_template('edit.html', form=form, user=user)



@user_blueprint.route('/<int:id>', methods =["GET", "PATCH", "DELETE"])
def show(id):
    found_user = User.query.get(id)
    print found_user
    if request.method == b"PATCH":
        form = UserForm(request.form)
        if form.validate():
            found_user.email = request.form['email']
            found_user.name = request.form['name']
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('user.index'))
        return render_template('edit.html', form=form, user=found_user)
    if request.method == b"DELETE":
        print request.form
        form = DeleteForm(request.form)
        print form.validate()
        if form.validate():
            print 'hi'
            db.session.delete(found_user)
            db.session.commit()
            print '!DELETED'
        return redirect(url_for('user.index'))
    return render_template('show.html', user=found_user)