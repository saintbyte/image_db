#!/usr/bin/env python3
import argparse
import pathlib
import sqlite3

from dotenv import load_dotenv
load_dotenv()


def _normalization_db_filename(db_file: str) -> str:
    if not db_file.endswith(".db") or not db_file.endswith(".sqllite") or not db_file.endswith(".sqllite3"):
        db_file = db_file + ".sqllite3"
    return db_file


def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Create database of image files",
        epilog="may The Force be with you!",
    )
    parser.add_argument(
        "--db",
        nargs=1,
        type=str,
        required=True,
        help="path to db",
    )
    parser.add_argument(
        "--path",
        nargs=1,
        type=str,
        required=True,
        help="path to get list image",
    )
    args = parser.parse_args()
    db_file: str = args.db[0]
    db_file = _normalization_db_filename(db_file)
    try:
        sqlite_connection = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Error on open database file: {e}")
        quit()
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)
    cursor.close()

if __name__ == "__main__":
    main()