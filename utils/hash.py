from pathlib import Path
from typing import Any
import hashlib

import imagehash
from PIL import Image


def hash_image(file: Any) -> imagehash.ImageHash:
    if isinstance(file, Path):
        image_obj = Image.open(file)
    else:
        raise ValueError("Need PIL.Image or pathlib.Path")
    return imagehash.average_hash(image_obj)


def hash_md5_file(file_name: Path):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
