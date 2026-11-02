
import sqlite3

# Pieslēgties pie DB
database = sqlite3.connect("festivals.db")
database.execute("PRAGMA foreign_keys = ON")
cursor = database.cursor()


# Izveidot tabulu ar atrašanās vietām
cursor.execute("""
CREATE TABLE IF NOT EXISTS locations(
    location_id INTEGER PRIMARY KEY,
    nosaukums TEXT NOT NULL,
    adrese TEXT,
    pilseta TEXT,
    valsts TEXT,
    ietilpiba INTEGER
)
""")


# Izveidot tabulu ar festivāliem
cursor.execute("""
CREATE TABLE IF NOT EXISTS festivals(
    festival_id INTEGER PRIMARY KEY,
    nosaukums TEXT NOT NULL,
    apraksts TEXT,
    sakuma_datums TEXT,
    beigu_datums TEXT,
    location_id INTEGER,
    FOREIGN KEY (location_id)
        REFERENCES locations(location_id)
)
""")


# Izveidot tabulu ar skatuvēm
cursor.execute("""
CREATE TABLE IF NOT EXISTS stages(
    stage_id INTEGER PRIMARY KEY,
    festival_id INTEGER NOT NULL,
    nosaukums TEXT NOT NULL,
    apraksts TEXT,
    ietilpiba INTEGER,
    FOREIGN KEY (festival_id)
        REFERENCES festivals(festival_id)
)
""")


# Izveidot tabulu ar māksliniekiem
cursor.execute("""
CREATE TABLE IF NOT EXISTS artists(
    artist_id INTEGER PRIMARY KEY,
    skatuves_vards TEXT NOT NULL,
    zanrs TEXT,
    valsts TEXT,
    biografija TEXT
)
""")


# Izveidot tabulu ar uzstāšanos
cursor.execute("""
CREATE TABLE IF NOT EXISTS performances(
    performance_id INTEGER PRIMARY KEY,
    festival_id INTEGER NOT NULL,
    stage_id INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    sakuma_laiks TEXT,
    beigu_laiks TEXT,
    FOREIGN KEY (festival_id)
        REFERENCES festivals(festival_id),
    FOREIGN KEY (stage_id)
        REFERENCES stages(stage_id),
    FOREIGN KEY (artist_id)
        REFERENCES artists(artist_id)
)
""")


# Izveidot tabulu ar biļešu veidiem
cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_types(
    ticket_type_id INTEGER PRIMARY KEY,
    festival_id INTEGER NOT NULL,
    nosaukums TEXT NOT NULL,
    cena REAL,
    pieejamais_daudzums INTEGER,
    FOREIGN KEY (festival_id)
        REFERENCES festivals(festival_id)
)
""")


# Izveidot tabulu ar apmeklētājiem
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    vards TEXT,
    uzvards TEXT,
    epasts TEXT,
    telefons TEXT,
    registracijas_datums TEXT
)
""")


# Izveidot tabulu ar biļetēm
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
    ticket_id INTEGER PRIMARY KEY,
    ticket_type_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    qr_kods TEXT,
    pirkuma_datums TEXT,
    statuss TEXT,
    FOREIGN KEY (ticket_type_id)
        REFERENCES ticket_types(ticket_type_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
)
""")


# Izveidot tabulu ar pakalpojumiem
cursor.execute("""
CREATE TABLE IF NOT EXISTS services(
    service_id INTEGER PRIMARY KEY,
    festival_id INTEGER NOT NULL,
    nosaukums TEXT,
    veids TEXT,
    atrasanas_vieta TEXT,
    FOREIGN KEY (festival_id)
        REFERENCES festivals(festival_id)
)
""")


# Izveidot tabulu ar darbiniekiem
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff(
    staff_id INTEGER PRIMARY KEY,
    festival_id INTEGER NOT NULL,
    vards TEXT,
    uzvards TEXT,
    amats TEXT,
    telefons TEXT,
    FOREIGN KEY (festival_id)
        REFERENCES festivals(festival_id)
)
""")


# Ievietot sākotnējos datus

cursor.execute("""
INSERT OR IGNORE INTO locations
VALUES (1, "Mežaparks", "Ostas prospekts", "Rīga", "Latvija", 50000)
""")

cursor.execute("""
INSERT OR IGNORE INTO festivals
VALUES (1, "Summer Sound", "Mūzikas festivāls", "2026-07-31", "2026-08-01", 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO stages
VALUES (1, 1, "Galvenā skatuve", "Lielā skatuve", 10000)
""")

cursor.execute("""
INSERT OR IGNORE INTO artists
VALUES (1, "Example Band", "Pop", "Latvija", "Mūzikas grupa")
""")

cursor.execute("""
INSERT OR IGNORE INTO performances
VALUES (1, 1, 1, 1, "18:00", "19:00")
""")

cursor.execute("""
INSERT OR IGNORE INTO ticket_types
VALUES (1, 1, "Parastā biļete", 35.00, 1000)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES (1, "Anna", "Liepa", "anna@gmail.com", "20000000", "2026-01-10")
""")

cursor.execute("""
INSERT OR IGNORE INTO tickets
VALUES (1, 1, 1, "QR001", "2026-01-15", "Aktīva")
""")

cursor.execute("""
INSERT OR IGNORE INTO services
VALUES (1, 1, "Ēdināšana", "Ēdiens", "Pie galvenās skatuves")
""")

cursor.execute("""
INSERT OR IGNORE INTO staff
VALUES (1, 1, "Jānis", "Bērziņš", "Organizators", "20000001")
""")


# Savienot tabulas un saglabāt datus
database.commit()
database.close()
