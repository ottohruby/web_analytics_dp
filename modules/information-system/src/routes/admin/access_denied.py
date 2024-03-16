from . import bp

from flask import redirect, url_for, flash
from flask_login import logout_user

@bp.route('/access_denied')
def access_denied():
    return redirect(url_for('admin.login'))

