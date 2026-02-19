"""
Soft Assertions Examples.

This demonstrates how to use soft assertions to:
- Continue test execution even after failures
- Collect all failures and report at the end
- Use with Playwright, API, and Mobile tests
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.soft_assert import SoftAssert
from config.config import Config


@allure.epic("Soft Assertions")
@allure.feature("Web Testing with Soft Assertions")
class TestSoftAssertions:
    """Demonstrate soft assertions in different scenarios."""
    
    @allure.story("Product Page Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test products page with soft assertions")
    @allure.description("""
        This test demonstrates soft assertions:
        - Multiple assertions are checked
        - Test continues even if some fail
        - All failures are reported at the end
    """)
    @pytest.mark.regression
    def test_products_with_soft_assertions(
        self,
        page: Page,
        config: Config,
        soft_assert: SoftAssert
    ):
        """Test products page using soft assertions."""
        
        # Login first
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        with allure.step("Login"):
            login_page.navigate_to_login_page()
            login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
        
        with allure.step("Verify products page with soft assertions"):
            # Multiple assertions - all will be checked
            soft_assert.assert_true(
                "inventory.html" in page.url,
                "URL should contain 'inventory.html'"
            )
            
            page_title = products_page.get_page_title()
            soft_assert.assert_equal(
                page_title,
                "Products",
                "Page title should be 'Products'"
            )
            
            product_count = products_page.get_product_count()
            soft_assert.assert_greater(
                product_count,
                0,
                "Should have at least one product"
            )
            soft_assert.assert_equal(
                product_count,
                6,
                "Should have exactly 6 products"
            )
            
            # Get all product names
            product_names = products_page.get_all_product_names()
            soft_assert.assert_true(
                isinstance(product_names, list),
                "Product names should be a list"
            )
            soft_assert.assert_true(
                len(product_names) > 0,
                "Product names list should not be empty"
            )
            
            # Check specific product exists
            soft_assert.assert_in(
                "Sauce Labs Backpack",
                product_names,
                "Should have 'Sauce Labs Backpack' product"
            )
            
            # Check cart badge initially not visible
            cart_count = products_page.get_cart_item_count()
            soft_assert.assert_equal(
                cart_count,
                0,
                "Cart should be empty initially"
            )
            
            # All assertions will be checked, and failures reported at the end
            soft_assert.assert_all()
    
    @allure.story("Form Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test form fields with soft assertions")
    @pytest.mark.regression
    def test_form_validation_with_soft_assertions(
        self,
        page: Page,
        soft_assert: SoftAssert
    ):
        """Test form field validation using soft assertions."""
        
        login_page = LoginPage(page)
        
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Validate login page elements"):
            # Verify all form elements are present
            soft_assert.assert_true(
                login_page.is_visible(login_page.USERNAME_INPUT),
                "Username field should be visible"
            )
            
            soft_assert.assert_true(
                login_page.is_visible(login_page.PASSWORD_INPUT),
                "Password field should be visible"
            )
            
            soft_assert.assert_true(
                login_page.is_visible(login_page.LOGIN_BUTTON),
                "Login button should be visible"
            )
            
            soft_assert.assert_true(
                login_page.is_visible(login_page.LOGO),
                "Logo should be visible"
            )
            
            # Check page URL
            soft_assert.assert_contains(
                page.url,
                "saucedemo.com",
                "URL should contain 'saucedemo.com'"
            )
            
            # Check page title
            page_title = page.title()
            soft_assert.assert_contains(
                page_title,
                "Swag Labs",
                "Page title should contain 'Swag Labs'"
            )
            
            # Report all validation results
            soft_assert.assert_all()
    
    @allure.story("Multiple Actions")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test multiple product operations with soft assertions")
    @pytest.mark.regression
    def test_multiple_products_soft_assertions(
        self,
        page: Page,
        config: Config,
        soft_assert: SoftAssert
    ):
        """Test adding multiple products with soft assertions."""
        
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        # Login
        login_page.navigate_to_login_page()
        login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
        
        products_to_test = [
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-bolt-t-shirt"
        ]
        
        with allure.step("Add multiple products and verify"):
            for i, product_id in enumerate(products_to_test, 1):
                with allure.step(f"Add product {i}: {product_id}"):
                    products_page.add_product_to_cart(product_id)
                    
                    # Verify cart count after each addition
                    cart_count = products_page.get_cart_item_count()
                    soft_assert.assert_equal(
                        cart_count,
                        i,
                        f"Cart should have {i} item(s) after adding {product_id}"
                    )
        
        with allure.step("Verify final cart state"):
            final_count = products_page.get_cart_item_count()
            soft_assert.assert_equal(
                final_count,
                len(products_to_test),
                f"Final cart count should be {len(products_to_test)}"
            )
            
            # Report all assertions
            soft_assert.assert_all()
    
    @allure.story("Sorting Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test product sorting with soft assertions")
    @pytest.mark.regression
    def test_sorting_with_soft_assertions(
        self,
        page: Page,
        config: Config,
        soft_assert: SoftAssert
    ):
        """Test product sorting using soft assertions."""
        
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        # Login
        login_page.navigate_to_login_page()
        login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
        
        with allure.step("Test sorting by name A-Z"):
            products_page.sort_products("az")
            product_names = products_page.get_all_product_names()
            sorted_names = sorted(product_names)
            
            soft_assert.assert_equal(
                product_names,
                sorted_names,
                "Products should be sorted A-Z"
            )
        
        with allure.step("Test sorting by name Z-A"):
            products_page.sort_products("za")
            product_names = products_page.get_all_product_names()
            reverse_sorted = sorted(product_names, reverse=True)
            
            soft_assert.assert_equal(
                product_names,
                reverse_sorted,
                "Products should be sorted Z-A"
            )
        
        with allure.step("Test sorting by price low to high"):
            products_page.sort_products("lohi")
            prices = products_page.get_all_product_prices()
            price_values = [float(p.replace("$", "")) for p in prices]
            sorted_prices = sorted(price_values)
            
            soft_assert.assert_equal(
                price_values,
                sorted_prices,
                "Prices should be sorted low to high"
            )
        
        with allure.step("Test sorting by price high to low"):
            products_page.sort_products("hilo")
            prices = products_page.get_all_product_prices()
            price_values = [float(p.replace("$", "")) for p in prices]
            reverse_sorted_prices = sorted(price_values, reverse=True)
            
            soft_assert.assert_equal(
                price_values,
                reverse_sorted_prices,
                "Prices should be sorted high to low"
            )
        
        # Check all sorting validations
        soft_assert.assert_all()
    
    @allure.story("Negative Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test invalid login with soft assertions")
    @pytest.mark.regression
    def test_invalid_login_soft_assertions(
        self,
        page: Page,
        soft_assert: SoftAssert
    ):
        """Test invalid login scenarios with soft assertions."""
        
        login_page = LoginPage(page)
        
        with allure.step("Test empty credentials"):
            login_page.navigate_to_login_page()
            login_page.click_login_button()
            
            soft_assert.assert_true(
                login_page.is_error_message_displayed(),
                "Error message should be displayed for empty credentials"
            )
        
        with allure.step("Test invalid username"):
            page.reload()
            login_page.login("invalid_user", "invalid_pass")
            
            soft_assert.assert_true(
                login_page.is_error_message_displayed(),
                "Error message should be displayed for invalid credentials"
            )
            
            error_text = login_page.get_error_message()
            soft_assert.assert_contains(
                error_text,
                "Epic sadface",
                "Error message should contain 'Epic sadface'"
            )
        
        with allure.step("Test locked user"):
            page.reload()
            login_page.login("locked_out_user", "secret_sauce")
            
            soft_assert.assert_true(
                login_page.is_error_message_displayed(),
                "Error message should be displayed for locked user"
            )
            
            error_text = login_page.get_error_message()
            soft_assert.assert_contains(
                error_text.lower(),
                "locked out",
                "Error message should mention user is locked"
            )
        
        # Verify all error scenarios
        soft_assert.assert_all()


@allure.epic("Soft Assertions")
@allure.feature("Data Validation")
class TestDataValidationSoftAssert:
    """Test data validation with soft assertions."""
    
    @allure.story("List Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test list operations with soft assertions")
    @pytest.mark.regression
    def test_list_validation(self, soft_assert: SoftAssert):
        """Test list validation with soft assertions."""
        
        test_list = [1, 2, 3, 4, 5]
        
        with allure.step("Validate list operations"):
            soft_assert.assert_true(
                isinstance(test_list, list),
                "Should be a list"
            )
            
            soft_assert.assert_equal(
                len(test_list),
                5,
                "List should have 5 elements"
            )
            
            soft_assert.assert_in(
                3,
                test_list,
                "List should contain 3"
            )
            
            soft_assert.assert_not_in(
                10,
                test_list,
                "List should not contain 10"
            )
            
            soft_assert.assert_equal(
                test_list[0],
                1,
                "First element should be 1"
            )
            
            soft_assert.assert_equal(
                test_list[-1],
                5,
                "Last element should be 5"
            )
            
            soft_assert.assert_all()
