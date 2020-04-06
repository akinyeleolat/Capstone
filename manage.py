from flask_script import Manager
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Movie, Actor

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# custom seed command
@manager.command
def seed():
    Movie(title='Nikita', release_date='2017-12-12').insert()
    Movie(title='Last Ship', release_date='2016-08-12').insert()
    Movie(title='Face Off', release_date='2003-12-12').insert()
    Movie(title='Seeker', release_date='2009-11-12').insert()

    Actor(name='Arnold Swaztnigger', age=76, gender='male').insert()
    Actor(name='Mike Etim', age=40, gender='male').insert()
    Actor(name='Mary Balo', age=29, gender='female').insert()
    Actor(name='Nelly Dido', age=29, gender='female').insert()


if __name__ == '__main__':
    manager.run()
