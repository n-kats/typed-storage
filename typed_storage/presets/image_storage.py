from typing import Callable, TypeVar, Type
from pathlib import Path

from PIL import Image
from typed_storage.core import TypedStorage


class ImageBase:
    """Base class for image storage"""

    def __init__(self, id_: str, image: Image.Image):
        self.__id = id_
        self.__image = image

    @property
    def id(self) -> str:
        return self.__id

    @property
    def image(self) -> Image.Image:
        return self.__image


_T_IMAGE = TypeVar("_T_IMAGE", bound=ImageBase)


def image_storage(
    image_type: Type[_T_IMAGE],
    directry: str,
    to_sub_path: Callable[[_T_IMAGE], str],
    id_from_path: Callable[[str], str],
):
    def to_path(item: _T_IMAGE) -> str:
        return str(Path(directry) / to_sub_path(item))

    def save(item: _T_IMAGE, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        item.image.save(path)

    def load(path: str) -> _T_IMAGE:
        id_ = id_from_path(path)
        return image_type(id_=id_, image=Image.open(path))

    def is_loadable(path: str, actual_path: str) -> bool:
        if not Path(actual_path).is_file():
            return False

        if not Path(path).is_relative_to(directry):
            return False

        return True

    return TypedStorage(
        image_type,
        to_path=to_path,
        save_fn=save,
        load_fn=load,
        is_loadable_fn=is_loadable,
    )
