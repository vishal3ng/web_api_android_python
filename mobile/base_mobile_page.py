"""
Base Mobile Page for Appium mobile testing.
"""
import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple, List
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class BaseMobilePage:
    """Base class for all Mobile Page Objects."""
    
    def __init__(self, driver: WebDriver):
        """
        Initialize BaseMobilePage.
        
        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator: Tuple[str, str]):
        """
        Find element with explicit wait.
        
        Args:
            locator: Tuple of (By, locator_value)
            
        Returns:
            WebElement
        """
        logger.info(f"Finding element: {locator}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element
    
    @allure.step("Find elements: {locator}")
    def find_elements(self, locator: Tuple[str, str]) -> List:
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By, locator_value)
            
        Returns:
            List of WebElements
        """
        logger.info(f"Finding elements: {locator}")
        return self.driver.find_elements(*locator)
    
    @allure.step("Click element: {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click an element.
        
        Args:
            locator: Tuple of (By, locator_value)
        """
        logger.info(f"Clicking element: {locator}")
        element = self.find_element(locator)
        element.click()
    
    @allure.step("Send keys to element: {locator}")
    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """
        Send keys to element.
        
        Args:
            locator: Tuple of (By, locator_value)
            text: Text to send
        """
        logger.info(f"Sending keys to {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text from element.
        
        Args:
            locator: Tuple of (By, locator_value)
            
        Returns:
            Element text
        """
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Got text from {locator}: {text}")
        return text
    
    @allure.step("Check if element is displayed: {locator}")
    def is_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is displayed.
        
        Args:
            locator: Tuple of (By, locator_value)
            
        Returns:
            True if displayed
        """
        try:
            element = self.find_element(locator)
            is_displayed = element.is_displayed()
            logger.info(f"Element {locator} displayed: {is_displayed}")
            return is_displayed
        except TimeoutException:
            logger.info(f"Element {locator} not found")
            return False
    
    @allure.step("Wait for element: {locator}")
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 30) -> None:
        """
        Wait for element to be present.
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Wait timeout in seconds
        """
        logger.info(f"Waiting for element: {locator}")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    @allure.step("Swipe: {direction}")
    def swipe(self, direction: str = "up", duration: int = 800) -> None:
        """
        Swipe in specified direction.
        
        Args:
            direction: up, down, left, right
            duration: Swipe duration in ms
        """
        logger.info(f"Swiping {direction}")
        size = self.driver.get_window_size()
        
        if direction == "up":
            start_x = size['width'] // 2
            start_y = size['height'] * 0.8
            end_x = size['width'] // 2
            end_y = size['height'] * 0.2
        elif direction == "down":
            start_x = size['width'] // 2
            start_y = size['height'] * 0.2
            end_x = size['width'] // 2
            end_y = size['height'] * 0.8
        elif direction == "left":
            start_x = size['width'] * 0.8
            start_y = size['height'] // 2
            end_x = size['width'] * 0.2
            end_y = size['height'] // 2
        else:  # right
            start_x = size['width'] * 0.2
            start_y = size['height'] // 2
            end_x = size['width'] * 0.8
            end_y = size['height'] // 2
        
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    
    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Scroll to element.
        
        Args:
            locator: Tuple of (By, locator_value)
        """
        logger.info(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("mobile: scroll", {"element": element})
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot.
        
        Args:
            name: Screenshot name
            
        Returns:
            Screenshot path
        """
        from datetime import datetime
        from pathlib import Path
        
        screenshot_dir = Path("reports/screenshots/mobile")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{screenshot_dir}/{name}_{timestamp}.png"
        
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        # Attach to Allure
        allure.attach.file(
            screenshot_path,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        
        return screenshot_path
    
    @allure.step("Tap at coordinates: ({x}, {y})")
    def tap(self, x: int, y: int) -> None:
        """
        Tap at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        logger.info(f"Tapping at ({x}, {y})")
        self.driver.tap([(x, y)])
    
    @allure.step("Long press element: {locator}")
    def long_press(self, locator: Tuple[str, str], duration: int = 1000) -> None:
        """
        Long press on element.
        
        Args:
            locator: Tuple of (By, locator_value)
            duration: Press duration in ms
        """
        logger.info(f"Long pressing element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("mobile: longClickGesture", {
            "elementId": element.id,
            "duration": duration
        })
    
    @allure.step("Hide keyboard")
    def hide_keyboard(self) -> None:
        """Hide mobile keyboard."""
        logger.info("Hiding keyboard")
        try:
            self.driver.hide_keyboard()
        except:
            logger.warning("Keyboard not visible or unable to hide")
    
    @allure.step("Get attribute '{attribute}' from element: {locator}")
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get element attribute.
        
        Args:
            locator: Tuple of (By, locator_value)
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"Got attribute '{attribute}': {value}")
        return value
    
    @allure.step("Wait for element to be clickable: {locator}")
    def wait_for_clickable(self, locator: Tuple[str, str], timeout: int = 30) -> None:
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Wait timeout in seconds
        """
        logger.info(f"Waiting for element to be clickable: {locator}")
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @allure.step("Get current activity")
    def get_current_activity(self) -> str:
        """
        Get current activity (Android).
        
        Returns:
            Current activity name
        """
        activity = self.driver.current_activity
        logger.info(f"Current activity: {activity}")
        return activity
    
    @allure.step("Press back button")
    def press_back(self) -> None:
        """Press device back button."""
        logger.info("Pressing back button")
        self.driver.back()
    
    @allure.step("Launch app")
    def launch_app(self) -> None:
        """Launch the application."""
        logger.info("Launching app")
        self.driver.launch_app()
    
    @allure.step("Close app")
    def close_app(self) -> None:
        """Close the application."""
        logger.info("Closing app")
        self.driver.close_app()
    
    @allure.step("Reset app")
    def reset_app(self) -> None:
        """Reset the application."""
        logger.info("Resetting app")
        self.driver.reset()
