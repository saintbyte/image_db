import pathlib
import sqlite3
import PIL
from PIL import Image

from utils.hash import hash_image, hash_md5_file

Image.MAX_IMAGE_PIXELS = None


class Sqllite3ImageRepositoryExistsException(Exception):
    pass


class Sqllite3ImageRepositoryNotImageOrReadException(Exception):
    pass


class Sqllite3ImageRepository:
    """ Репозиторий для путей к картинкам в виде БД """
    _default_ext = ".sqllite3"
    _allowed_sqllite_file_ext = [
        ".sqllite",
        ".db",
        ".sqllite3"
    ]
    _image_db_table = "image_db"

    def _normalization_db_filename(self, db_file: str) -> str:
        has_allowed_ext: bool = False
        for ext in self._allowed_sqllite_file_ext:
            if db_file.endswith(ext.lower()):
                has_allowed_ext = True
                break
        if not has_allowed_ext:
            db_file = f"{db_file}{self._default_ext}"
        return db_file

    def __init__(self, db_file: str):
        self.db_file = self._normalization_db_filename(db_file)
        try:
            self._connection: sqlite3.Connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            if not self._connection:
                return
            self._connection.close()
            print(f"Error on open database file: {e}")
            quit()
        cursor = self._connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        sql: str = "select * from sqlite_master where type = 'table'"
        cursor.execute(sql)
        tables = [table[1] for table in cursor.fetchall()]
        if self._image_db_table not in tables:
            self._create_db()
        cursor.close()

    def _create_db(self):
        cursor = self._connection.cursor()
        sql_create_image_db: str = f"""create table IF NOT EXISTS  {self._image_db_table}
        (
            path   TEXT,
            file_hash   TEXT,
            width  integer,
            height integer,
            size   integer,
            hash   TEXT
        );
        """
        cursor.execute(sql_create_image_db)
        sql_index_image_db: str = f"create index IF NOT EXISTS  {self._image_db_table}_hash_index on image_db(hash);"
        cursor.execute(sql_index_image_db)
        cursor.close()

    @staticmethod
    def _get_image_size(file_path):
        with Image.open(file_path) as img:
            width, height = img.size
        return width, height

    @staticmethod
    def _get_file_size(image_path):
        return image_path.stat().st_size

    def add(self, image_path: pathlib.Path):
        print(image_path)
        cursor = self._connection.cursor()
        try:
            width, height = Sqllite3ImageRepository._get_image_size(image_path)
        except Image.DecompressionBombError as e:
            raise Sqllite3ImageRepositoryNotImageOrReadException
        except PIL.UnidentifiedImageError as e:
            raise Sqllite3ImageRepositoryNotImageOrReadException

        size = Sqllite3ImageRepository._get_file_size(image_path)
        hash_obj = hash_image(image_path)
        md5_hash = hash_md5_file(image_path)
        sql = f"""INSERT INTO {self._image_db_table} 
            (
                 path,
                 file_hash, 
                 width,
                 height,
                 size,
                 hash
        ) VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql,  (
                           image_path.as_posix(),
                           md5_hash,
                           width,
                           height,
                           size,
                           str(hash_obj)
                       ))
        self._connection.commit()
