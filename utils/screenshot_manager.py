"""
Screenshot utility for capturing and managing screenshots.
"""
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class ScreenshotManager:
    """Manage screenshots during test execution."""
    
    SCREENSHOT_DIR = Path("reports/screenshots")
    
    @classmethod
    def setup(cls):
        """Create screenshot directory if not exists."""
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def capture(
        cls,
        page: Page,
        name: str,
        full_page: bool = True,
        attach_to_allure: bool = True
    ) -> str:
        """
        Capture screenshot.
        
        Args:
            page: Playwright Page object
            name: Screenshot name
            full_page: Capture full page
            attach_to_allure: Attach to Allure report
            
        Returns:
            Screenshot file path
        """
        cls.setup()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = cls.SCREENSHOT_DIR / filename
        
        logger.info(f"Capturing screenshot: {filename}")
        page.screenshot(path=str(filepath), full_page=full_page)
        
        if attach_to_allure:
            allure.attach.file(
                str(filepath),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        
        return str(filepath)
    
    @classmethod
    def capture_element(
        cls,
        page: Page,
        locator: str,
        name: str,
        attach_to_allure: bool = True
    ) -> str:
        """
        Capture screenshot of specific element.
        
        Args:
            page: Playwright Page object
            locator: Element locator
            name: Screenshot name
            attach_to_allure: Attach to Allure report
            
        Returns:
            Screenshot file path
        """
        cls.setup()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = cls.SCREENSHOT_DIR / filename
        
        logger.info(f"Capturing element screenshot: {filename}")
        page.locator(locator).screenshot(path=str(filepath))
        
        if attach_to_allure:
            allure.attach.file(
                str(filepath),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        
        return str(filepath)
