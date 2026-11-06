"""Simple terminal interface for viewing and searching records."""
from db import create_tables
from functions import TABLES, get_all


def main():
    create_tables()
    table_names = list(TABLES)
    while True:
        print("\nFESTIVAL DATABASE")
        for number, table_name in enumerate(table_names, 1):
            print(f"{number}. {table_name}")
        print("0. Exit")
        choice = input("Select a table: ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(table_names):
            print("Invalid choice")
            continue
        table_name = table_names[int(choice) - 1]
        search_text = input("Search (Enter = all records): ")
        for record in get_all(table_name, search_text):
            print(record)


if __name__ == "__main__":
    main()
