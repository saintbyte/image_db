#!/usr/bin/env python3
import argparse
import pathlib

from dotenv import load_dotenv
from repositories.image.files import ImageFilesRepository
from repositories.image.sqllite_db import Sqllite3ImageRepository
from repositories.image.sqllite_db import Sqllite3ImageRepositoryExistsException
load_dotenv()

def main():
    parser = argparse.ArgumentParser(

        prog="setup_db.py",
        description='Create database of image files',
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
        "--parameter",
        nargs=1,
        type=str,
        required=True,
        help="Parameter",
    )
    parser.add_argument(
        "--value",
        nargs=1,
        type=str,
        required=True,
        help="Value of parameter",
    )

    args = parser.parse_args()
    db_file: str = args.db[0]

    image_db = Sqllite3ImageRepository(db_file)

if __name__ == "__main__":
    main()