from abc import ABC, abstractmethod


class BaseStore(ABC):
    def get_features(self):
        pass
