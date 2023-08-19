import os

import yaml

from trendup_config.file_config import FileConfig


class YamlConfig(FileConfig):

    def __init__(self, path: str):
        self.file_path = path
        self.yml = self._load_file_to_yml_cfg(path)

    def get_or_default(self, key: str, default: any) -> any:
        keys = key.split(".")
        current = self.yml

        for (index, key) in enumerate(keys):
            if key not in current:
                current[key] = default if index == len(keys) - 1 else {}
                self.save()

            current = current[key]

        return current

    def _load_file_to_yml_cfg(self, path):
        self._create_file_if_not_exist(path)
        return yaml.load(open(path, "r"), Loader=yaml.FullLoader) or {}

    def save(self):
        with open(self.file_path, "w+") as f:
            yaml.dump(self.yml, f, default_flow_style=False)

    def _create_file_if_not_exist(self, path: str):
        if not os.path.exists(path):
            open(path, "w+").close()
