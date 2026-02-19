"""
Login functionality test suite.
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.config import Config


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:
    """Test cases for login functionality."""
    
    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test successful login with valid credentials")
    @allure.description("Verify user can login successfully with valid username and password")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, page: Page, config: Config):
        """Test successful login with valid credentials."""
        # Arrange
        login_page = LoginPage(page)
        products_page = ProductsPage(page)
        
        # Act
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Verify login page is loaded"):
            login_page.verify_login_page_loaded()
        
        with allure.step("Login with valid credentials"):
            login_page.login(
                username=config.VALID_USERNAME,
                password=config.VALID_PASSWORD
            )
        
        # Assert
        with allure.step("Verify user is redirected to products page"):
            products_page.verify_products_page_loaded()
            assert "inventory.html" in page.url
    
    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test login fails with invalid credentials")
    @allure.description("Verify appropriate error message is shown for invalid credentials")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_with_invalid_credentials(self, page: Page):
        """Test login fails with invalid credentials."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Login with invalid credentials"):
            login_page.login(username="invalid_user", password="invalid_pass")
        
        # Assert
        with allure.step("Verify error message is displayed"):
            assert login_page.is_error_message_displayed()
            error_text = login_page.get_error_message()
            assert "Epic sadface" in error_text
            allure.attach(error_text, "Error Message", allure.attachment_type.TEXT)
    
    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test login fails with empty username")
    @allure.description("Verify error message when username is not provided")
    @pytest.mark.regression
    def test_login_with_empty_username(self, page: Page):
        """Test login fails with empty username."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Enter password only"):
            login_page.enter_password("some_password")
        
        with allure.step("Click login button"):
            login_page.click_login_button()
        
        # Assert
        with allure.step("Verify error message for missing username"):
            assert login_page.is_error_message_displayed()
            error_text = login_page.get_error_message()
            assert "Username is required" in error_text
    
    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test login fails with empty password")
    @allure.description("Verify error message when password is not provided")
    @pytest.mark.regression
    def test_login_with_empty_password(self, page: Page, config: Config):
        """Test login fails with empty password."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Enter username only"):
            login_page.enter_username(config.VALID_USERNAME)
        
        with allure.step("Click login button"):
            login_page.click_login_button()
        
        # Assert
        with allure.step("Verify error message for missing password"):
            assert login_page.is_error_message_displayed()
            error_text = login_page.get_error_message()
            assert "Password is required" in error_text
    
    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test login fails with locked out user")
    @allure.description("Verify error message when attempting to login with locked out user")
    @pytest.mark.regression
    def test_login_with_locked_user(self, page: Page):
        """Test login fails with locked out user."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Login with locked out user"):
            login_page.login(username="locked_out_user", password="secret_sauce")
        
        # Assert
        with allure.step("Verify locked out error message"):
            assert login_page.is_error_message_displayed()
            error_text = login_page.get_error_message()
            assert "locked out" in error_text.lower()
