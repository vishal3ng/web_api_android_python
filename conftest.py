"""
Pytest configuration and fixtures for the test framework.
"""
import pytest
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, Browser, BrowserContext
from config.config import Config
from utils.logger import Logger
from utils.email_notification import EmailNotification
from utils.soft_assert import SoftAssert

# Mobile Testing
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# API Testing
from api.api_client import APIClient

logger = Logger.get_logger(__name__)

# Track test execution statistics
test_stats = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "start_time": None,
    "end_time": None
}


@pytest.fixture(scope="session")
def config():
    """Provide configuration object."""
    return Config()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page for each test."""
    page = context.new_page()
    logger.info(f"New page created: {page.url}")
    
    # Set default timeout
    page.set_default_timeout(30000)
    
    yield page
    
    # Cleanup
    logger.info(f"Closing page: {page.url}")
    page.close()


@pytest.fixture(scope="function")
def context(browser: Browser, config: Config) -> BrowserContext:
    """Create a new browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="reports/videos/" if config.RECORD_VIDEO else None,
        record_video_size={"width": 1920, "height": 1080} if config.RECORD_VIDEO else None,
    )
    
    # Enable tracing for debugging
    if config.ENABLE_TRACING:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace on failure
    if config.ENABLE_TRACING:
        trace_path = f"reports/traces/trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        Path("reports/traces").mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=trace_path)
        logger.info(f"Trace saved: {trace_path}")
    
    context.close()


@pytest.fixture(scope="function")
def mobile_driver(config: Config):
    """
    Create Appium driver for mobile testing.
    
    Returns:
        Appium WebDriver instance
    """
    logger.info("Initializing mobile driver")
    
    if config.PLATFORM_NAME.lower() == "android":
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = config.DEVICE_NAME
        options.app_package = config.APP_PACKAGE
        options.app_activity = config.APP_ACTIVITY
        options.automation_name = config.AUTOMATION_NAME
    else:  # iOS
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.device_name = config.DEVICE_NAME
        options.bundle_id = config.BUNDLE_ID
        options.automation_name = "XCUITest"
        if config.UDID:
            options.udid = config.UDID
    
    driver = appium_webdriver.Remote(
        config.APPIUM_SERVER_URL,
        options=options
    )
    
    logger.info(f"Mobile driver initialized: {config.PLATFORM_NAME}")
    
    yield driver
    
    # Cleanup
    logger.info("Closing mobile driver")
    driver.quit()


@pytest.fixture(scope="function")
def api_client(config: Config) -> APIClient:
    """
    Create API client for API testing.
    
    Returns:
        APIClient instance
    """
    logger.info("Creating API client")
    client = APIClient(base_url=config.API_BASE_URL)
    return client


@pytest.fixture(scope="function")
def soft_assert() -> SoftAssert:
    """
    Create soft assertion instance.
    
    Returns:
        SoftAssert instance
    """
    return SoftAssert()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and attach screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Update test statistics
        if report.failed:
            test_stats["failed"] += 1
            logger.error(f"Test FAILED: {item.nodeid}")
            
            # Try to capture screenshot on failure
            if "page" in item.funcargs:
                page = item.funcargs["page"]
                screenshot_path = f"reports/screenshots/failed_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
                
                try:
                    page.screenshot(path=screenshot_path, full_page=True)
                    allure.attach.file(
                        screenshot_path,
                        name=f"Screenshot - {item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Screenshot saved: {screenshot_path}")
                    
                    # Send email notification for failure
                    if Config.SEND_EMAIL_ON_FAILURE:
                        email = EmailNotification()
                        email.send_test_failure_notification(
                            test_name=item.nodeid,
                            error_message=str(report.longrepr),
                            screenshot_path=screenshot_path
                        )
                except Exception as e:
                    logger.warning(f"Failed to capture screenshot or send email: {e}")
            
            # For mobile tests
            elif "mobile_driver" in item.funcargs:
                driver = item.funcargs["mobile_driver"]
                screenshot_path = f"reports/screenshots/mobile/failed_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                Path("reports/screenshots/mobile").mkdir(parents=True, exist_ok=True)
                
                try:
                    driver.save_screenshot(screenshot_path)
                    allure.attach.file(
                        screenshot_path,
                        name=f"Mobile Screenshot - {item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Mobile screenshot saved: {screenshot_path}")
                except Exception as e:
                    logger.warning(f"Failed to capture mobile screenshot: {e}")
        
        elif report.passed:
            test_stats["passed"] += 1
            logger.info(f"Test PASSED: {item.nodeid}")
        
        elif report.skipped:
            test_stats["skipped"] += 1
            logger.warning(f"Test SKIPPED: {item.nodeid}")


@pytest.fixture(autouse=True)
def test_metadata(request):
    """Add test metadata to Allure report."""
    allure.dynamic.feature(request.module.__name__)
    allure.dynamic.story(request.function.__name__)
    
    # Add markers as labels
    for marker in request.node.iter_markers():
        allure.dynamic.label(marker.name, marker.name)


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create necessary directories
    Path("reports/allure-results").mkdir(parents=True, exist_ok=True)
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/screenshots/mobile").mkdir(parents=True, exist_ok=True)
    Path("reports/videos").mkdir(parents=True, exist_ok=True)
    Path("reports/traces").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    
    # Initialize test statistics
    test_stats["start_time"] = datetime.now()
    test_stats["total"] = 0
    test_stats["passed"] = 0
    test_stats["failed"] = 0
    test_stats["skipped"] = 0
    
    logger.info("Test execution started")


def pytest_collection_modifyitems(items):
    """Hook to modify test collection."""
    test_stats["total"] = len(items)
    logger.info(f"Collected {len(items)} tests")


def pytest_sessionfinish(session, exitstatus):
    """Hook called after whole test run finished."""
    test_stats["end_time"] = datetime.now()
    duration = (test_stats["end_time"] - test_stats["start_time"]).total_seconds()
    
    logger.info(f"Test execution finished with status: {exitstatus}")
    logger.info(f"Total: {test_stats['total']}, "
                f"Passed: {test_stats['passed']}, "
                f"Failed: {test_stats['failed']}, "
                f"Skipped: {test_stats['skipped']}")
    logger.info(f"Duration: {duration:.2f} seconds")
    
    # Send email report at the end
    if Config.SEND_EMAIL_REPORT:
        try:
            email = EmailNotification()
            email.send_test_report(
                total_tests=test_stats["total"],
                passed=test_stats["passed"],
                failed=test_stats["failed"],
                skipped=test_stats["skipped"],
                duration=duration,
                include_allure_report=True
            )
            logger.info("Email report sent successfully")
        except Exception as e:
            logger.error(f"Failed to send email report: {e}")
