import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import BaseModel

from typed_storage import TypedStorageGroup, json_storage


class A(BaseModel):
    item_id: str
    value: int


class B(BaseModel):
    item_id: str
    value: str


class TestTypedStorageGroup(unittest.TestCase):
    def test_save_load_list(self):
        with TemporaryDirectory() as tmpdir:
            group = TypedStorageGroup(
                root_dir=Path(tmpdir),
                storages=[
                    json_storage(A, "A", to_sub_path=lambda x: f"{x.item_id}.json"),
                    json_storage(B, "B", to_sub_path=lambda x: f"{x.item_id}.json"),
                ],
            )

            a = A(item_id="a", value=1)
            b = B(item_id="b", value="b")

            group.save(a)
            group.save(b)

            self.assertEqual(sorted((group.list_all())), ["A/a.json", "B/b.json"])

            load_a = group.load("A/a.json")
            load_b = group.load("B/b.json")
            self.assertEqual(load_a, a)
            self.assertEqual(load_b, b)


if __name__ == "__main__":
    unittest.main()
