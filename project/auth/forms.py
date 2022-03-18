from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
import phonenumbers
import email_validator

from project.models import User

# TODO: validate (normalize) email with spaces


class LoginForm(FlaskForm):
	
	email = StringField('Email', validators=[
		DataRequired(message='Required field'),
		Email(),  # message='Invalid email'
		Length(min=5, max=100)
	], render_kw={"placeholder": "test placeholder"})
	
	password = PasswordField('Password', validators=[
		DataRequired(message='Required field')
	], description="test placeholder")
	remember_me = BooleanField('Remember Me')
	
	submit = SubmitField('Let me in!')


class RegisterForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
	email = EmailField('Email', validators=[DataRequired(), Email(), Length(min=5, max=100)])
	phone = TelField('Phone', validators=[DataRequired(), Length(min=9, max=20)])
	password = PasswordField('Password', validators=[
		DataRequired(),
		Length(min=8, max=32),
		Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$",
		       message='Invalid password pattern')
	])
	password_check = PasswordField('Password Check', validators=[
		DataRequired(),
		Length(min=8, max=32),
		EqualTo('password', message="Passwords do not match")
	])
	
	submit = SubmitField('Register')
	
	@staticmethod
	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("Email already registered")
	
	@staticmethod
	def validate_phone(self, phone):
		if phone.data[0] != '+':
			phone.data = '+' + phone.data
		try:
			p = phonenumbers.parse(phone.data)
			if not phonenumbers.is_valid_number(p):
				# TODO what to do if
				raise ValueError()
			phone.data = phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
		except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
			raise ValidationError('Invalid phone number')


class ResetPasswordRequestForm(FlaskForm):
	email = EmailField('Email', validators=[DataRequired(), Email(message='Invalid email')])
	
	submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[
		DataRequired(),
		Length(min=8, max=32),
		Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$")
	])
	password_check = PasswordField('Repeat Password', validators=[
		DataRequired(),
		Length(min=8, max=32),
		EqualTo('password')
	])
	
	submit = SubmitField('Request Password Reset')
