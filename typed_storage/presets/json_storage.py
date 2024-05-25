from pathlib import Path
from pydantic import BaseModel
from typing import Type, TypeVar, Callable

from typed_storage.core import TypedStorage

_T_PYDANTIC_TYPE = TypeVar("_T_PYDANTIC_TYPE", bound=BaseModel)


def json_storage(
    data_type: Type[_T_PYDANTIC_TYPE],
    directry: str,
    to_sub_path: Callable[[_T_PYDANTIC_TYPE], str],
):
    def to_path(item: _T_PYDANTIC_TYPE):
        return str(Path(directry) / to_sub_path(item))

    def save(item: _T_PYDANTIC_TYPE, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(item.model_dump_json())

    def load(path: str) -> _T_PYDANTIC_TYPE:
        return data_type.model_validate_json(Path(path).read_text())

    def is_loadable_fn(path: str):
        if Path(path) == Path(directry):
            return False
        return Path(path).is_relative_to(directry)

    return TypedStorage(
        data_type,
        to_path=to_path,
        save_fn=save,
        load_fn=load,
        is_loadable_fn=is_loadable_fn,
    )
