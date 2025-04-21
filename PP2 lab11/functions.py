import psycopg2
import csv

# ----------------------------
# Database Connection
# ----------------------------
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="lab10.2",
        user="postgres",
        password="12345678"
    )

# ----------------------------
# Call search by pattern function
# ----------------------------
def call_search_pattern():
    conn = create_connection()
    cur = conn.cursor()
    pattern = input("Enter pattern to search (name or phone): ")
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()
    print("\n📋 Matched Records:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    cur.close()
    conn.close()

# ----------------------------
# Call insert or update single user
# ----------------------------
def call_insert_or_update():
    conn = create_connection()
    cur = conn.cursor()
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    print("✅ Inserted/Updated successfully!")
    cur.close()
    conn.close()

# ----------------------------
# Insert many users via loop with validation
# ----------------------------
def call_insert_many():
    conn = create_connection()
    cur = conn.cursor()
    n = int(input("How many users to insert? "))
    names = []
    phones = []
    for _ in range(n):
        names.append(input("Enter name: "))
        phones.append(input("Enter phone: "))

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    cur.execute("SELECT insert_many_users(%s, %s)", (names, phones))
    invalid_data = cur.fetchone()[0]
    if invalid_data:
        print("❌ Invalid entries:", invalid_data)
    else:
        print("✅ All users inserted!")
    conn.commit()
    cur.close()
    conn.close()

# ----------------------------
# Pagination query
# ----------------------------
def call_paginated_query():
    conn = create_connection()
    cur = conn.cursor()
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM get_paginated_users(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    print("\n📋 Paginated Results:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    cur.close()
    conn.close()

# ----------------------------
# Call delete by name or phone
# ----------------------------
def call_delete():
    conn = create_connection()
    cur = conn.cursor()
    print("Delete by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Your choice: ")
    name = phone = None
    if choice == "1":
        name = input("Enter name to delete: ")
    elif choice == "2":
        phone = input("Enter phone to delete: ")
    else:
        print("❌ Invalid option")
        return
    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()
    print("✅ Deleted successfully!")
    cur.close()
    conn.close()

# ----------------------------
# Main Menu
# ----------------------------
def main():
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("4. Pagination query")
        print("5. Delete user")
        print("6. Exit")

        option = input("Choose option: ")

        if option == "1":
            call_search_pattern()
        elif option == "2":
            call_insert_or_update()
        elif option == "3":
            call_insert_many()
        elif option == "4":
            call_paginated_query()
        elif option == "5":
            call_delete()
        elif option == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid input. Try again.")

if __name__ == "__main__":
    main()