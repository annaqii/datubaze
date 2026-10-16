from db import create_tables
from functions import TABLES, get_all, add_record, delete_record


def choose_table():

    tables = list(TABLES.keys())

    print("\nTabulas:")

    for i, table in enumerate(
        tables,
        start=1
    ):

        print(
            i,
            table
        )

    try:

        number = int(
            input("Izvēlies tabulu: ")
        )

        return tables[
            number - 1
        ]

    except:

        print(
            "Nepareiza izvēle"
        )

        return None


def show_records(table):

    rows = get_all(table)

    for row in rows:

        print(row)


def add_terminal(table):

    values = []

    for field in TABLES[table]:

        value = input(
            field + ": "
        )

        values.append(value)

    add_record(
        table,
        values
    )

    print(
        "Ieraksts pievienots"
    )


def run_terminal():

    create_tables()

    while True:

        print("\nFestivālu datubāze")

        print(
            "1 - Parādīt datus"
        )

        print(
            "2 - Pievienot ierakstu"
        )

        print(
            "3 - Dzēst ierakstu"
        )

        print(
            "0 - Iziet"
        )

        choice = input(
            "Izvēle: "
        )

        if choice == "0":
            break

        table = choose_table()

        if table is None:
            continue

        if choice == "1":

            show_records(table)

        elif choice == "2":

            add_terminal(table)

        elif choice == "3":

            record_id = input(
                "Ievadi ID: "
            )

            delete_record(
                table,
                record_id
            )

            print(
                "Ieraksts dzēsts"
            )


if __name__ == "__main__":
    run_terminal()