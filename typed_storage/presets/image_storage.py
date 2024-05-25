from typing import Callable, TypeVar, Type
from pathlib import Path

from PIL import Image
from typed_storage.core import TypedStorage


class ImageBase:
    """Base class for image storage"""

    def __init__(self, image: Image.Image):
        self.__image = image

    @property
    def image(self):
        return self.__image


_T_IMAGE = TypeVar("_T_IMAGE", bound=ImageBase)


def image_storage(
    image_type: Type[_T_IMAGE],
    directry: Path,
    to_sub_path: Callable[[_T_IMAGE], str],
):
    def to_path(item: _T_IMAGE) -> str:
        return str(directry / to_sub_path(item))

    def save(item: _T_IMAGE, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        item.image.save(path)

    def load(path: str) -> _T_IMAGE:
        return image_type(Image.open(path))

    def is_loadable_fn(path: str) -> bool:
        return Path(path).is_relative_to(directry)

    return TypedStorage(
        image_type,
        to_path=to_path,
        save_fn=save,
        load_fn=load,
        is_loadable_fn=is_loadable_fn,
    )
