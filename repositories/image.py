import pathlib
import sqlite3


class Sqllite3ImageRepository():
    _default_ext = ".sqllite3"
    _allowed_sqllite_file_ext = [".sqllite",
                                 ".db",
                                 ".sqllite3"
                                 ]
    _image_db_table = "image_db"

    def _normalization_db_filename(self, db_file: str) -> str:
        has_allowed_ext: bool = False
        for ext in self._allowed_sqllite_file_ext:
            if db_file.endswith(ext):
                has_allowed_ext = True
        if not has_allowed_ext:
            db_file = f"db_file{self._default_ext}"
        return db_file

    def __init__(self, db_file: str):
        try:
            self._connection: sqlite3.Connection = sqlite3.connect(db_file)
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
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        print(tables)
        if self._image_db_table not in tables:
            self._create_db()

        cursor.close()

    def _create_db(self):
        cursor = self._connection.cursor()
        sql_create_image_db:str = f"""create table {self._image_db_table}
        (
            path   TEXT,
            width  integer,
            height integer,
            size   integer,
            hash   TEXT
        );
        """
        cursor.execute(sql_create_image_db)
        sql_index_image_db:str = f"create index {self._image_db_table}_hash_index on image_db(hash);"
        cursor.execute(sql_index_image_db)
        cursor.close()