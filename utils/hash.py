from pathlib import Path
from typing import Any

import imagehash
from PIL import Image


def hash_image(file: Any) -> imagehash.ImageHash:
    if isinstance(file, Path):
        image_obj = Image.open(file)
    else:
        raise ValueError("Need PIL.Image or pathlib.Path")
    return imagehash.average_hash(image_obj)
