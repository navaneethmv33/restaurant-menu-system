"""
Menu Manager for Restaurant Menu System
Handles all menu item CRUD operations (Create, Read, Update, Delete)
"""

import sqlite3
from typing import List, Tuple, Optional, Dict

class MenuManager:
    """Handles menu item operations and category management"""
    
    def __init__(self, db_manager):
        """Initialize with a database manager instance"""
        self.db = db_manager
        print("🍽️  Menu Manager initialized")
    
    # ========== MENU ITEM OPERATIONS ==========
    
    def add_menu_item(self, name: str, description: str, price: float,
                     category_id: int, preparation_time: int = 15,
                     ingredients: str = "", allergens: str = "",
                     calories: int = 0) -> bool:
        """
        Add a new menu item
        Returns True if successful, False if failed
        """
        print(f"➕ Adding menu item: {name}")
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO menu_items (name, description, price, category_id,
                                      preparation_time, ingredients, allergens, calories)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, price, category_id, preparation_time,
                  ingredients, allergens, calories))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Menu item '{name}' added successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Failed to add menu item '{name}': {e}")
            return False
    
    def get_all_menu_items(self) -> List[Tuple]:
        """Get all menu items with their category names"""
        print("📋 Fetching all menu items...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.item_id, m.name, m.description, m.price, c.name as category,
                   m.is_available, m.preparation_time, m.ingredients, m.allergens, m.calories
            FROM menu_items m
            LEFT JOIN categories c ON m.category_id = c.category_id
            ORDER BY c.name, m.name
        ''')
        
        result = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(result)} menu items")
        return result
    
    def get_menu_by_category(self, category_id: int) -> List[Tuple]:
        """Get menu items for a specific category"""
        print(f"📂 Fetching menu items for category ID: {category_id}")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT item_id, name, description, price, is_available,
                   preparation_time, ingredients, allergens, calories
            FROM menu_items
            WHERE category_id = ? AND is_available = 1
            ORDER BY name
        ''', (category_id,))
        
        result = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(result)} items in category")
        return result
    
    def search_menu_items(self, search_term: str) -> List[Tuple]:
        """Search menu items by name or description"""
        print(f"🔍 Searching for: '{search_term}'")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT m.item_id, m.name, m.description, m.price, c.name as category,
                   m.is_available, m.preparation_time, m.ingredients, m.allergens, m.calories
            FROM menu_items m
            LEFT JOIN categories c ON m.category_id = c.category_id
            WHERE (m.name LIKE ? OR m.description LIKE ?) AND m.is_available = 1
            ORDER BY m.name
        ''', (search_pattern, search_pattern))
        
        result = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(result)} matching items")
        return result
    
    def update_menu_item(self, item_id: int, **kwargs) -> bool:
        """
        Update menu item information
        kwargs can include: name, description, price, category_id, 
        preparation_time, ingredients, allergens, calories, is_available
        """
        print(f"✏️ Updating menu item ID: {item_id}")
        
        if not kwargs:
            print("❌ No update data provided")
            return False
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if value is not None:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                print("❌ No valid update fields provided")
                return False
            
            # Add updated_at timestamp
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(item_id)
            
            query = f"UPDATE menu_items SET {', '.join(updates)} WHERE item_id = ?"
            
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Menu item {item_id} updated successfully!")
                conn.close()
                return True
            else:
                print(f"❌ Menu item {item_id} not found")
                conn.close()
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Failed to update menu item {item_id}: {e}")
            return False
    
    def delete_menu_item(self, item_id: int) -> bool:
        """Delete a menu item (only if not in any orders)"""
        print(f"🗑️ Attempting to delete menu item ID: {item_id}")
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # For now, just delete directly
            # TODO: In a full system, check for existing orders first
            cursor.execute("DELETE FROM menu_items WHERE item_id = ?", (item_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Menu item {item_id} deleted successfully!")
                conn.close()
                return True
            else:
                print(f"❌ Menu item {item_id} not found")
                conn.close()
                return False
                
        except sqlite3.Error as e:
            print(f"❌ Failed to delete menu item {item_id}: {e}")
            return False
    
    def get_item_by_id(self, item_id: int) -> Optional[Tuple]:
        """Get a specific menu item by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.item_id, m.name, m.description, m.price, c.name as category,
                   m.is_available, m.preparation_time, m.ingredients, m.allergens, m.calories
            FROM menu_items m
            LEFT JOIN categories c ON m.category_id = c.category_id
            WHERE m.item_id = ?
        ''', (item_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    # ========== CATEGORY OPERATIONS ==========
    
    def add_category(self, name: str, description: str = "") -> bool:
        """Add a new category"""
        print(f"📂 Adding category: {name}")
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO categories (name, description)
                VALUES (?, ?)
            ''', (name, description))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Category '{name}' added successfully!")
            return True
            
        except sqlite3.IntegrityError:
            print(f"❌ Category '{name}' already exists!")
            return False
        except sqlite3.Error as e:
            print(f"❌ Failed to add category '{name}': {e}")
            return False
    
    def get_all_categories(self) -> List[Tuple]:
        """Get all categories"""
        print("📂 Fetching all categories...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category_id, name, description, is_active
            FROM categories
            ORDER BY name
        ''')
        
        result = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(result)} categories")
        return result
    
    def get_category_by_id(self, category_id: int) -> Optional[Tuple]:
        """Get a specific category by ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category_id, name, description, is_active
            FROM categories
            WHERE category_id = ?
        ''', (category_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    # ========== UTILITY METHODS ==========
    
    def get_menu_statistics(self) -> Dict[str, int]:
        """Get statistics about the menu"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Total items
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        total_items = cursor.fetchone()[0]
        
        # Available items
        cursor.execute("SELECT COUNT(*) FROM menu_items WHERE is_available = 1")
        available_items = cursor.fetchone()[0]
        
        # Total categories
        cursor.execute("SELECT COUNT(*) FROM categories WHERE is_active = 1")
        total_categories = cursor.fetchone()[0]
        
        # Average price
        cursor.execute("SELECT AVG(price) FROM menu_items WHERE is_available = 1")
        avg_price = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_items': total_items,
            'available_items': available_items,
            'unavailable_items': total_items - available_items,
            'total_categories': total_categories,
            'average_price': round(avg_price, 2)
        }

