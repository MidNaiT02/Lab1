import psycopg2
import unicodedata

# Set up database connection
connection = psycopg2.connect(
    host="localhost",
    database="lab10.2",
    user="postgres",
    password="12345678"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Function to sanitize input (remove non-ASCII characters)
def sanitize_input(input_string):
    # Normalize the input string and remove non-ASCII characters
    return ''.join(c for c in unicodedata.normalize('NFKD', input_string) if unicodedata.category(c) != 'Mn')

# 1. Call the `find_contacts_by_pattern` function
def find_contacts(pattern):
    cursor.execute("SELECT * FROM find_contacts_by_pattern(%s);", (pattern,))
    results = cursor.fetchall()
    return results

# 2. Call the `add_or_update_contact` procedure
def add_or_update_contact(name, phone):
    cursor.execute("CALL add_or_update_contact(%s, %s);", (name, phone))
    connection.commit()

# 3. Call the `bulk_insert_contacts` procedure
def bulk_insert_contacts(users_list):
    for user in users_list:
        user_name, user_phone = user.split(",")  # Assuming the format 'name,phone'
        cursor.execute("CALL add_or_update_contact(%s, %s);", (user_name, user_phone))
    connection.commit()

# 4. Call the `paginate_contacts_query` function
def paginate_contacts(limit, offset):
    cursor.execute("SELECT * FROM paginate_contacts_query(%s, %s);", (limit, offset))
    results = cursor.fetchall()
    return results

# 5. Call the `remove_contact_by_identifier` procedure
def remove_contact(identifier):
    cursor.execute("CALL remove_contact_by_identifier(%s);", (identifier,))
    connection.commit()

# Function to display the menu
def show_menu():
    print("\nChoose an option by number:")
    print("1. Search contacts by pattern")
    print("2. Add or update a contact")
    print("3. Bulk insert contacts")
    print("4. Paginate contacts")
    print("5. Remove contact by username or phone")
    print("6. Exit")

# Function to handle user input for choosing options
def user_input():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == "1":
                pattern = input("Enter the pattern (name/phone to search): ")
                pattern = sanitize_input(pattern)  # Sanitize input to remove any invalid characters
                contacts = find_contacts(pattern)
                for contact in contacts:
                    print(contact)

            elif choice == "2":
                name = input("Enter the name of the contact: ")
                name = sanitize_input(name)  # Sanitize input for name
                phone = input("Enter the phone number: ")
                phone = sanitize_input(phone)  # Sanitize input for phone
                add_or_update_contact(name, phone)
                print(f"Contact {name} has been added or updated.")

            elif choice == "3":
                users_input = input("Enter users in the format 'name,phone' separated by commas (e.g., John,1234567890): ")
                users_list = users_input.split(",")  # This splits by commas, adjust if list of names/phones is needed
                bulk_insert_contacts(users_list)
                print("Bulk insert completed.")

            elif choice == "4":
                limit = int(input("Enter the number of contacts to fetch per page: "))
                offset = int(input("Enter the offset (page number * limit): "))
                contacts_page = paginate_contacts(limit, offset)
                for contact in contacts_page:
                    print(contact)

            elif choice == "5":
                identifier = input("Enter the username or phone number of the contact to remove: ")
                identifier = sanitize_input(identifier)  # Sanitize identifier
                remove_contact(identifier)
                print(f"Contact with identifier {identifier} has been removed.")

            elif choice == "6":
                print("Exiting...")
                break  # Exit the loop and close the program

            else:
                print("Invalid choice, please select a valid option (1-6).")
        except Exception as e:
            print(f"Error occurred: {e}")

# Start the program
user_input()

# Close the cursor and connection when done
cursor.close()
connection.close()
