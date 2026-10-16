from db import get_connection


TABLES = {
    "Locations": [
        "name",
        "address",
        "city",
        "country",
        "max_capacity"
    ],

    "Festivals": [
        "title",
        "description",
        "start_date",
        "end_date",
        "location_id"
    ],

    "Stages": [
        "festival_id",
        "name",
        "description",
        "capacity"
    ],

    "Artists": [
        "stage_name",
        "genre",
        "country",
        "bio"
    ],

    "Performances": [
        "festival_id",
        "stage_id",
        "artist_id",
        "start_time",
        "end_time"
    ],

    "Ticket_type": [
        "festival_id",
        "name",
        "price",
        "available_quantity"
    ],

    "Users": [
        "first_name",
        "last_name",
        "email",
        "phone",
        "registration_date"
    ],

    "Tickets": [
        "ticket_type_id",
        "visitor_id",
        "qr_code",
        "purchase_date",
        "status"
    ],

    "Services": [
        "festival_id",
        "name",
        "type",
        "location_description"
    ],

    "Staff": [
        "festival_id",
        "first_name",
        "last_name",
        "role",
        "phone"
    ]
}


def get_columns(table):
    return ["id"] + TABLES[table]


def get_all(table):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")

    rows = cursor.fetchall()

    conn.close()

    return rows


def add_record(table, values):
    fields = TABLES[table]

    field_names = ", ".join(fields)

    placeholders = ", ".join(["?"] * len(fields))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO {table} ({field_names}) VALUES ({placeholders})",
        values
    )

    conn.commit()
    conn.close()


def update_record(table, record_id, values):
    fields = TABLES[table]

    changes = ", ".join(
        [f"{field} = ?" for field in fields]
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE {table} SET {changes} WHERE id = ?",
        list(values) + [record_id]
    )

    conn.commit()
    conn.close()


def delete_record(table, record_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"DELETE FROM {table} WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()


def search_records(table, text):
    columns = get_columns(table)

    conditions = " OR ".join(
        [f"CAST({column} AS TEXT) LIKE ?" for column in columns]
    )

    values = [f"%{text}%"] * len(columns)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT * FROM {table} WHERE {conditions}",
        values
    )

    rows = cursor.fetchall()

    conn.close()

    return rows