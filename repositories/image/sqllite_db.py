import pathlib
import sqlite3
from enum import Enum
from typing import Optional

import PIL
from PIL import Image

from utils.hash import hash_image, hash_md5_file

Image.MAX_IMAGE_PIXELS = None


class ImageStatus(Enum):
    """Статус изображений в базе"""
    NEW = 0
    MOVE_TO_DATASET_PATH = 100
    REMOVE_IN_DATASET_PATH = 200
    READY_TO_WORK = 300
    SEND_TO_WORK = 400
    AFTER_WORK = 500
    IGNORED = 600


class Duplicates(Enum):
    """Дубликаты изображений"""
    BY_FILE_HASH = 1
    BY_IMAGE_HASH = 2
    WRONG = 3


class Sqllite3ImageRepositoryExistsException(Exception):
    pass


class Sqllite3ImageRepositoryNotImageOrReadException(Exception):
    pass


class Sqllite3RepositoryBase():
    """Базовый класс для работы sqllite3 как хранилищем"""
    _default_ext = ".sqlite3"
    _allowed_sqllite_file_ext = [
        ".sqllite",
        ".sqlite",
        ".db",
        ".sqllite3",
        ".sqlite3",
    ]

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _normalization_db_filename(self, db_file: str) -> str:
        has_allowed_ext: bool = False
        for ext in self._allowed_sqllite_file_ext:
            if db_file.endswith(ext.lower()):
                has_allowed_ext = True
                break
        if not has_allowed_ext:
            db_file = f"{db_file}{self._default_ext}"
        return db_file

    def __init__(self, db_file: str, create: bool = True):

        self.db_file = self._normalization_db_filename(db_file)
        try:
            self._connection: sqlite3.Connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            if not self._connection:
                return
            self._connection.close()
            print(f"Error on open database file: {e}")
            quit()
        if create:
            self.create_db()

    def create_db(self):
        """Функция, где создаются таблицы в базе"""
        raise NotImplemented


class Sqllite3ImageRepository(Sqllite3RepositoryBase):
    """ Репозиторий для путей к картинкам в виде БД """
    version = "1"
    current_rowid: Optional[int]=None
    _image_db_table = "image_db"
    _settings_table = "settings"
    _duplicates_table = "duplicates"

    def create_db(self):
        self._create_images_paths_tables()
        self._create_settings_tables()
        self._create_duplicates_tables()

    def is_image_fb(self) -> bool:
        cursor = self._connection.cursor()
        sql_query = """
             SELECT 
                 name 
             FROM 
                 sqlite_master
             WHERE
                 type='table';
        """
        cursor.execute(sql_query)
        tables: list = [row[0] for row in cursor.fetchall()]
        all_tables: list = self._all_tables()
        tables_result: list = []
        for table in all_tables:
            if table in tables:
                tables_result.append(True)
                continue
            tables_result.append(False)
        cursor.close()
        if all(tables_result):
            return True
        return False

    def _all_tables(self):
        return [
            self._image_db_table,
            # self._settings_table,
            # self._duplicates_table
        ]

    def _create_images_paths_tables(self):
        cursor = self._connection.cursor()
        sql_images_paths_table: str = f"""create table IF NOT EXISTS  {self._image_db_table}
        (
            path   TEXT,
            file_hash   TEXT,
            width  integer,
            height integer,
            size   integer,
            hash   TEXT,
            dataset_name TEXT,
            status integer
        );
        """
        cursor.execute(sql_images_paths_table)
        sql_index_image_db: str = f"create index IF NOT EXISTS  {self._image_db_table}_hash_index on image_db(hash);"
        cursor.execute(sql_index_image_db)
        cursor.close()

    def _create_settings_tables(self):
        cursor = self._connection.cursor()
        sql_settings_table: str = f"""create table IF NOT EXISTS  {self._settings_table}
               (
                   parameter   TEXT,
                   value   TEXT
               );
               """
        cursor.execute(sql_settings_table)
        cursor.close()

    def _create_duplicates_tables(self):
        cursor = self._connection.cursor()
        """
        sql_settings_table: str = f"" "create table IF NOT EXISTS  {self._duplicates_table}
            (
                parameter   TEXT,
                value   TEXT
            );
            "" "
        cursor.execute(sql_settings_table)
        """
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
                 hash,
                 dataset_name,
                 status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            image_path.as_posix(),
            md5_hash,
            width,
            height,
            size,
            str(hash_obj),
            "",
            ImageStatus.NEW.value,
        ))
        self._connection.commit()

    def get_images(self, *, direction: Optional[str] = None, first: bool = False ) -> Optional[dict]:
        self._connection.row_factory = self.dict_factory
        cursor = self._connection.cursor()
        sql_query = f"""
                    SELECT 
                        ROWID,
                        path,
                        file_hash, 
                        width,
                        height,
                        size,
                        hash,
                        dataset_name,
                        status
                    FROM 
                        {self._image_db_table}
        """
        if direction == "next":
            sql_query = f"""
                {sql_query} 
                WHERE 
                    ROWID>{self.current_rowid}
                ORDER BY 
                    ROWID  
            """
        if direction == "prev":
            sql_query = f"""
                {sql_query} 
                WHERE 
                    ROWID<{self.current_rowid}
                ORDER BY 
                    ROWID DESC
            """
        if first:
            sql_query = f"""{sql_query}
                    ORDER BY 
                        ROWID 
            """
        sql_query = f"""{sql_query} LIMIT 1"""
        cursor.execute(sql_query)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        self.current_rowid = result["rowid"]
        return result

    def get_first_image(self) -> Optional[dict]:
        return self.get_images(first=True)

    def get_next_image(self) -> Optional[dict]:
        return self.get_images(direction="next")

    def get_prev_image(self) -> Optional[dict]:
        return self.get_images(direction="prev")
