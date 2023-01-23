from HalfFoodsScanner.classes.purchaseinfo import PurchaseInfo
from HalfFoodsScanner.dataloaders.textloader import TextLoader
import os

def init_product_key() -> dict[str, str]:
    """Creates a default product lookup key that contains the default product codes and descriptions."""
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
        os.system('cls' if os.name == 'nt' else 'clear')
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
            case "3":
                product_key = add_product_type(product_key)
            case "9":
                break
            case _:
                input("Invalid selection. Press Enter to retry...")
                

def detailed_menu(product_key: dict[str, str]):
    purchase_info = load_data(product_key)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("""
        1: Print detailed order summary
        2: View subtypes
        
        9: Return
        
        """)
        selection = input()
        match selection:
            case "1":
                print(purchase_info.get_advanced_purchase_information())
                input("\n Press Enter to Return...")
            case "2":
                print("Type one of the listed product types:")
                for i, product_type in enumerate(selection_key := sorted(list(product_key.keys()))):
                    print(f"{i}: {product_type}")
                product_type_num = int(input())
                print(purchase_info.get_subtypes(selection_key[product_type_num]))
                input("\n Press Enter to Return...")
                
            case "9":
                input("Returning to Main Menu, press Enter to Return...")
                break


def print_basic_data(product_key: dict[str, str]) -> None:

    try:
        purchase_info = load_data(product_key)
        print(purchase_info.get_basic_purchase_information())
        input("\n Press Enter to Return...")
    except FileNotFoundError:
        input("File not found! Press Enter to Return...")


def load_data(product_key) -> PurchaseInfo:
    path_to_data = input("Input path to data: ")

    # based on path, use a different loader
    datareader = TextLoader()
    purchase_info = datareader.load_data(product_key, path_to_data)
    return purchase_info


def add_product_type(product_key: dict[str, str]) -> dict[str, str]:
    product_key_id = input("Input four letter product abbreivation: ")
    if len(product_key_id) != 4:
        input("Product key is not four letters. Press Enter to Return...")
    product_key_def = input("Input description of product: ")
    product_key[product_key_id] = product_key_def
    return product_key


if __name__ == "__main__":
    main()
