"""
Complete Framework Demonstration.

This test file demonstrates ALL framework capabilities:
- Web testing (Playwright)
- API testing
- Soft assertions
- Email notifications
- Allure reporting
- Multiple test types
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from api.api_client import APIClient
from utils.soft_assert import SoftAssert
from utils.email_notification import EmailNotification
from config.config import Config


@allure.epic("Complete Framework Demonstration")
@allure.feature("All Features Combined")
class TestCompleteFramework:
    """
    Comprehensive test demonstrating all framework features.
    
    This class shows:
    1. Web testing with Playwright
    2. API testing
    3. Soft assertions
    4. Email notifications
    5. Allure reporting
    6. Data-driven testing
    7. Fixtures usage
    """
    
    @allure.story("End-to-End with All Features")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Complete E2E test with web, API, and soft assertions")
    @allure.description("""
        This comprehensive test demonstrates:
        - Web UI testing
        - API integration
        - Soft assertions
        - Email notifications on failure
        - Complete Allure reporting
        - Screenshot capture
        - Test data management
    """)
    @allure.tag("e2e", "smoke", "demo")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_complete_framework_demo(
        self,
        page: Page,
        api_client: APIClient,
        soft_assert: SoftAssert,
        config: Config
    ):
        """Complete demonstration of all framework features."""
        
        # ============================================================
        # STEP 1: API Testing
        # ============================================================
        with allure.step("Step 1: API Testing - Fetch user data"):
            allure.attach("API testing component", "Info", allure.attachment_type.TEXT)
            
            # Make API call
            response = api_client.get("/users/1")
            
            # Validate with soft assertions
            soft_assert.assert_equal(
                response.status_code,
                200,
                "API should return 200"
            )
            soft_assert.assert_true(
                api_client.validate_response_time(response, 5.0),
                "Response time should be under 5 seconds"
            )
            
            user_data = response.json()
            soft_assert.assert_in("name", user_data, "Response should have 'name'")
            soft_assert.assert_in("email", user_data, "Response should have 'email'")
        
        # ============================================================
        # STEP 2: Web Testing - Login
        # ============================================================
        with allure.step("Step 2: Web Testing - Login to application"):
            allure.attach("Web testing with Playwright", "Info", allure.attachment_type.TEXT)
            
            login_page = LoginPage(page)
            products_page = ProductsPage(page)
            
            # Navigate and login
            login_page.navigate_to_login_page()
            
            # Take screenshot before login
            login_page.take_screenshot("before_login")
            
            # Verify login page elements with soft assertions
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
            
            # Perform login
            login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
            
            # Take screenshot after login
            products_page.take_screenshot("after_login")
        
        # ============================================================
        # STEP 3: Products Page Validation
        # ============================================================
        with allure.step("Step 3: Validate products page"):
            allure.attach("Product validation", "Info", allure.attachment_type.TEXT)
            
            # Verify products page loaded
            products_page.verify_products_page_loaded()
            
            # Get product information
            product_count = products_page.get_product_count()
            product_names = products_page.get_all_product_names()
            product_prices = products_page.get_all_product_prices()
            
            # Validate with soft assertions
            soft_assert.assert_greater(
                product_count,
                0,
                "Should have at least one product"
            )
            soft_assert.assert_equal(
                product_count,
                len(product_names),
                "Product count should match names count"
            )
            soft_assert.assert_equal(
                product_count,
                len(product_prices),
                "Product count should match prices count"
            )
            
            # Attach product data to report
            allure.attach(
                f"Product Count: {product_count}",
                "Product Statistics",
                allure.attachment_type.TEXT
            )
            allure.attach(
                "\n".join(product_names),
                "Product Names",
                allure.attachment_type.TEXT
            )
            allure.attach(
                "\n".join(product_prices),
                "Product Prices",
                allure.attachment_type.TEXT
            )
        
        # ============================================================
        # STEP 4: Shopping Cart Operations
        # ============================================================
        with allure.step("Step 4: Add products to cart"):
            allure.attach("Shopping cart operations", "Info", allure.attachment_type.TEXT)
            
            products_to_add = ["sauce-labs-backpack", "sauce-labs-bike-light"]
            
            for product_id in products_to_add:
                products_page.add_product_to_cart(product_id)
            
            # Verify cart count
            cart_count = products_page.get_cart_item_count()
            soft_assert.assert_equal(
                cart_count,
                len(products_to_add),
                f"Cart should have {len(products_to_add)} items"
            )
            
            # Take screenshot with items in cart
            products_page.take_screenshot("cart_with_items")
        
        # ============================================================
        # STEP 5: Product Sorting Validation
        # ============================================================
        with allure.step("Step 5: Validate product sorting"):
            allure.attach("Sorting validation", "Info", allure.attachment_type.TEXT)
            
            # Sort by name A-Z
            products_page.sort_products("az")
            sorted_names = products_page.get_all_product_names()
            
            soft_assert.assert_equal(
                sorted_names,
                sorted(sorted_names),
                "Products should be sorted alphabetically"
            )
            
            # Sort by price
            products_page.sort_products("lohi")
            prices = products_page.get_all_product_prices()
            price_values = [float(p.replace("$", "")) for p in prices]
            
            soft_assert.assert_equal(
                price_values,
                sorted(price_values),
                "Products should be sorted by price"
            )
        
        # ============================================================
        # STEP 6: API Integration Check
        # ============================================================
        with allure.step("Step 6: Additional API validation"):
            allure.attach("API integration check", "Info", allure.attachment_type.TEXT)
            
            # Fetch multiple posts
            response = api_client.get("/posts")
            posts = response.json()
            
            soft_assert.assert_true(
                len(posts) > 0,
                "Should have posts in response"
            )
            soft_assert.assert_true(
                isinstance(posts, list),
                "Response should be a list"
            )
            
            # Create new post
            new_post = {
                "title": "Test from Framework",
                "body": "Complete framework demonstration",
                "userId": 1
            }
            create_response = api_client.post("/posts", json_data=new_post)
            
            soft_assert.assert_equal(
                create_response.status_code,
                201,
                "Post creation should return 201"
            )
        
        # ============================================================
        # STEP 7: Final Validation
        # ============================================================
        with allure.step("Step 7: Final validation and cleanup"):
            allure.attach("Final checks", "Info", allure.attachment_type.TEXT)
            
            # Remove one item from cart
            products_page.remove_product_from_cart("sauce-labs-backpack")
            
            updated_cart = products_page.get_cart_item_count()
            soft_assert.assert_equal(
                updated_cart,
                1,
                "Cart should have 1 item after removal"
            )
            
            # Take final screenshot
            products_page.take_screenshot("final_state")
        
        # ============================================================
        # VERIFY ALL SOFT ASSERTIONS
        # ============================================================
        with allure.step("Verify all soft assertions"):
            # This will raise an exception if any soft assertions failed
            # All failures will be collected and reported together
            soft_assert.assert_all()
        
        # ============================================================
        # TEST SUMMARY
        # ============================================================
        with allure.step("Test execution summary"):
            summary = {
                "web_tests": "PASSED",
                "api_tests": "PASSED",
                "soft_assertions": f"Total: {soft_assert.assertion_count}",
                "screenshots": "Captured",
                "status": "SUCCESS"
            }
            
            allure.attach(
                str(summary),
                "Test Summary",
                allure.attachment_type.JSON
            )
    
    @allure.story("Intentional Failure for Email Demo")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test that fails to demonstrate email notification")
    @allure.description("""
        This test intentionally fails to demonstrate:
        - Email notification on failure
        - Screenshot capture on failure
        - Error reporting
        
        IMPORTANT: This test is skipped by default.
        To see email notification, enable it and run:
        pytest tests/test_complete_demo.py::TestCompleteFramework::test_intentional_failure_for_email
    """)
    @pytest.mark.skip(reason="Intentionally fails - only run to demo email notifications")
    def test_intentional_failure_for_email(self, page: Page, config: Config):
        """
        This test fails intentionally to demonstrate email notifications.
        
        When run with email configured, you'll receive:
        - Immediate failure notification
        - Screenshot attached
        - Error details
        """
        
        login_page = LoginPage(page)
        
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("This step will fail intentionally"):
            # This assertion will fail
            assert False, "This is an intentional failure to demonstrate email notifications"
    
    @allure.story("Data-Driven Testing Example")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test with multiple data sets")
    @pytest.mark.parametrize("username,password,should_fail", [
        ("standard_user", "secret_sauce", False),
        ("locked_out_user", "secret_sauce", True),
        ("invalid_user", "wrong_password", True),
    ])
    @pytest.mark.regression
    def test_data_driven_login(
        self,
        page: Page,
        username: str,
        password: str,
        should_fail: bool,
        soft_assert: SoftAssert
    ):
        """Demonstrate data-driven testing with parametrize."""
        
        login_page = LoginPage(page)
        
        with allure.step(f"Test login with {username}"):
            login_page.navigate_to_login_page()
            login_page.login(username, password)
            
            if should_fail:
                soft_assert.assert_true(
                    login_page.is_error_message_displayed(),
                    f"Error should be shown for {username}"
                )
            else:
                soft_assert.assert_contains(
                    page.url,
                    "inventory.html",
                    f"Should redirect for valid user {username}"
                )
            
            soft_assert.assert_all()


@allure.epic("Email Notification Test")
@allure.feature("Email Functionality")
class TestEmailNotifications:
    """Test email notification functionality."""
    
    @allure.story("Email Configuration")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify email configuration")
    @pytest.mark.skip(reason="Only run when testing email setup")
    def test_email_configuration(self):
        """
        Test email configuration without running actual tests.
        
        This checks if email settings are configured correctly.
        """
        
        with allure.step("Check email configuration"):
            assert Config.SENDER_EMAIL, "Sender email not configured"
            assert Config.SENDER_PASSWORD, "Sender password not configured"
            assert Config.RECEIVER_EMAILS, "Receiver emails not configured"
            assert Config.SMTP_SERVER, "SMTP server not configured"
        
        with allure.step("Test email connection"):
            email = EmailNotification()
            
            # Try to send test email
            success = email.send_test_report(
                total_tests=1,
                passed=1,
                failed=0,
                skipped=0,
                duration=0.1,
                include_allure_report=False
            )
            
            assert success, "Failed to send test email"
            
            allure.attach(
                "Email sent successfully",
                "Email Test Result",
                allure.attachment_type.TEXT
            )
