from flask import render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from ..models import User
from . import profile


@profile.route('/')
@login_required
def profile_main():
	return redirect(url_for('.profile_user', user_id=current_user.user_id))


@profile.route('/<user_id>')
@login_required
def profile_user(user_id):
	user = User.query.filter_by(user_id=user_id).first_or_404()
	if current_user.user_id != user.user_id:
		flash('Not yours!', 'danger')
		abort(401)

	return render_template('profile/profile.html')
