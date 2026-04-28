import csv
from TSIS1.connect import get_connection


def create_table():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE
            )
        """)

        conn.commit()
        cur.close()
        print("Table created successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while creating table:", e)

    finally:
        if conn:
            conn.close()


def insert_from_console():
    conn = None
    try:
        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )

        conn.commit()
        cur.close()
        print("Contact added successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while inserting contact:", e)

    finally:
        if conn:
            conn.close()


def insert_from_csv(filename="contacts.csv"):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                phone = row["phone"].strip()

                try:
                    cur.execute(
                        "INSERT INTO phonebook (name, phone) VALUES (%s, %s) "
                        "ON CONFLICT (phone) DO NOTHING",
                        (name, phone)
                    )
                except Exception as inner_error:
                    print("Skipped row:", row, "| Error:", inner_error)
                    conn.rollback()

        conn.commit()
        cur.close()
        print("CSV data imported successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while importing CSV:", e)

    finally:
        if conn:
            conn.close()


def update_contact():
    conn = None
    try:
        search_name = input("Enter the contact name to update: ").strip()
        choice = input("What do you want to update? (1-name, 2-phone): ").strip()

        conn = get_connection()
        cur = conn.cursor()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            cur.execute(
                "UPDATE phonebook SET name = %s WHERE name = %s",
                (new_name, search_name)
            )
        elif choice == "2":
            new_phone = input("Enter new phone: ").strip()
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE name = %s",
                (new_phone, search_name)
            )
        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Updated rows:", cur.rowcount)
        cur.close()

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while updating contact:", e)

    finally:
        if conn:
            conn.close()


def query_all_contacts():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, phone FROM phonebook ORDER BY id")
        rows = cur.fetchall()

        if rows:
            print("\nAll contacts:")
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

        cur.close()

    except Exception as e:
        print("Error while querying contacts:", e)

    finally:
        if conn:
            conn.close()


def query_by_name():
    conn = None
    try:
        keyword = input("Enter name keyword: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s",
            (f"%{keyword}%",)
        )

        rows = cur.fetchall()

        if rows:
            print("\nMatching contacts:")
            for row in rows:
                print(row)
        else:
            print("No matching contacts found.")

        cur.close()

    except Exception as e:
        print("Error while searching by name:", e)

    finally:
        if conn:
            conn.close()


def query_by_phone_prefix():
    conn = None
    try:
        prefix = input("Enter phone prefix: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, phone FROM phonebook WHERE phone LIKE %s",
            (prefix + "%",)
        )

        rows = cur.fetchall()

        if rows:
            print("\nMatching contacts:")
            for row in rows:
                print(row)
        else:
            print("No matching contacts found.")

        cur.close()

    except Exception as e:
        print("Error while searching by phone prefix:", e)

    finally:
        if conn:
            conn.close()


def delete_contact():
    conn = None
    try:
        choice = input("Delete by: 1-name, 2-phone: ").strip()

        conn = get_connection()
        cur = conn.cursor()

        if choice == "1":
            name = input("Enter name: ").strip()
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        elif choice == "2":
            phone = input("Enter phone: ").strip()
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Deleted rows:", cur.rowcount)
        cur.close()

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error while deleting contact:", e)

    finally:
        if conn:
            conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update contact")
        print("5. Show all contacts")
        print("6. Search by name")
        print("7. Search by phone prefix")
        print("8. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_all_contacts()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_phone_prefix()
        elif choice == "8":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()