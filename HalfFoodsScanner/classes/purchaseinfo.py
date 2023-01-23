from dataclasses import dataclass
from datetime import datetime

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