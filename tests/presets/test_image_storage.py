import unittest
from PIL import Image
from pathlib import Path
from tempfile import TemporaryDirectory

from typed_storage import TypedStorageGroup, image_storage, ImageBase


class ImageA(ImageBase):
    pass


class ImageB(ImageBase):
    pass


class TestTypedStorageGroup(unittest.TestCase):
    def test_save_load_list(self):
        with TemporaryDirectory() as tmpdir:
            group = TypedStorageGroup(
                root_dir=Path(tmpdir),
                storages=[
                    image_storage(
                        ImageA, "image_a", to_sub_path=lambda x: f"{x.id}.png", id_from_path=lambda x: Path(x).stem),
                    image_storage(
                        ImageB, "image_b", to_sub_path=lambda x: f"{x.id}.png", id_from_path=lambda x: Path(x).stem),
                ]
            )
            image = Image.new("RGB", (100, 100))

            group.save(ImageA("a", image))
            group.save(ImageB("b", image))

            self.assertEqual(sorted(group.list_all()), [
                             "image_a/a.png", "image_b/b.png"])

            load_a = group.load("image_a/a.png")
            load_b = group.load("image_b/b.png")
            self.assertEqual(load_a.id, "a")
            self.assertTrue(isinstance(load_a, ImageA))
            self.assertEqual(load_b.id, "b")
            self.assertTrue(isinstance(load_b, ImageB))


if __name__ == '__main__':
    unittest.main()
