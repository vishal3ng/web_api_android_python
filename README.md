# Playwright Pytest Allure Test Automation Framework

A production-ready, industry-standard test automation framework using Python, Playwright, Pytest, and Allure reporting with Page Object Model (POM) design pattern.

## 🚀 Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Playwright**: Modern browser automation with cross-browser support
- **Pytest**: Powerful testing framework with extensive plugin ecosystem
- **Allure Reporting**: Beautiful, detailed test reports with screenshots and videos
- **Parallel Execution**: Run tests in parallel for faster execution
- **Custom Logger**: Structured logging with different log levels
- **Screenshot on Failure**: Automatic screenshot capture on test failures
- **Video Recording**: Optional video recording of test execution
- **Trace Debugging**: Playwright trace files for detailed debugging
- **Fake Data Generation**: Built-in fake data generator using Faker
- **Configuration Management**: Centralized configuration with environment support
- **Retry Mechanism**: Auto-retry failed tests
- **CI/CD Ready**: Easy integration with Jenkins, GitHub Actions, etc.

## 📁 Project Structure

```
playwright-pytest-framework/
├── config/                     # Configuration files
│   ├── __init__.py
│   └── config.py              # Central configuration management
├── pages/                      # Page Object Models
│   ├── __init__.py
│   ├── base_page.py           # Base page with common methods
│   ├── login_page.py          # Login page object
│   └── products_page.py       # Products page object
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_login.py          # Login tests
│   └── test_products.py       # Products tests
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Custom logger
│   ├── test_data.py           # Test data management
│   └── screenshot_manager.py  # Screenshot utilities
├── data/                       # Test data files
├── reports/                    # Test reports
│   ├── allure-results/        # Allure raw results
│   ├── allure-report/         # Allure HTML report
│   ├── html-report/           # Pytest HTML report
│   ├── screenshots/           # Test screenshots
│   ├── videos/                # Test videos
│   └── traces/                # Playwright traces
├── logs/                       # Log files
├── conftest.py                # Pytest fixtures and hooks
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                  # This file
```

## 🛠️ Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Allure command-line tool (for viewing reports)

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd playwright-pytest-framework
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**
```bash
playwright install
```

5. **Install Allure (Optional - for report viewing)**
```bash
# MacOS
brew install allure

# Windows (using Scoop)
scoop install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

6. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🏃 Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_login.py
```

### Run specific test
```bash
pytest tests/test_login.py::TestLogin::test_successful_login
```

### Run tests by markers
```bash
# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run critical tests
pytest -m critical
```

### Run tests in parallel
```bash
pytest -n auto
```

### Run tests with retry on failure
```bash
pytest --reruns 2 --reruns-delay 1
```

### Run in headless mode
```bash
pytest --headed=false
```

### Run with specific browser
```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

## 📊 Viewing Reports

### Allure Report

1. **Generate and open report**
```bash
allure serve reports/allure-results
```

2. **Generate report only**
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

3. **Open existing report**
```bash
allure open reports/allure-report
```

### HTML Report

Open the file: `reports/html-report/report.html` in a browser

## 🎯 Test Markers

- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.critical` - Critical path tests
- `@pytest.mark.login` - Login functionality tests
- `@pytest.mark.checkout` - Checkout flow tests
- `@pytest.mark.slow` - Tests that take longer time

## 📝 Writing Tests

### Example Test

```python
import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage

@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:
    
    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_successful_login(self, page: Page):
        login_page = LoginPage(page)
        
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
        
        with allure.step("Login with valid credentials"):
            login_page.login("username", "password")
        
        with allure.step("Verify successful login"):
            assert "dashboard" in page.url
```

### Example Page Object

```python
from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    
    # Locators
    USERNAME = "#username"
    PASSWORD = "#password"
    LOGIN_BTN = "#login"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
```

## 🔧 Configuration

Edit `config/config.py` or `.env` file:

- `ENV`: Environment (dev, qa, staging, prod)
- `BASE_URL`: Application base URL
- `BROWSER`: Browser to use (chromium, firefox, webkit)
- `HEADLESS`: Run in headless mode (true/false)
- `RECORD_VIDEO`: Enable video recording (true/false)
- `ENABLE_TRACING`: Enable Playwright tracing (true/false)
- `DEFAULT_TIMEOUT`: Default timeout in milliseconds
- `PARALLEL_WORKERS`: Number of parallel workers

## 🐛 Debugging

### View trace file
```bash
playwright show-trace reports/traces/trace_*.zip
```

### Enable verbose logging
```bash
pytest -vv
```

### Keep browser open
```bash
pytest --headed --slowmo 1000
```

## 📦 CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        run: pytest
      - name: Upload Allure Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: allure-results
          path: reports/allure-results
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/)
- [Pytest](https://pytest.org/)
- [Allure Framework](https://docs.qameta.io/allure/)

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Happy Testing! 🚀**
