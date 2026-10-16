import sqlite3

DB_NAME = "festivals.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS Locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            country TEXT,
            max_capacity INTEGER
        );

        CREATE TABLE IF NOT EXISTS Festivals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            location_id INTEGER,
            FOREIGN KEY (location_id) REFERENCES Locations(id)
        );

        CREATE TABLE IF NOT EXISTS Stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            festival_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            capacity INTEGER,
            FOREIGN KEY (festival_id) REFERENCES Festivals(id)
        );

        CREATE TABLE IF NOT EXISTS Artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stage_name TEXT NOT NULL,
            genre TEXT,
            country TEXT,
            bio TEXT
        );

        CREATE TABLE IF NOT EXISTS Performances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            festival_id INTEGER NOT NULL,
            stage_id INTEGER NOT NULL,
            artist_id INTEGER NOT NULL,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY (festival_id) REFERENCES Festivals(id),
            FOREIGN KEY (stage_id) REFERENCES Stages(id),
            FOREIGN KEY (artist_id) REFERENCES Artists(id)
        );

        CREATE TABLE IF NOT EXISTS Ticket_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            festival_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL,
            available_quantity INTEGER,
            FOREIGN KEY (festival_id) REFERENCES Festivals(id)
        );

        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            registration_date TEXT
        );

        CREATE TABLE IF NOT EXISTS Tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_type_id INTEGER NOT NULL,
            visitor_id INTEGER NOT NULL,
            qr_code TEXT,
            purchase_date TEXT,
            status TEXT,
            FOREIGN KEY (ticket_type_id) REFERENCES Ticket_type(id),
            FOREIGN KEY (visitor_id) REFERENCES Users(id)
        );

        CREATE TABLE IF NOT EXISTS Services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            festival_id INTEGER NOT NULL,
            name TEXT,
            type TEXT,
            location_description TEXT,
            FOREIGN KEY (festival_id) REFERENCES Festivals(id)
        );

        CREATE TABLE IF NOT EXISTS Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            festival_id INTEGER NOT NULL,
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            phone TEXT,
            FOREIGN KEY (festival_id) REFERENCES Festivals(id)
        );
        """
    )

    conn.commit()
    conn.close()