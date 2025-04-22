import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="lab11",           # Database name
    user="postgres",            # Username
    password="12345678",        # Password
    host="localhost",           # PostgreSQL server address (localhost for local connections)
    port="5432"                 # Default PostgreSQL port
)

# Create a cursor object
cur = conn.cursor()

# Function to search for users based on a pattern
def search_users(pattern):
    query = "SELECT * FROM search_users(%s);"
    cur.execute(query, (pattern,))
    result = cur.fetchall()
    return result

# Function to insert or update a user
def insert_or_update_user(name, phone):
    query = "CALL insert_or_update_user(%s, %s);"
    cur.execute(query, (name, phone))
    conn.commit()

# Function to insert multiple users
def insert_multiple_users(user_list):
    query = "CALL insert_multiple_users(%s);"
    cur.execute(query, (user_list,))
    conn.commit()

# Function for pagination to get users with limit and offset
def get_paginated_users(limit, offset):
    query = "SELECT * FROM get_paginated_users(%s, %s);"
    cur.execute(query, (limit, offset))
    result = cur.fetchall()
    return result

# Function to delete a user by username or phone number
def delete_user(input_value):
    query = "CALL delete_user_by_username_or_phone(%s);"
    cur.execute(query, (input_value,))
    conn.commit()

# Function to display the menu and get user's choice
def display_menu():
    print("\nSelect an operation:")
    print("1. Search users by pattern")
    print("2. Insert or update user")
    print("3. Insert multiple users")
    print("4. Get paginated users")
    print("5. Delete user by username or phone")
    print("6. Exit")

# Main program loop
while True:
    display_menu()
    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        pattern = input("Enter the search pattern (name, surname, or phone): ")
        users = search_users(pattern)
        print("Users found:")
        for user in users:
            print(user)

    elif choice == '2':
        name = input("Enter user name: ")
        phone = input("Enter user phone number: ")
        insert_or_update_user(name, phone)
        print(f"User {name} with phone {phone} inserted/updated.")

    elif choice == '3':
        user_list = input("Enter a list of users (name:phone) separated by commas: ").split(',')
        insert_multiple_users(user_list)
        print("Multiple users inserted/updated.")

    elif choice == '4':
        limit = int(input("Enter the number of users to display (limit): "))
        offset = int(input("Enter the offset (starting point): "))
        paginated_users = get_paginated_users(limit, offset)
        print("Paginated users:")
        for user in paginated_users:
            print(user)

    elif choice == '5':
        input_value = input("Enter username or phone number to delete: ")
        delete_user(input_value)
        print(f"User with {input_value} deleted.")

    elif choice == '6':
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Please select a valid option.")
    
    # Ask if the user wants to perform another action
    another_action = input("Do you want to perform another action? (y/n): ")
    if another_action.lower() != 'y':
        break

# Close the cursor and connection
cur.close()
conn.close()
