
from db import create_tables
from functions import (
    add_record,
    get_records,
    search_records,
    update_record,
    delete_record,
    get_festivals
)


def show_festivals():
    festivals = get_festivals()

    if not festivals:
        print("Festivālu nav.")
        return

    for festival in festivals:
        print(festival)


def main():
    create_tables()

    while True:
        print("\n=== FESTIVĀLU SISTĒMA ===")
        print("1. Pievienot festivālu")
        print("2. Apskatīt festivālus")
        print("3. Meklēt festivālu pēc nosaukuma")
        print("4. Labot festivālu")
        print("5. Dzēst festivālu")
        print("6. Pievienot atrašanās vietu")
        print("7. Apskatīt atrašanās vietas")
        print("8. Pievienot mākslinieku")
        print("9. Apskatīt māksliniekus")
        print("0. Iziet")

        choice = input("Izvēlies darbību: ")

        try:
            if choice == "1":
                title = input("Festivāla nosaukums: ")
                description = input("Apraksts: ") or None
                start = input("Sākuma datums (GGGG-MM-DD): ") or None
                end = input("Beigu datums (GGGG-MM-DD): ") or None
                location = input("Atrašanās vietas ID (vai Enter): ")

                record_id = add_record("Festivals", {
                    "title": title,
                    "description": description,
                    "start_date": start,
                    "end_date": end,
                    "location_id": int(location) if location else None
                })
                print(f"Festivāls pievienots! ID: {record_id}")

            elif choice == "2":
                show_festivals()

            elif choice == "3":
                title = input("Meklējamais nosaukums: ")
                results = search_records("Festivals", "title", title)
                for row in results:
                    print(row)
                if not results:
                    print("Nekas nav atrasts.")

            elif choice == "4":
                record_id = int(input("Festivāla ID: "))
                title = input("Jaunais nosaukums: ")

                changed = update_record(
                    "Festivals", record_id, {"title": title}
                )
                print("Festivāls atjaunināts." if changed
                      else "Festivāls nav atrasts.")

            elif choice == "5":
                record_id = int(input("Dzēšamā festivāla ID: "))
                deleted = delete_record("Festivals", record_id)
                print("Festivāls dzēsts." if deleted
                      else "Festivāls nav atrasts.")

            elif choice == "6":
                name = input("Vietas nosaukums: ")
                address = input("Adrese: ") or None
                city = input("Pilsēta: ") or None
                country = input("Valsts: ") or None
                capacity = input("Maksimālā ietilpība: ")

                record_id = add_record("Locations", {
                    "name": name,
                    "address": address,
                    "city": city,
                    "country": country,
                    "max_capacity": int(capacity) if capacity else None
                })
                print(f"Vieta pievienota! ID: {record_id}")

            elif choice == "7":
                for row in get_records("Locations"):
                    print(row)

            elif choice == "8":
                stage_name = input("Mākslinieka skatuves vārds: ")
                genre = input("Žanrs: ")
                country = input("Valsts: ") or None
                bio = input("Biogrāfija: ") or None

                record_id = add_record("Artists", {
                    "stage_name": stage_name,
                    "genre": genre,
                    "country": country,
                    "bio": bio
                })
                print(f"Mākslinieks pievienots! ID: {record_id}")

            elif choice == "9":
                for row in get_records("Artists"):
                    print(row)

            elif choice == "0":
                print("Programma aizvērta.")
                break

            else:
                print("Nederīga izvēle.")

        except (ValueError, TypeError) as error:
            print(f"Nepareizi ievaddati: {error}")
        except Exception as error:
            print(f"Kļūda: {error}")


if __name__ == "__main__":
    main()