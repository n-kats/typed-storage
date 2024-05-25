import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from typed_storage import TypedStorage, TypedStorageGroup


def _save_str(s: str, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(s)


class TestTypedStorageGroup(unittest.TestCase):
    def test_save_load_list(self):
        with TemporaryDirectory() as tmpdir:
            group = TypedStorageGroup(
                root_dir=Path(tmpdir),
                storages=[
                    TypedStorage(
                        item_type=str,
                        to_path=lambda _: "text",
                        save_fn=_save_str,
                        load_fn=lambda path: Path(path).read_text(),
                        is_loadable_fn=lambda path, actual_path: Path(path).name
                        == "text",
                    ),
                    TypedStorage(
                        item_type=int,
                        to_path=lambda _: "number",
                        save_fn=lambda x, path: _save_str(str(x), path),
                        load_fn=lambda path: int(Path(path).read_text()),
                        is_loadable_fn=lambda path, actual_path: Path(
                            actual_path
                        ).is_relative_to(Path(tmpdir) / "number"),
                    ),
                ],
            )

            group.save("hello")
            group.save(42)

            self.assertEqual(set(group.list_all()), {"text", "number"})
            self.assertEqual(set(group.list_all([str])), {"text"})
            self.assertEqual(group.load("text"), "hello")
            self.assertEqual(group.load("number"), 42)


if __name__ == "__main__":
    unittest.main()
