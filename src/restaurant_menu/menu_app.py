"""
Complete Menu Management Application
Combines all menu management functionality with user authentication
"""

import sys
import os
from typing import Optional, Tuple

from .models.database import DatabaseManager
from .managers.user_manager import UserManager
from .managers.menu_manager import MenuManager
from .ui.menu_cli import MenuCLI

class MenuManagementApp:
    """Complete Menu Management Application"""
    
    def __init__(self):
        """Initialize the application"""
        print("🍽️  Initializing Restaurant Menu Management System...")
        
        # Initialize core components
        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.menu_manager = MenuManager(self.db_manager)
        self.menu_cli = MenuCLI(self.menu_manager, self.user_manager)
        
        # Current user session
        self.current_user = None
        
        print("✅ Application initialized successfully!")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Display welcome screen"""
        self.clear_screen()
        print("=" * 60)
        print("        🍽️  RESTAURANT MENU MANAGEMENT SYSTEM  🍽️")
        print("=" * 60)
        print("             Welcome to your digital menu!")
        print("=" * 60)
    
    def show_login_menu(self):
        """Display login/registration menu"""
        print("\n--- 🔐 AUTHENTICATION ---")
        print("1. 🔑 Login")
        print("2. 📝 Register New Staff")
        print("3. 🚪 Exit")
        print("-" * 30)
        
        choice = input("Enter your choice (1-3): ").strip()
        return choice
    
    def handle_login(self):
        """Handle user login"""
        print("\n--- 🔐 LOGIN ---")
        print("Default accounts:")
        print("  👑 Admin: username='admin', password='admin123'")
        print("  👨‍🍳 Staff: username='staff', password='staff123'")
        print()
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return False
        
        password = input("Password: ").strip()
        if not password:
            print("❌ Password cannot be empty.")
            return False
        
        user = self.user_manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            self.clear_screen()
            print(f"🎉 Welcome, {user[3] or user[1]}!")
            print(f"👤 Role: {user[2].title()}")
            return True
        else:
            print("❌ Invalid credentials. Please try again.")
            input("Press Enter to continue...")
            return False
    
    def handle_registration(self):
        """Handle new staff registration"""
        print("\n--- 📝 REGISTER NEW STAFF ---")
        
        username = input("Username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return
        
        password = input("Password: ").strip()
        if not password:
            print("❌ Password cannot be empty.")
            return
        
        full_name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        
        if self.user_manager.register_user(username, password, "staff", full_name, email):
            print("✅ Registration successful! You can now login.")
        else:
            print("❌ Registration failed. Username might already exist.")
        
        input("Press Enter to continue...")
    
    def show_main_menu(self):
        """Show main menu based on user role"""
        if self.current_user[2] == 'admin':
            return self.show_admin_menu()
        else:
            return self.show_staff_menu()
    
    def show_admin_menu(self):
        """Show admin menu"""
        print(f"\n--- 👑 ADMIN PANEL - {self.current_user[3] or self.current_user[1]} ---")
        print("📋 MENU MANAGEMENT:")
        print("  1. 👀 View All Menu Items")
        print("  2. ➕ Add New Menu Item") 
        print("  3. ✏️  Update Menu Item")
        print("  4. 🗑️  Delete Menu Item")
        print("  5. 🔍 Search Menu Items")
        print("\n📂 CATEGORY MANAGEMENT:")
        print("  6. 📂 View Categories")
        print("  7. ➕ Add New Category")
        print("\n📊 REPORTS & INFO:")
        print("  8. 📊 Menu Statistics")
        print("  9. 👥 View All Users")
        print("\n🔧 SYSTEM:")
        print("  10. 🚪 Logout")
        print("-" * 50)
        
        choice = input("Enter your choice (1-10): ").strip()
        return choice
    
    def show_staff_menu(self):
        """Show staff menu"""
        print(f"\n--- 👨‍🍳 STAFF PANEL - {self.current_user[3] or self.current_user[1]} ---")
        print("📋 MENU OPERATIONS:")
        print("  1. 👀 View All Menu Items")
        print("  2. 🔍 Search Menu Items")
        print("  3. 📂 Browse by Category")
        print("  4. 📊 Menu Statistics")
        print("\n🔧 SYSTEM:")
        print("  5. 🚪 Logout")
        print("-" * 40)
        
        choice = input("Enter your choice (1-5): ").strip()
        return choice
    
    def handle_admin_choice(self, choice: str):
        """Handle admin menu choices"""
        if choice == '1':
            self.view_all_menu_items()
        elif choice == '2':
            self.add_menu_item()
        elif choice == '3':
            self.menu_cli.update_menu_item_interface()
        elif choice == '4':
            self.menu_cli.delete_menu_item_interface()
        elif choice == '5':
            self.menu_cli.search_menu_interface()
        elif choice == '6':
            self.view_categories()
        elif choice == '7':
            self.add_category()
        elif choice == '8':
            self.menu_cli.show_menu_statistics()
            self.menu_cli.pause()
        elif choice == '9':
            self.view_all_users()
        elif choice == '10':
            self.logout()
            return False
        else:
            print("❌ Invalid choice. Please try again.")
            self.menu_cli.pause()
        
        return True
    
    def handle_staff_choice(self, choice: str):
        """Handle staff menu choices"""
        if choice == '1':
            self.view_all_menu_items()
        elif choice == '2':
            self.menu_cli.search_menu_interface()
        elif choice == '3':
            self.browse_by_category()
        elif choice == '4':
            self.menu_cli.show_menu_statistics()
            self.menu_cli.pause()
        elif choice == '5':
            self.logout()
            return False
        else:
            print("❌ Invalid choice. Please try again.")
            self.menu_cli.pause()
        
        return True
    
    def view_all_menu_items(self):
        """View all menu items"""
        self.menu_cli.show_menu_header("👀 ALL MENU ITEMS")
        
        items = self.menu_manager.get_all_menu_items()
        
        if not items:
            print("📭 No menu items found.")
        else:
            show_details = self.menu_cli.get_user_choice(
                "Show detailed view? (y/n)", ['y', 'yes', 'n', 'no']
            )
            
            detailed = show_details in ['y', 'yes']
            self.menu_cli.display_menu_items(items, show_details=detailed)
            
            if not detailed:
                # Option to view specific item details
                view_item = self.menu_cli.get_user_choice(
                    "View specific item details? (y/n)", ['y', 'yes', 'n', 'no']
                )
                
                if view_item in ['y', 'yes']:
                    item_id = self.menu_cli.get_number_input("Enter Item ID", min_val=1)
                    if item_id:
                        item = self.menu_manager.get_item_by_id(int(item_id))
                        if item:
                            self.menu_cli.show_item_details(item)
                        else:
                            print(f"❌ Item with ID {int(item_id)} not found.")
        
        self.menu_cli.pause()
    
    def add_menu_item(self):
        """Add new menu item"""
        self.menu_cli.show_menu_header("➕ ADD NEW MENU ITEM")
        
        item_data = self.menu_cli.get_menu_item_input()
        
        if item_data:
            if self.menu_manager.add_menu_item(**item_data):
                print("✅ Menu item added successfully!")
            else:
                print("❌ Failed to add menu item.")
        else:
            print("❌ Menu item creation cancelled.")
        
        self.menu_cli.pause()
    
    def view_categories(self):
        """View all categories"""
        self.menu_cli.show_menu_header("📂 ALL CATEGORIES")
        
        categories = self.menu_manager.get_all_categories()
        self.menu_cli.display_categories(categories)
        
        if categories:
            # Option to view items in a category
            view_items = self.menu_cli.get_user_choice(
                "View items in a specific category? (y/n)", ['y', 'yes', 'n', 'no']
            )
            
            if view_items in ['y', 'yes']:
                cat_id = self.menu_cli.get_number_input("Enter Category ID", min_val=1)
                if cat_id:
                    items = self.menu_manager.get_menu_by_category(int(cat_id))
                    if items:
                        category = self.menu_manager.get_category_by_id(int(cat_id))
                        print(f"\n🍽️  Items in '{category[1]}':")
                        # Convert items to display format
                        display_items = []
                        for item in items:
                            # Add category name for display consistency
                            display_item = item[:4] + (category[1],) + item[4:]
                            display_items.append(display_item)
                        self.menu_cli.display_menu_items(display_items)
                    else:
                        print(f"📭 No items found in category {int(cat_id)}.")
        
        self.menu_cli.pause()
    
    def add_category(self):
        """Add new category"""
        self.menu_cli.show_menu_header("➕ ADD NEW CATEGORY")
        
        name = input("Category Name: ").strip()
        if not name:
            print("❌ Category name is required.")
            self.menu_cli.pause()
            return
        
        description = input("Description (optional): ").strip()
        
        if self.menu_manager.add_category(name, description):
            print("✅ Category added successfully!")
        else:
            print("❌ Failed to add category. Name might already exist.")
        
        self.menu_cli.pause()
    
    def browse_by_category(self):
        """Browse menu items by category"""
        self.menu_cli.show_menu_header("📂 BROWSE BY CATEGORY")
        
        categories = self.menu_manager.get_all_categories()
        if not categories:
            print("📭 No categories found.")
            self.menu_cli.pause()
            return
        
        self.menu_cli.display_categories(categories)
        
        cat_id = self.menu_cli.get_number_input("Enter Category ID to browse", min_val=1)
        if not cat_id:
            return
        
        cat_id = int(cat_id)
        category = self.menu_manager.get_category_by_id(cat_id)
        
        if not category:
            print(f"❌ Category {cat_id} not found.")
            self.menu_cli.pause()
            return
        
        items = self.menu_manager.get_menu_by_category(cat_id)
        
        if items:
            print(f"\n🍽️  Items in '{category[1]}':")
            # Convert items to display format
            display_items = []
            for item in items:
                # Add category name for display consistency
                display_item = item[:4] + (category[1],) + item[4:]
                display_items.append(display_item)
            self.menu_cli.display_menu_items(display_items, show_details=True)
        else:
            print(f"📭 No items found in '{category[1]}'.")
        
        self.menu_cli.pause()
    
    def view_all_users(self):
        """View all users (admin only)"""
        self.menu_cli.show_menu_header("👥 ALL USERS")
        
        users = self.user_manager.get_all_users()
        
        if not users:
            print("📭 No users found.")
        else:
            print(f"\n👥 SYSTEM USERS ({len(users)} total):")
            print("=" * 80)
            print(f"{'ID':<4} {'Username':<15} {'Role':<8} {'Full Name':<20} {'Email':<20}")
            print("=" * 80)
            
            for user in users:
                print(f"{user[0]:<4} {user[1]:<15} {user[2]:<8} "
                      f"{(user[3] or 'Not set')[:19]:<20} {(user[4] or 'Not set')[:19]:<20}")
        
        self.menu_cli.pause()
    
    def logout(self):
        """Logout current user"""
        name = self.current_user[3] or self.current_user[1]
        print(f"\n👋 Goodbye, {name}!")
        print("Logging out...")
        self.current_user = None
        self.clear_screen()
    
    def run(self):
        """Main application loop"""
        self.show_welcome()
        
        try:
            while True:
                if not self.current_user:
                    # Login loop
                    choice = self.show_login_menu()
                    
                    if choice == '1':
                        self.handle_login()
                    elif choice == '2':
                        self.handle_registration()
                    elif choice == '3':
                        print("\n👋 Thank you for using Restaurant Menu Management System!")
                        print("Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice. Please try again.")
                        self.menu_cli.pause()
                else:
                    # Main application loop
                    choice = self.show_main_menu()
                    
                    if self.current_user[2] == 'admin':
                        continue_app = self.handle_admin_choice(choice)
                    else:
                        continue_app = self.handle_staff_choice(choice)
                    
                    if not continue_app:
                        # User logged out, continue to login screen
                        continue
        
        except KeyboardInterrupt:
            print("\n\n👋 Application interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            print("Please contact system administrator.")

# Test the complete application when this file is run directly
if __name__ == "__main__":
    print("🧪 Testing Complete Menu Management Application...")
    
    app = MenuManagementApp()
    
    # Quick test of functionality
    print("\n🔍 Testing menu statistics...")
    app.menu_cli.show_menu_statistics()
    
    print("\n📋 Testing menu display...")
    items = app.menu_manager.get_all_menu_items()
    app.menu_cli.display_menu_items(items[:3])  # Show first 3 items
    
    print("\n✅ Application components tested successfully!")
    print("Run app.run() to start the interactive application.")