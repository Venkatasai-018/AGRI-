# AgriGo - Setup and Usage Guide

## Features Added
✅ SQLite Database Integration
✅ User Authentication (Login/Signup)
✅ Professional UI Design
✅ Secure Password Hashing
✅ Session Management
✅ Protected Routes (requires login)

## Database Schema
- **Users Table**
  - id (Primary Key)
  - username (Unique)
  - email (Unique)
  - password_hash (Encrypted)
  - full_name
  - created_at

## How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open your browser and go to: http://127.0.0.1:5000
   - The database will be automatically created on first run

## Usage Flow

1. **Sign Up**: Create a new account at `/signup`
2. **Login**: Login with your credentials at `/login`
3. **Access Services**: Once logged in, you can access:
   - Crop Disease Detection
   - Fertilizer Recommendation
   - Crop Recommendation
4. **Logout**: Click the logout button in the navigation bar

## Default Features

### Public Pages (No Login Required)
- Home page (/)
- Login page (/login)
- Signup page (/signup)

### Protected Pages (Login Required)
- Crop Recommendation (/crop-recommendation)
- Fertilizer Recommendation (/fertilizer-recommendation)
- Crop Disease Detection (/crop-disease)

## Database Location
- The SQLite database will be created as `agri.db` in the project root directory

## Security Features
- Password hashing using Werkzeug
- Session management with Flask-Login
- CSRF protection
- Secure cookie handling

## Notes
- Change the SECRET_KEY in app.py before deploying to production
- The database is automatically created when you run the app for the first time
- All user passwords are securely hashed and never stored in plain text
