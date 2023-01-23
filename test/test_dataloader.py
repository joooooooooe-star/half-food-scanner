import datetime
import random
import string
import unittest
from unittest import mock
from unittest.mock import patch, mock_open

from HalfFoodsScanner.dataloaders.textloader import TextLoader
from HalfFoodsScanner.classes.purchaseinfo import PurchaseInfo


class TestTextLoaderMethods(unittest.TestCase):

    # SETUP
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
    name_line = "05011984Joseph"

    def test_one_of_each_product(self):
        """Tests that each product generates and contributes to the quantity.
        """

        # SETUP
        mock_list = [self.name_line]
        for key in self.product_key.keys():
            subtype = "".join(random.choices(string.ascii_uppercase, k=6))
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"{key}{subtype}{id}")

        mock_data = "\n".join(mock_list)

        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(11, result.quantity)

    def test_one_valid_one_invalid_product(self):
        """Tests that an invalid product name still adds to the quantity
        """

        # SETUP
        mock_list = [self.name_line]
        subtype = "".join(random.choices(string.ascii_uppercase, k=6))
        id = "".join(random.choices(string.ascii_uppercase, k=20))
        mock_list.append(f"FRZN{subtype}{id}")
        mock_list.append(f"ARZN{subtype}{id}")

        mock_data = "\n".join(mock_list)

        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(2, result.quantity)

    def test_name_and_date(self):
        """Tests that the date is correct"""

        # SETUP
        mock_list = [self.name_line]
        subtype = "".join(random.choices(string.ascii_uppercase, k=6))
        id = "".join(random.choices(string.ascii_uppercase, k=20))
        mock_list.append(f"FRZN{subtype}{id}")
        mock_data = "\n".join(mock_list)

        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(datetime.datetime(1984, 5, 1),
                             result.purchase_date)
            self.assertEqual("Joseph", result.customer_name)

    def test_most_common(self):
        """Tests that the most common product type is correct"""

        # SETUP
        mock_list = [self.name_line]

        biggest = 0
        biggest_cat = ""
        for key in self.product_key.keys():
            randomizer = random.randrange(50)
            if randomizer > biggest:
                biggest = randomizer
                biggest_cat = key
            for _ in range(randomizer):
                subtype = "".join(random.choices(string.ascii_uppercase, k=6))
                id = "".join(random.choices(string.ascii_uppercase, k=20))
                mock_list.append(f"{key}{subtype}{id}")

        mock_data = "\n".join(mock_list)

        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(
                self.product_key[biggest_cat],
                result.get_advanced_purchase_information(self.product_key)[1])

    def test_subtype_checker_standard(self):
        """Tests that all subtypes show up"""

        # SETUP
        mock_list = [self.name_line]
        mock_subtypes = ["AAAAAA", "BBBBBB", "CCCCCC", "DDDDDD"]
        for sub in mock_subtypes:
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"FRZN{sub}{id}")

        mock_data = "\n".join(mock_list)
        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(set(mock_subtypes), result.subtype_lookup["FRZN"])

    def test_subtype_checker_duplicate(self):
        """Tests that all subtypes show up"""

        # SETUP
        mock_list = [self.name_line]
        mock_subtypes = ["AAAAAA", "BBBBBB", "BBBBBB", "CCCCCC", "DDDDDD"]
        for sub in mock_subtypes:
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"FRZN{sub}{id}")

        mock_data = "\n".join(mock_list)
        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(set(mock_subtypes), result.subtype_lookup["FRZN"])

    def test_unique_ids(self):
        """Tests that all uniques are added to data class"""

        # SETUP
        mock_list = [self.name_line]
        mock_types = ["GRPA", "MISC"]
        sorted_uniques_one = []
        sorted_uniques_two = []
        for _ in range(100):
            ptype = random.choice(mock_types)
            stype = "".join(random.choices(string.ascii_uppercase, k=6))
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"{ptype}{stype}{id}")
            if ptype == "GRPA":
                sorted_uniques_one.append(id)
            else:
                sorted_uniques_two.append(id)

        sorted_uniques_one.sort()
        sorted_uniques_two.sort()
        mock_data = "\n".join(mock_list)
        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(sorted_uniques_one,
                             sorted(result.product_type_history["GRPA"]))
            self.assertEqual(sorted_uniques_two,
                             sorted(result.product_type_history["MISC"]))

    def test_invalid_product_type(self):
        """Tests that invalid product keys will not be considered for most common"""

        # SETUP
        mock_list = [self.name_line]
        for i in range(100):
            if i > 80:
                ptype = "GRPA"
            else:
                ptype = "FFFF"
            stype = "".join(random.choices(string.ascii_uppercase, k=6))
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"{ptype}{stype}{id}")

        mock_data = "\n".join(mock_list)
        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(
                self.product_key["GRPA"],
                result.get_advanced_purchase_information(self.product_key)[1])

    def test_corruption(self):
        """Tests simple case for single character corruption"""

        # SETUP
        mock_list = [self.name_line]
        mock_types = ["GRPA", "GRKA", "BRPA", "GFPA", "GRPX"]

        for _ in range(100):
            ptype = random.choice(mock_types)
            stype = "".join(random.choices(string.ascii_uppercase, k=6))
            id = "".join(random.choices(string.ascii_uppercase, k=20))
            mock_list.append(f"{ptype}{stype}{id}")

        mock_data = "\n".join(mock_list)
        my_loader = TextLoader()
        mock_open = mock.mock_open(read_data=mock_data)
        with mock.patch("builtins.open", mock_open):
            result: PurchaseInfo = my_loader.load_data(self.product_key,
                                                       "filename")
            self.assertEqual(100, len(result.product_type_history["GRPA"]))


if __name__ == "__main__":
    unittest.main()