#!/usr/bin/env python3
"""
Migration script to add module assignment fields to user_module_progress table
Run this script to update the existing database schema.
"""

import sqlite3
import os

def migrate_database():
    """Add new fields to user_module_progress table for module assignment"""
    
    # Database file path
    db_path = "coincraft.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Checking current user_module_progress table schema...")
        
        # Check if the table exists
        cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='user_module_progress'
        """)
        
        table_sql = cursor.fetchone()
        if table_sql:
            print("📋 Current user_module_progress table schema:")
            print(table_sql[0])
            
            # Check if new fields already exist
            cursor.execute("PRAGMA table_info(user_module_progress)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            new_fields = ['assigned_by', 'assigned_at', 'due_date', 'status']
            missing_fields = [field for field in new_fields if field not in column_names]
            
            if missing_fields:
                print(f"\n🔧 Adding missing fields: {missing_fields}")
                
                # Add new fields one by one
                for field in missing_fields:
                    if field == 'assigned_by':
                        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN assigned_by TEXT REFERENCES users(id)")
                        print("✅ Added assigned_by field")
                    elif field == 'assigned_at':
                        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN assigned_at DATETIME")
                        print("✅ Added assigned_at field")
                    elif field == 'due_date':
                        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN due_date DATETIME")
                        print("✅ Added due_date field")
                    elif field == 'status':
                        cursor.execute("ALTER TABLE user_module_progress ADD COLUMN status VARCHAR(20) DEFAULT 'assigned'")
                        print("✅ Added status field")
                
                # Commit changes
                conn.commit()
                
                print("\n✅ Successfully added all missing fields!")
                
                # Verify the changes
                cursor.execute("PRAGMA table_info(user_module_progress)")
                new_columns = cursor.fetchall()
                print("\n📋 Updated table schema:")
                for col in new_columns:
                    print(f"  {col[1]} ({col[2]})")
                
            else:
                print("✅ All required fields already exist - no migration needed")
                
        else:
            print("❌ user_module_progress table not found!")
            return False
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print("📝 This will add module assignment fields to user_module_progress table")
    print("⚠️  Make sure to backup your database before running this script!")
    
    response = input("\nDo you want to continue? (y/N): ")
    if response.lower() in ['y', 'yes']:
        if migrate_database():
            print("\n🎉 Migration completed successfully!")
        else:
            print("\n💥 Migration failed!")
    else:
        print("❌ Migration cancelled.")
