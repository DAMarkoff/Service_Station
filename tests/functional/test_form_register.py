"""
This file (test_form_register.py) contains the functional tests for the `register` form.

These tests use POSTs to '/register' URL to check for the proper behavior
of the `register` form fields validation.
"""
import pytest
from flask_login import current_user

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
	

def test_valid_register_form_filled(test_client, init_database):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using valid new_user credentials
	THEN check the response is valid, user is registered and logged in
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)


# ----------------------------------  First_name Field ---------------------------------------------------


@pytest.mark.parametrize("spaced_or_blank_first_name", [
	' ',  # single-spaced 'First Name' field
	'',  # blank 'First Name' field
])
def test_fist_name_single_spaced(test_client, init_database, spaced_or_blank_first_name):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a single-spaced or blank 'First Name'
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': spaced_or_blank_first_name,
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'This field is required' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	

@pytest.mark.parametrize("valid_first_name_length", [
	'a',  # min 'First Name' length
	'aa',  # +1 min 'First Name' length
	'49_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvs',  # -1 max 'First Name' length
	'50_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsd'  # max 'First Name' length
])
def test_fist_name_valid_length(test_client, init_database, valid_first_name_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a valid 'First Name' length
	THEN check the response is valid, user is registered and logged in
	"""
	new_user = {
		'first_name': valid_first_name_length,
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)
	

@pytest.mark.parametrize("invalid_first_name_length", [
	'51_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsdd',  # +1 max 'First Name' length
	'70_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsdvsdzvsdvsdcdsfcsdasd'  # +much more max 'First Name' length
])
def test_fist_name_invalid_length(test_client, init_database, invalid_first_name_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using an invalid 'First Name' length
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': invalid_first_name_length,
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Field must be between 1 and 50 characters long.' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data


# ----------------------------------  Last_name Field ---------------------------------------------------


@pytest.mark.parametrize("spaced_or_blank_last_name", [
	' ',  # single-spaced 'Last Name' field
	'',  # blank 'Last Name' field
])
def test_last_name_single_spaced_or_blank(test_client, init_database, spaced_or_blank_last_name):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a single-spaced or blank 'Last Name'
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': spaced_or_blank_last_name,
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'This field is required' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data


@pytest.mark.parametrize("valid_last_name_length", [
	'a',  # min 'Last Name' length
	'aa',  # +1 min 'Last Name' length
	'49_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvs',  # -1 max 'Last Name' length
	'50_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsd'  # max 'Last Name' length
])
def test_last_name_valid_length(test_client, init_database, valid_last_name_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a valid 'Last Name' length
	THEN check the response is valid, user is registered and logged in
	"""
	new_user = {
		'first_name': 'John',
		'last_name': valid_last_name_length,
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)


@pytest.mark.parametrize("invalid_last_name_length", [
	'51_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsdd',  # +1 max 'Last Name' length
	'70_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsdvcsdvsdvsdzvsdvsdcdsfcsdasd'  # +much more max 'Last Name' length
])
def test_last_name_invalid_length(test_client, init_database, invalid_last_name_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using an invalid 'Last Name' length
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': invalid_last_name_length,
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Field must be between 1 and 50 characters long.' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	
	
# ----------------------------------  Email Field ---------------------------------------------------


@pytest.mark.parametrize("spaced_or_blank_email", [
	' ',  # single-spaced 'Email' field
	'',  # blank 'Email' field
])
def test_email_single_spaced(test_client, init_database, spaced_or_blank_email):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a single-spaced or blank 'Email'
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': ' ',
		'phone': '442083661177',
		'password': spaced_or_blank_email,
		'password_check': spaced_or_blank_email
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'This field is required' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	

@pytest.mark.parametrize("invalid_email_pattern", [
	'emailgmail.com',  # an email without required @ sign
	'email@gmailcom'  # an email without required . sign
])
def test_email_less_than_min_length(test_client, init_database, invalid_email_pattern):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using invalid email pattern
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': invalid_email_pattern,
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Invalid email' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data


@pytest.mark.parametrize("valid_email_length", [
	'e@e.e',  # min 'Email' length
	'ee@e.e',  # +1 char to min 'Email'
	# -1 char to max 'Email' length
	'99_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvsaadf@csddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv',
	# max 'Email' length
	'100_chars_vsaadfcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvsaadf@csddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv'
])
def test_email_valid_length(test_client, init_database, valid_email_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a valid 'Email' length
	THEN check the response is valid, user is registered and logged in
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': valid_email_length,
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)


@pytest.mark.parametrize("invalid_email_length", [
	'ee',  # less than min length border 'Email' field filled
	'e@ee',  # -1 less than min length border 'Email' field filled
	# +1 char to max 'Email' length
	'101_char_vsaadfvvcsddvdsfcsdvsdvsaadfcsddvdsfcsdvsdvs@aadfcsddvdsfsdvsaadfcsddvdsfcsdvsdvsaadfcsd.sdv',
	# +much more to the 'Email' length
	'110_chars_sdfsdfSsdfdsfsdfsdfsdfSsdfdsfsdfsdfsdfSsdfds@fsdfsdfsdfSsdfdsfsdfsdfsdsadsadaasdafSsdfdsfsdgmail.com'
])
def test_email_more_than_max_length(test_client, init_database, invalid_email_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using more than max 'Email' length
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': invalid_email_length,
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Field must be between 5 and 100 characters long.' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	

def test_email_registration_using_an_already_registered_email(test_client, init_database):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using an already registered email
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email1@gmail.com',  # already registered email in init_database fixture
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'Password1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Email already registered' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data


# ----------------------------------  Password Field ---------------------------------------------------


@pytest.mark.parametrize("spaced_or_blank_password", [
	' ',  # single-spaced 'Password' field
	'',  # blank 'Password' field
])
def test_password_single_spaced_or_blank(test_client, init_database, spaced_or_blank_password):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a valid password length pattern
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': spaced_or_blank_password,
		'password_check': spaced_or_blank_password
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'This field is required' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data


@pytest.mark.parametrize("valid_password_length_pattern", [
	'Parsed1!',  # min length 'Password' field filled
	'ParsedA1!',  # +1 char to min border 'Password' field length
	'ParsedA1!asdasdasdasdasdasdasda',  # -1 char to max border 'Password' field length
	'ParsedA1!asdasdasdasdasdasdasdaa',  # max border 'Password' field length
])
def test_password_valid_length_pattern(test_client, init_database, valid_password_length_pattern):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a valid password length pattern 8 - 32 chars
	THEN check the response is valid, user is registered and logged in
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': valid_password_length_pattern,
		'password_check': valid_password_length_pattern
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)
	

@pytest.mark.parametrize("char", ['@', '$', '!', '%', '*', '?', '&'])
def test_password_contains_at_least_one_of_the_required_special_chars(test_client, init_database, char):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using the password contains one of the required chars
	THEN check the response is valid, user is logged in
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': f'Password1{char}',
		'password_check': f'Password1{char}'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Thanks for registering' in response.data
	assert b"Log Out" in response.data
	assert b"Log In" not in response.data
	assert b"Register" not in response.data
	
	logout_delete(test_client)
	
	
@pytest.mark.parametrize("char", [',', '.', '(', ')', '#', '^', '-'])
def test_password_should_not_contain_other_spec_chars_than_required(test_client, init_database, char):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using the password that contain one of the char that is not required
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': f'Password1{char}',
		'password_check': f'Password1{char}'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Invalid password pattern' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	
	
@pytest.mark.parametrize("invalid_password_pattern", [
	'password1!',  # the password without any uppercase letters
	'PASSWORD1!',  # the password without any lowercase letters
	'PasswordA!',  # the password without any digits
])
def test_password_contains_uppercase_lowercase_digit(test_client, init_database, invalid_password_pattern):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using an invalid password pattern
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': invalid_password_pattern,
		'password_check': invalid_password_pattern
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Invalid password pattern' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	

@pytest.mark.parametrize("invalid_password_length", [
	'Pad1!',  # less than min length border 'Password' field filled
	'Pared1!',  # -1 less than min length border 'Password' field filled
	'ParsedA1!asdasdasdasdasdasdasdaaa',  # +1 char to max border 'Password' field length
	'ParsedA1!asdasdasdasdasdasdasdaasdasdasdasdasdasda',  # +much more chars to max border 'Password' field length
])
def test_password_invalid_length_pattern(test_client, init_database, invalid_password_length):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using an invalid password length pattern 8 - 32 chars
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': invalid_password_length,
		'password_check': invalid_password_length
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b'Field must be between 8 and 32 characters long.' in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	
	
def test_password_not_matched(test_client, init_database):
	"""
	GIVEN a Flask application configured for testing
	WHEN the '/register' page is posted to (POST) using a not matched passwords
	THEN check an error message is returned to the user
	"""
	new_user = {
		'first_name': 'John',
		'last_name': 'Rambo',
		'email': 'email@gmail.com',
		'phone': '442083661177',
		'password': 'Password1!',
		'password_check': 'PassWord1!'
	}
	response = test_client.post('/register', data=new_user, follow_redirects=True)
	assert response.status_code == 200
	assert b"ServiceStation" in response.data
	assert b"Passwords do not match" in response.data
	assert b"Log Out" not in response.data
	assert b"Log In" in response.data
	assert b"Register" in response.data
	