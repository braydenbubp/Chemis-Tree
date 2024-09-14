import os
import django
from django.db import connection
import sqlite3

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemapp.settings")
django.setup()

def test_db_insertion():
    try:
        with connection.cursor() as cursor:
            # Method 1: Using Django's cursor
            try:
                cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ["test_entry_1"])
                print("Insertion successful using Django's cursor with %s placeholder")
            except Exception as e:
                print(f"Error with Django's cursor and %s placeholder: {str(e)}")

            # Method 2: Using Django's cursor with ? placeholder
            try:
                cursor.execute("INSERT INTO test_table (name) VALUES (?)", ["test_entry_2"])
                print("Insertion successful using Django's cursor with ? placeholder")
            except Exception as e:
                print(f"Error with Django's cursor and ? placeholder: {str(e)}")

            # Method 3: Using sqlite3 directly
            try:
                db_path = connection.settings_dict['NAME']
                with sqlite3.connect(db_path) as sqlite_conn:
                    sqlite_cursor = sqlite_conn.cursor()
                    sqlite_cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test_entry_3",))
                    sqlite_conn.commit()
                print("Insertion successful using sqlite3 directly")
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")

            # Verify insertions
            cursor.execute("SELECT * FROM test_table")
            result = cursor.fetchall()
            print(f"Test table contents: {result}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_db_insertion()
