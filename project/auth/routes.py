import datetime

from flask import render_template, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from loguru import logger
from werkzeug.utils import redirect
from psycopg2.errors import DatabaseError

from . import auth
from .forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from .. import db
from ..email import send_password_reset_email
from ..models import User

# TODO: не работает try-except на БД
# TODO: подтверждение email после регистрации


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.info(f'{current_user.email} tried to log in again')
        return redirect(url_for('main.index'))
    
    login_form = LoginForm()
    next_url = request.args.get('next')
    
    if login_form.validate_on_submit():
        try:
            user = User.query.filter_by(email=login_form.email.data.strip()).first()
        except DatabaseError:
            logger.error(f'DB error when user {login_form.email.data.strip()} tried to log in')
            db.session.rollback()
            flash('Sorry, database error', 'danger')
            return redirect(url_for('.login'))
        else:
            if user is None or not user.check_password(login_form.password.data.strip()):
                flash('Invalid email or password', 'danger')
                return redirect(url_for('.login'))
            
            login_user(user, remember=login_form.remember_me.data)
            logger.info(f'{current_user.email} logged in')
            flash('Welcome!', 'success')
            return redirect(next_url or url_for('main.index'))
        
    return render_template('auth/login.html', form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if current_user.is_authenticated:
        logger.info(f'{current_user.email} tried to register again')
        flash('Email already registered', 'success')
        return redirect(url_for('main.index'))
    
    if register_form.validate_on_submit():
        
        new_user = User(
            first_name=register_form.first_name.data.strip(),
            last_name=register_form.last_name.data.strip(),
            email=register_form.email.data.strip(),
            phone=register_form.phone.data.strip(),
            password=register_form.password.data.strip()
        )
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except DatabaseError:
            logger.error(f'DB error when user {new_user.email} tried to register')
            db.session.rollback()
            flash('Sorry, database error', 'danger')
            return redirect(url_for('.register'))
        else:
            user = User.query.filter_by(email=new_user.email).first()
            login_user(user)
            logger.info(f'{user.email} has been registered')
            flash('Thanks for registering', 'success')
            return redirect(f'profile/{user.user_id}')
        
    return render_template('auth/register.html', form=register_form)


@auth.route('/logout')
@login_required
def logout():
    flash('Logged out', 'success')
    logger.info(f'{current_user.email} has been logged out')
    logout_user()
    return redirect(url_for('.login'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        
        email_to_reset = form.email.data.strip()
        try:
            user = User.query.filter_by(email=email_to_reset).first()
        except DatabaseError:
            logger.error(f'DB error when user {email_to_reset} tried to request password reset')
            db.session.rollback()
            flash('Sorry, database error', 'danger')
            return redirect(url_for('.reset_password_request'))
        else:
            if user:
                logger.warning(f'{user.email} requested password reset')
                send_password_reset_email(user)
            else:
                logger.error(f'Anonymous {email_to_reset} tried to request password reset')
                flash('Unknown email', 'danger')
                redirect(url_for('.reset_password_request'))
                
            flash('Check your email for the instructions to reset your password', 'success')
            return redirect(url_for('.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


# Decorator for DB errors
# def db_exception(flash_text=None, flash_category=None, log_text=None):
#     def db_dec(func):
#         def wrapper():
#
#             try:
#                 func()
#             except DatabaseError:
#                 if flash_text and flash_category:
#                     flash(flash_text, flash_category)
#                 db.session.rollback()
#                 if log_text:
#                     logger.error(log_text)
#
#         return wrapper
#     return db_dec


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    try:
        user = User.verify_reset_password_token(token)
    except DatabaseError:
        logger.error('Retry: DB error when unknown user tried to reset password.')
        db.session.rollback()
        return redirect(url_for('.reset_password', token=token))
    else:
        if not user:
            logger.warning('Failed attempt - reset password. User unknown.')
            return redirect(url_for('main.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data.strip())
        
        try:
            db.session.commit()
        except DatabaseError:
            logger.error(f'Retry: DB error when user {user.email} tried to set new password.')
            flash('Sorry, database error, try again', 'danger')
            return redirect(url_for('.reset_password', token=token))
        
        logger.info(f'{user.email} changed password')
        flash('Your password has been reset.', 'success')
        return redirect(url_for('.login'))
    return render_template('auth/reset_password.html', form=form)


# @auth.route('/delete/<user_id>', methods=['GET'])
# def delete_user(user_id):
#     user = User.query.filter_by(user_id=user_id).first()
#     db.session.delete(user)
#     db.session.commit()
#     return True
