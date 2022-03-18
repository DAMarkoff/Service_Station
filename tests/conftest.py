import pytest
import testing.postgresql
from loguru import logger

from project import create_app, db
from project.models import User, UsersGroup

postgresql = testing.postgresql.Postgresql(port=7654)


class NewTestUser(User):
    def __init__(self, email):
        super().__init__(
            first_name='First_Name',
            last_name='Last_Name',
            email=email,
            phone='442083661177',
            password='Password1!'
        )
        
        
@pytest.fixture(scope='function')
def new_user(request):
    user = NewTestUser(request.param)
    logger.info(f'adding {user.email} to the db')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Drop and Create the database and the database table
    logger.info('------------------------------START------------------------------------------------')
    db.session.commit()
    db.drop_all()
    logger.info('db drop all')
    
    db.create_all()
    logger.info('db create all')

    # Insert user_group data
    user_group = UsersGroup(
        group_id=2,
        group_name='users'
    )
    db.session.add(user_group)
    db.session.commit()
    
    # Insert user data
    user1 = User(
        first_name='First_Name1',
        last_name='Last_Name1',
        email='email1@gmail.com',
        phone='442083661177',
        password='Password1!'
    )
    db.session.add(user1)
    logger.info(f'db add user {user1.email}')

    db.session.commit()
    
    yield  # this is where the testing happens!
    
    db.session.commit()
    db.drop_all()
    logger.info('db drop all')
    logger.info('---------------------------END---------------------------------------------------')
    
    # postgresql.stop()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='email1@gmail.com', password='Password1!'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
