# phonebook.py

from connect import get_connection


def execute_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
    print(f"{filename} executed successfully.")


def setup_database():
    execute_sql_file("functions.sql")
    execute_sql_file("procedures.sql")


def upsert_contact(name, phone, surname=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, phone, surname))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Upsert completed for {name}.")


def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    print("\nSearch results:")
    for row in rows:
        print(row)


def get_paginated_contacts(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    print(f"\nPaginated contacts (LIMIT={limit}, OFFSET={offset}):")
    for row in rows:
        print(row)


def insert_many_contacts(names, phones):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s);", (names, phones))

    # invalid_contacts temp table-дан қате мәліметтерді аламыз
    cur.execute("SELECT * FROM invalid_contacts;")
    invalid_rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    print("\nBulk insert completed.")
    if invalid_rows:
        print("Invalid data:")
        for row in invalid_rows:
            print(row)
    else:
        print("No invalid data.")


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Deleted contact(s) by name or phone: {value}")


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    print("\nAll contacts:")
    for row in rows:
        print(row)


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Setup database")
        print("2. Upsert contact")
        print("3. Search contacts by pattern")
        print("4. Insert many contacts")
        print("5. Get paginated contacts")
        print("6. Delete contact by name or phone")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            setup_database()

        elif choice == "2":
            name = input("Enter name: ")
            surname = input("Enter surname (optional): ")
            phone = input("Enter phone: ")
            surname = surname if surname.strip() else None
            upsert_contact(name, phone, surname)

        elif choice == "3":
            pattern = input("Enter search pattern: ")
            search_contacts(pattern)

        elif choice == "4":
            n = int(input("How many contacts do you want to insert? "))
            names = []
            phones = []

            for i in range(n):
                name = input(f"Enter name {i+1}: ")
                phone = input(f"Enter phone {i+1}: ")
                names.append(name)
                phones.append(phone)

            insert_many_contacts(names, phones)

        elif choice == "5":
            limit = int(input("Enter LIMIT: "))
            offset = int(input("Enter OFFSET: "))
            get_paginated_contacts(limit, offset)

        elif choice == "6":
            value = input("Enter username or phone to delete: ")
            delete_contact(value)

        elif choice == "7":
            show_all_contacts()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()