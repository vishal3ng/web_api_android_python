"""
Products page test suite.
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.config import Config


@allure.epic("E-commerce")
@allure.feature("Products")
class TestProducts:
    """Test cases for products functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page, config: Config):
        """Setup method - login before each test."""
        login_page = LoginPage(page)
        login_page.navigate_to_login_page()
        login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
        
        # Wait for products page to load
        products_page = ProductsPage(page)
        products_page.verify_products_page_loaded()
    
    @allure.story("Product Display")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test products are displayed after login")
    @allure.description("Verify products are visible and displayed correctly on products page")
    @pytest.mark.smoke
    def test_products_displayed(self, page: Page):
        """Test products are displayed on the page."""
        # Arrange
        products_page = ProductsPage(page)
        
        # Act & Assert
        with allure.step("Verify products page title"):
            title = products_page.get_page_title()
            assert "Products" in title
        
        with allure.step("Verify products are displayed"):
            product_count = products_page.get_product_count()
            assert product_count > 0, "No products displayed"
            allure.attach(str(product_count), "Product Count", allure.attachment_type.TEXT)
    
    @allure.story("Shopping Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test adding product to cart")
    @allure.description("Verify user can add products to shopping cart")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_add_product_to_cart(self, page: Page):
        """Test adding a product to cart."""
        # Arrange
        products_page = ProductsPage(page)
        product_name = "sauce-labs-backpack"
        
        # Act
        with allure.step(f"Add product '{product_name}' to cart"):
            products_page.add_product_to_cart(product_name)
        
        # Assert
        with allure.step("Verify cart badge shows 1 item"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 1, f"Expected 1 item in cart, got {cart_count}"
    
    @allure.story("Shopping Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test adding multiple products to cart")
    @allure.description("Verify user can add multiple products to shopping cart")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_add_multiple_products_to_cart(self, page: Page):
        """Test adding multiple products to cart."""
        # Arrange
        products_page = ProductsPage(page)
        products_to_add = ["sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-bolt-t-shirt"]
        
        # Act
        with allure.step("Add multiple products to cart"):
            for product in products_to_add:
                products_page.add_product_to_cart(product)
        
        # Assert
        with allure.step(f"Verify cart badge shows {len(products_to_add)} items"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == len(products_to_add)
    
    @allure.story("Shopping Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test removing product from cart")
    @allure.description("Verify user can remove products from shopping cart")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_remove_product_from_cart(self, page: Page):
        """Test removing a product from cart."""
        # Arrange
        products_page = ProductsPage(page)
        product_name = "sauce-labs-backpack"
        
        # Act
        with allure.step("Add product to cart"):
            products_page.add_product_to_cart(product_name)
        
        with allure.step("Remove product from cart"):
            products_page.remove_product_from_cart(product_name)
        
        # Assert
        with allure.step("Verify cart is empty"):
            cart_count = products_page.get_cart_item_count()
            assert cart_count == 0
    
    @allure.story("Product Sorting")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test sorting products by name A-Z")
    @allure.description("Verify products can be sorted alphabetically")
    @pytest.mark.regression
    def test_sort_products_by_name_az(self, page: Page):
        """Test sorting products by name A to Z."""
        # Arrange
        products_page = ProductsPage(page)
        
        # Act
        with allure.step("Sort products A to Z"):
            products_page.sort_products("az")
        
        with allure.step("Get product names"):
            product_names = products_page.get_all_product_names()
        
        # Assert
        with allure.step("Verify products are sorted alphabetically"):
            assert product_names == sorted(product_names)
            allure.attach(str(product_names), "Sorted Products", allure.attachment_type.TEXT)
    
    @allure.story("Product Sorting")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test sorting products by name Z-A")
    @allure.description("Verify products can be sorted in reverse alphabetical order")
    @pytest.mark.regression
    def test_sort_products_by_name_za(self, page: Page):
        """Test sorting products by name Z to A."""
        # Arrange
        products_page = ProductsPage(page)
        
        # Act
        with allure.step("Sort products Z to A"):
            products_page.sort_products("za")
        
        with allure.step("Get product names"):
            product_names = products_page.get_all_product_names()
        
        # Assert
        with allure.step("Verify products are sorted in reverse"):
            assert product_names == sorted(product_names, reverse=True)
    
    @allure.story("Product Sorting")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test sorting products by price low to high")
    @allure.description("Verify products can be sorted by price ascending")
    @pytest.mark.regression
    def test_sort_products_by_price_low_to_high(self, page: Page):
        """Test sorting products by price low to high."""
        # Arrange
        products_page = ProductsPage(page)
        
        # Act
        with allure.step("Sort products by price (low to high)"):
            products_page.sort_products("lohi")
        
        with allure.step("Get product prices"):
            prices = products_page.get_all_product_prices()
            # Convert to float for comparison
            price_values = [float(price.replace("$", "")) for price in prices]
        
        # Assert
        with allure.step("Verify products are sorted by price"):
            assert price_values == sorted(price_values)
            allure.attach(str(prices), "Sorted Prices", allure.attachment_type.TEXT)
    
    @allure.story("Logout")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test user logout")
    @allure.description("Verify user can logout successfully")
    @pytest.mark.smoke
    def test_logout(self, page: Page):
        """Test user logout functionality."""
        # Arrange
        products_page = ProductsPage(page)
        login_page = LoginPage(page)
        
        # Act
        with allure.step("Logout from application"):
            products_page.logout()
        
        # Assert
        with allure.step("Verify user is redirected to login page"):
            login_page.verify_login_page_loaded()
            assert page.url == "https://www.saucedemo.com/"
