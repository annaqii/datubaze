"""Simple database functions: add, view, search, edit, delete."""
import sqlite3
from db import get_connection

TABLES = {
    'locations': ['name', 'address', 'city', 'country', 'max_capacity'],
    'festivals': ['title', 'description', 'start_date', 'end_date', 'location_id'],
    'stages': ['festival_id', 'name', 'description', 'capacity'],
    'artists': ['stage_name', 'genre', 'country', 'bio'],
    'performances': ['festival_id', 'stage_id', 'artist_id', 'start_time', 'end_time'],
    'ticket_type': ['festival_id', 'name', 'price', 'available_quantity'],
    'users': ['first_name', 'last_name', 'email', 'phone', 'registration_date'],
    'tickets': ['ticket_type_id', 'visitor_id', 'qr_code', 'purchase_date', 'status'],
    'services': ['festival_id', 'name', 'type', 'location_description'],
    'staff': ['festival_id', 'first_name', 'last_name', 'role', 'phone'],
}


def table_info(table_name):
    if table_name not in TABLES:
        raise ValueError("Unknown table")
    return TABLES[table_name]


def convert_values(table_name, values):
    fields = table_info(table_name)
    if len(values) != len(fields):
        raise ValueError("Incorrect number of fields")
    with get_connection() as connection:
        field_types = {row[1]: row[2].upper() for row in connection.execute(f'PRAGMA table_info("{table_name}")')}
    converted = []
    for field, value in zip(fields, values):
        value = str(value).strip()
        if not value:
            converted.append(None)
        elif "INT" in field_types[field]:
            converted.append(int(value))
        elif "REAL" in field_types[field]:
            converted.append(float(value.replace(",", ".")))
        else:
            converted.append(value)
    return converted


def get_all(table_name, search_text=""):
    fields = table_info(table_name)
    with get_connection() as connection:
        if search_text.strip():
            search_fields = ["id"] + fields
            conditions = " OR ".join(f'CAST("{field}" AS TEXT) LIKE ?' for field in search_fields)
            return connection.execute(f'SELECT * FROM "{table_name}" WHERE {conditions} ORDER BY id',
                                      [f"%{search_text.strip()}%"] * len(search_fields)).fetchall()
        return connection.execute(f'SELECT * FROM "{table_name}" ORDER BY id').fetchall()


def add_record(table_name, values):
    fields = table_info(table_name)
    converted = convert_values(table_name, values)
    column_names = ", ".join(f'"{field}"' for field in fields)
    placeholders = ", ".join("?" for _ in fields)
    with get_connection() as connection:
        cursor = connection.execute(f'INSERT INTO "{table_name}" ({column_names}) VALUES ({placeholders})', converted)
        return cursor.lastrowid


def update_record(table_name, record_id, values):
    fields = table_info(table_name)
    converted = convert_values(table_name, values)
    assignments = ", ".join(f'"{field}" = ?' for field in fields)
    with get_connection() as connection:
        cursor = connection.execute(f'UPDATE "{table_name}" SET {assignments} WHERE id = ?',
                                    converted + [int(record_id)])
        return cursor.rowcount


def delete_record(table_name, record_id):
    table_info(table_name)
    with get_connection() as connection:
        cursor = connection.execute(f'DELETE FROM "{table_name}" WHERE id = ?', (int(record_id),))
        return cursor.rowcount
