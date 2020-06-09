from abc import ABC, abstractmethod

class AbstractModel(ABC):
    def __init__(self):
        self.parameters = None
        
    @abstractmethod
    def load_data(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def train_model(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def test_model(self) -> None:
        raise NotImplementedError