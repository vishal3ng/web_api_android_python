# Enhanced Test Automation Framework - Complete Guide

## 🚀 New Features Added

This enhanced version includes:

### 1. ✅ Mobile Testing with Appium
- Android and iOS app testing support
- BaseMobilePage with 30+ mobile-specific methods
- Touch gestures (swipe, tap, long press)
- Mobile screenshot capture
- Example mobile tests

### 2. ✅ API Testing
- RESTful API testing with APIClient
- Support for GET, POST, PUT, DELETE, PATCH requests
- Response validation (status code, time, JSON schema)
- Request/Response logging in Allure
- Retry mechanism for API calls
- Example API tests with public JSONPlaceholder API

### 3. ✅ Soft Assertions
- Continue test execution even after assertion failures
- Collect all failures and report at end
- Support for 10+ assertion types
- Integration with Allure reporting
- Example tests demonstrating soft assertions

### 4. ✅ Email Notifications
- Automatic email on test failure
- Complete test report email at the end
- HTML formatted emails with statistics
- Attach screenshots on failure
- Attach complete report ZIP file
- Customizable SMTP settings

### 5. ✅ Enhanced Reporting
- Test execution statistics tracking
- Pass/Fail rate calculation
- Email reports with charts
- ZIP file with all reports and logs

---

## 📦 Complete Feature List

### Web Testing (Playwright)
- ✅ Page Object Model
- ✅ Cross-browser testing (Chrome, Firefox, Safari)
- ✅ Headless/Headed modes
- ✅ Screenshot on failure
- ✅ Video recording
- ✅ Trace files for debugging
- ✅ Parallel execution

### Mobile Testing (Appium)
- ✅ Android testing
- ✅ iOS testing
- ✅ Touch gestures
- ✅ Mobile page objects
- ✅ Device interactions
- ✅ Mobile screenshot capture

### API Testing
- ✅ RESTful API testing
- ✅ Request/Response validation
- ✅ JSON schema validation
- ✅ Response time validation
- ✅ Authentication support
- ✅ Retry mechanism

### Assertions
- ✅ Hard assertions (pytest)
- ✅ Soft assertions (custom)
- ✅ Playwright expect assertions
- ✅ API response assertions

### Reporting
- ✅ Allure reports
- ✅ HTML reports
- ✅ Email notifications
- ✅ Screenshots
- ✅ Videos
- ✅ Trace files
- ✅ Logs

### Configuration
- ✅ Environment-based config
- ✅ .env file support
- ✅ Multiple environments
- ✅ Configurable timeouts
- ✅ Email settings

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 2. Setup Appium (for Mobile Testing)

```bash
# Install Node.js first, then:
npm install -g appium
appium driver install uiautomator2  # For Android
appium driver install xcuitest      # For iOS

# Start Appium server
appium
```

### 3. Configure Email (Optional)

Edit `.env` file:

```bash
SEND_EMAIL_REPORT=true
SEND_EMAIL_ON_FAILURE=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECEIVER_EMAILS=recipient1@example.com,recipient2@example.com
```

**Note for Gmail:**
- Enable 2-Factor Authentication
- Generate App Password: https://myaccount.google.com/apppasswords
- Use App Password instead of regular password

---

## 🏃 Running Tests

### Web Tests (Playwright)

```bash
# Run all web tests
pytest tests/test_login.py tests/test_products.py

# Run with specific marker
pytest -m smoke
```

### API Tests

```bash
# Run API tests
pytest tests/test_api_examples.py -m api

# Run specific API test
pytest tests/test_api_examples.py::TestAPIExamples::test_get_all_posts
```

### Mobile Tests (Requires Appium Setup)

```bash
# Make sure Appium server is running first
appium

# In another terminal, run mobile tests
pytest tests/test_mobile_examples.py -m mobile

# Android specific
pytest -m android

# iOS specific
pytest -m ios
```

### Soft Assertion Tests

```bash
# Run soft assertion examples
pytest tests/test_soft_assertions.py

# These tests demonstrate continuing after failures
```

### Run All Tests

```bash
# Run everything
pytest

# Run with email report
SEND_EMAIL_REPORT=true pytest
```

---

## 📧 Email Notifications

### Email on Test Failure

When a test fails, an email is automatically sent (if configured) with:
- Test name
- Error message
- Screenshot (if available)
- Timestamp

### End-of-Execution Report

After all tests complete, a comprehensive email is sent with:
- Test statistics (total, passed, failed, skipped)
- Pass rate percentage
- Execution duration
- Environment and browser info
- Attached ZIP file containing:
  - Allure reports
  - Screenshots
  - Logs

### Sample Email Report

```
Subject: ✅ Test Report - PASSED (100% Pass Rate)

Test Execution Report
=====================

Summary:
- Total Tests: 25
- Passed: 23
- Failed: 2
- Skipped: 0
- Pass Rate: 92%
- Duration: 45.5 seconds

Environment: qa
Browser: chromium

[View attached report ZIP for details]
```

---

## 🧪 Test Examples

### 1. Web Test with Soft Assertions

```python
def test_products_with_soft_assertions(page, config, soft_assert):
    login_page = LoginPage(page)
    products_page = ProductsPage(page)
    
    # Login
    login_page.navigate_to_login_page()
    login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
    
    # Multiple assertions - all will be checked
    soft_assert.assert_equal(page.url, "expected_url")
    soft_assert.assert_true(products_page.is_visible())
    soft_assert.assert_greater(products_page.get_count(), 0)
    
    # Report all at once
    soft_assert.assert_all()
```

### 2. API Test

```python
def test_api_get_post(api_client):
    response = api_client.get("/posts/1")
    
    assert api_client.validate_status_code(response, 200)
    assert api_client.validate_response_time(response, 2.0)
    
    post = response.json()
    assert "title" in post
```

