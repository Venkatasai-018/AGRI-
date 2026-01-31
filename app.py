from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import random, os
from werkzeug.utils import secure_filename
from functions import img_predict, get_diseases_classes, get_crop_recommendation, get_fertilizer_recommendation, soil_types, Crop_types, crop_list
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User

app = Flask(__name__)
random.seed(0)
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

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/', methods=['GET', 'POST'])
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
			flash('Login successful! Welcome back, ' + user.username + '!', 'success')
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
		
		flash('Registration successful! Welcome to AgriGo, ' + new_user.username + '!', 'success')
		# Auto-login the user after signup
		login_user(new_user)
		return redirect(url_for('dashboard'))
	
	return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.', 'info')
	return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html', user=current_user)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		message = request.form.get('message')
		flash(f'Thank you {name}! Your message has been received. We will get back to you soon.', 'success')
		return redirect(url_for('contact'))
	return render_template('contact.html')

@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
	if request.method == "POST":
		try:
			to_predict_list = request.form.to_dict()
			to_predict_list = list(to_predict_list.values())
			to_predict_list = list(map(float, to_predict_list))
			result = get_crop_recommendation(to_predict_list)
			flash('Crop recommendation generated successfully!', 'success')
			return render_template("recommend_result.html", result=result)
		except Exception as e:
			flash(f'Error generating recommendation: {str(e)}', 'error')
			return render_template('crop-recommend.html')
	else:
		return render_template('crop-recommend.html')

@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
def fertilizer_recommendation():
	if request.method == "POST":
		try:
			to_predict_list = request.form.to_dict()
			to_predict_list = list(to_predict_list.values())
			to_predict_list = list(map(float, to_predict_list))
			result = get_fertilizer_recommendation(
				num_features=to_predict_list[:-2],
				cat_features=to_predict_list[-2:]
			)
			flash('Fertilizer recommendation generated successfully!', 'success')
			return render_template("recommend_result.html", result=result)
		except Exception as e:
			flash(f'Error generating recommendation: {str(e)}', 'error')
			return render_template(
				'fertilizer-recommend.html', 
				soil_types=enumerate(soil_types),
				crop_types=enumerate(Crop_types)
			)
	else:
		return render_template(
			'fertilizer-recommend.html', 
			soil_types=enumerate(soil_types),
			crop_types=enumerate(Crop_types)
		)
@app.route('/disease-prediction', methods=['GET', 'POST'])
@login_required
def disease_prediction():
	if request.method=="GET":
		return render_template('crop-disease.html', crops=crop_list)
	else:
		try:
			if 'file' not in request.files:
				flash('No file uploaded. Please select an image.', 'error')
				return render_template('crop-disease.html', crops=crop_list)
			
			file = request.files["file"]
			crop = request.form["crop"]
			
			if file.filename == '':
				flash('No file selected. Please choose an image.', 'error')
				return render_template('crop-disease.html', crops=crop_list)
			
			# Validate file extension
			allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
			if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
				flash('Invalid file type. Please upload an image (png, jpg, jpeg, gif, bmp).', 'error')
				return render_template('crop-disease.html', crops=crop_list)

			basepath = os.path.dirname(__file__)
			# Create uploads folder if it doesn't exist
			os.makedirs(os.path.join(basepath, 'uploads'), exist_ok=True)
			
			file_path = os.path.join(basepath,'uploads',  secure_filename(file.filename))
			file.save(file_path)
			prediction = img_predict(file_path, crop)
			result = get_diseases_classes(crop, prediction)
			
			flash('Disease prediction completed successfully!', 'success')
			return render_template('disease-prediction-result.html', image_file_name=file.filename, result=result)
		except Exception as e:
			flash(f'Error processing image: {str(e)}', 'error')
			return render_template('crop-disease.html', crops=crop_list)

@app.route('/uploads/<filename>')
def send_file(filename):
	return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)