from flask_login import current_user
from loguru import logger

from . import errors
from flask import render_template, request


@errors.app_errorhandler(401)
def not_authorized(e):
    user = current_user.email if current_user.is_authenticated else 'Guest'
    logger.warning(f'The user {user} takes unauthorized access to {request.url}')
    return render_template('errors/401.html'), 401


@errors.app_errorhandler(404)
def page_not_found(e):
    logger.warning(f'{request.url}')
    return render_template('errors/404.html'), 404
