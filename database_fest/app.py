"""Festival Databases grafiskā programma (Tkinter)."""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from db import create_tables
from functions import TABLES, get_all, add_record, update_record, delete_record


class FestivalApp:
    def __init__(self, window):
        self.window = window
        window.title("Festival Database")
        window.geometry("1120x720")
        self.entries = {}
        self.trees = {}
        self.searches = {}
        self.messages = {}
        self.selected_ids = {}
        ttk.Label(window, text="Festival Database", font=("Arial", 19, "bold")).pack(pady=10)
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)
        for name in TABLES:
            self.create_tab(notebook, name)

    def create_tab(self, notebook, name):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=name)
        fields = TABLES[name]
        self.selected_ids[name] = None
        top = ttk.Frame(frame)
        top.pack(fill="x", padx=10, pady=8)
        ttk.Label(top, text="Search (any field):").pack(side="left")
        search = tk.StringVar()
        self.searches[name] = search
        ttk.Entry(top, textvariable=search, width=30).pack(side="left", padx=6)
        ttk.Button(top, text="Search", command=lambda n=name: self.show_records(n)).pack(side="left")
        ttk.Button(top, text="Show all", command=lambda n=name: self.clear_search(n)).pack(side="left", padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10)
        columns = ["id"] + fields
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=11)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=145, minwidth=90)
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.trees[name] = tree
        tree.bind("<<TreeviewSelect>>", lambda event, n=name: self.select_record(n))

        form = ttk.LabelFrame(frame, text="Record details (select a row to edit)")
        form.pack(fill="x", padx=10, pady=10)
        self.entries[name] = {}
        for i, field in enumerate(fields):
            row, col = divmod(i, 3)
            ttk.Label(form, text=field).grid(row=row * 2, column=col, sticky="w", padx=8, pady=(6, 0))
            entry = ttk.Entry(form, width=32)
            entry.grid(row=row * 2 + 1, column=col, sticky="ew", padx=8, pady=(0, 6))
            self.entries[name][field] = entry
        for col in range(3):
            form.columnconfigure(col, weight=1)
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", padx=10, pady=4)
        ttk.Button(buttons, text="Add", command=lambda n=name: self.add(n)).pack(side="left", padx=3)
        ttk.Button(buttons, text="Save changes", command=lambda n=name: self.update(n)).pack(side="left", padx=3)
        ttk.Button(buttons, text="Delete selected", command=lambda n=name: self.delete(n)).pack(side="left", padx=3)
        ttk.Button(buttons, text="Clear fields", command=lambda n=name: self.clear_form(n)).pack(side="left", padx=3)
        ttk.Button(buttons, text="Refresh list", command=lambda n=name: self.show_records(n)).pack(side="left", padx=3)
        msg = ttk.Label(frame, text="")
        msg.pack(anchor="w", padx=14, pady=5)
        self.messages[name] = msg
        self.show_records(name)

    def status(self, name, text):
        self.messages[name].config(text=text)

    def values(self, name):
        return [entry.get() for entry in self.entries[name].values()]

    def clear_form(self, name):
        self.selected_ids[name] = None
        for entry in self.entries[name].values():
            entry.delete(0, tk.END)
        self.trees[name].selection_remove(self.trees[name].selection())
        self.status(name, "Fields cleared. Ready for a new record.")

    def select_record(self, name):
        tree = self.trees[name]
        selection = tree.selection()
        if not selection:
            return
        values = tree.item(selection[0], "values")
        self.selected_ids[name] = values[0]
        for entry, value in zip(self.entries[name].values(), values[1:]):
            entry.delete(0, tk.END)
            entry.insert(0, "" if value == "None" else value)
        self.status(name, f"Selected record ID={values[0]}. Edit fields and save changes.")

    def clear_search(self, name):
        self.searches[name].set("")
        self.show_records(name)

    def show_records(self, name):
        tree = self.trees[name]
        try:
            rows = get_all(name, self.searches[name].get())
            for item in tree.get_children():
                tree.delete(item)
            for row in rows:
                tree.insert("", "end", values=["" if value is None else value for value in row])
            self.status(name, f"Records found: {len(rows)}")
        except (sqlite3.Error, ValueError) as error:
            self.status(name, f"Error: {error}")

    def add(self, name):
        try:
            record_id = add_record(name, self.values(name))
            self.clear_form(name)
            self.show_records(name)
            self.status(name, f"Record added! ID={record_id}")
        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror("Add error", str(error))

    def update(self, name):
        record_id = self.selected_ids[name]
        if record_id is None:
            messagebox.showinfo("Select a record", "Select a table row first!")
            return
        try:
            changed = update_record(name, record_id, self.values(name))
            self.clear_form(name)
            self.show_records(name)
            self.status(name, "Record updated!" if changed else "Record not found.")
        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror("Update error", str(error))

    def delete(self, name):
        record_id = self.selected_ids[name]
        if record_id is None:
            messagebox.showinfo("Select a record", "Select a table row first!")
            return
        if not messagebox.askyesno("Confirmation", f"Delete record ID={record_id}?"):
            return
        try:
            deleted = delete_record(name, record_id)
            self.clear_form(name)
            self.show_records(name)
            self.status(name, "Record deleted!" if deleted else "Record not found.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Cannot delete", "This record is referenced by another table. Delete related records first.")
        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror("Delete error", str(error))


def main():
    create_tables()
    root = tk.Tk()
    FestivalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
