import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='website/*',
    omit=[
        'website/tests/*',
        'website/config.py',
    ]
)
COV.start()

from website import app, db, models
from website.models import User

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('website/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('website/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()
    db.session.commit()


@manager.command
def add_users():
    users = [
        {
            'username': 'test',
            'full_name': 'test',
            'password': '***',
            'admin': False,
        },
        {
            'username': 'johndoe',
            'full_name': 'John Doe',
            'password': '***',
            'admin': False,
        },
        {
            'username': 'janedoe',
            'full_name': 'Jane Doe',
            'password': '***',
            'admin': False,
        },
        {
            'username': 'admin',
            'full_name': 'Administrator',
            'password': '***',
            'admin': True,
        },
    ]
    for user in users:
        db.session.add(User(username=user['username'],
                            full_name=user['full_name'],
                            password=user['password'],
                            admin=user['admin']))
    db.session.commit()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.session.commit()
    db.drop_all()


if __name__ == '__main__':
    manager.run()
