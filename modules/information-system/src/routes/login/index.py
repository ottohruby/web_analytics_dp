from flask import request, jsonify
from src.routes.login import bp
# from src.models.user import User


from datetime import datetime

# @bp.route('/', methods=["POST", "GET"])
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(username=form.username.data).first()
# 		if user:
# 			if check_password_hash(user.password, form.password.data):
# 				login_user(user, remember=form.remember.data)
# 				return redirect(url_for('dashboard'))
# 		return '<h1>Invalid username or password</h1>'
# 		#return '<h1>' + form.username.data + '' + form.password.data + '</h1>'
# 	return render_template('login.html', form=form)

@bp.route('/')
def login_index():
    return jsonify({"message": "running"}), 200