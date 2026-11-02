
import sqlite3


# Pieslegties pie DB

def connect():
    database = sqlite3.connect("festivals.db", timeout=10)
    database.execute("PRAGMA foreign_keys = ON")
    return database


# Pievienot atrasanas vietu

def add_location(name, address, city, country, capacity):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO locations
            (nosaukums, adrese, pilseta, valsts, ietilpiba)
            VALUES (?, ?, ?, ?, ?)
        """, (name, address, city, country, capacity))

        database.commit()
        location_id = cursor.lastrowid

        return location_id

    finally:
        database.close()


# Pievienot festivalu

def add_festival(name, description, start_date, end_date, location_id):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO festivals
            (nosaukums, apraksts, sakuma_datums, beigu_datums, location_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, start_date, end_date, location_id))

        database.commit()
        festival_id = cursor.lastrowid

        return festival_id

    finally:
        database.close()


# Pievienot skatuvi

def add_stage(festival_id, name, description, capacity):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO stages
            (festival_id, nosaukums, apraksts, ietilpiba)
            VALUES (?, ?, ?, ?)
        """, (festival_id, name, description, capacity))

        database.commit()
        stage_id = cursor.lastrowid

        return stage_id

    finally:
        database.close()


# Pievienot makslinieku

def add_artist(name, genre, country, bio):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO artists
            (skatuves_vards, zanrs, valsts, biografija)
            VALUES (?, ?, ?, ?)
        """, (name, genre, country, bio))

        database.commit()
        artist_id = cursor.lastrowid

        return artist_id

    finally:
        database.close()


# Pievienot uzstasanos

def add_performance(festival_id, stage_id, artist_id, start_time, end_time):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO performances
            (festival_id, stage_id, artist_id, sakuma_laiks, beigu_laiks)
            VALUES (?, ?, ?, ?, ?)
        """, (festival_id, stage_id, artist_id, start_time, end_time))

        database.commit()
        performance_id = cursor.lastrowid

        return performance_id

    finally:
        database.close()


# Pievienot biletes veidu

def add_ticket_type(festival_id, name, price, quantity):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO ticket_types
            (festival_id, nosaukums, cena, pieejamais_daudzums)
            VALUES (?, ?, ?, ?)
        """, (festival_id, name, price, quantity))

        database.commit()
        ticket_type_id = cursor.lastrowid

        return ticket_type_id

    finally:
        database.close()


# Pievienot apmekletaju

def add_user(name, surname, email, phone, date):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO users
            (vards, uzvards, epasts, telefons, registracijas_datums)
            VALUES (?, ?, ?, ?, ?)
        """, (name, surname, email, phone, date))

        database.commit()
        user_id = cursor.lastrowid

        return user_id

    finally:
        database.close()


# Pievienot bileti

def add_ticket(ticket_type_id, user_id, qr_code, date, status):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO tickets
            (ticket_type_id, user_id, qr_kods, pirkuma_datums, statuss)
            VALUES (?, ?, ?, ?, ?)
        """, (ticket_type_id, user_id, qr_code, date, status))

        database.commit()
        ticket_id = cursor.lastrowid

        return ticket_id

    finally:
        database.close()


# Pievienot pakalpojumu

def add_service(festival_id, name, service_type, location):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO services
            (festival_id, nosaukums, veids, atrasanas_vieta)
            VALUES (?, ?, ?, ?)
        """, (festival_id, name, service_type, location))

        database.commit()
        service_id = cursor.lastrowid

        return service_id

    finally:
        database.close()


# Pievienot darbinieku

def add_staff(festival_id, name, surname, role, phone):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO staff
            (festival_id, vards, uzvards, amats, telefons)
            VALUES (?, ?, ?, ?, ?)
        """, (festival_id, name, surname, role, phone))

        database.commit()
        staff_id = cursor.lastrowid

        return staff_id

    finally:
        database.close()


# Iegut atrasanas vietas

def get_locations():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM locations")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut festivalus

def get_festivals():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM festivals")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut skatuves

def get_stages():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM stages")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut maksliniekus

def get_artists():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM artists")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut uzsanos

def get_performances():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM performances")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut biletes veidus

def get_ticket_types():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM ticket_types")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut apmekletajus

def get_user():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut biletes

def get_tickets():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM tickets")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut pakalpojumus

def get_services():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM services")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut darbiniekus

def get_staff():
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM staff")
        return cursor.fetchall()

    finally:
        database.close()


# Iegut visus ierakstus
# Izmanto terminala un app.py vajadzibam

def get_all(table):
    database = connect()

    try:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    finally:
        database.close()

# Dzest ierakstu

def delete_record(table, record_id):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute(
            f"DELETE FROM {table} WHERE id = ?",
            (record_id,)
        )

        database.commit()

    finally:
        database.close()

def add_user(name, surname, email, phone, date):
    database = connect()

    try:
        cursor = database.cursor()

        cursor.execute("""
            INSERT INTO users
            (vards, uzvards, epasts, telefons, registracijas_datums)
            VALUES (?, ?, ?, ?, ?)
        """, (name, surname, email, phone, date))

        database.commit()
        user_id = cursor.lastrowid

        return user_id

    finally:
        database.close()