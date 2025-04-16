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
# Insert from Console
# ----------------------------
def insert_from_console():
    conn = create_connection()
    cur = conn.cursor()
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("✅ Inserted successfully!")
    cur.close()
    conn.close()

# ----------------------------
# Insert from CSV
# ----------------------------
def insert_from_csv(filename):
    conn = create_connection()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("✅ CSV data inserted!")
    cur.close()
    conn.close()

# ----------------------------
# Update Entry
# ----------------------------
def update_entry():
    conn = create_connection()
    cur = conn.cursor()
    name = input("Enter the name of the user to update: ")
    choice = input("Update (1) Name or (2) Phone? ")
    if choice == "1":
        new_name = input("Enter new name: ")
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, name))
    elif choice == "2":
        new_phone = input("Enter new phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    else:
        print("❌ Invalid choice")
        return
    conn.commit()
    print("✅ Updated successfully!")
    cur.close()
    conn.close()

# ----------------------------
# Query Data
# ----------------------------
def query_data():
    conn = create_connection()
    cur = conn.cursor()
    print("Search options:")
    print("1. All entries")
    print("2. By name")
    print("3. By phone")
    choice = input("Choose option: ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        name = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
    elif choice == "3":
        phone = input("Enter phone to search: ")
        cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{phone}%",))
    else:
        print("❌ Invalid option")
        return

    rows = cur.fetchall()
    print("\n📋 PhoneBook Records:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    print("----------------------")
    cur.close()
    conn.close()

# ----------------------------
# Delete Entry
# ----------------------------
def delete_entry():
    conn = create_connection()
    cur = conn.cursor()
    print("Delete by:")
    print("1. Name")
    print("2. Phone")
    choice = input("Your choice: ")
    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("❌ Invalid option")
        return
    conn.commit()
    print("✅ Deleted successfully!")
    cur.close()
    conn.close()

# ----------------------------
# View All Data ()
# ----------------------------
def view_all():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print("\n📋 All PhoneBook Records:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    print("----------------------")
    cur.close()
    conn.close()

# ----------------------------
# Main Menu
# ----------------------------
def main():
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update entry")
        print("4. Search data")
        print("5. Delete entry")
        print("6. View all data")
        print("7. Exit")

        option = input("Choose option: ")

        if option == "1":
            insert_from_console()
        elif option == "2":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif option == "3":
            update_entry()
        elif option == "4":
            query_data()
        elif option == "5":
            delete_entry()
        elif option == "6":
            view_all()
        elif option == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid input. Try again.")

if __name__ == "__main__":
    main()
