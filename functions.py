
from db import connect


# Atļautās tabulas un to lauki
TABLES = {
    "Festivals": [
        "festival_id", "title", "description",
        "start_date", "end_date", "location_id"
    ],
    "Locations": [
        "id", "name", "address", "city", "country", "max_capacity"
    ],
    "Stages": [
        "id", "festival_id", "name", "description", "capacity"
    ],
    "Artists": ["id", "stage_name", "genre", "country", "bio"],
    "Performances": [
        "id", "festival_id", "stage_id", "artist_id",
        "start_time", "end_time"
    ],
    "Users": [
        "id", "first_name", "last_name", "email",
        "phone", "registration_date"
    ],
    "Ticket_type": [
        "id", "festival_id", "name", "price", "available_quantity"
    ],
    "Tickets": [
        "id", "ticket_type_id", "visitor_id",
        "qr_code", "purchase_date", "status"
    ],
    "Services": [
        "id", "festival_id", "name", "type", "location_description"
    ],
    "Staff": [
        "id", "festival_id", "first_name",
        "last_name", "role", "phone"
    ]
}

PRIMARY_KEYS = {
    "Festivals": "festival_id",
    "Locations": "id",
    "Stages": "id",
    "Artists": "id",
    "Performances": "id",
    "Users": "id",
    "Ticket_type": "id",
    "Tickets": "id",
    "Services": "id",
    "Staff": "id"
}


# Pievieno ierakstu jebkurai tabulai
def add_record(table, data):
    if table not in TABLES:
        raise ValueError("Nezināma tabula.")

    columns = [
        column for column in data
        if column in TABLES[table]
        and column != PRIMARY_KEYS[table]
    ]

    if not columns:
        raise ValueError("Nav norādīti lauki.")

    sql = (
        f"INSERT INTO {table} ({', '.join(columns)}) "
        f"VALUES ({', '.join('?' for _ in columns)})"
    )
    values = [data[column] for column in columns]

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(sql, values)
        database.commit()
        return cursor.lastrowid
    except Exception:
        database.rollback()
        raise
    finally:
        database.close()


# Iegūst visus ierakstus
def get_records(table):
    if table not in TABLES:
        raise ValueError("Nezināma tabula.")

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()
    finally:
        database.close()


# Meklē pēc izvēlēta lauka
def search_records(table, column, value):
    if table not in TABLES or column not in TABLES[table]:
        raise ValueError("Nezināma tabula vai lauks.")

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(
            f"SELECT * FROM {table} "
            f"WHERE CAST({column} AS TEXT) LIKE ?",
            (f"%{value}%",)
        )
        return cursor.fetchall()
    finally:
        database.close()


# Labo ierakstu pēc ID
def update_record(table, record_id, data):
    if table not in TABLES:
        raise ValueError("Nezināma tabula.")

    primary_key = PRIMARY_KEYS[table]
    columns = [
        column for column in data
        if column in TABLES[table] and column != primary_key
    ]

    if not columns:
        raise ValueError("Nav norādīti lauki labošanai.")

    sql = (
        f"UPDATE {table} SET "
        + ", ".join(f"{column} = ?" for column in columns)
        + f" WHERE {primary_key} = ?"
    )
    values = [data[column] for column in columns] + [record_id]

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(sql, values)
        database.commit()
        return cursor.rowcount
    except Exception:
        database.rollback()
        raise
    finally:
        database.close()


# Dzēš ierakstu pēc ID
def delete_record(table, record_id):
    if table not in TABLES:
        raise ValueError("Nezināma tabula.")

    primary_key = PRIMARY_KEYS[table]

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(
            f"DELETE FROM {table} WHERE {primary_key} = ?",
            (record_id,)
        )
        database.commit()
        return cursor.rowcount
    except Exception:
        database.rollback()
        raise
    finally:
        database.close()


# Parāda festivālus kopā ar atrašanās vietām
def get_festivals():
    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute("""
            SELECT f.festival_id, f.title, f.start_date,
                   f.end_date, l.name
            FROM Festivals f
            LEFT JOIN Locations l ON f.location_id = l.id
            ORDER BY f.festival_id
        """)
        return cursor.fetchall()
    finally:
        database.close()