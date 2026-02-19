"""
Login Page Object.
"""
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class LoginPage(BasePage):
    """Page Object for Login Page."""
    
    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "h3[data-test='error']"
    LOGO = ".login_logo"
    
    def __init__(self, page: Page):
        """
        Initialize LoginPage.
        
        Args:
            page: Playwright Page object
        """
        super().__init__(page)
        self.url = "https://www.saucedemo.com"
    
    @allure.step("Navigate to Login Page")
    def navigate_to_login_page(self) -> 'LoginPage':
        """
        Navigate to login page.
        
        Returns:
            LoginPage instance
        """
        logger.info(f"Navigating to login page: {self.url}")
        self.navigate(self.url)
        self.wait_for_element(self.LOGO)
        return self
    
    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username.
        
        Args:
            username: Username to enter
            
        Returns:
            LoginPage instance
        """
        logger.info(f"Entering username: {username}")
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    @allure.step("Enter password")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password.
        
        Args:
            password: Password to enter
            
        Returns:
            LoginPage instance
        """
        logger.info("Entering password")
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    @allure.step("Click login button")
    def click_login_button(self) -> None:
        """Click login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Perform login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.
        
        Args:
            username: Username
            password: Password
        """
        logger.info(f"Performing login for user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        logger.info("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    @allure.step("Check if error message is displayed")
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is displayed
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    @allure.step("Verify login page loaded")
    def verify_login_page_loaded(self) -> None:
        """Verify login page is loaded."""
        logger.info("Verifying login page loaded")
        self.assert_element_visible(self.LOGO)
        self.assert_element_visible(self.USERNAME_INPUT)
        self.assert_element_visible(self.PASSWORD_INPUT)
        self.assert_element_visible(self.LOGIN_BUTTON)
