#!/usr/bin/env python3
"""
Restaurant Menu Management System
Main Entry Point

This is the starting point of our application.
Run this file to start the Restaurant Menu System.
"""

import sys
from pathlib import Path

# Add src directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main function - entry point of the application"""
    try:
        # Import and run the complete menu application
        from restaurant_menu.menu_app import MenuManagementApp
        
        # Create and run the application
        app = MenuManagementApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        print("Make sure all files are created correctly.")
        print("\nProject structure should be:")
        print("  src/restaurant_menu/models/database.py")
        print("  src/restaurant_menu/managers/user_manager.py")
        print("  src/restaurant_menu/managers/menu_manager.py")
        print("  src/restaurant_menu/ui/menu_cli.py")
        print("  src/restaurant_menu/menu_app.py")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()