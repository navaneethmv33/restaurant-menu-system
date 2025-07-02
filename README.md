🍽️ Restaurant Menu Management System
📋 Table of Contents
Features
Quick Start
Installation
Project Structure
Usage Guide
Database Schema
Screenshots
✨ Features
🔐 Authentication System
Role-based Access Control: Admin and Staff roles with different permissions
User Registration: Add new staff members to the system
Session Management: Secure login/logout functionality
📊 Menu Management (CRUD Operations)
Create: Add new menu items with detailed information
Read: View all menu items, search, and browse by category
Update: Modify menu item details, prices, and availability
Delete: Remove menu items from the system
📂 Category Management
Organize Menu: Group items into logical categories
Category CRUD: Add, view, and manage food categories
Category Browsing: Filter menu items by category
📈 Reports & Analytics
Menu Statistics: Track total items, availability, and pricing
User Management: View all registered users (Admin only)
Data Insights: Average pricing and category distribution
💻 User-Friendly Interface
Clean CLI: Intuitive command-line interface with emojis
Input Validation: Comprehensive error handling and validation
Progress Indicators: Clear feedback for all operations
Cross-Platform: Works on Windows, macOS, and Linux
🚀 Quick Start
Prerequisites
Python 3.7 or higher
SQLite3 (included with Python)
Terminal/Command Prompt access
Installation & Running
Option 1: Using the Installer (Recommended)

# Download and run the installer
python install.py
Option 2: Manual Setup

# Clone the repository
git clone https://github.com/yourusername/restaurant-menu-system.git
cd restaurant-menu-system

# Run the application
python main.py
Option 3: Quick Run Scripts

# Windows
run.bat

# Linux/macOS
./run.sh
Default Login Credentials
Role	Username	Password	Access Level
👑 Admin	admin	admin123	Full system access
👨‍🍳 Staff	staff	staff123	Menu viewing & search
📦 Installation
Automated Installation
The project includes an intelligent installer that sets up everything automatically:

Download the installer: install.py
Run the installer:
python install.py
Follow the prompts - the installer will:
Check system requirements
Create project structure
Set up database with sample data
Create run scripts
Verify installation
Manual Installation
If you prefer to set up manually:

# Create project directory
mkdir restaurant-menu-system
cd restaurant-menu-system

# Create directory structure
mkdir -p src/restaurant_menu/{models,managers,ui}
mkdir -p {data,logs,backups,docs,config}

# Create __init__.py files
touch src/__init__.py
touch src/restaurant_menu/__init__.py
touch src/restaurant_menu/{models,managers,ui}/__init__.py

# Copy source files (database.py, user_manager.py, etc.)
# Run the application
python main.py
📁 Project Structure
restaurant-menu-system/
├── 📄 README.md                    # Project documentation
├── 📄 main.py                      # Application entry point
├── 📄 install.py                   # Automated installer
├── 📄 requirements.txt             # Python dependencies
├── 📄 run.bat                      # Windows run script
├── 📄 run.sh                       # Unix/Linux run script
├── 📁 src/                         # Source code
│   └── 📁 restaurant_menu/
│       ├── 📄 menu_app.py          # Main application class
│       ├── 📁 models/
│       │   └── 📄 database.py      # Database operations
│       ├── 📁 managers/
│       │   ├── 📄 user_manager.py  # User authentication
│       │   └── 📄 menu_manager.py  # Menu CRUD operations
│       └── 📁 ui/
│           └── 📄 menu_cli.py      # Command-line interface
├── 📁 data/                        # Database storage
│   └── 📄 restaurant_menu.db       # SQLite database file
├── 📁 logs/                        # Application logs
├── 📁 backups/                     # Database backups
├── 📁 docs/                        # Additional documentation
└── 📁 config/                      # Configuration files
📖 Usage Guide
🔐 Getting Started
Start the application:

python main.py
Login with default credentials:

Admin: admin / admin123
Staff: staff / staff123
Explore the features based on your role!

