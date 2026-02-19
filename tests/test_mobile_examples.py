"""
Mobile Testing Examples using Appium.

This demonstrates mobile testing with:
- Android/iOS app testing
- Mobile page objects
- Touch gestures
- Soft assertions
"""
import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from mobile.base_mobile_page import BaseMobilePage
from utils.soft_assert import SoftAssert


class LoginMobilePage(BaseMobilePage):
    """Example Login Page for mobile app."""
    
    # Android locators (update these for your actual app)
    USERNAME_INPUT = (AppiumBy.ID, "com.example.app:id/username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.example.app:id/password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.app:id/login_button")
    ERROR_MESSAGE = (AppiumBy.ID, "com.example.app:id/error_message")
    
    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        """Enter username."""
        self.send_keys(self.USERNAME_INPUT, username)
    
    @allure.step("Enter password")
    def enter_password(self, password: str):
        """Enter password."""
        self.send_keys(self.PASSWORD_INPUT, password)
    
    @allure.step("Click login button")
    def click_login(self):
        """Click login button."""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Login with credentials")
    def login(self, username: str, password: str):
        """Perform complete login."""
        self.enter_username(username)
        self.enter_password(password)
        self.hide_keyboard()
        self.click_login()
    
    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)


class HomeMobilePage(BaseMobilePage):
    """Example Home Page for mobile app."""
    
    WELCOME_TEXT = (AppiumBy.ID, "com.example.app:id/welcome_text")
    MENU_BUTTON = (AppiumBy.ID, "com.example.app:id/menu_button")
    
    @allure.step("Get welcome text")
    def get_welcome_text(self) -> str:
        """Get welcome message."""
        return self.get_text(self.WELCOME_TEXT)
    
    @allure.step("Verify home page loaded")
    def verify_home_page(self):
        """Verify home page is loaded."""
        assert self.is_displayed(self.WELCOME_TEXT)


@allure.epic("Mobile Testing")
@allure.feature("Android App")
@pytest.mark.mobile
class TestMobileExamples:
    """
    Example mobile tests using Appium.
    
    Note: These tests require:
    1. Appium server running (appium)
    2. Android emulator or real device
    3. App package and activity configured in .env
    """
    
    @allure.story("Mobile Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test successful mobile login")
    @pytest.mark.skip(reason="Requires actual mobile app and Appium setup")
    def test_mobile_successful_login(self, mobile_driver):
        """Test successful login on mobile app."""
        
        login_page = LoginMobilePage(mobile_driver)
        home_page = HomeMobilePage(mobile_driver)
        
        with allure.step("Login with valid credentials"):
            login_page.login("test_user", "test_password")
        
        with allure.step("Verify home page loaded"):
            home_page.verify_home_page()
            welcome_text = home_page.get_welcome_text()
            assert "Welcome" in welcome_text
    
    @allure.story("Mobile Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test mobile login with invalid credentials")
    @pytest.mark.skip(reason="Requires actual mobile app and Appium setup")
    def test_mobile_invalid_login(self, mobile_driver):
        """Test login failure on mobile app."""
        
        login_page = LoginMobilePage(mobile_driver)
        
        with allure.step("Login with invalid credentials"):
            login_page.login("invalid_user", "invalid_pass")
        
        with allure.step("Verify error message"):
            assert login_page.is_displayed(login_page.ERROR_MESSAGE)
            error_text = login_page.get_error_message()
            assert len(error_text) > 0
    
    @allure.story("Mobile Gestures")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test swipe gestures")
    @pytest.mark.skip(reason="Requires actual mobile app and Appium setup")
    def test_mobile_swipe_gesture(self, mobile_driver):
        """Test swipe gesture on mobile."""
        
        page = BaseMobilePage(mobile_driver)
        
        with allure.step("Swipe up"):
            page.swipe("up")
            page.take_screenshot("after_swipe_up")
        
        with allure.step("Swipe down"):
            page.swipe("down")
            page.take_screenshot("after_swipe_down")
    
    @allure.story("Mobile with Soft Assertions")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test mobile page with soft assertions")
    @pytest.mark.skip(reason="Requires actual mobile app and Appium setup")
    def test_mobile_with_soft_assertions(self, mobile_driver, soft_assert: SoftAssert):
        """Test mobile page elements with soft assertions."""
        
        login_page = LoginMobilePage(mobile_driver)
        
        with allure.step("Verify login page elements"):
            soft_assert.assert_true(
                login_page.is_displayed(login_page.USERNAME_INPUT),
                "Username field should be displayed"
            )
            soft_assert.assert_true(
                login_page.is_displayed(login_page.PASSWORD_INPUT),
                "Password field should be displayed"
            )
            soft_assert.assert_true(
                login_page.is_displayed(login_page.LOGIN_BUTTON),
                "Login button should be displayed"
            )
            
            # Verify attributes
            username_enabled = login_page.get_attribute(login_page.USERNAME_INPUT, "enabled")
            soft_assert.assert_equal(username_enabled, "true", "Username field should be enabled")
            
            # Check all assertions
            soft_assert.assert_all()


@allure.epic("Mobile Testing")
@allure.feature("iOS App")
@pytest.mark.mobile
@pytest.mark.ios
class TestIOSExamples:
    """Example iOS mobile tests."""
    
    @allure.story("iOS Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test iOS app login")
    @pytest.mark.skip(reason="Requires actual iOS app and Appium setup")
    def test_ios_login(self, mobile_driver):
        """Test login on iOS app."""
        
        # iOS specific test implementation
        page = BaseMobilePage(mobile_driver)
        
        with allure.step("Perform iOS login"):
            # iOS locators would use accessibility IDs or XPath
            pass
        
        with allure.step("Verify login success"):
            page.take_screenshot("ios_login_success")


# Integration test combining Web + API
@allure.epic("Integration Testing")
@allure.feature("Web + API")
class TestWebAPIIntegration:
    """Integration tests combining Web and API testing."""
    
    @allure.story("Create user via API and verify in Web")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test Web and API integration")
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_web_api_integration(self, api_client: APIClient):
        """
        Test integration between Web and API.
        
        This is a template showing how to combine API and Web testing.
        """
        
        with allure.step("Create user via API"):
            new_user = {
                "name": "Test User",
                "email": "test@example.com",
                "username": "testuser"
            }
            response = api_client.post("/users", json_data=new_user)
            assert api_client.validate_status_code(response, 201)
            
            created_user = response.json()
            user_id = created_user.get("id")
        
        with allure.step("Verify user via API"):
            response = api_client.get(f"/users/{user_id}")
            assert api_client.validate_status_code(response, 200)
            
            user = response.json()
            assert user["name"] == new_user["name"]
            assert user["email"] == new_user["email"]
            print("check git 0.2")
            print("new ch 0.2")
        
        # Could then verify in web UI
        # with allure.step("Verify user in Web UI"):
        #     # Navigate to users page and verify
        #     pass
