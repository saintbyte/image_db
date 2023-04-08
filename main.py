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
        prog="main.py",
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
        "--path",
        nargs=1,
        type=str,
        required=True,
        help="path to get list image",
    )
    args = parser.parse_args()
    db_file: str = args.db[0]

    image_db = Sqllite3ImageRepository(db_file)
    path = pathlib.Path(args.path[0])
    images = ImageFilesRepository(path)
    for file in images.get_list():
        try:
            image_db.add(file)
        except Sqllite3ImageRepositoryExistsException:
            print(f"{file} is exists in database")




if __name__ == "__main__":
    main()
