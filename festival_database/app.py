import tkinter as tk
from tkinter import ttk, messagebox
from db import create_tables
from functions import TABLES, get_all, add_record, update_record, delete_record
import os

create_tables()
window = tk.Tk()

# Colors
BACKGROUND = "#F8F7FC"
PURPLE = "#6D5AA8"
LIGHT_PURPLE = "#EDE9F5"
TEXT = "#29243A"
WHITE = "#FFFFFF"

window.configure(bg=BACKGROUND)

style = ttk.Style()
style.theme_use("clam")

style.configure(".", font=("Arial", 10))

style.configure("TFrame", background=BACKGROUND)
style.configure("TLabel", background=BACKGROUND, foreground=TEXT)

style.configure(
    "TLabelframe",
    background=BACKGROUND,
    bordercolor="#D8D1E8"
)

style.configure(
    "TLabelframe.Label",
    background=BACKGROUND,
    foreground=TEXT
)

style.configure(
    "TEntry",
    fieldbackground=WHITE,
    foreground=TEXT,
    padding=5
)

style.configure(
    "TButton",
    background=PURPLE,
    foreground=WHITE,
    padding=8,
    borderwidth=0
)

style.map(
    "TButton",
    background=[("active", "#59478F")]
)

style.configure("TNotebook", background=BACKGROUND)

style.configure(
    "TNotebook.Tab",
    background=LIGHT_PURPLE,
    foreground=TEXT,
    padding=(12, 8)
)

style.map(
    "TNotebook.Tab",
    background=[("selected", PURPLE)],
    foreground=[("selected", WHITE)]
)

style.configure(
    "Treeview",
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT,
    rowheight=27
)

style.configure(
    "Treeview.Heading",
    background=LIGHT_PURPLE,
    foreground=TEXT
)

style.map(
    "Treeview",
    background=[("selected", PURPLE)],
    foreground=[("selected", WHITE)]
)

window.title('Festival Database')
window.geometry('1050x850')

#banner

banner_path = os.path.join(os.path.dirname(__file__), "banner.png")

banner_image = tk.PhotoImage(file=banner_path)

banner = tk.Canvas(
    window,
    height=200,
    highlightthickness=0
)
banner.pack(fill="x")

banner.create_image(
    0, -250,
    image=banner_image,
    anchor="nw"
)

tabs = ttk.Notebook(window)
tabs.pack(fill='both', expand=True, padx=10, pady=10)

# Easy-to-read field names
names = {
    "id": "ID",
    "festival_id": "Festival ID",
    "location_id": "Location ID",
    "stage_id": "Stage ID",
    "artist_id": "Artist ID",
    "performance_id": "Performance ID",
    "ticket_type_id": "Ticket Type ID",
    "visitor_id": "Visitor ID",
    "user_id": "User ID",
    "ticket_id": "Ticket ID",
    "service_id": "Service ID",
    "staff_id": "Staff ID",

    "stage_name": "Stage Name",
    "title": "Title",
    "location_description": "Location description",
    "description": "Description",
    "max_capacity": "Capacity",
    "address": "Address",
    "city": "City",
    "country": "Country",

    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "Email Address",
    "phone": "Phone Number",
    "phone_number": "Phone Number",

    "start_date": "Start Date",
    "end_date": "End Date",
    "start_time": "Start Time",
    "end_time": "End Time",
    "registration_date": "Registration Date",
    "time": "Time",

    "price": "Price",
    "available_quantity": "Available quantity",
    "type": "Type",
    "category": "Category",
    "genre": "Music Genre",

    "qr_code": "QR Code",
    "purchase_date": "Purchase Date",
    "status": "Status",
    "role": "Role"
}
for table_name, fields in TABLES.items():
    tab = ttk.Frame(tabs)
    tabs.add(tab, text=table_name)

    search_box = ttk.Entry(tab, width=35)
    search_box.pack(pady=5)

    columns = ['id'] + fields

    list_frame = ttk.Frame(tab)
    list_frame.pack(fill='both', expand=True, padx=10)
    table = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
    for column in columns:
        table.heading(column, text=names.get(column, column))
        table.column(column, width=145)
    table.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscrollcommand=scrollbar.set)

    form = ttk.LabelFrame(tab, text='Record fields')
    form.pack(fill='x', padx=10, pady=10)
    inputs = []
    for index, field in enumerate(fields):
        row, column = divmod(index, 3)
        ttk.Label(form, text=names.get(field, field)).grid(row=row * 2, column=column, padx=8, sticky='w')
        entry = ttk.Entry(form, width=30)
        entry.grid(row=row * 2 + 1, column=column, padx=8, pady=5)
        inputs.append(entry)

    buttons = ttk.Frame(tab)
    buttons.pack(pady=5)
    result = ttk.Label(tab, text='')
    result.pack(pady=5)

    # Default arguments remember the correct widgets for each tab.
    def show_records(name=table_name, tree=table, search=search_box, status=result):
        try:
            records = get_all(name, search.get())
            for item in tree.get_children():
                tree.delete(item)
            for record in records:
                tree.insert('', 'end', values=['' if value is None else value for value in record])
            status.config(text=f'Records found: {len(records)}')
        except Exception as error:
            messagebox.showerror('Error', str(error))

    def clear_fields(entries=inputs, tree=table):
        for entry in entries:
            entry.delete(0, tk.END)
        tree.selection_remove(tree.selection())

    def select_record(event, tree=table, entries=inputs):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], 'values')
            for entry, value in zip(entries, values[1:]):
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def add(name=table_name, entries=inputs, refresh=show_records, clear=clear_fields):
        try:
            new_id = add_record(name, [entry.get() for entry in entries])
            clear()
            refresh()
            messagebox.showinfo('Added', f'New record ID: {new_id}')
        except Exception as error:
            messagebox.showerror('Error', str(error))

    def edit(name=table_name, tree=table, entries=inputs, refresh=show_records, clear=clear_fields):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Select record', 'Select a row first.')
            return
        record_id = tree.item(selected[0], 'values')[0]
        try:
            update_record(name, record_id, [entry.get() for entry in entries])
            clear()
            refresh()
        except Exception as error:
            messagebox.showerror('Error', str(error))

    def remove(name=table_name, tree=table, refresh=show_records, clear=clear_fields):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Select record', 'Select a row first.')
            return
        record_id = tree.item(selected[0], 'values')[0]
        if messagebox.askyesno('Delete', f'Delete record {record_id}?'):
            try:
                delete_record(name, record_id)
                clear()
                refresh()
            except Exception as error:
                messagebox.showerror('Error', str(error))

    def search_all(search=search_box, refresh=show_records):
        search.delete(0, tk.END)
        refresh()

    table.bind('<<TreeviewSelect>>', select_record)
    ttk.Button(buttons, text='Search', command=show_records).pack(side='left', padx=3)
    ttk.Button(buttons, text='Show all', command=search_all).pack(side='left', padx=3)
    ttk.Button(buttons, text='Add', command=add).pack(side='left', padx=3)
    ttk.Button(buttons, text='Edit selected', command=edit).pack(side='left', padx=3)
    ttk.Button(buttons, text='Delete selected', command=remove).pack(side='left', padx=3)
    ttk.Button(buttons, text='Clear fields', command=clear_fields).pack(side='left', padx=3)
    show_records()

window.mainloop()
