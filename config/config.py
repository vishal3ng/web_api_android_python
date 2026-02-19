"""
Configuration management for the test framework.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class for the framework."""
    
    # Environment
    ENV = os.getenv("ENV", "qa").lower()
    
    # Base URLs
    BASE_URLS = {
        "dev": "https://dev.example.com",
        "qa": "https://qa.example.com",
        "staging": "https://staging.example.com",
        "prod": "https://www.example.com"
    }
    
    BASE_URL = os.getenv("BASE_URL", BASE_URLS.get(ENV, BASE_URLS["qa"]))
    
    # Browser Settings
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down execution in ms
    
    # Timeouts (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    
    # Video Recording
    RECORD_VIDEO = os.getenv("RECORD_VIDEO", "false").lower() == "true"
    
    # Tracing
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))
    
    # Test Data
    TEST_DATA_PATH = Path("data")
    
    # Credentials (should be in .env file)
    VALID_USERNAME = os.getenv("VALID_USERNAME", "standard_user")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD", "secret_sauce")
    
    # API Settings
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    
    # Mobile Testing - Appium Settings
    APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
    PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")  # Android or iOS
    DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
    APP_PACKAGE = os.getenv("APP_PACKAGE", "com.example.app")
    APP_ACTIVITY = os.getenv("APP_ACTIVITY", ".MainActivity")
    AUTOMATION_NAME = os.getenv("AUTOMATION_NAME", "UiAutomator2")  # UiAutomator2 for Android, XCUITest for iOS
    
    # iOS Specific
    BUNDLE_ID = os.getenv("BUNDLE_ID", "com.example.app")
    UDID = os.getenv("UDID", "")
    
    # Email Notification Settings
    SEND_EMAIL_REPORT = os.getenv("SEND_EMAIL_REPORT", "false").lower() == "true"
    SEND_EMAIL_ON_FAILURE = os.getenv("SEND_EMAIL_ON_FAILURE", "true").lower() == "true"
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
    RECEIVER_EMAILS = os.getenv("RECEIVER_EMAILS", "").split(",")  # Comma-separated
    
    # Soft Assertions
    USE_SOFT_ASSERT = os.getenv("USE_SOFT_ASSERT", "true").lower() == "true"
    
    # Parallel Execution
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "4"))
    
    # Screenshot Settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    FULL_PAGE_SCREENSHOT = os.getenv("FULL_PAGE_SCREENSHOT", "true").lower() == "true"
    
    # Reporting
    ALLURE_RESULTS_DIR = "reports/allure-results"
    ALLURE_REPORT_DIR = "reports/allure-report"
    HTML_REPORT_PATH = "reports/html-report/report.html"
    
    @classmethod
    def get_url(cls, path: str = "") -> str:
        """
        Get full URL by appending path to base URL.
        
        Args:
            path: URL path to append
            
        Returns:
            Full URL
        """
        return f"{cls.BASE_URL}/{path.lstrip('/')}" if path else cls.BASE_URL
    
    @classmethod
    def display_config(cls):
        """Display current configuration."""
        print("\n" + "="*50)
        print("TEST CONFIGURATION")
        print("="*50)
        print(f"Environment: {cls.ENV}")
        print(f"Base URL: {cls.BASE_URL}")
        print(f"Browser: {cls.BROWSER}")
        print(f"Headless: {cls.HEADLESS}")
        print(f"Record Video: {cls.RECORD_VIDEO}")
        print(f"Enable Tracing: {cls.ENABLE_TRACING}")
        print(f"Default Timeout: {cls.DEFAULT_TIMEOUT}ms")
        print("="*50 + "\n")