# Test the menu manager when this file is run directly
if __name__ == "__main__":
    print("Testing Menu Manager...")
    
    # Import required modules
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent.parent))
    
    from src.restaurant_menu.models.database import DatabaseManager
    
    # Create instances
    db = DatabaseManager()
    menu_manager = MenuManager(db)
    
    print("\n🧪 Testing category operations...")
    
    # Test getting categories
    categories = menu_manager.get_all_categories()
    print(f"Categories found: {len(categories)}")
    for cat in categories:
        print(f"  - {cat[1]}: {cat[2]}")
    
    print("\n🧪 Testing adding menu items...")
    
    # Add some sample menu items
    sample_items = [
        ("Caesar Salad", "Fresh romaine lettuce with parmesan cheese", 12.99, 5, 10),
        ("Grilled Chicken", "Juicy grilled chicken breast", 18.99, 2, 20),
        ("Chocolate Cake", "Rich chocolate cake with vanilla ice cream", 8.99, 3, 5),
        ("Fresh Coffee", "Freshly brewed house coffee", 3.99, 4, 3),
    ]
    
    for name, desc, price, cat_id, prep_time in sample_items:
        success = menu_manager.add_menu_item(name, desc, price, cat_id, prep_time)
        if not success:
            print(f"  (Item '{name}' might already exist)")
    
    print("\n🧪 Testing menu retrieval...")
    
    # Get all menu items
    all_items = menu_manager.get_all_menu_items()
    print(f"\nAll menu items ({len(all_items)}):")
    for item in all_items:
        print(f"  {item[0]}. {item[1]} - ${item[3]:.2f} ({item[4]})")
    
    print("\n🧪 Testing search functionality...")
    
    # Test search
    search_results = menu_manager.search_menu_items("chicken")
    print(f"\nSearch results for 'chicken' ({len(search_results)}):")
    for item in search_results:
        print(f"  {item[0]}. {item[1]} - ${item[3]:.2f}")
    
    print("\n🧪 Testing statistics...")
    
    # Get statistics
    stats = menu_manager.get_menu_statistics()
    print(f"\nMenu Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n✅ Menu Manager testing completed!")