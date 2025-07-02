"""
Menu CLI Interface for Restaurant Menu System
Provides user-friendly command-line interface for menu management
"""

import os
from typing import List, Tuple, Optional, Dict

class MenuCLI:
    """Command Line Interface for Menu Management"""
    
    def __init__(self, menu_manager, user_manager):
        """Initialize with menu and user managers"""
        self.menu_manager = menu_manager
        self.user_manager = user_manager
        self.current_user = None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self, title: str):
        """Show a formatted header"""
        print("\n" + "=" * 60)
        print(f"        🍽️  {title.upper()}  🍽️")
        print("=" * 60)
    
    def show_menu_header(self, subtitle: str):
        """Show menu section header"""
        print(f"\n--- {subtitle} ---")
    
    def pause(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user input"""
        input(f"\n{message}")
    
    def get_user_choice(self, prompt: str, valid_choices: List[str]) -> str:
        """Get user choice with validation"""
        while True:
            choice = input(f"{prompt}: ").strip().lower()
            if choice in valid_choices:
                return choice
            print(f"❌ Invalid choice. Please choose from: {', '.join(valid_choices)}")
    
    def get_number_input(self, prompt: str, min_val: float = None, max_val: float = None) -> Optional[float]:
        """Get number input with validation"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not value:
                    return None
                
                num = float(value)
                
                if min_val is not None and num < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                
                if max_val is not None and num > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                
                return num
                
            except ValueError:
                print("❌ Please enter a valid number")
    
    def display_categories(self, categories: List[Tuple]):
        """Display categories in a formatted table"""
        if not categories:
            print("📭 No categories found.")
            return
        
        print("\n📂 AVAILABLE CATEGORIES:")
        print("-" * 60)
        print(f"{'ID':<4} {'Name':<20} {'Status':<10} {'Description':<25}")
        print("-" * 60)
        
        for cat in categories:
            status = "✅ Active" if cat[3] else "❌ Inactive"
            description = (cat[2] or "No description")[:24]
            print(f"{cat[0]:<4} {cat[1]:<20} {status:<10} {description:<25}")
    
    def display_menu_items(self, items: List[Tuple], show_details: bool = False):
        """Display menu items in a formatted table"""
        if not items:
            print("📭 No menu items found.")
            return
        
        print(f"\n🍽️  MENU ITEMS ({len(items)} items):")
        print("=" * 100)
        
        if show_details:
            print(f"{'ID':<4} {'Name':<25} {'Category':<15} {'Price':<8} {'Prep':<6} {'Available':<10}")
        else:
            print(f"{'ID':<4} {'Name':<30} {'Category':<15} {'Price':<8} {'Available':<10}")
        
        print("=" * 100)
        
        for item in items:
            availability = "✅ Yes" if item[5] else "❌ No"
            category = (item[4] or "No Category")[:14]
            
            if show_details:
                prep_time = f"{item[6]}min" if item[6] else "N/A"
                print(f"{item[0]:<4} {item[1][:24]:<25} {category:<15} "
                      f"${item[3]:<7.2f} {prep_time:<6} {availability:<10}")
                
                # Show description if available
                if item[2]:
                    print(f"     📝 {item[2]}")
                
                # Show allergens if any
                if item[8]:
                    print(f"     ⚠️  Allergens: {item[8]}")
                
                print()  # Empty line between items
            else:
                print(f"{item[0]:<4} {item[1][:29]:<30} {category:<15} "
                      f"${item[3]:<7.2f} {availability:<10}")
    
    def get_menu_item_input(self) -> Optional[Dict]:
        """Get menu item information from user"""
        print("\n--- ➕ ADD NEW MENU ITEM ---")
        
        # Show available categories first
        categories = self.menu_manager.get_all_categories()
        if not categories:
            print("❌ No categories available. Please add categories first.")
            return None
        
        self.display_categories(categories)
        
        try:
            print("\nEnter menu item details:")
            
            name = input("Item Name: ").strip()
            if not name:
                print("❌ Item name is required.")
                return None
            
            description = input("Description: ").strip()
            
            price = self.get_number_input("Price ($)", min_val=0.01)
            if price is None:
                print("❌ Price is required.")
                return None
            
            # Get category
            category_id = self.get_number_input("Category ID", min_val=1)
            if category_id is None:
                print("❌ Category ID is required.")
                return None
            
            category_id = int(category_id)
            
            # Verify category exists
            if not any(cat[0] == category_id for cat in categories):
                print(f"❌ Category ID {category_id} does not exist.")
                return None
            
            # Optional fields
            prep_time = self.get_number_input("Preparation time (minutes, default 15)", min_val=1)
            if prep_time is None:
                prep_time = 15
            else:
                prep_time = int(prep_time)
            
            ingredients = input("Ingredients (optional): ").strip()
            allergens = input("Allergens (optional): ").strip()
            
            calories = self.get_number_input("Calories (optional)", min_val=0)
            if calories is not None:
                calories = int(calories)
            else:
                calories = 0
            
            return {
                'name': name,
                'description': description,
                'price': price,
                'category_id': category_id,
                'preparation_time': prep_time,
                'ingredients': ingredients,
                'allergens': allergens,
                'calories': calories
            }
            
        except KeyboardInterrupt:
            print("\n❌ Input cancelled.")
            return None
    
    def show_item_details(self, item: Tuple):
        """Show detailed information about a menu item"""
        print(f"\n--- 📋 ITEM DETAILS ---")
        print(f"ID: {item[0]}")
        print(f"Name: {item[1]}")
        print(f"Description: {item[2] or 'No description'}")
        print(f"Price: ${item[3]:.2f}")
        print(f"Category: {item[4] or 'No category'}")
        print(f"Available: {'✅ Yes' if item[5] else '❌ No'}")
        print(f"Preparation Time: {item[6]} minutes")
        print(f"Ingredients: {item[7] or 'Not specified'}")
        print(f"Allergens: {item[8] or 'None'}")
        print(f"Calories: {item[9] or 'Not specified'}")
    
    def search_menu_interface(self):
        """Interactive menu search interface"""
        while True:
            self.show_menu_header("🔍 SEARCH MENU ITEMS")
            
            search_term = input("Enter search term (name or description): ").strip()
            if not search_term:
                print("❌ Please enter a search term.")
                continue
            
            results = self.menu_manager.search_menu_items(search_term)
            
            if not results:
                print(f"📭 No items found matching '{search_term}'.")
            else:
                print(f"\n🔍 Search Results for '{search_term}':")
                self.display_menu_items(results)
                
                # Option to view details
                view_details = self.get_user_choice(
                    "View item details? (y/n)", ['y', 'yes', 'n', 'no']
                )
                
                if view_details in ['y', 'yes']:
                    item_id = self.get_number_input("Enter Item ID", min_val=1)
                    if item_id:
                        item = self.menu_manager.get_item_by_id(int(item_id))
                        if item:
                            self.show_item_details(item)
                        else:
                            print(f"❌ Item with ID {int(item_id)} not found.")
            
            # Continue searching?
            continue_search = self.get_user_choice(
                "Search again? (y/n)", ['y', 'yes', 'n', 'no']
            )
            
            if continue_search in ['n', 'no']:
                break
    
    def update_menu_item_interface(self):
        """Interactive interface for updating menu items"""
        self.show_menu_header("✏️ UPDATE MENU ITEM")
        
        # Show all items first
        items = self.menu_manager.get_all_menu_items()
        if not items:
            print("📭 No menu items found.")
            return
        
        self.display_menu_items(items)
        
        item_id = self.get_number_input("Enter Item ID to update", min_val=1)
        if not item_id:
            return
        
        item_id = int(item_id)
        
        # Get current item details
        current_item = self.menu_manager.get_item_by_id(item_id)
        if not current_item:
            print(f"❌ Item with ID {item_id} not found.")
            return
        
        print(f"\nCurrent details for: {current_item[1]}")
        self.show_item_details(current_item)
        
        print("\nEnter new values (press Enter to keep current value):")
        
        updates = {}
        
        # Get new values
        new_name = input(f"Name [{current_item[1]}]: ").strip()
        if new_name:
            updates['name'] = new_name
        
        new_desc = input(f"Description [{current_item[2] or 'None'}]: ").strip()
        if new_desc:
            updates['description'] = new_desc
        
        new_price = self.get_number_input(f"Price [${current_item[3]:.2f}]", min_val=0.01)
        if new_price:
            updates['price'] = new_price
        
        new_prep = self.get_number_input(f"Prep time [{current_item[6]} min]", min_val=1)
        if new_prep:
            updates['preparation_time'] = int(new_prep)
        
        # Availability toggle
        current_availability = "Available" if current_item[5] else "Not Available"
        toggle = self.get_user_choice(
            f"Availability [{current_availability}] - Toggle? (y/n)", 
            ['y', 'yes', 'n', 'no']
        )
        if toggle in ['y', 'yes']:
            updates['is_available'] = not current_item[5]
        
        if not updates:
            print("❌ No changes made.")
            return
        
        # Confirm updates
        print(f"\nUpdates to be made:")
        for key, value in updates.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        
        confirm = self.get_user_choice("Confirm updates? (y/n)", ['y', 'yes', 'n', 'no'])
        if confirm in ['y', 'yes']:
            if self.menu_manager.update_menu_item(item_id, **updates):
                print("✅ Menu item updated successfully!")
            else:
                print("❌ Failed to update menu item.")
        else:
            print("❌ Update cancelled.")
    
    def delete_menu_item_interface(self):
        """Interactive interface for deleting menu items"""
        self.show_menu_header("🗑️ DELETE MENU ITEM")
        
        # Show all items
        items = self.menu_manager.get_all_menu_items()
        if not items:
            print("📭 No menu items found.")
            return
        
        self.display_menu_items(items)
        
        item_id = self.get_number_input("Enter Item ID to delete", min_val=1)
        if not item_id:
            return
        
        item_id = int(item_id)
        
        # Get item details for confirmation
        item = self.menu_manager.get_item_by_id(item_id)
        if not item:
            print(f"❌ Item with ID {item_id} not found.")
            return
        
        print(f"\nItem to be deleted:")
        print(f"  - {item[1]} (${item[3]:.2f})")
        print(f"  - {item[2] or 'No description'}")
        
        confirm = self.get_user_choice(
            "⚠️  Are you sure you want to delete this item? (y/n)", 
            ['y', 'yes', 'n', 'no']
        )
        
        if confirm in ['y', 'yes']:
            if self.menu_manager.delete_menu_item(item_id):
                print("✅ Menu item deleted successfully!")
            else:
                print("❌ Failed to delete menu item.")
        else:
            print("❌ Deletion cancelled.")
    
    def show_menu_statistics(self):
        """Display menu statistics"""
        self.show_menu_header("📊 MENU STATISTICS")
        
        stats = self.menu_manager.get_menu_statistics()
        
        print(f"📋 Total Menu Items: {stats['total_items']}")
        print(f"✅ Available Items: {stats['available_items']}")
        print(f"❌ Unavailable Items: {stats['unavailable_items']}")
        print(f"📂 Total Categories: {stats['total_categories']}")
        print(f"💰 Average Price: ${stats['average_price']:.2f}")

# Test the menu CLI when this file is run directly
if __name__ == "__main__":
    print("Testing Menu CLI...")
    
    # Import required modules
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent.parent))
    
    from src.restaurant_menu.models.database import DatabaseManager
    from src.restaurant_menu.managers.menu_manager import MenuManager
    from src.restaurant_menu.managers.user_manager import UserManager
    
    # Create instances
    db = DatabaseManager()
    menu_manager = MenuManager(db)
    user_manager = UserManager(db)
    menu_cli = MenuCLI(menu_manager, user_manager)
    
    # Test display functions
    print("\n🧪 Testing category display...")
    categories = menu_manager.get_all_categories()
    menu_cli.display_categories(categories)
    
    print("\n🧪 Testing menu items display...")
    items = menu_manager.get_all_menu_items()
    menu_cli.display_menu_items(items, show_details=True)
    
    print("\n🧪 Testing statistics display...")
    menu_cli.show_menu_statistics()
    
    print("\n✅ Menu CLI testing completed!")