"""
Database Manager for Restaurant Menu System
Handles all database operations using SQLite
"""

import sqlite3
import hashlib
from pathlib import Path
from typing import Optional

class DatabaseManager:
    """Manages all database operations for the Restaurant Menu System"""
    
    def __init__(self, db_name: str = "restaurant_menu.db"):
        """Initialize database manager and create database file"""
        # Store database in the data folder
        self.db_path = Path("data") / db_name
        # Create data directory if it doesn't exist
        self.db_path.parent.mkdir(exist_ok=True)
        
        print(f"📁 Database will be stored at: {self.db_path}")
        
        # Initialize the database
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create all necessary tables"""
        print("🗄️  Initializing database tables...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Users table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'staff',
                full_name TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Menu Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category_id INTEGER,
                is_available BOOLEAN DEFAULT 1,
                preparation_time INTEGER DEFAULT 15,
                ingredients TEXT,
                allergens TEXT,
                calories INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database tables created successfully!")
        
        # Create default data
        self.create_default_data()
    
    def create_default_data(self):
        """Create default admin user and sample categories"""
        print("👤 Creating default users and sample data...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if admin user already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            # Create admin user
            admin_password = self.hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ("admin", admin_password, "admin", "System Administrator", "admin@restaurant.com"))
            
            # Create staff user
            staff_password = self.hash_password("staff123")
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ("staff", staff_password, "staff", "Restaurant Staff", "staff@restaurant.com"))
            
            print("✅ Default users created:")
            print("   👑 Admin - Username: 'admin', Password: 'admin123'")
            print("   👨‍🍳 Staff - Username: 'staff', Password: 'staff123'")
        
        # Check if categories exist
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            # Create sample categories
            categories = [
                ("Appetizers", "Start your meal with our delicious appetizers"),
                ("Main Courses", "Our signature main dishes"),
                ("Desserts", "Sweet treats to end your meal"),
                ("Beverages", "Refreshing drinks and beverages"),
                ("Salads", "Fresh and healthy salad options")
            ]
            
            cursor.executemany('''
                INSERT INTO categories (name, description)
                VALUES (?, ?)
            ''', categories)
            
            print("✅ Sample categories created!")
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def test_connection(self):
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            print("✅ Database connection test successful!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

# Test the database manager when this file is run directly
if __name__ == "__main__":
    print("Testing Database Manager...")
    db = DatabaseManager()
    db.test_connection()