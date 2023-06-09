from selenium import webdriver
from selenium.webdriver.common.by import By

import unittest
import random

from page_objects.login_page import Login_Page
from page_objects.inventory_page import Inventory_Page
from page_objects.checkout_page import Checkout_Page

class Test_Checkout(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        
        self.login_page = Login_Page(self.driver)
        self.inventory_page = Inventory_Page(self.driver)
        self.checkout_page = Checkout_Page(self.driver)

        self.login_page.complete_login("standard_user", "secret_sauce")

    def test_checkout(self):
        # access cart and check that has no items
        self.inventory_page.reset_app_state()
        products_quantity_in_cart = random.randint(1, 6)
        products_in_cart = []
        products_index_list = []
        for i in range(0, products_quantity_in_cart):
            # choose a random product index that is not already on the products_in_cart
            product_index = -1
            while(product_index == -1 or product_index in products_index_list):
                product_index = random.randint(0, 5)
            products_index_list.append(product_index)
            # add product index, title and value to products_in_cart array
            products_in_cart.append({
                "index": product_index,
                "title" : self.inventory_page.get_inventory_item_title_by_index(product_index),
                "price" : self.inventory_page.get_inventory_item_price_by_index(product_index)
            })
            # add product to cart
            self.inventory_page.add_item_to_cart_by_index(product_index)
        
        # access cart and check it has products_in_cart
        self.inventory_page.access_cart()
        total_value = 0
        for product in products_in_cart:
            self.assertIn(
                product["title"],
                self.inventory_page.get_inventory_items_titles()
            )
            
            self.assertIn(
                product["price"],
                self.inventory_page.get_inventory_items_prices()
            )

            total_value += product["price"]

        # checkout
        self.inventory_page.go_to_checkout()

        # fulfill checkout
        self.checkout_page.fulfill_checkout_informantion('Carlos', 'Montoya', '123')
        
        # validate total price without tax
        self.assertEqual( 
            self.checkout_page.get_total_value(), 
            total_value, 
            'Total item values without tax does not match.' 
        )

        # click finish
        self.checkout_page.finish_overview()
        # validate success message
        assert(
            self.checkout_page.get_checkout_status_message(),
            'Checkout: Complete!',
            'Status message incorrect.'
        )

        assert(
            self.checkout_page.get_checkout_complete_message(),
            'Thank you for your order!',
            'Thank message incorrect.'
        )
        
        

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()