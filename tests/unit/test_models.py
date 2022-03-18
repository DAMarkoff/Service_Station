"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from loguru import logger

from project.models import User
from tests.conftest import NewTestUser


user = NewTestUser('email@gmail.com')


def test_new_user_with_fixture():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    # user = User.query.filter_by(email='email@gmail.com').first()
    
    assert user.email == 'email@gmail.com'
    assert user.password != 'Password1!'


def test_setting_password():
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    user.set_password('MyNewPassword')
    assert user.password != 'MyNewPassword'
    assert user.check_password('MyNewPassword')
    assert not user.check_password('MyNewPassword2')
    assert not user.check_password('Password1!')
