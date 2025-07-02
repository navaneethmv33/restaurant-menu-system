"""
User Manager for Restaurant Menu System
Handles user authentication and management
"""

import sqlite3
from typing import Optional, List, Tuple

class UserManager:
    """Handles user authentication and user management operations"""
    
    def __init__(self, db_manager):
        """Initialize with a database manager instance"""
        self.db = db_manager
        print("👤 User Manager initialized")
    
    def authenticate_user(self, username: str, password: str) -> Optional[Tuple]:
        """
        Authenticate a user with username and password
        Returns user info if successful, None if failed
        """
        print(f"🔐 Attempting to authenticate user: {username}")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Hash the provided password
        password_hash = self.db.hash_password(password)
        
        # Query database for user
        cursor.execute('''
            SELECT user_id, username, role, full_name, email 
            FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"✅ Authentication successful for {username} ({result[2]})")
            return result
        else:
            print(f"❌ Authentication failed for {username}")
            return None
    
    def register_user(self, username: str, password: str, role: str = "staff", 
                     full_name: str = "", email: str = "") -> bool:
        """
        Register a new user
        Returns True if successful, False if username already exists
        """
        print(f"📝 Attempting to register new user: {username}")
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Hash the password
            password_hash = self.db.hash_password(password)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, role, full_name, email))
            
            conn.commit()
            conn.close()
            
            print(f"✅ User '{username}' registered successfully!")
            return True
            
        except sqlite3.IntegrityError:
            print(f"❌ Username '{username}' already exists!")
            return False
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False
    
    def get_all_users(self) -> List[Tuple]:
        """Get all users (for admin use)"""
        print("👥 Fetching all users...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, role, full_name, email, created_at 
            FROM users
            ORDER BY created_at DESC
        ''')
        
        result = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(result)} users")
        return result
    
    def get_user_info(self, user_id: int) -> Optional[Tuple]:
        """Get information for a specific user"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, role, full_name, email, created_at
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result

# Test the user manager when this file is run directly
if __name__ == "__main__":
    print("Testing User Manager...")
    
    # Import database manager
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent.parent))
    
    from src.restaurant_menu.models.database import DatabaseManager
    
    # Create instances
    db = DatabaseManager()
    user_manager = UserManager(db)
    
    # Test authentication with default users
    print("\n🧪 Testing authentication...")
    
    # Test admin login
    admin_user = user_manager.authenticate_user("admin", "admin123")
    if admin_user:
        print(f"Admin user info: {admin_user}")
    
    # Test staff login
    staff_user = user_manager.authenticate_user("staff", "staff123")
    if staff_user:
        print(f"Staff user info: {staff_user}")
    
    # Test wrong password
    wrong_user = user_manager.authenticate_user("admin", "wrongpassword")
    
    print("\n🧪 Testing user registration...")
    # Test registering a new user
    new_user_success = user_manager.register_user(
        "testuser", "testpass", "staff", "Test User", "test@test.com"
    )
    
    # Test registering duplicate user
    duplicate_user = user_manager.register_user("admin", "newpass")
    
    print("\n👥 All users:")
    users = user_manager.get_all_users()
    for user in users:
        print(f"  - {user[1]} ({user[2]}) - {user[3]}")
    
    print("\n✅ User Manager testing completed!")