### 3. Mobile Test

```python
def test_mobile_login(mobile_driver):
    login_page = LoginMobilePage(mobile_driver)
    
    login_page.login("user", "pass")
    login_page.take_screenshot("after_login")
```

### 4. Integration Test (Web + API)

```python
def test_web_api_integration(page, api_client):
    # Create via API
    response = api_client.post("/users", json_data={...})
    user_id = response.json()["id"]
    
    # Verify in Web
    page.goto(f"/users/{user_id}")
    assert page.is_visible("#user-details")
```

---

## 📊 Soft Assertions Guide

### Available Assertions

```python
soft_assert.assert_equal(actual, expected, message)
soft_assert.assert_not_equal(actual, expected, message)
soft_assert.assert_true(condition, message)
soft_assert.assert_false(condition, message)
soft_assert.assert_in(item, container, message)
soft_assert.assert_not_in(item, container, message)
soft_assert.assert_is_none(obj, message)
soft_assert.assert_is_not_none(obj, message)
soft_assert.assert_greater(actual, expected, message)
soft_assert.assert_less(actual, expected, message)
soft_assert.assert_contains(text, substring, message)
```

### Usage Pattern

```python
def test_with_soft_assertions(soft_assert):
    # All these will be checked
    soft_assert.assert_equal(1, 1)
    soft_assert.assert_true(True)
    soft_assert.assert_in("a", ["a", "b"])
    
    # Must call assert_all() at the end
    soft_assert.assert_all()
```

### Benefits

1. **Continue Execution**: Test doesn't stop at first failure
2. **See All Issues**: Get complete picture of what failed
3. **Better Debugging**: More context about failures
4. **Cleaner Reports**: All failures in one place

---

## 📱 Mobile Testing with Appium

### Prerequisites

1. **Android**:
   - Android Studio
   - Android SDK
   - Emulator or real device
   - adb configured

2. **iOS**:
   - Xcode
   - iOS Simulator or real device
   - WebDriverAgent

### Configuration

Edit `.env`:

```bash
# Android
PLATFORM_NAME=Android
DEVICE_NAME=emulator-5554
APP_PACKAGE=com.example.app
APP_ACTIVITY=.MainActivity

# iOS
PLATFORM_NAME=iOS
DEVICE_NAME=iPhone 14
BUNDLE_ID=com.example.app
UDID=your-device-udid
```

### Available Mobile Methods

```python
# Navigation
page.click(locator)
page.send_keys(locator, text)
page.swipe("up")
page.scroll_to_element(locator)

# Validation
page.is_displayed(locator)
page.get_text(locator)
page.get_attribute(locator, attr)

# Gestures
page.tap(x, y)
page.long_press(locator)
page.hide_keyboard()

# Device
page.press_back()
page.take_screenshot(name)
```

---

## 🔧 API Testing Guide

### Basic Usage

```python
api = APIClient(base_url="https://api.example.com")

# Set authentication
api.set_auth_token("your-token")

# Make requests
response = api.get("/endpoint")
response = api.post("/endpoint", json_data={...})
response = api.put("/endpoint", json_data={...})
response = api.delete("/endpoint")

# Validate
api.validate_status_code(response, 200)
api.validate_response_time(response, 2.0)
api.validate_json_schema(response, schema)
```

### With Soft Assertions

```python
def test_api_with_soft_assert(api_client, soft_assert):
    response = api_client.get("/posts/1")
    post = response.json()
    
    soft_assert.assert_equal(response.status_code, 200)
    soft_assert.assert_in("title", post)
    soft_assert.assert_in("body", post)
    
    soft_assert.assert_all()
```

---

## 📈 Test Execution Tracking

The framework automatically tracks:
- Total tests run
- Passed/Failed/Skipped counts
- Execution duration
- Pass rate percentage

This data is used for:
- Email reports
- Allure reports
- Console output
- Logs

---

## 🎯 Best Practices

### 1. Use Soft Assertions For:
- ✅ Form validation (check all fields)
- ✅ Page element verification
- ✅ API response validation
- ✅ Data validation
- ❌ Critical path assertions (use hard asserts)

### 2. Email Configuration:
- Use separate email for automation
- Enable app passwords
- Test email config separately
- Keep credentials in .env (not in code)

### 3. Mobile Testing:
- Use stable locators (ID preferred)
- Add explicit waits
- Handle app permissions
- Test on real devices when possible

### 4. API Testing:
- Validate response structure
- Check response times
- Use JSON schema validation
- Test error scenarios

---

## 🐛 Troubleshooting

### Email Not Sending

```bash
# Test SMTP connection
python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).ehlo()"

# Check credentials in .env
# For Gmail, use App Password, not regular password
```

### Mobile Tests Not Running

```bash
# Check Appium server
appium

# Check device connection (Android)
adb devices

# Check Appium doctor
appium-doctor --android
appium-doctor --ios
```

### Soft Assertions Not Working

```python
# Always call assert_all() at the end
soft_assert.assert_equal(1, 1)
soft_assert.assert_all()  # Don't forget this!
```

---

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Appium Documentation](http://appium.io/docs/en/latest/)
- [Allure Report](https://docs.qameta.io/allure/)
- [pytest Documentation](https://docs.pytest.org/)

---

## 🎉 Summary

This enhanced framework provides:
- ✅ Complete web testing (Playwright)
- ✅ Mobile testing (Appium)
- ✅ API testing (REST)
- ✅ Soft assertions
- ✅ Email notifications
- ✅ Comprehensive reporting
- ✅ CI/CD ready
- ✅ Production-ready code

Perfect for enterprise test automation!
