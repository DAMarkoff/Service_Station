"""
This file (test_form_login.py) contains the functional tests for the `login` form.

These tests use POSTs to '/login' URL to check for the proper behavior
of the `login` form fields validation.
"""
import pytest
from flask_login import current_user
from loguru import logger

from project import db
from project.models import User


def logout_delete(test_client):
    user = User.query.filter_by(email=current_user.email).first()
    
    # Log out current_user
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out' in response.data
    
    # delete current_user
    if user.email != 'email1@gmail.com':
        db.session.delete(user)
        db.session.commit()
    

def test_valid_login_form_filled(test_client, init_database):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using valid new_user credentials
    THEN check the response is valid
    """
    # user = new_user()
    response = test_client.post('/login', data={
                                                    'email': 'email1@gmail.com',
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Register" not in response.data

    logout_delete(test_client)

# ----------------------------------  Email Field ---------------------------------------------------


@pytest.mark.parametrize("spaced_or_blank_email", [
    ' ',  # single-spaced 'First Name' field
    '',  # blank 'First Name' field
])
def test_email_single_spaced_or_blank(test_client, init_database, spaced_or_blank_email):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using a single-spaced or blank 'Email'
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login', data={
                                                    'email': spaced_or_blank_email,
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Required field' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" not in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data
    

@pytest.mark.parametrize("new_user", [
    'a@a',  # less than min 'Email' length
    'a@aa',  # -1 min 'Email' length
    # +1 max 'Email' length
    '101_char_vsaadfvvcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvs@aadfcsddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv',
    # much more than max 'Email' length
    '110_chars_sdfsdfSsdfdsfsdfsdfsdfSsdfdsfsdfsdfsdfSsdfds@fsdfsdfsdfSsdfdsfsdfsdfsdsadsadaasdafSsdfdsfsdgmail.com',
], indirect=True)
def test_email_invalid_length(test_client, init_database, new_user):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using an invalid email length
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login', data={
                                                    'email': new_user.email,  # invalid email length
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    logger.info(new_user.email)
    assert response.status_code == 200
    assert b'Field must be between 5 and 100 characters long.' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" not in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data


@pytest.mark.parametrize('new_user', [
    'a@a.a',  # min 'Email' length
    'a@aa.a',  # +1 min 'Email' length
    # -1 max 'Email' length
    '99_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvsaadf@csddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv',
    # max 'Email' length
    '100_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvsaadf@csddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv'
], indirect=True)
def test_email_valid_length(test_client, init_database, new_user):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using a valid email length
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/login', data={
                                                    'email': new_user.email,  # valid email length
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    logger.info(new_user.email)
    assert response.status_code == 200
    assert b'Welcome!' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" in response.data
    assert b"Log In" not in response.data
    assert b"Register" not in response.data
    
    logout_delete(test_client)
    

@pytest.mark.parametrize("invalid_email_pattern", [
    'aaa.a',  # invalid 'Email' pattern without @ sign
    'a@aaa'  # invalid 'Email' pattern without . sign
])
def test_email_invalid_length_or_pattern(test_client, init_database, invalid_email_pattern):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using an invalid email pattern
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login', data={
                                                    'email': invalid_email_pattern,  # invalid email pattern
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    assert b'Invalid email' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" not in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data


# ----------------------------------  Password Field ---------------------------------------------------


def test_password_blank(test_client, init_database):
    """
    GIVEN a Flask application configured for testing AND new_user
    WHEN the '/login' page is posted to (POST) using blank password
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login', data={
        'email': 'email@google.com',
        'password': ''  # invalid blank password
    }, follow_redirects=True)
    assert b'Required field' in response.data
    assert b"ServiceStation" in response.data
    assert b"Log Out" not in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data
  