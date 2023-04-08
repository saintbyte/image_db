import pathlib
from typing import Union, Optional


class ImageFilesRepository:
    """ Слои хранилища картинок """
    allowed_image_ext = [".png", ".jpg", ".jpeg", ]

    def __init__(self, path: Union[str, pathlib.Path]):
        self._path = path
        if isinstance(path, str):
            self._path = pathlib.Path(path)
        if not self._path.exists():
            raise ValueError("Path not exists")

    def is_image(self, image_path: pathlib.Path) -> bool:
        if not image_path.is_file():
            return False
        try:
            ext = image_path.suffixes[-1]
        except IndexError:
            # Файл без расширения
            return False
        if ext.lower() in self.allowed_image_ext:
            return True
        return False

    def get_list(self, path: Optional[pathlib.Path] = None) -> list:
        if path is None:
            path = self._path
        result = []
        files = path.glob("*")
        for item in files:
            if item.is_dir():
                result = result + self.get_list(item)
                continue
            if self.is_image(item):
                result.append(item)
        return result
