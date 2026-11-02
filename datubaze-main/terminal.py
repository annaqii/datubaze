
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
    get_locations,
    get_festivals,
    get_stages,
    get_artists,
    get_performances,
    get_ticket_types,
    get_user,
    get_tickets,
    get_services,
    get_staff
)


while True:

    print("\nFESTIVĀLU DATABĀZE")

    print("1 - Parādīt atrašanās vietas")
    print("2 - Parādīt festivālus")
    print("3 - Parādīt skatuves")
    print("4 - Parādīt māksliniekus")
    print("5 - Parādīt uzstāšanās")
    print("6 - Parādīt biļešu veidus")
    print("7 - Parādīt apmeklētājus")
    print("8 - Parādīt biļetes")
    print("9 - Parādīt pakalpojumus")
    print("10 - Parādīt darbiniekus")

    print("\n11 - Pievienot festivālu")
    print("12 - Pievienot apmeklētāju")
    print("13 - Pievienot biļeti")
    print("14 - Pievienot mākslinieku")

    print("0 - Iziet")

    choice = input("Izvēle: ")


    # Parādīt atrašanās vietas

    if choice == "1":

        print("\nATRAŠANĀS VIETAS")

        for location in get_locations():
            print(location)


    # Parādīt festivālus

    elif choice == "2":

        print("\nFESTIVĀLI")

        for festival in get_festivals():
            print(festival)


    # Parādīt skatuves

    elif choice == "3":

        print("\nSKATUVES")

        for stage in get_stages():
            print(stage)


    # Parādīt māksliniekus

    elif choice == "4":

        print("\nMĀKSLINIEKI")

        for artist in get_artists():
            print(artist)


    # Parādīt uzstāšanās

    elif choice == "5":

        print("\nUZSTĀŠANĀS")

        for performance in get_performances():
            print(performance)


    # Parādīt biļešu veidus

    elif choice == "6":

        print("\nBIĻEŠU VEIDI")

        for ticket in get_ticket_types():
            print(ticket)


    # Parādīt apmeklētājus

    elif choice == "7":

        print("\nAPMEKLĒTĀJI")

        for user in get_user():
            print(user)


    # Parādīt biļetes

    elif choice == "8":

        print("\nBIĻETES")

        for ticket in get_tickets():
            print(ticket)


    # Parādīt pakalpojumus

    elif choice == "9":

        print("\nPAKALPOJUMI")

        for service in get_services():
            print(service)


    # Parādīt darbiniekus

    elif choice == "10":

        print("\nDARBINIEKI")

        for worker in get_staff():
            print(worker)


    # Pievienot festivālu

    elif choice == "11":

        print("\nPIEVIENOT FESTIVĀLU")

        name = input("Festivāla nosaukums: ")
        description = input("Apraksts: ")
        start = input("Sākuma datums: ")
        end = input("Beigu datums: ")
        location = int(input("Atrašanās vietas ID: "))

        festival_id = add_festival(
            name,
            description,
            start,
            end,
            location
        )

        print("Festivāls pievienots. ID:", festival_id)


    # Pievienot apmeklētāju

    elif choice == "12":

        print("\nPIEVIENOT APMEKLĒTĀJU")

        name = input("Vārds: ")
        surname = input("Uzvārds: ")
        email = input("E-pasts: ")
        phone = input("Telefons: ")
        date = input("Reģistrācijas datums: ")

        user_id = add_user(
            name,
            surname,
            email,
            phone,
            date
        )

        print("Apmeklētājs pievienots. ID:", user_id)


    # Pievienot biļeti

    elif choice == "13":

        print("\nPIEVIENOT BIĻETI")

        ticket_type = int(input("Biļetes veida ID: "))
        user = int(input("Apmeklētāja ID: "))
        qr = input("QR kods: ")
        date = input("Pirkuma datums: ")
        status = input("Statuss: ")

        ticket_id = add_ticket(
            ticket_type,
            user,
            qr,
            date,
            status
        )

        print("Biļete pievienota. ID:", ticket_id)


    # Pievienot mākslinieku

    elif choice == "14":

        print("\nPIEVIENOT MĀKSLINIEKU")

        name = input("Skatuves vārds: ")
        genre = input("Žanrs: ")
        country = input("Valsts: ")
        bio = input("Biogrāfija: ")

        artist_id = add_artist(
            name,
            genre,
            country,
            bio
        )

        print("Mākslinieks pievienots. ID:", artist_id)


    elif choice == "0":
        break

    else:
        print("Nepareiza izvēle!")
