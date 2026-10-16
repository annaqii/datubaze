import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from functions import (
    TABLES,
    get_columns,
    get_all,
    add_record,
    update_record,
    delete_record,
    search_records
)


class FestivalApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Festivālu datubāze")
        self.geometry("1200x700")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self.table_frames = {}

        for table in TABLES:
            self.create_tab(table)


    def create_tab(self, table):

        frame = ttk.Frame(self.tabs)

        self.tabs.add(
            frame,
            text=table
        )

        columns = get_columns(table)

        # Meklēšana
        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=10)

        ttk.Label(
            search_frame,
            text="Meklēt:"
        ).pack(side="left")

        search_entry = ttk.Entry(
            search_frame
        )

        search_entry.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Meklēt",
            command=lambda: self.search(table)
        ).pack(side="left")

        ttk.Button(
            search_frame,
            text="Visi ieraksti",
            command=lambda: self.refresh(table)
        ).pack(side="left", padx=5)


        # Tabula
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10
        )


        # Ievades lauki
        form = ttk.Frame(frame)
        form.pack(pady=10)

        entries = {}

        for i, field in enumerate(TABLES[table]):

            ttk.Label(
                form,
                text=field
            ).grid(
                row=i,
                column=0,
                padx=5,
                pady=2
            )

            entry = ttk.Entry(
                form,
                width=30
            )

            entry.grid(
                row=i,
                column=1,
                padx=5,
                pady=2
            )

            entries[field] = entry


        # Pogas
        buttons = ttk.Frame(frame)
        buttons.pack(pady=5)

        ttk.Button(
            buttons,
            text="Pievienot",
            command=lambda: self.add(table)
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons,
            text="Labot",
            command=lambda: self.update(table)
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons,
            text="Dzēst",
            command=lambda: self.delete(table)
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons,
            text="Notīrīt",
            command=lambda: self.clear_entries(table)
        ).pack(
            side="left",
            padx=5
        )

        tree.bind(
            "<<TreeviewSelect>>",
            lambda event: self.fill_entries(table)
        )

        self.table_frames[table] = {
            "tree": tree,
            "entries": entries,
            "search": search_entry
        }

        self.refresh(table)


    def refresh(self, table, rows=None):

        tree = self.table_frames[table]["tree"]

        for item in tree.get_children():
            tree.delete(item)

        if rows is None:
            rows = get_all(table)

        for row in rows:
            tree.insert(
                "",
                "end",
                values=row
            )


    def get_values(self, table):

        entries = self.table_frames[table]["entries"]

        values = []

        for field in TABLES[table]:
            values.append(
                entries[field].get()
            )

        return values


    def clear_entries(self, table):

        entries = self.table_frames[table]["entries"]

        for entry in entries.values():

            entry.delete(
                0,
                tk.END
            )


    def add(self, table):

        values = self.get_values(table)

        try:

            add_record(
                table,
                values
            )

            self.refresh(table)

            self.clear_entries(table)

        except sqlite3.Error as error:

            messagebox.showerror(
                "Kļūda",
                str(error)
            )


    def get_selected_id(self, table):

        tree = self.table_frames[table]["tree"]

        selected = tree.selection()

        if not selected:
            return None

        values = tree.item(
            selected[0],
            "values"
        )

        return values[0]


    def update(self, table):

        record_id = self.get_selected_id(table)

        if record_id is None:

            messagebox.showwarning(
                "Kļūda",
                "Izvēlies ierakstu"
            )

            return

        values = self.get_values(table)

        try:

            update_record(
                table,
                record_id,
                values
            )

            self.refresh(table)

        except sqlite3.Error as error:

            messagebox.showerror(
                "Kļūda",
                str(error)
            )


    def delete(self, table):

        record_id = self.get_selected_id(table)

        if record_id is None:

            messagebox.showwarning(
                "Kļūda",
                "Izvēlies ierakstu"
            )

            return

        try:

            delete_record(
                table,
                record_id
            )

            self.refresh(table)

            self.clear_entries(table)

        except sqlite3.Error as error:

            messagebox.showerror(
                "Kļūda",
                str(error)
            )


    def fill_entries(self, table):

        tree = self.table_frames[table]["tree"]

        selected = tree.selection()

        if not selected:
            return

        row = tree.item(
            selected[0],
            "values"
        )

        entries = self.table_frames[table]["entries"]

        values = row[1:]

        for field, value in zip(
            TABLES[table],
            values
        ):

            entries[field].delete(
                0,
                tk.END
            )

            entries[field].insert(
                0,
                value
            )


    def search(self, table):

        text = self.table_frames[
            table
        ]["search"].get()

        if text == "":

            self.refresh(table)

            return

        rows = search_records(
            table,
            text
        )

        self.refresh(
            table,
            rows
        )