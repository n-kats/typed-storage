from typing import Callable
from pathlib import Path

from PIL import Image
from typed_storage.core import TypedStorage


def image_storage(
    directry: Path,
    to_sub_path: Callable[[str], str],
):
    def to_path(item: str):
        return str(directry / to_sub_path(item))

    def save(item: Image.Image, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        item.save(path)

    def load(path: str) -> Image.Image:
        return Image.open(path)

    def is_loadable_fn(path: str):
        return Path(path).is_relative_to(directry)

    return TypedStorage(
        Image.Image,
        to_path=to_path,
        save_fn=save,
        load_fn=load,
        is_loadable_fn=is_loadable_fn,
    )
