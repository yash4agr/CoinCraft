#!/usr/bin/env python3
"""
Migration script to remove unique constraint from classes.class_code
Run this script to update the existing database schema.
"""

import sqlite3
import os

def migrate_database():
    """Remove unique constraint from classes.class_code column"""
    
    # Database file path
    db_path = "coincraft.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Checking current database schema...")
        
        # Check if the unique constraint exists
        cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='classes'
        """)
        
        table_sql = cursor.fetchone()
        if table_sql:
            print("📋 Current classes table schema:")
            print(table_sql[0])
            
            # Check if unique constraint exists on class_code
            if "UNIQUE" in table_sql[0] and "class_code" in table_sql[0]:
                print("\n🔧 Removing unique constraint from class_code...")
                
                # Create new table without unique constraint
                cursor.execute("""
                    CREATE TABLE classes_new (
                        id TEXT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        teacher_id TEXT,
                        description TEXT,
                        class_code VARCHAR(20),
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME
                    )
                """)
                
                # Copy data from old table
                cursor.execute("""
                    INSERT INTO classes_new 
                    SELECT id, name, teacher_id, description, class_code, is_active, created_at 
                    FROM classes
                """)
                
                # Drop old table
                cursor.execute("DROP TABLE classes")
                
                # Rename new table
                cursor.execute("ALTER TABLE classes_new RENAME TO classes")
                
                # Commit changes
                conn.commit()
                
                print("✅ Successfully removed unique constraint from class_code!")
                
                # Verify the change
                cursor.execute("""
                    SELECT sql FROM sqlite_master 
                    WHERE type='table' AND name='classes'
                """)
                
                new_table_sql = cursor.fetchone()
                print("\n📋 New classes table schema:")
                print(new_table_sql[0])
                
            else:
                print("✅ No unique constraint found on class_code - no migration needed")
                
        else:
            print("❌ Classes table not found!")
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
    print("📝 This will remove the unique constraint from classes.class_code")
    print("⚠️  Make sure to backup your database before running this script!")
    
    response = input("\nDo you want to continue? (y/N): ")
    if response.lower() in ['y', 'yes']:
        if migrate_database():
            print("\n🎉 Migration completed successfully!")
        else:
            print("\n💥 Migration failed!")
    else:
        print("❌ Migration cancelled.")
