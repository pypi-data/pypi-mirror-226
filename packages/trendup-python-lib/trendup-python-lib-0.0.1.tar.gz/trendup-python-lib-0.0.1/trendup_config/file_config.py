from abc import abstractmethod


class FileConfig:

    @abstractmethod
    def get_or_default(self, key: str, default: any) -> any:
        pass
