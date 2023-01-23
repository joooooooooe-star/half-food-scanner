from abc import ABC, abstractmethod
from HalfFoodsScanner.classes.purchaseinfo import PurchaseInfo

class DataLoader(ABC):
    """An abstract class to be used if there needs to be some other loading method
    such as a URL or JSON file.
    """

    @abstractmethod
    def load_data(self, data_path: str) -> PurchaseInfo:
        """Abstract loading method

        Args:
            data_path (str): Path to the data

        Returns:
            PurchaseInfo: After data is parsed, return purchase info
        """
        pass
