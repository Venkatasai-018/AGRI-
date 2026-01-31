# AgriGo - Agricultural Intelligence Platform

## 🌾 Overview
AgriGo is an AI-powered agricultural platform that provides farmers with intelligent crop recommendations, fertilizer suggestions, and disease detection capabilities.

## ✨ Features Implemented

### Authentication System
- ✅ User Registration (Sign Up)
- ✅ User Login
- ✅ Secure Password Hashing
- ✅ Session Management
- ✅ Logout Functionality

### Database
- ✅ SQLite Database
- ✅ User Management System
- ✅ Automatic Table Creation

### Professional UI
- ✅ Modern, Responsive Design
- ✅ Beautiful Login/Signup Pages
- ✅ Interactive Dashboard
- ✅ Flash Messages for User Feedback
- ✅ Professional Navigation
- ✅ Mobile-Friendly Layout

### Protected Routes
- ✅ Crop Recommendation Page
- ✅ Fertilizer Recommendation Page
- ✅ Crop Disease Detection Page
- ✅ User Dashboard

## 📁 Project Structure

```
AGRI-/
├── app.py                      # Main app (with TensorFlow - commented out)
├── app_ui_only.py             # UI-only version (NO TensorFlow required) ⭐
├── database.py                # Database models
├── functions.py               # ML functions (requires TensorFlow)
├── init_db.py                 # Database initialization script
├── requirements.txt           # Python dependencies
├── SETUP_GUIDE.md            # Setup instructions
├── templates/
│   ├── index.html            # Landing page
│   ├── login.html            # Login page ⭐
│   ├── signup.html           # Signup page ⭐
│   ├── dashboard.html        # User dashboard ⭐
│   ├── crop-recommend.html
│   ├── fertilizer-recommend.html
│   ├── crop-disease.html
│   └── ...
├── static/
│   ├── css/
│   │   └── main.css          # Updated professional styles
│   ├── images/
│   └── js/
├── models/                    # ML models (for future use)
├── dataset/                   # Training datasets
└── uploads/                   # User uploaded files
```

## 🚀 Quick Start

### Option 1: UI-Only Version (Recommended for Testing)

**No TensorFlow or ML dependencies needed!**

```bash
# 1. Install basic dependencies
pip install Flask Flask-SQLAlchemy Flask-Login

# 2. Run the UI-only version
python app_ui_only.py

# 3. Open browser
http://localhost:5000
```

### Option 2: Full Version (With ML Features)

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Run the full app
python app.py

# 3. Open browser
http://localhost:5000
```

## 📝 Usage Instructions

### 1. Create an Account
- Navigate to http://localhost:5000
- Click "Sign Up" button
- Fill in your details:
  - Full Name
  - Username (unique)
  - Email (unique)
  - Password
  - Confirm Password
- Click "Sign Up"

### 2. Login
- Go to Login page
- Enter your username and password
- Click "Login"
- You'll be redirected to the dashboard

### 3. Access Features
Once logged in, you can access:
- **Dashboard**: Overview of all services
- **Crop Recommendation**: Get crop suggestions
- **Fertilizer Recommendation**: Get fertilizer advice
- **Disease Detection**: Upload crop images for analysis

### 4. Logout
- Click the "Logout" button in the navigation bar

## 🎨 UI Improvements Made

1. **Login Page**
   - Modern split-screen design
   - Gradient backgrounds
   - Smooth animations
   - Form validation
   - Flash messages

2. **Signup Page**
   - Professional form layout
   - Password confirmation
   - Email validation
   - User-friendly error messages

3. **Home Page**
   - Updated navigation with auth buttons
   - User welcome message when logged in
   - Logout button for authenticated users
   - Flash message alerts

4. **Dashboard**
   - Welcome section with user name
   - Service cards with icons
   - Statistics section
   - Responsive grid layout
   - Modern card design with hover effects

5. **Overall Design**
   - Consistent color scheme (Purple/Blue gradient)
   - Professional typography (Poppins font)
   - Smooth transitions and animations
   - Mobile-responsive layout
   - Box shadows and modern styling

## 🔒 Security Features

- **Password Hashing**: Using Werkzeug's secure password hashing
- **Session Management**: Flask-Login handles user sessions
- **Protected Routes**: `@login_required` decorator protects sensitive pages
- **CSRF Protection**: Built into Flask
- **Secure Cookies**: Configured in Flask app

## 🗄️ Database Schema

### Users Table
| Column        | Type      | Description                |
|--------------|-----------|----------------------------|
| id           | Integer   | Primary key (auto)         |
| username     | String    | Unique username            |
| email        | String    | Unique email address       |
| password_hash| String    | Hashed password            |
| full_name    | String    | User's full name           |
| created_at   | DateTime  | Registration timestamp     |

## 📦 Dependencies

### Core Dependencies (UI-Only)
```
Flask==2.0.3
Flask-SQLAlchemy==2.5.1
Flask-Login==0.6.0
Werkzeug==2.0.3
```

### ML Dependencies (Full Version)
```
tensorflow-cpu==2.8.0
keras==2.8.0
numpy==1.22.3
scikit-learn==1.0.2
Pillow==9.0.1
```

## 🔧 Configuration

### Secret Key
⚠️ **Important**: Change the SECRET_KEY before deploying to production!

In `app_ui_only.py` or `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Database Location
The SQLite database is created as `agri.db` in the project root directory.

## 🌐 Routes

### Public Routes (No Login Required)
- `/` - Home page
- `/login` - Login page
- `/signup` - Signup page

### Protected Routes (Login Required)
- `/dashboard` - User dashboard
- `/crop-recommendation` - Crop recommendation
- `/fertilizer-recommendation` - Fertilizer recommendation
- `/crop-disease` - Disease detection
- `/profile` - User profile
- `/logout` - Logout

## 🐛 Troubleshooting

### Issue: TensorFlow Import Error
**Solution**: Use `app_ui_only.py` instead of `app.py`

### Issue: Database doesn't exist
**Solution**: Run the app once - it will auto-create the database

### Issue: Port already in use
**Solution**: Change the port in the run command:
```python
app.run(debug=True, port=5001)
```

## 📈 Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] User profile editing
- [ ] Admin panel
- [ ] Activity history
- [ ] Export reports
- [ ] Multi-language support
- [ ] Dark mode toggle

## 👨‍💻 Development

### Running in Development Mode
```bash
python app_ui_only.py
```

### Running in Production Mode
```bash
# Set environment variable
export FLASK_ENV=production

# Use a production server like Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_ui_only:app
```

## 📄 License
This project is for educational purposes.

## 🤝 Support
For issues or questions, please check the SETUP_GUIDE.md file.

---

**Current Status**: ✅ Authentication & UI Complete | ⏳ ML Features Pending (TensorFlow)
