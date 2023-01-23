from dataclasses import dataclass
from datetime import datetime

@dataclass
class PurchaseInfo:
    """This class represents the PurchaseInfo extracted from a data source.

    customer_name: Name of the customer
    purchase_date: Date when purchase was made
    quantity: Total quantity of purchase. (Note: includes items purchased with an invalid product type.)
    product_type_history: For each product type, contains a list of IDs.
    subtype_lookup: For each product type, a list of subtypes.
    """

    customer_name: str
    purchase_date: datetime
    quantity: int
    product_type_history: dict[str, list[str]]
    subtype_lookup: dict[str, set[str]]


    def get_basic_purchase_information(self) -> str:
        """
        Returns the purchase information required by Question 1 as a formattted string.

        :return: Formatted string of the basic purchasing information.
        """
        return f"""
            Customer Name: {self.customer_name}
            Date of Purchase: {self.purchase_date}
            Quantity: {self.quantity}
            """
    
    def get_advanced_purchase_information(self) -> str:
        """
        Returns the additional information required by Question 2 as a formattted string.

        :return: Formatted string of the additional purchasing information.
        """
        str_ret = []

        # While formatting string, search for most common product type
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
        """
        Returns all subtypes for a given product type in the customer's purchase information.

        :product_type: The product type to search for
        :returns: A string containing all the subtypes, or a string if that product type is not found in the
                 purchase order.
        """
        if product_type in self.subtype_lookup:
            return "".join(["Subtypes: ", ",".join(self.subtype_lookup[product_type])])
        else:
            return "Product Type not found"
