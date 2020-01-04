

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('postgresql+psycopg2://vagrant:123456@/catalog')

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
    picture='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwnmu.edu%2Fwp-content%2Fuploads%2FDollarphotoclub_62315685.jpg&f=1&nofb=1',
    category=category1)
session.add(item1)
session.commit()

item2 = Item(
    user_id=1,
    name='Soccer Shoes',
    description='Make the smart unmatched stability, traction and durability on polished indoor surfaces.',
    picture='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ebayimg.com%2Fimages%2Fi%2F172422685003-0-1%2Fs-l1000.jpg&f=1&nofb=1',
    category=category1)
session.add(item2)
session.commit()

category2 = Category(user_id=1, name='Skateboard')
session.add(category2)
session.commit()

item3 = Item(
    user_id=1,
    name='Deck',
    description='Give your skate complete a responsive update with the new Deathwish Gang',
    picture='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fscene7.zumiez.com%2Fis%2Fimage%2Fzumiez%2Fpdp_hero%2FRIPNDIP-We-Out-Here-8.25%2526quot%253B-Skateboard-Deck-_263748-front-US.jpg&f=1&nofb=1',
    category=category2)
session.add(item3)
session.commit()

print 'added items'
