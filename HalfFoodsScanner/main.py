from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class BasicPurchaseInfo:

    customer_name: str
    purchase_date: datetime
    quantity: int

    def __str__(self):
        return f"""
            Customer Name: {self.customer_name}
            Date of Purchase: {self.purchase_date}
            Quantity: {self.quantity}
            """

class DataLoader(ABC):

    @abstractmethod
    def load_data(self, data_path: str) -> None:
        pass

    def get_basic_purchase_info(self) -> BasicPurchaseInfo:
        pass

class TextLoader(DataLoader):

    def load_data(self, data_path: str) -> None:
        with open(data_path) as f:
            
            # retrieve customer information from first line
            # Line format: [MMDDYYYY][Name]
            first_line = f.readline()
            self.purchase_date = datetime.strptime(first_line[:8], "%m%d%Y")
            self.name = first_line[8:]

            # get products
            self.product_count = 0
            for line in f.readlines():
                self.product_count += 1

    def get_basic_purchase_info(self) -> BasicPurchaseInfo:
        return BasicPurchaseInfo(self.name, self.purchase_date, self.product_count)

def init_product_key() -> dict[str, str]:
    product_key = {
        "BEVG": "Beverages",
        "BAKE": "Baked Goods",
        "CANF": "Canned Foods",
        "CNSB": "Condiments/Spices/Baking",
        "SNCN": "Snacks/Candy",
        "DREG": "Dairy/Eggs",
        "FRZN": "Frozen Foods",
        "FRVG": "Fruits/Vegetables",
        "GRPA": "Grains/Pastas",
        "MTSF": "Meat/Seafood",
        "MISC": "Misc",
        }
    return product_key

def main():

    # load product key
    product_key = init_product_key()

    # menu
    while True:
        print("""
        1: Print basic data summary
        2: Print detailed data summary
        3: Get subtypes for product type
        4: Add product type
        9: Quit

        :

        """)
        selection = input()
        if selection == "1":
            print_basic_data(product_key)
        if selection == "9":
            break


def print_basic_data(product_key: dict[str, str]) -> None:

    try:
        data_loader = load_data()
        print(data_loader.get_basic_purchase_info())
    except FileNotFoundError:
        print("File not found! Press Enter to return to menu.")
        input()
        os.system('cls' if os.name == 'nt' else 'clear')



def load_data() -> DataLoader:
    path_to_data = input("input path: ")

    # based on path, use a different loader
    datareader = TextLoader()
    datareader.load_data(path_to_data)
    return datareader

if __name__ == "__main__":
    main()
