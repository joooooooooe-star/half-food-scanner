from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import os

def error_checker(str_one: str, str_two: str) -> bool:
    
    error_count = 0
    for i, ch in enumerate(str_one):
        if str_two[i] != ch:
            error_count += 1
        if error_count > 2:
            return False
    return True

@dataclass
class PurchaseInfo:

    customer_name: str
    purchase_date: datetime
    quantity: int
    product_type_history: dict[str, list[str]]
    subtype_lookup: dict[str, set[str]]


    def get_basic_purchase_information(self) -> str:
        return f"""
            Customer Name: {self.customer_name}
            Date of Purchase: {self.purchase_date}
            Quantity: {self.quantity}
            """
    
    def get_advanced_purchase_information(self) -> str:
        
        str_ret = []
        max_count = 0
        max_str = "None"
        for product_type, id_list in self.product_type_history.items():
            item_list = ", ".join(id_list)
            str_ret.append(f"{product_type} -- {len(id_list)} items: {item_list}")
            if (id_count := len(id_list)) > max_count:
                max_count = id_count
                max_str = product_type
        str_ret.append("\n")
        str_ret.append(f"Most common product type: {max_str}")

        return "\n".join(str_ret)

    def get_subtypes(self, product_type: str) -> str:
        if product_type in self.subtype_lookup:
            return "".join(["Subtypes: ", ",".join(self.subtype_lookup[product_type])])
        else:
            return "Product Type not found"

class DataLoader(ABC):

    @abstractmethod
    def load_data(self, data_path: str) -> PurchaseInfo:
        pass

class TextLoader(DataLoader):

    def load_data(self, product_key: dict[str, str], data_path: str) -> PurchaseInfo:
        with open(data_path) as f:
            
            # retrieve customer information from first line
            # Line format: [MMDDYYYY][Name]
            first_line = f.readline()
            purchase_date = datetime.strptime(first_line[:8], "%m%d%Y")
            customer_name = first_line[8:]

            product_type_history = defaultdict(list)
            subtype_lookup = defaultdict(set) 

            # get products
            product_count = 0
            for line in f.readlines():
                product_type = line[:4]
                subtype = line[4:10]
                product_id = line[10:].strip()
                if product_type in product_key:
                    product_type_history[product_type].append(product_id)
                    subtype_lookup[product_type].add(subtype)
                
                # adjust for error
                else:
                    for product_key_id in product_key:
                        if error_checker(product_type, product_key_id):
                            corrected_product_type = product_key_id
                            product_type_history[corrected_product_type].append(product_id)
                            subtype_lookup[corrected_product_type].add(subtype)
                            break
                        
                product_count += 1
        
        return PurchaseInfo(customer_name, purchase_date, product_count, product_type_history, subtype_lookup)

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
        2: Detailed Menu
        3: Add product type
        9: Quit

        """)
        selection = input()
        match selection:
            case "1":
                print_basic_data(product_key)
            case "2":
                detailed_menu(product_key)
            case "9":
                break
            case _:
                print("Invalid selection. Press Enter to retry.")
                input()
                
        os.system("cls" if os.name == "nt" else "clear")

def detailed_menu(product_key: dict[str, str]):
    purchase_info = load_data(product_key)

    while True:
        print("""
        1: Print detailed order summary
        2: View subtypes
        
        9: Return
        
        """)
        selection = input()
        match selection:
            case "1":
                print(purchase_info.get_advanced_purchase_information())
                print("\n Press Enter to Return...")
                input()
            case "2":
                print("Type one of the listed product types:")
                for i, product_type in enumerate(selection_key := sorted(list(product_key.keys()))):
                    print(f"{i}: {product_type}")
                product_type_num = int(input())
                print(purchase_info.get_subtypes(selection_key[product_type_num]))
                print("\n Press Enter to Return...")
                input()
                
            case "9":
                print("Returning to Main Menu...")
                break




def print_basic_data(product_key: dict[str, str]) -> None:

    try:
        purchase_info = load_data(product_key)
        print(purchase_info.get_basic_purchase_information())
        print("\n Press Enter to Return...")
        input()
    except FileNotFoundError:
        print("File not found! Press Enter to return to menu.")
        input()
        os.system('cls' if os.name == 'nt' else 'clear')



def load_data(product_key) -> PurchaseInfo:
    path_to_data = input("input path: ")

    # based on path, use a different loader
    datareader = TextLoader()
    purchase_info = datareader.load_data(product_key, path_to_data)
    return purchase_info

if __name__ == "__main__":
    main()
