"""
Products Page Object (Inventory/Home Page after login).
"""
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger
from typing import List

logger = Logger.get_logger(__name__)


class ProductsPage(BasePage):
    """Page Object for Products/Inventory Page."""
    
    # Locators
    PAGE_TITLE = ".title"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    PRODUCT_ITEM = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[id^='add-to-cart']"
    REMOVE_BUTTON = "button[id^='remove']"
    SORT_DROPDOWN = ".product_sort_container"
    HAMBURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    
    def __init__(self, page: Page):
        """
        Initialize ProductsPage.
        
        Args:
            page: Playwright Page object
        """
        super().__init__(page)
    
    @allure.step("Verify products page loaded")
    def verify_products_page_loaded(self) -> None:
        """Verify products page is loaded."""
        logger.info("Verifying products page loaded")
        self.wait_for_element(self.PAGE_TITLE)
        self.assert_text_contains(self.PAGE_TITLE, "Products")
    
    @allure.step("Get page title")
    def get_page_title(self) -> str:
        """
        Get page title text.
        
        Returns:
            Page title
        """
        return self.get_text(self.PAGE_TITLE)
    
    @allure.step("Get product count")
    def get_product_count(self) -> int:
        """
        Get total number of products displayed.
        
        Returns:
            Number of products
        """
        count = self.get_elements_count(self.PRODUCT_ITEM)
        logger.info(f"Total products: {count}")
        return count
    
    @allure.step("Get all product names")
    def get_all_product_names(self) -> List[str]:
        """
        Get names of all products.
        
        Returns:
            List of product names
        """
        products = self.page.locator(self.PRODUCT_NAME).all_inner_texts()
        logger.info(f"Product names: {products}")
        return products
    
    @allure.step("Get all product prices")
    def get_all_product_prices(self) -> List[str]:
        """
        Get prices of all products.
        
        Returns:
            List of product prices
        """
        prices = self.page.locator(self.PRODUCT_PRICE).all_inner_texts()
        logger.info(f"Product prices: {prices}")
        return prices
    
    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name: str) -> 'ProductsPage':
        """
        Add a specific product to cart.
        
        Args:
            product_name: Name of the product
            
        Returns:
            ProductsPage instance
        """
        logger.info(f"Adding product to cart: {product_name}")
        # Convert product name to button ID
        product_id = product_name.lower().replace(" ", "-")
        button_id = f"#add-to-cart-{product_id}"
        self.click(button_id)
        return self
    
    @allure.step("Remove product from cart: {product_name}")
    def remove_product_from_cart(self, product_name: str) -> 'ProductsPage':
        """
        Remove a specific product from cart.
        
        Args:
            product_name: Name of the product
            
        Returns:
            ProductsPage instance
        """
        logger.info(f"Removing product from cart: {product_name}")
        product_id = product_name.lower().replace(" ", "-")
        button_id = f"#remove-{product_id}"
        self.click(button_id)
        return self
    
    @allure.step("Get cart item count")
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart.
        
        Returns:
            Cart item count
        """
        if self.is_visible(self.SHOPPING_CART_BADGE):
            count = int(self.get_text(self.SHOPPING_CART_BADGE))
            logger.info(f"Cart items: {count}")
            return count
        logger.info("Cart is empty")
        return 0
    
    @allure.step("Click shopping cart")
    def click_shopping_cart(self) -> None:
        """Click shopping cart icon."""
        logger.info("Clicking shopping cart")
        self.click(self.SHOPPING_CART_LINK)
    
    @allure.step("Sort products by: {sort_option}")
    def sort_products(self, sort_option: str) -> 'ProductsPage':
        """
        Sort products using dropdown.
        
        Args:
            sort_option: Sort option value
                - 'az': Name (A to Z)
                - 'za': Name (Z to A)
                - 'lohi': Price (low to high)
                - 'hilo': Price (high to low)
                
        Returns:
            ProductsPage instance
        """
        logger.info(f"Sorting products by: {sort_option}")
        self.select_option(self.SORT_DROPDOWN, value=sort_option)
        return self
    
    @allure.step("Open hamburger menu")
    def open_menu(self) -> 'ProductsPage':
        """
        Open hamburger menu.
        
        Returns:
            ProductsPage instance
        """
        logger.info("Opening hamburger menu")
        self.click(self.HAMBURGER_MENU)
        self.wait_for_element(self.LOGOUT_LINK)
        return self
    
    @allure.step("Logout")
    def logout(self) -> None:
        """Logout from application."""
        logger.info("Logging out")
        self.open_menu()
        self.click(self.LOGOUT_LINK)
    
    @allure.step("Click product: {product_name}")
    def click_product(self, product_name: str) -> None:
        """
        Click on a product to view details.
        
        Args:
            product_name: Name of the product
        """
        logger.info(f"Clicking product: {product_name}")
        self.page.locator(self.PRODUCT_NAME, has_text=product_name).click()
