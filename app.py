from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, jsonify
import random, os, json
from werkzeug.utils import secure_filename
import google.generativeai as genai
from functions import img_predict, get_diseases_classes, get_crop_recommendation, get_fertilizer_recommendation, soil_types, Crop_types, crop_list
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, User

app = Flask(__name__)
random.seed(0)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agri.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyDYour-API-Key-Here'  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

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
		
		flash('Registration successful! Welcome to Agricare, ' + new_user.username + '!', 'success')
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

@app.route('/farmbot')
def farmbot():
	return render_template('farmbot.html')

@app.route('/farmbot/chat', methods=['POST'])
def farmbot_chat():
	try:
		data = request.get_json()
		user_message = data.get('message', '')
		
		if not user_message:
			return jsonify({'success': False, 'error': 'No message provided'})
		
		# Create system prompt to restrict responses to farming topics
		system_prompt = """You are Farm Bot, an AI agricultural expert assistant for Agricare platform. 
		You ONLY answer questions related to:
		- Agriculture and farming
		- Crop cultivation and management
		- Plant diseases and pest control
		- Fertilizers and soil management
		- Irrigation and water management
		- Organic farming practices
		- Agricultural technology and techniques
		- Crop recommendations
		- Harvesting and post-harvest management
		
		If a question is NOT related to farming or agriculture, politely respond:
		"I'm Farm Bot, specialized in agricultural topics. I can only help with farming-related questions. Please ask me about crops, diseases, fertilizers, or farming techniques!"
		
		Keep responses concise, practical, and farmer-friendly. Use simple language.
		"""
		
		# Initialize Gemini model
		model = genai.GenerativeModel('gemini-pro')
		
		# Generate response
		full_prompt = f"{system_prompt}\n\nUser Question: {user_message}\n\nFarm Bot:"
		response = model.generate_content(full_prompt)
		
		return jsonify({
			'success': True,
			'response': response.text
		})
		
	except Exception as e:
		print(f"Error in farmbot_chat: {str(e)}")
		return jsonify({
			'success': False,
			'error': 'Failed to generate response. Please try again.'
		})

def get_disease_analysis(crop, disease_name):
	"""Get detailed disease analysis from Gemini API"""
	try:
		prompt = f"""As an agricultural disease expert, provide a comprehensive analysis for the following crop disease:

Crop: {crop}
Disease: {disease_name}

Please provide detailed information in the following structure (use JSON format):

{{
  "disease_name": "{disease_name}",
  "severity": "Low/Moderate/High/Critical",
  "description": "Brief description of the disease (2-3 sentences)",
  "symptoms": ["symptom1", "symptom2", "symptom3"],
  "causes": ["cause1", "cause2"],
  "treatment": {{
    "immediate_actions": ["action1", "action2"],
    "chemical_treatment": ["chemical1 with dosage", "chemical2 with dosage"],
    "organic_treatment": ["organic1", "organic2"]
  }},
  "prevention": ["prevention1", "prevention2", "prevention3"],
  "impact": "Description of potential yield impact if untreated",
  "timeline": "Expected treatment duration",
  "additional_tips": ["tip1", "tip2"]
}}

Provide ONLY the JSON response without any additional text or markdown formatting."""

		model = genai.GenerativeModel('gemini-pro')
		response = model.generate_content(prompt)
		
		# Parse the JSON response
		import re
		response_text = response.text.strip()
		# Remove markdown code blocks if present
		response_text = re.sub(r'```json\s*|\s*```', '', response_text)
		
		analysis = json.loads(response_text)
		return analysis
		
	except Exception as e:
		print(f"Error in disease analysis: {str(e)}")
		# Return default structure if API fails
		return {
			"disease_name": disease_name,
			"severity": "Unknown",
			"description": "Disease analysis is currently unavailable.",
			"symptoms": ["Unable to fetch symptoms"],
			"causes": ["Unable to fetch causes"],
			"treatment": {
				"immediate_actions": ["Consult with local agricultural expert"],
				"chemical_treatment": ["Consult with agricultural specialist"],
				"organic_treatment": ["Consult with agricultural specialist"]
			},
			"prevention": ["Regular monitoring of crops"],
			"impact": "Consult with agricultural expert for impact assessment",
			"timeline": "Varies",
			"additional_tips": ["Seek professional guidance"]
		}

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
			
			# Get AI-powered disease analysis from Gemini
			disease_analysis = get_disease_analysis(crop, result)
			
			flash('Disease prediction completed successfully!', 'success')
			return render_template('disease-prediction-result.html', 
				image_file_name=file.filename, 
				result=result,
				crop=crop,
				analysis=disease_analysis)
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