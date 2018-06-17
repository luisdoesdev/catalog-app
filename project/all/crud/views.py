# project/recipes/views.py

from flask import render_template, Blueprint


crud_blueprint = Blueprint('crud',__name__, template_folder='templates')


@crud_blueprint.route('/add', methods=['GET', 'POST'])
#@login_required
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

