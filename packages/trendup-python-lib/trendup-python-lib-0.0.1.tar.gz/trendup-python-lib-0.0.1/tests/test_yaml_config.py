import tempfile
from unittest import TestCase

from trendup_config.yaml_config import YamlConfig


class TestYamlConfig(TestCase):

    def setUp(self) -> None:
        self.file = tempfile.mktemp()

    def test_get_or_default(self):
        with self.subTest("should return value from file if exist"):
            self.overwrite_to_file("key: value")
            self.assertEqual("value", self._get_new_config().get_or_default("key", "default"))

        with self.subTest("should return default value and write into if key is not exist"):
            self.overwrite_to_file("")
            self.assertEqual("default", self._get_new_config().get_or_default("key", "default"))
            self.assert_file_content("key: default\n")

        with self.subTest("should working with nested key"):
            self.overwrite_to_file("""
            key:
              nested: value""")

            self.assertEqual({"nested": "value"}, self._get_new_config().get_or_default("key", "default"))
            self.assertEqual("value", self._get_new_config().get_or_default("key.nested", "default"))

    def _get_new_config(self):
        return YamlConfig(self.file)

    def overwrite_to_file(self, content):
        with open(self.file, "w+") as f:
            f.write(content)
            f.flush()
            f.close()

    def assert_file_content(self, content):
        with open(self.file, "r") as f:
            self.assertEqual(content, f.read())
