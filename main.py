import sqlite3
import os

#Connect to DB
database = sqlite3.connect("festival.db")
database.execute("PRAGMA foreign_keys = ON")

cursor = database.cursor()

#Create table Festivals
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Festivals(
        festival_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE,
        location_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES Locations(id))
""")

#Create table Locations
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Locations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        city TEXT,
        country TEXT,
        max_capacity INTEGER)
""")

#Create table Stages
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        festival_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        capacity INTEGER,
        FOREIGN KEY (festival_id) REFERENCES Festivals(festival_id)
    )
""")

#Create table Artists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Artists(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_name TEXT NOT NULL,
        genre TEXT NOT NULL,
        country TEXT,
        bio TEXT
    )
""")

#Create table Performances
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Performances(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        festival_id INTEGER,
        stage_id INTEGER,
        artist_id INTEGER,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        FOREIGN KEY (festival_id) REFERENCES Festivals(festival_id),
        FOREIGN KEY (stage_id) REFERENCES Stages(id),
        FOREIGN KEY (artist_id) REFERENCES Artists(id)
    )
""")

#Create table Users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        registration_date TIMESTAMP
    )
""")

#Create table Ticket_type
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ticket_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        festival_id INTEGER,
        name TEXT NOT NULL,
        price DECIMAL (10,2) NOT NULL,
        available_quantity INTEGER,
        FOREIGN KEY (festival_id) REFERENCES Festivals(festival_id)
    )
""")

#Create table Tickets
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_type_id INTEGER,
        visitor_id INTEGER,
        qr_code TEXT,
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        FOREIGN KEY (ticket_type_id) REFERENCES Ticket_type(id),
        FOREIGN KEY (visitor_id) REFERENCES Users(id)
    )
""")

#Create table Services
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        festival_id INTEGER,
        name TEXT NOT NULL,
        type TEXT,
        location_description TEXT,
        FOREIGN KEY (festival_id) REFERENCES Festivals(festival_id)
    )
""")

#Create table Staff
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        festival_id INTEGER,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT,
        phone TEXT,
        FOREIGN KEY (festival_id) REFERENCES Festivals(festival_id)
    )
""")

database.commit()
database.close()
