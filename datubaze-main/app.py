
import tkinter as tk
from tkinter import ttk

from functions import (
    add_location,
    add_festival,
    add_stage,
    add_artist,
    add_performance,
    add_ticket_type,
    add_user,
    add_ticket,
    add_service,
    add_staff,
    get_all,
    delete_record
)


# Galvenais logs ==================================

window = tk.Tk()

window.title("Festivālu datubāze")
window.geometry("1000x800")


header = tk.Label(
    window,
    text="Festivālu datubāze",
    font=("Arial", 20, "bold")
)

header.pack(pady=15)


# Cilnes ==========================================

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True)


# Tabulu lauki ====================================

TABLES = {

    "Atrašanās vietas": (
        "locations",
        ["nosaukums", "adrese", "pilseta", "valsts", "ietilpiba"]
    ),

    "Festivāli": (
        "festivals",
        ["nosaukums", "apraksts", "sakuma_datums", "beigu_datums", "location_id"]
    ),

    "Skatuves": (
        "stages",
        ["festival_id", "nosaukums", "apraksts", "ietilpiba"]
    ),

    "Mākslinieki": (
        "artists",
        ["skatuves_vards", "zanrs", "valsts", "biografija"]
    ),

    "Uzstāšanās": (
        "performances",
        ["festival_id", "stage_id", "artist_id", "sakuma_laiks", "beigu_laiks"]
    ),

    "Biļešu veidi": (
        "ticket_types",
        ["festival_id", "nosaukums", "cena", "pieejamais_daudzums"]
    ),

    "Apmeklētāji": (
        "users",
        ["vards", "uzvards", "epasts", "telefons", "registracijas_datums"]
    ),

    "Biļetes": (
        "tickets",
        ["ticket_type_id", "user_id", "qr_kods", "pirkuma_datums", "statuss"]
    ),

    "Pakalpojumi": (
        "services",
        ["festival_id", "nosaukums", "veids", "atrasanas_vieta"]
    ),

    "Darbinieki": (
        "staff",
        ["festival_id", "vards", "uzvards", "amats", "telefons"]
    )
}

# Saglabāt ievades laukus

entries = {}
results = {}
trees = {}


# Pievienot ierakstu ==============================

def addFromWindow(table):

    database_table, fields = TABLES[table]

    values = []

    for field in fields:

        value = entries[table][field].get()

        if value == "":
            results[table].config(
                text="Aizpildi visus laukus!",
                fg="red"
            )
            return

        values.append(value)

    try:

        if database_table == "Locations":
            add_location(*values)

        elif database_table == "Festivals":
            add_festival(*values)

        elif database_table == "Stages":
            add_stage(*values)

        elif database_table == "Artists":
            add_artist(*values)

        elif database_table == "Performances":
            add_performance(*values)

        elif database_table == "Ticket_type":
            add_ticket_type(*values)

        elif database_table == "Users":
            add_user(*values)

        elif database_table == "Tickets":
            add_ticket(*values)

        elif database_table == "Services":
            add_service(*values)

        elif database_table == "Staff":
            add_staff(*values)

        for entry in entries[table].values():
            entry.delete(0, tk.END)

        results[table].config(
            text="Ieraksts pievienots!",
            fg="green"
        )

        showRecords(table)

    except Exception as error:

        results[table].config(
            text=f"Kļūda: {error}",
            fg="red"
        )


# Parādīt ierakstus ===============================

def showRecords(table):

    database_table, fields = TABLES[table]

    tree = trees[table]

    for item in tree.get_children():
        tree.delete(item)

    try:

        records = get_all(database_table)

        for record in records:
            tree.insert(
                "",
                "end",
                values=record
            )

    except Exception as error:

        results[table].config(
            text=f"Kļūda: {error}",
            fg="red"
        )


# Dzēst ierakstu ==================================

def deleteFromWindow(table):

    database_table, fields = TABLES[table]

    tree = trees[table]

    selected = tree.selection()

    if not selected:
        results[table].config(
            text="Izvēlies ierakstu!",
            fg="red"
        )
        return

    values = tree.item(
        selected[0],
        "values"
    )

    record_id = values[0]

    try:

        delete_record(database_table, record_id)

        results[table].config(
            text="Ieraksts dzēsts!",
            fg="green"
        )

        showRecords(table)

    except Exception as error:

        results[table].config(
            text=f"Kļūda: {error}",
            fg="red"
        )


# Izveidot cilnes =================================

def createTab(table):

    database_table, fields = TABLES[table]

    frame = ttk.Frame(tabs)

    tabs.add(
        frame,
        text=table
    )

    # Tabula

    tree = ttk.Treeview(
        frame,
        columns=["ID"] + fields,
        show="headings"
    )

    for column in ["ID"] + fields:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=130
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    trees[table] = tree

    # Ievades lauki

    block = tk.LabelFrame(
        frame,
        text="Pievienot " + table,
        padx=10,
        pady=10
    )

    block.pack(
        fill="x",
        padx=20,
        pady=10
    )

    entries[table] = {}

    for field in fields:

        tk.Label(
            block,
            text=field
        ).pack()

        entry = tk.Entry(
            block,
            width=50
        )

        entry.pack(pady=3)

        entries[table][field] = entry

    # Poga pievienošanai

    button = tk.Button(
        block,
        text="Pievienot",
        command=lambda: addFromWindow(table)
    )

    button.pack(pady=5)

    # Rezultāts

    result = tk.Label(
        block,
        text=""
    )

    result.pack(pady=5)

    results[table] = result

    # Dzēšanas poga

    delete_button = tk.Button(
        block,
        text="Dzēst ierakstu",
        command=lambda: deleteFromWindow(table)
    )

    delete_button.pack(pady=5)

    # Atjaunot sarakstu

    refresh_button = tk.Button(
        block,
        text="Atjaunot sarakstu",
        command=lambda: showRecords(table)
    )

    refresh_button.pack(pady=5)

    showRecords(table)


# Izveidot visas cilnes ===========================

for table in TABLES:
    createTab(table)


# Programmas palaišana ============================

window.mainloop()
