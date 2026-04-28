import csv
import json
import psycopg2
from connect import get_connection

# TSIS1 PhoneBook Extended
# Features: groups, many phones, email, birthday, JSON/CSV, search, sort, pagination


# ---------- HELPERS ----------
def get_group_id(cur, group_name):
    # Create group if needed and return its id
    cur.execute(
        "INSERT INTO groups(name) VALUES(%s) ON CONFLICT DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    return cur.fetchone()[0]


def add_contact(cur, name, email, birthday, group_name):
    # Add one contact
    group_id = get_group_id(cur, group_name)

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES(%s, %s, %s, %s)
        ON CONFLICT(name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
    """, (name, email, birthday, group_id))


def add_phone_python(cur, name, phone, phone_type):
    # Add phone using SQL procedure
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))


# ---------- SAMPLE DATA ----------
def insert_sample_data():
    # Insert 5 contacts for testing
    conn = get_connection()
    cur = conn.cursor()

    sample_contacts = [
        ("Dias", "dias@gmail.com", "2007-09-17", "Friend", "87001234567", "mobile"),
        ("Ali", "ali@mail.com", "2006-05-10", "Family", "87001111111", "home"),
        ("Sara", "sara@gmail.com", "2005-03-22", "Work", "87002222222", "work"),
        ("John", "john@gmail.com", "2004-11-01", "Friend", "87003333333", "mobile"),
        ("Anna", "anna@mail.com", "2003-07-15", "Other", "87004444444", "mobile")
    ]

    for name, email, birthday, group_name, phone, phone_type in sample_contacts:
        add_contact(cur, name, email, birthday, group_name)

        # Avoid duplicate phone
        cur.execute("""
            SELECT p.id
            FROM phones p
            JOIN contacts c ON p.contact_id = c.id
            WHERE c.name=%s AND p.phone=%s
        """, (name, phone))

        if cur.fetchone() is None:
            add_phone_python(cur, name, phone, phone_type)

    conn.commit()
    cur.close()
    conn.close()
    print("5 sample contacts inserted.")


# ---------- SHOW CONTACTS ----------
def show_contacts(sort_by="name"):
    # Show contacts with selected sorting
    conn = get_connection()
    cur = conn.cursor()

    allowed_sort = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }

    order_column = allowed_sort.get(sort_by, "c.name")

    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_column}
    """)

    rows = cur.fetchall()

    for row in rows:
        print(f"Name: {row[0]} | Email: {row[1]} | Birthday: {row[2]} | Group: {row[3]} | Added: {row[4]}")

    cur.close()
    conn.close()


def show_contact_phones(contact_name):
    # Show all phone numbers of one contact
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.phone, p.type
        FROM phones p
        JOIN contacts c ON p.contact_id = c.id
        WHERE c.name=%s
    """, (contact_name,))

    rows = cur.fetchall()

    print(f"Phones for {contact_name}:")
    for phone, phone_type in rows:
        print(f"{phone} ({phone_type})")

    cur.close()
    conn.close()


# ---------- FILTER AND SEARCH ----------
def filter_by_group(group_name):
    # Show contacts from one group
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """, (group_name,))

    for row in cur.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    cur.close()
    conn.close()


def search_by_email(text):
    # Search contacts by email part
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name
    """, (f"%{text}%",))

    for row in cur.fetchall():
        print(f"{row[0]} | {row[1]}")

    cur.close()
    conn.close()


def search_all_fields(text):
    # Search by name, email or phone using DB function
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (text,))

    for row in cur.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} ({row[5]})")

    cur.close()
    conn.close()


# ---------- PAGINATION ----------
def pagination_console():
    # Navigate contacts page by page
    conn = get_connection()
    cur = conn.cursor()

    limit = 2
    offset = 0

    while True:
        cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

        cmd = input("next / prev / quit: ").lower()

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break
        else:
            print("Unknown command.")

    cur.close()
    conn.close()


# ---------- JSON EXPORT ----------
def export_to_json(filename="contacts_export.json"):
    # Export contacts with phones to JSON
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)

    contacts = []

    for contact_id, name, email, birthday, group_name in cur.fetchall():
        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id=%s
        """, (contact_id,))

        phones = [
            {"phone": phone, "type": phone_type}
            for phone, phone_type in cur.fetchall()
        ]

        contacts.append({
            "name": name,
            "email": email,
            "birthday": str(birthday),
            "group": group_name,
            "phones": phones
        })

    with open(filename, "w") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()
    print(f"Exported to {filename}")


# ---------- JSON IMPORT ----------
def import_from_json(filename="contacts.json"):
    # Import contacts from JSON with duplicate handling
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r") as file:
        contacts = json.load(file)

    for item in contacts:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip or overwrite? ").lower()

            if choice == "skip":
                continue

        add_contact(
            cur,
            item["name"],
            item.get("email"),
            item.get("birthday"),
            item.get("group", "Other")
        )

        for phone in item.get("phones", []):
            cur.execute("""
                SELECT p.id
                FROM phones p
                JOIN contacts c ON p.contact_id = c.id
                WHERE c.name=%s AND p.phone=%s
            """, (name, phone["phone"]))

            if cur.fetchone() is None:
                add_phone_python(cur, name, phone["phone"], phone["type"])

    conn.commit()
    cur.close()
    conn.close()
    print("JSON import finished.")


# ---------- CSV IMPORT ----------
def import_from_csv(filename="contacts.csv"):
    # Import new fields from CSV
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            add_contact(
                cur,
                row["name"],
                row["email"],
                row["birthday"],
                row["group"]
            )

            add_phone_python(
                cur,
                row["name"],
                row["phone"],
                row["type"]
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV import finished.")


# ---------- MOVE GROUP ----------
def move_contact_to_group():
    # Move contact using SQL procedure
    name = input("Contact name: ")
    group_name = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact moved.")


# ---------- CONSOLE MENU ----------
def menu():
    # Main console menu
    while True:
        print("""
========== PHONEBOOK ==========
1. Insert 5 sample contacts
2. Show contacts
3. Add phone
4. Move contact to group
5. Search all fields
6. Filter by group
7. Search by email
8. Sort contacts
9. Pagination
10. Export JSON
11. Import JSON
12. Import CSV
13. Show contact phones
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            insert_sample_data()

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            name = input("Contact name: ")
            phone = input("Phone: ")
            phone_type = input("Type (home/work/mobile): ")
            conn = get_connection()
            cur = conn.cursor()
            add_phone_python(cur, name, phone, phone_type)
            conn.commit()
            cur.close()
            conn.close()
            print("Phone added.")

        elif choice == "4":
            move_contact_to_group()

        elif choice == "5":
            text = input("Search: ")
            search_all_fields(text)

        elif choice == "6":
            group_name = input("Group: ")
            filter_by_group(group_name)

        elif choice == "7":
            text = input("Email search: ")
            search_by_email(text)

        elif choice == "8":
            sort_by = input("Sort by name/birthday/date: ")
            show_contacts(sort_by)

        elif choice == "9":
            pagination_console()

        elif choice == "10":
            export_to_json()

        elif choice == "11":
            import_from_json()

        elif choice == "12":
            import_from_csv()

        elif choice == "13":
            name = input("Contact name: ")
            show_contact_phones(name)

        elif choice == "0":
            break

        else:
            print("Wrong choice.")


if __name__ == "__main__":
    menu()
