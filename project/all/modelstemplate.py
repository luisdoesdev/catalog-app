

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///models.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()


User1 = User(name='Robo Roboto', email='roboto@gmail.com')
session.add(User1)
session.commit()

# Categories Templates

category1 = Category(user_id=1, name='Soccer')
session.add(category1)
session.commit()

item1 = Item(
    user_id=1,
    name=' Soccer Ball',
    description='Compressed layer enhances ball reaction to create a heavier shot upon impact Graphic design aids peripheral and central vision',
    category=category1)
session.add(item1)
session.commit()

item2 = Item(
    user_id=1,
    name='Soccer Shoes',
    description='Make the smart unmatched stability, traction and durability on polished indoor surfaces.',
    category=category1)
session.add(item2)
session.commit()

category2 = Category(user_id=1, name='Skateboard')
session.add(category2)
session.commit()

item3 = Item(
    user_id=1,
    name='Deck',
    description='Give your skate complete a responsive update with the new Deathwish Gang Logo Mamba skateboard deck. Give your tricks some stylish flare with the floral rose and Deathwish gang logo graphic on a 7-ply maple constructed deck that has a medium concave shape.',
    category=category2)
session.add(item3)
session.commit()

print 'added items'
