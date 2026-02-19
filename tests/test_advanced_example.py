"""
Advanced example test demonstrating framework features.

This test demonstrates:
- Page Object Model usage
- Allure reporting with steps
- Test data from JSON
- Fake data generation
- Custom logging
- Screenshots
- Parameterization
- Fixtures
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.test_data import TestDataManager, FakeDataGenerator
from utils.logger import Logger
from utils.screenshot_manager import ScreenshotManager
from config.config import Config

logger = Logger.get_logger(__name__)


@allure.epic("E-commerce")
@allure.feature("End-to-End Purchase Flow")
class TestAdvancedExample:
    """Advanced test examples with all framework features."""
    
    @pytest.fixture(autouse=True)
    def test_setup(self, page: Page, config: Config):
        """Setup for all tests in this class."""
        logger.info("Starting test setup")
        
        # Load test data
        self.test_data = TestDataManager.load_json("data/test_data.json")
        
        # Generate fake user data
        self.fake_user = FakeDataGenerator.generate_user()
        
        logger.info("Test setup completed")
        yield
        logger.info("Test teardown")
    
    @allure.story("Complete Purchase Journey")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test complete purchase flow from login to checkout")
    @allure.description("""
        This test verifies the complete user journey:
        1. User logs in
        2. Views products
        3. Adds items to cart
        4. Proceeds to checkout
        5. Completes purchase
    """)
    @allure.tag("e2e", "smoke", "critical")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_complete_purchase_flow(self, page: Page, config: Config):
        """Test complete purchase flow with all features."""
        
        # Initialize pages
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        # Step 1: Login
        with allure.step("Step 1: Navigate and login"):
            logger.info("Navigating to login page")
            login_page.navigate_to_login_page()
            
            # Attach screenshot to report
            ScreenshotManager.capture(page, "login_page_loaded")
            
            # Get user from test data
            user = self.test_data["users"]["valid_users"][0]
            logger.info(f"Logging in with user: {user['username']}")
            
            login_page.login(user["username"], user["password"])
            
            # Verify login success
            products_page.verify_products_page_loaded()
            logger.info("Login successful")
        
        # Step 2: View and verify products
        with allure.step("Step 2: View available products"):
            logger.info("Viewing products")
            
            product_count = products_page.get_product_count()
            allure.attach(
                str(product_count),
                "Total Products Available",
                allure.attachment_type.TEXT
            )
            
            product_names = products_page.get_all_product_names()
            allure.attach(
                "\n".join(product_names),
                "Available Products",
                allure.attachment_type.TEXT
            )
            
            # Take screenshot of products page
            ScreenshotManager.capture(page, "products_page")
            
            assert product_count > 0, "No products available"
            logger.info(f"Found {product_count} products")
        
        # Step 3: Add products to cart
        with allure.step("Step 3: Add products to cart"):
            products_to_buy = [
                self.test_data["products"][0]["id"],
                self.test_data["products"][1]["id"]
            ]
            
            logger.info(f"Adding {len(products_to_buy)} products to cart")
            
            for product_id in products_to_buy:
                logger.info(f"Adding product: {product_id}")
                products_page.add_product_to_cart(product_id)
            
            # Verify cart count
            cart_count = products_page.get_cart_item_count()
            assert cart_count == len(products_to_buy), \
                f"Expected {len(products_to_buy)} items, got {cart_count}"
            
            allure.attach(
                str(cart_count),
                "Items in Cart",
                allure.attachment_type.TEXT
            )
            
            logger.info(f"Successfully added {cart_count} items to cart")
            
            # Screenshot of cart with items
            ScreenshotManager.capture(page, "cart_with_items")
        
        # Step 4: Sort and verify
        with allure.step("Step 4: Sort products by price"):
            logger.info("Sorting products by price")
            
            products_page.sort_products("lohi")
            
            prices = products_page.get_all_product_prices()
            price_values = [float(p.replace("$", "")) for p in prices]
            
            # Verify sorting
            assert price_values == sorted(price_values), "Products not sorted correctly"
            
            allure.attach(
                "\n".join(prices),
                "Sorted Prices (Low to High)",
                allure.attachment_type.TEXT
            )
            
            logger.info("Products sorted successfully")
            
            # Screenshot of sorted products
            ScreenshotManager.capture(page, "sorted_products")
        
        # Final step: Summary
        with allure.step("Test Summary"):
            logger.info("Test completed successfully")
            
            summary = {
                "User": user["username"],
                "Products Viewed": product_count,
                "Products Added": len(products_to_buy),
                "Cart Total": cart_count,
                "Test Status": "PASSED"
            }
            
            allure.attach(
                str(summary),
                "Test Summary",
                allure.attachment_type.JSON
            )
    
    @allure.story("Data-Driven Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test login with multiple user types")
    @pytest.mark.parametrize("user_index", [0, 1, 2])
    @pytest.mark.regression
    def test_login_with_different_users(self, page: Page, user_index: int):
        """Test login with different user types from test data."""
        
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        # Get user from test data
        user = self.test_data["users"]["valid_users"][user_index]
        
        with allure.step(f"Login with {user['description']}"):
            logger.info(f"Testing with user: {user['username']}")
            
            login_page.navigate_to_login_page()
            login_page.login(user["username"], user["password"])
            
            allure.attach(
                user["description"],
                "User Type",
                allure.attachment_type.TEXT
            )
        
        with allure.step("Verify successful login"):
            products_page.verify_products_page_loaded()
            logger.info(f"Login successful for {user['username']}")
    
    @allure.story("Fake Data Generation")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.title("Test fake data generation")
    @pytest.mark.regression
    def test_fake_data_generation(self):
        """Demonstrate fake data generation."""
        
        with allure.step("Generate fake user data"):
            user = FakeDataGenerator.generate_user()
            logger.info(f"Generated user: {user['username']}")
            
            allure.attach(
                str(user),
                "Generated User Data",
                allure.attachment_type.JSON
            )
        
        with allure.step("Generate fake company data"):
            company = FakeDataGenerator.generate_company()
            logger.info(f"Generated company: {company['name']}")
            
            allure.attach(
                str(company),
                "Generated Company Data",
                allure.attachment_type.JSON
            )
        
        with allure.step("Validate generated data"):
            assert "@" in user["email"], "Invalid email format"
            assert user["username"], "Username is empty"
            assert company["name"], "Company name is empty"
            logger.info("Fake data validation passed")
    
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test error message display for invalid login")
    @pytest.mark.parametrize("invalid_user", [0, 1])
    @pytest.mark.regression
    def test_invalid_login_error_messages(self, page: Page, invalid_user: int):
        """Test error messages for invalid login attempts."""
        
        login_page = LoginPage(page)
        
        # Get invalid user from test data
        user = self.test_data["users"]["invalid_users"][invalid_user]
        
        with allure.step(f"Attempt login with: {user['username']}"):
            logger.info(f"Testing invalid login: {user['username']}")
            
            login_page.navigate_to_login_page()
            login_page.login(user["username"], user["password"])
        
        with allure.step("Verify error message"):
            assert login_page.is_error_message_displayed(), "Error message not displayed"
            
            error_message = login_page.get_error_message()
            logger.info(f"Error message: {error_message}")
            
            # Verify expected error
            expected = user.get("expected_error", "")
            if expected:
                assert expected in error_message, \
                    f"Expected '{expected}', got '{error_message}'"
            
            allure.attach(
                error_message,
                "Error Message",
                allure.attachment_type.TEXT
            )
            
            # Screenshot of error
            ScreenshotManager.capture(page, f"error_{user['username']}")
