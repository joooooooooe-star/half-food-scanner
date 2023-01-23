from abc import ABC, abstractmethod
from HalfFoodsScanner.classes.purchaseinfo import PurchaseInfo

class DataLoader(ABC):

    @abstractmethod
    def load_data(self, data_path: str) -> PurchaseInfo:
        pass
