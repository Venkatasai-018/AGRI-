"""
AgriGo - UI Only Version (No ML Features)
This version focuses on authentication and user interface without TensorFlow dependencies
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# ============ Authentication Routes ============

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		
		user = User.query.filter_by(username=username).first()
		
		if user and user.check_password(password):
			login_user(user)
			flash('Login successful! Welcome back, ' + user.full_name or user.username + '!', 'success')
			next_page = request.args.get('next')
			return redirect(next_page if next_page else url_for('dashboard'))
		else:
			flash('Invalid username or password', 'error')
	
	return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		full_name = request.form.get('full_name')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		
		# Validation
		if password != confirm_password:
			flash('Passwords do not match!', 'error')
			return render_template('signup.html')
		
		if User.query.filter_by(username=username).first():
			flash('Username already exists!', 'error')
			return render_template('signup.html')
		
		if User.query.filter_by(email=email).first():
			flash('Email already registered!', 'error')
			return render_template('signup.html')
		
		# Create new user
		new_user = User(username=username, email=email, full_name=full_name)
		new_user.set_password(password)
		
		db.session.add(new_user)
		db.session.commit()
		
		flash('Registration successful! Please login.', 'success')
		return redirect(url_for('login'))
	
	return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out successfully.', 'info')
	return redirect(url_for('index'))


# ============ Dashboard & Feature Pages ============

@app.route('/dashboard')
@login_required
def dashboard():
	"""User dashboard showing all available services"""
	return render_template('dashboard.html')


@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
	flash('Crop Recommendation feature - ML models will be integrated soon!', 'info')
	return render_template('crop-recommend.html')


@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
def fertilizer_recommendation():
	flash('Fertilizer Recommendation feature - ML models will be integrated soon!', 'info')
	soil_types = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
	crop_types = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts']
	return render_template('fertilizer-recommend.html', soil_types=enumerate(soil_types), crop_types=enumerate(crop_types))


@app.route('/crop-disease', methods=['GET', 'POST'])
@login_required
def find_crop_disease():
	flash('Crop Disease Detection feature - ML models will be integrated soon!', 'info')
	crop_list = ['apple', 'cherry', 'corn', 'grape', 'peach', 'pepper', 'potato', 'strawberry', 'tomato']
	return render_template('crop-disease.html', crops=crop_list)


# ============ User Profile Routes ============

@app.route('/profile')
@login_required
def profile():
	"""User profile page"""
	return render_template('profile.html', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
	"""Edit user profile"""
	if request.method == 'POST':
		full_name = request.form.get('full_name')
		email = request.form.get('email')
		
		# Check if email is already taken by another user
		existing_user = User.query.filter_by(email=email).first()
		if existing_user and existing_user.id != current_user.id:
			flash('Email already in use by another account!', 'error')
			return render_template('edit_profile.html', user=current_user)
		
		current_user.full_name = full_name
		current_user.email = email
		
		db.session.commit()
		flash('Profile updated successfully!', 'success')
		return redirect(url_for('profile'))
	
	return render_template('edit_profile.html', user=current_user)


# ============ About & Info Pages ============

@app.route('/about')
def about():
	"""About page"""
	return render_template('about.html')


@app.route('/contact')
def contact():
	"""Contact page"""
	return render_template('contact.html')


# ============ Error Handlers ============

# Commented out - error templates not created yet
# @app.errorhandler(404)
# def not_found(error):
# 	return render_template('404.html'), 404


# @app.errorhandler(500)
# def internal_error(error):
# 	db.session.rollback()
# 	return render_template('500.html'), 500


# ============ Initialize & Run ============

if __name__ == '__main__':
	with app.app_context():
		# Create all database tables
		db.create_all()
		print("✅ Database initialized successfully!")
		print("🌐 Starting AgriGo UI-only version...")
		print("📝 Note: ML features are disabled. Install TensorFlow to enable them.")
	
	app.run(debug=True, host='0.0.0.0', port=5000)
