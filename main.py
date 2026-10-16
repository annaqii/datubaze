from db import create_tables
from app import FestivalApp


def main():
    create_tables()
    app = FestivalApp()
    app.mainloop()


if __name__ == "__main__":
    main()