👑 Admin Functions
Menu Management
View All Items: Browse the complete menu with details
Add New Items: Create menu items with:
Name and description
Price and category
Preparation time
Ingredients and allergens
Calorie information
Update Items: Modify any menu item details
Delete Items: Remove items from the menu
Search Items: Find items by name or description
Category Management
View Categories: See all menu categories
Add Categories: Create new food categories
Organize Menu: Group items logically
System Administration
View All Users: Monitor staff accounts
Menu Statistics: Track system metrics
User Registration: Add new staff members
👨‍🍳 Staff Functions
Menu Operations
View Menu: Browse all available items
Search Menu: Find specific items quickly
Browse by Category: Filter items by food type
View Statistics: Check menu overview
🔍 Search Features
The system provides powerful search capabilities:

Name Search: Find items by partial name matching
Description Search: Search within item descriptions
Category Filter: Browse items within specific categories
Real-time Results: Instant feedback as you search
📊 Sample Data
The system comes with sample data including:

Categories:

🥗 Appetizers
🍖 Main Courses
🍰 Desserts
🥤 Beverages
🥬 Salads
Sample Menu Items:

Caesar Salad ($12.99)
Grilled Chicken ($18.99)
Chocolate Cake ($8.99)
Fresh Coffee ($3.99)
🗄️ Database Schema
Entity Relationship Diagram
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    Users    │     │  Categories  │     │ Menu Items  │
├─────────────┤     ├──────────────┤     ├─────────────┤
│ user_id (PK)│     │category_id(PK│     │ item_id (PK)│
│ username    │     │ name         │────▶│ name        │
│ password_hash│     │ description  │     │ description │
│ role        │     │ is_active    │     │ price       │
│ full_name   │     │ created_at   │     │ category_id │
│ email       │     └──────────────┘     │ is_available│
│ created_at  │                          │ prep_time   │
└─────────────┘                          │ ingredients │
                                         │ allergens   │
                                         │ calories    │
                                         │ created_at  │
                                         │ updated_at  │
                                         └─────────────┘
Table Definitions
Users Table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'staff',
    full_name TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Categories Table
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Menu Items Table
CREATE TABLE menu_items (
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
);
Relationships
Categories → Menu Items: One-to-Many (One category can have multiple items)
Users → System Access: Role-based permissions (Admin/Staff)
📸 Screenshots
Login Screen
============================================================
        🍽️  RESTAURANT MENU MANAGEMENT SYSTEM  🍽️
============================================================
             Welcome to your digital menu!
============================================================

--- 🔐 AUTHENTICATION ---
1. 🔑 Login
2. 📝 Register New Staff
3. 🚪 Exit
------------------------------
Enter your choice (1-3):
Admin Dashboard
--- 👑 ADMIN PANEL - System Administrator ---
📋 MENU MANAGEMENT:
  1. 👀 View All Menu Items
  2. ➕ Add New Menu Item
  3. ✏️  Update Menu Item
  4. 🗑️  Delete Menu Item
  5. 🔍 Search Menu Items

📂 CATEGORY MANAGEMENT:
  6. 📂 View Categories
  7. ➕ Add New Category

📊 REPORTS & INFO:
  8. 📊 Menu Statistics
  9. 👥 View All Users

🔧 SYSTEM:
  10. 🚪 Logout
--------------------------------------------------
Menu Display
🍽️  MENU ITEMS (6 items):
====================================================================================================
ID   Name                     Category        Price    Available 
====================================================================================================
1    Caesar Salad            Salads          $12.99   ✅ Yes    
2    Grilled Chicken         Main Courses    $18.99   ✅ Yes    
3    Chocolate Cake          Desserts        $8.99    ✅ Yes    
4    Fresh Coffee            Beverages       $3.99    ✅ Yes    
5    Margherita Pizza        Main Courses    $18.99   ✅ Yes    
6    Chicken Wings           Appetizers      $14.99   ✅ Yes    
