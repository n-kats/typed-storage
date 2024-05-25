from typing import Type, TypeVar, Generic, Callable, Sequence
from pathlib import Path

_T_ITEM = TypeVar("_T_ITEM")


class TypedStorage(Generic[_T_ITEM]):
    def __init__(
        self,
        item_type: Type[_T_ITEM],
        to_path: Callable[[_T_ITEM], str],
        save_fn: Callable[[_T_ITEM, str], None],
        load_fn: Callable[[str], _T_ITEM],
        is_loadable_fn: Callable[[str], bool],
    ):
        self.__item_type = item_type
        self.__to_path = to_path
        self.__save_fn = save_fn
        self.__load_fn = load_fn
        self.__is_loadable_fn = is_loadable_fn

    @property
    def item_type(self):
        return self.__item_type

    def to_path(self, item: _T_ITEM) -> str:
        return self.__to_path(item)

    def save(self, item: _T_ITEM, path: str):
        return self.__save_fn(item, path)

    def load(self, path: str) -> _T_ITEM:
        return self.__load_fn(path)

    def is_loadable(self, path: str) -> bool:
        return self.__is_loadable_fn(path)


def validate_unique(iterable):
    seen = set()
    duplicate = set()
    for item in iterable:
        if item in seen:
            duplicate.add(item)
        seen.add(item)

    if duplicate:
        raise ValueError(f"Duplicate items: {duplicate}")


class TypedStorageGroup:
    def __init__(
        self,
        root_dir: Path,
        storages: Sequence[TypedStorage],
        allow_duplicates: bool = False,
        ignore_missing_on_load: bool = False,
        ignore_missing_on_save: bool = False,
    ) -> None:
        self.__root_dir = root_dir
        if not allow_duplicates:
            validate_unique(storage.item_type for storage in storages)
        self.__storages = storages
        self.__ignore_missing_on_load = ignore_missing_on_load
        self.__ignore_missing_on_save = ignore_missing_on_save

    def save(self, item):
        storages = [
            storage
            for storage in self.__storages
            if isinstance(item, storage.item_type)
        ]
        if not self.__ignore_missing_on_save and not storages:
            raise ValueError(f"Item type {type(item)} not supported")

        for storage in storages:
            path = self.root / storage.to_path(item)
            storage.save(item, str(path))

    def load(self, path: str):
        storages = [
            storage for storage in self.__storages if storage.is_loadable(path)]

        if not self.__ignore_missing_on_load and not storages:
            raise ValueError(f"Path {path} not supported")

        if len(storages) > 1:
            raise ValueError(f"Path {path} is ambiguous")

        storage = storages[0]
        return storage.load(str(self.__root_dir / path))

    def list_all(self, types=None):
        outputs = []
        for path in self.__root_dir.glob("**/*"):
            relative_path = str(path.relative_to(self.__root_dir))
            storages = [
                storage
                for storage in self.__storages
                if storage.is_loadable(relative_path)
            ]
            if types:
                storages = [
                    storage for storage in storages if storage.item_type in types
                ]
            if storages:
                if len(storages) > 1:
                    raise ValueError(f"Path {relative_path} is ambiguous")
                outputs.append(relative_path)
        return outputs
