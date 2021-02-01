from flask import Flask, render_template, url_for, redirect
# import helpers.db_func as db_func

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('front/index.html')

@app.route('/login/')
def login():
	return render_template('auth/user/login.html')

@app.route('/login-post/', methods=['POST', 'GET'])
def login_post():
	pass

@app.route('/register/')
def register():
	return render_template('auth/user/register.html')

@app.route('/register-post/', methods=['POST', 'GET'])
def register_post():
	pass

@app.route('/forget-password/')
def forget_password():
	return render_template('auth/user/forget-password.html')

@app.route('/forget-password-post/', methods=['POST', 'GET'])
def forget_password_post():
	pass

@app.route('/dashboard/')
def dashboard():
	return render_template('back/user/html/ltr/dashboard.html')

@app.route('/investment-history/')
def investment_history():
	return render_template('back/user/html/ltr/investment-history.html')

@app.route('/deposit-history/')
def deposit_history():
	return render_template('back/user/html/ltr/deposit-history.html')
@app.route('/withdraw-history/')
def withdraw_history():
	return render_template('back/user/html/ltr/withdraw-history.html')

@app.route('/referral-history/')
def referral_history():
	return render_template('back/user/html/ltr/referral-history.html')

@app.route('/deposit/')
def deposit():
	return render_template('back/user/html/ltr/deposit.html')

@app.route('/withdraw/')
def withdraw():
	return render_template('back/user/html/ltr/withdraw.html')

@app.route('/login-history/')
def login_history():
	return render_template('back/user/html/ltr/login-history.html')

@app.route('/referral-tools/')
def referral_tools():
	return render_template('back/user/html/ltr/referral-tools.html')

@app.route('/referral-materials/')
def referral_materials():
	return render_template('back/user/html/ltr/referral-materials.html')

@app.route('/profile-settings/')
def profile_settings():
	return render_template('back/user/html/ltr/profile-settings.html')

@app.route('/settings/')
def settings():
	return render_template('back/user/html/ltr/settings.html')

@app.route('/admin-login/')
def admin_login():
	return render_template('auth/admin/admin-login.html')

@app.route('/admin-dashboard/')
def admin_dashboard():
	return render_template('back/admin/html/ltr/admin-dashboard.html')

@app.route('/admin-investment-plans/')
def admin_investment_plans():
	return render_template('back/admin/html/ltr/admin-investment-plans.html')

@app.route('/admin-deposit/')
def admin_deposit():
	return render_template('back/admin/html/ltr/admin-deposit.html')

@app.route('/admin-withdraw/')
def admin_withdraw():
	return render_template('back/admin/html/ltr/admin-withdraw.html')

@app.route('/admin-payment-backlog/')
def admin_payment_backlog():
	return render_template('back/admin/html/ltr/admin-payment-backlog.html')

@app.route('/admin-history-users/')
def admin_history_users():
	return render_template('back/admin/html/ltr/admin-history-users.html')

@app.route('/admin-history-user-investments/')
def admin_history_user_investments():
	return render_template('back/admin/html/ltr/admin-history-user-investments.html')

@app.route('/admin-history-deposit/')
def admin_history_deposit():
	return render_template('back/admin/html/ltr/admin-history-deposit.html')

@app.route('/admin-history-withdraw/')
def admin_history_withdraw():
	return render_template('back/admin/html/ltr/admin-history-withdraw.html')

@app.route('/admin-settings/')
def admin_settings():
	return render_template('back/admin/html/ltr/admin-settings.html')

@app.route('/logout/')
def logout():
	return 'logout'

@app.route('/admin-logout/')
def admin_logout():
	return 'admin-logout'
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
