"""
This file (test_auth.py) contains the functional tests for the `users` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `users` blueprint.
"""


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login', data={
                                                    'email': 'email1@gmail.com',
                                                    'password': 'Password1!'
                                                }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome!' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' in response.data
    assert b'Log In' not in response.data
    assert b'Register' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_invalid_password_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='email1@gmail.com', password='InvalidPassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_invalid_email_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='invalid_email@gmail.com', password='Password1!'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data
    

def test_invalid_email_pattern_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(
                                    email='email1gmail.com',  # @ is absent
                                    password='Password1!'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data
    

def test_login_already_logged_in(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) when the user is already logged in
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='no_need_email@gmail.com', password='NoNeedPassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'HELLO' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' in response.data
    assert b'Log In' not in response.data
    assert b'Register' not in response.data


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/register',
                                data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3@gmail.com',
                                    phone='442083661177',
                                    password='Password3!',
                                    password_check='Password3!'
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' in response.data
    assert b'Log In' not in response.data
    assert b'Register' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_invalid_passwords_not_matched_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3@gmail.com',
                                    phone='442083661177',
                                    password='Password3!',
                                    password_check='Paasword3!'  # Does NOT match!
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering' not in response.data
    assert b'[This field is required.]' not in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_invalid_email_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3gmail.com',  # @ is absent
                                    phone='442083661177',
                                    password='Password3!',
                                    password_check='Password3!'
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering' not in response.data
    assert b'Invalid email' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_invalid_password_pattern_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3gmail.com',
                                    phone='442083661177',
                                    password='Password3',  # required special ! is absent
                                    password_check='Password3'  # required special ! is absent
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering' not in response.data
    assert b'Invalid password pattern' in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data
    
    
def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) using an email address already registered
    THEN check an error message is returned to the user
    """
    # Register the new account
    test_client.post('/register',
                     data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3@gmail.com',
                                    phone='442083661177',
                                    password='Password3!',
                                    password_check='Password3!'
                                ),
                     follow_redirects=True)
    test_client.get('/logout', follow_redirects=True)
    # Try registering with the same email address
    response = test_client.post('/register',
                                data=dict(
                                    first_name='First_Name',
                                    last_name='Last_Name',
                                    email='email3@gmail.com',
                                    phone='442083661177',
                                    password='Password3!',
                                    password_check='Password3!'
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Email already registered' in response.data
    assert b'Thanks for registering' not in response.data
    assert b'ServiceStation' in response.data
    assert b'Log Out' not in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data
