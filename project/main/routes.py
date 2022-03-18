from flask import render_template
from flask_login import current_user

from loguru import logger

from . import main


@main.route('/')
@main.route('/index')
def index():
    user = current_user.email if current_user.is_authenticated else 'Guest'
    logger.info(f'User {user} is at the main page')
    return render_template('index.html')
