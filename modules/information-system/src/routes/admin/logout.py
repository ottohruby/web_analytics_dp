from . import bp

from flask import redirect, url_for, flash
from flask_login import logout_user

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('admin.login'))

