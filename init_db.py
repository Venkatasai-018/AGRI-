"""
Initialization script for AgriGo application
This script creates the database tables if they don't exist
"""
from app import app, db

with app.app_context():
    # Create all database tables
    db.create_all()
    print("✅ Database tables created successfully!")
    print("📊 Database location: agri.db")
    print("\n🚀 You can now run the application with: python app.py")
