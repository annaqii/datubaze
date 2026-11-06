"""SQLite connection and ERD-matching table definitions."""
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "festivals.db"

SCHEMA = 'CREATE TABLE IF NOT EXISTS "locations" (\n    "id" INTEGER PRIMARY KEY,\n    "name" TEXT NOT NULL,\n    "address" TEXT,\n    "city" TEXT,\n    "country" TEXT,\n    "max_capacity" INTEGER\n);\n\nCREATE TABLE IF NOT EXISTS "festivals" (\n    "id" INTEGER PRIMARY KEY,\n    "title" TEXT NOT NULL,\n    "description" TEXT,\n    "start_date" TEXT,\n    "end_date" TEXT,\n    "location_id" INTEGER,\n    FOREIGN KEY ("location_id") REFERENCES "locations"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "stages" (\n    "id" INTEGER PRIMARY KEY,\n    "festival_id" INTEGER NOT NULL,\n    "name" TEXT NOT NULL,\n    "description" TEXT,\n    "capacity" INTEGER,\n    FOREIGN KEY ("festival_id") REFERENCES "festivals"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "artists" (\n    "id" INTEGER PRIMARY KEY,\n    "stage_name" TEXT NOT NULL,\n    "genre" TEXT,\n    "country" TEXT,\n    "bio" TEXT\n);\n\nCREATE TABLE IF NOT EXISTS "performances" (\n    "id" INTEGER PRIMARY KEY,\n    "festival_id" INTEGER NOT NULL,\n    "stage_id" INTEGER NOT NULL,\n    "artist_id" INTEGER NOT NULL,\n    "start_time" TEXT,\n    "end_time" TEXT,\n    FOREIGN KEY ("festival_id") REFERENCES "festivals"("id"),\n    FOREIGN KEY ("stage_id") REFERENCES "stages"("id"),\n    FOREIGN KEY ("artist_id") REFERENCES "artists"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "ticket_type" (\n    "id" INTEGER PRIMARY KEY,\n    "festival_id" INTEGER NOT NULL,\n    "name" TEXT NOT NULL,\n    "price" REAL,\n    "available_quantity" INTEGER,\n    FOREIGN KEY ("festival_id") REFERENCES "festivals"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "users" (\n    "id" INTEGER PRIMARY KEY,\n    "first_name" TEXT,\n    "last_name" TEXT,\n    "email" TEXT,\n    "phone" TEXT,\n    "registration_date" TEXT\n);\n\nCREATE TABLE IF NOT EXISTS "tickets" (\n    "id" INTEGER PRIMARY KEY,\n    "ticket_type_id" INTEGER NOT NULL,\n    "visitor_id" INTEGER NOT NULL,\n    "qr_code" TEXT,\n    "purchase_date" TEXT,\n    "status" TEXT,\n    FOREIGN KEY ("ticket_type_id") REFERENCES "ticket_type"("id"),\n    FOREIGN KEY ("visitor_id") REFERENCES "users"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "services" (\n    "id" INTEGER PRIMARY KEY,\n    "festival_id" INTEGER NOT NULL,\n    "name" TEXT,\n    "type" TEXT,\n    "location_description" TEXT,\n    FOREIGN KEY ("festival_id") REFERENCES "festivals"("id")\n);\n\nCREATE TABLE IF NOT EXISTS "staff" (\n    "id" INTEGER PRIMARY KEY,\n    "festival_id" INTEGER NOT NULL,\n    "first_name" TEXT,\n    "last_name" TEXT,\n    "role" TEXT,\n    "phone" TEXT,\n    FOREIGN KEY ("festival_id") REFERENCES "festivals"("id")\n);'


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with get_connection() as connection:
        connection.executescript(SCHEMA)
