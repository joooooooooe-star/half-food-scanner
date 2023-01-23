from collections import defaultdict
from datetime import datetime

from HalfFoodsScanner.dataloaders.dataloader import DataLoader
from HalfFoodsScanner.dataloaders.helpers import error_checker
from HalfFoodsScanner.classes.purchaseinfo import PurchaseInfo

class TextLoader(DataLoader):

    def load_data(self, product_key: dict[str, str], data_path: str) -> PurchaseInfo:
        with open(data_path) as f:
            
            # retrieve customer information from first line
            # Line format: [MMDDYYYY][Name]
            first_line = f.readline()
            purchase_date = datetime.strptime(first_line[:8], "%m%d%Y")
            customer_name = first_line[8:].strip()

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