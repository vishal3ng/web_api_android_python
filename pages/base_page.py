"""
Base Page Object containing common methods for all page objects.
"""
import allure
from playwright.sync_api import Page, expect
from typing import Optional, List
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class BasePage:
    """Base class for all Page Objects."""
    
    def __init__(self, page: Page):
        """
        Initialize BasePage.
        
        Args:
            page: Playwright Page object
        """
        self.page = page
        self.timeout = 30000
    
    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Click element: {locator}")
    def click(self, locator: str) -> None:
        """
        Click an element.
        
        Args:
            locator: Element locator
        """
        logger.info(f"Clicking element: {locator}")
        self.page.locator(locator).click()
    
    @allure.step("Fill field '{locator}' with text")
    def fill(self, locator: str, text: str, clear: bool = True) -> None:
        """
        Fill text in an input field.
        
        Args:
            locator: Element locator
            text: Text to fill
            clear: Clear field before filling
        """
        logger.info(f"Filling field '{locator}' with text: {'*' * len(text) if 'password' in locator.lower() else text}")
        element = self.page.locator(locator)
        if clear:
            element.clear()
        element.fill(text)
    
    @allure.step("Type text in field: {locator}")
    def type(self, locator: str, text: str, delay: int = 100) -> None:
        """
        Type text with delay (simulates human typing).
        
        Args:
            locator: Element locator
            text: Text to type
            delay: Delay between keystrokes in ms
        """
        logger.info(f"Typing in field '{locator}'")
        self.page.locator(locator).type(text, delay=delay)
    
    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: str) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Element locator
            
        Returns:
            Element text content
        """
        text = self.page.locator(locator).inner_text()
        logger.info(f"Got text from '{locator}': {text}")
        return text
    
    @allure.step("Get attribute '{attribute}' from element: {locator}")
    def get_attribute(self, locator: str, attribute: str) -> Optional[str]:
        """
        Get attribute value of an element.
        
        Args:
            locator: Element locator
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        value = self.page.locator(locator).get_attribute(attribute)
        logger.info(f"Got attribute '{attribute}' from '{locator}': {value}")
        return value
    
    @allure.step("Wait for element: {locator}")
    def wait_for_element(self, locator: str, state: str = "visible", timeout: Optional[int] = None) -> None:
        """
        Wait for element to be in a specific state.
        
        Args:
            locator: Element locator
            state: Element state (visible, hidden, attached, detached)
            timeout: Timeout in milliseconds
        """
        logger.info(f"Waiting for element '{locator}' to be {state}")
        self.page.locator(locator).wait_for(state=state, timeout=timeout or self.timeout)
    
    @allure.step("Check if element is visible: {locator}")
    def is_visible(self, locator: str) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Element locator
            
        Returns:
            True if visible, False otherwise
        """
        is_visible = self.page.locator(locator).is_visible()
        logger.info(f"Element '{locator}' visible: {is_visible}")
        return is_visible
    
    @allure.step("Check if element is enabled: {locator}")
    def is_enabled(self, locator: str) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locator: Element locator
            
        Returns:
            True if enabled, False otherwise
        """
        is_enabled = self.page.locator(locator).is_enabled()
        logger.info(f"Element '{locator}' enabled: {is_enabled}")
        return is_enabled
    
    @allure.step("Select option '{value}' from dropdown: {locator}")
    def select_option(self, locator: str, value: str = None, label: str = None, index: int = None) -> None:
        """
        Select option from dropdown.
        
        Args:
            locator: Dropdown locator
            value: Option value
            label: Option label
            index: Option index
        """
        logger.info(f"Selecting option from '{locator}'")
        if value:
            self.page.locator(locator).select_option(value=value)
        elif label:
            self.page.locator(locator).select_option(label=label)
        elif index is not None:
            self.page.locator(locator).select_option(index=index)
    
    @allure.step("Hover over element: {locator}")
    def hover(self, locator: str) -> None:
        """
        Hover over an element.
        
        Args:
            locator: Element locator
        """
        logger.info(f"Hovering over element: {locator}")
        self.page.locator(locator).hover()
    
    @allure.step("Double click element: {locator}")
    def double_click(self, locator: str) -> None:
        """
        Double click an element.
        
        Args:
            locator: Element locator
        """
        logger.info(f"Double clicking element: {locator}")
        self.page.locator(locator).dblclick()
    
    @allure.step("Press key: {key}")
    def press_key(self, key: str) -> None:
        """
        Press a keyboard key.
        
        Args:
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
        """
        logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)
    
    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL
        """
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url
    
    @allure.step("Get page title")
    def get_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title
        """
        title = self.page.title()
        logger.info(f"Page title: {title}")
        return title
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str = "screenshot", full_page: bool = True) -> str:
        """
        Take a screenshot.
        
        Args:
            name: Screenshot name
            full_page: Take full page screenshot
            
        Returns:
            Screenshot path
        """
        from datetime import datetime
        from pathlib import Path
        
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{screenshot_dir}/{name}_{timestamp}.png"
        
        self.page.screenshot(path=screenshot_path, full_page=full_page)
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        # Attach to Allure report
        allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
        
        return screenshot_path
    
    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator: str) -> None:
        """
        Scroll to an element.
        
        Args:
            locator: Element locator
        """
        logger.info(f"Scrolling to element: {locator}")
        self.page.locator(locator).scroll_into_view_if_needed()
    
    @allure.step("Wait for page load")
    def wait_for_page_load(self, state: str = "networkidle") -> None:
        """
        Wait for page to load.
        
        Args:
            state: Load state (load, domcontentloaded, networkidle)
        """
        logger.info(f"Waiting for page load state: {state}")
        self.page.wait_for_load_state(state)
    
    @allure.step("Execute JavaScript")
    def execute_script(self, script: str, *args) -> any:
        """
        Execute JavaScript code.
        
        Args:
            script: JavaScript code
            args: Arguments to pass to the script
            
        Returns:
            Script result
        """
        logger.info("Executing JavaScript")
        return self.page.evaluate(script, *args)
    
    @allure.step("Get all elements count: {locator}")
    def get_elements_count(self, locator: str) -> int:
        """
        Get count of elements matching locator.
        
        Args:
            locator: Element locator
            
        Returns:
            Count of elements
        """
        count = self.page.locator(locator).count()
        logger.info(f"Found {count} elements matching '{locator}'")
        return count
    
    @allure.step("Accept alert")
    def accept_alert(self) -> None:
        """Accept browser alert dialog."""
        logger.info("Accepting alert")
        self.page.on("dialog", lambda dialog: dialog.accept())
    
    @allure.step("Dismiss alert")
    def dismiss_alert(self) -> None:
        """Dismiss browser alert dialog."""
        logger.info("Dismissing alert")
        self.page.on("dialog", lambda dialog: dialog.dismiss())
    
    # Assertion helpers using Playwright's expect
    @allure.step("Assert element visible: {locator}")
    def assert_element_visible(self, locator: str, timeout: Optional[int] = None) -> None:
        """
        Assert element is visible.
        
        Args:
            locator: Element locator
            timeout: Timeout in milliseconds
        """
        logger.info(f"Asserting element visible: {locator}")
        expect(self.page.locator(locator)).to_be_visible(timeout=timeout or self.timeout)
    
    @allure.step("Assert text equals: {expected_text}")
    def assert_text_equals(self, locator: str, expected_text: str) -> None:
        """
        Assert element text equals expected text.
        
        Args:
            locator: Element locator
            expected_text: Expected text
        """
        logger.info(f"Asserting text in '{locator}' equals: {expected_text}")
        expect(self.page.locator(locator)).to_have_text(expected_text)
    
    @allure.step("Assert text contains: {expected_text}")
    def assert_text_contains(self, locator: str, expected_text: str) -> None:
        """
        Assert element text contains expected text.
        
        Args:
            locator: Element locator
            expected_text: Expected text
        """
        logger.info(f"Asserting text in '{locator}' contains: {expected_text}")
        expect(self.page.locator(locator)).to_contain_text(expected_text)
    
    @allure.step("Assert URL contains: {expected_url}")
    def assert_url_contains(self, expected_url: str) -> None:
        """
        Assert current URL contains expected URL.
        
        Args:
            expected_url: Expected URL substring
        """
        logger.info(f"Asserting URL contains: {expected_url}")
        expect(self.page).to_have_url(expected_url, timeout=self.timeout)
