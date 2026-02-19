# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd playwright-pytest-framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browsers
playwright install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# The default settings work with https://www.saucedemo.com
```

### 3. Run Your First Test

```bash
# Run smoke tests (fastest)
pytest -m smoke

# Run specific test file
pytest tests/test_login.py

# Run with visual browser
pytest --headed

# Run in parallel for speed
pytest -n auto
```

### 4. View Reports

```bash
# Generate and open Allure report
allure serve reports/allure-results

# Or open HTML report
open reports/html-report/report.html
```

## 📝 Common Commands

### Using Pytest Directly

```bash
# Run all tests
pytest

# Run with specific browser
pytest --browser firefox

# Run specific test
pytest tests/test_login.py::TestLogin::test_successful_login

# Run by marker
pytest -m "smoke and critical"

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Using Shell Scripts (Linux/Mac)

```bash
# Make script executable (first time only)
chmod +x run_tests.sh

# Run smoke tests
./run_tests.sh smoke

# Run with Firefox
./run_tests.sh all firefox

# Run headed mode
./run_tests.sh smoke chromium true
```

### Using Batch Script (Windows)

```cmd
# Run smoke tests
run_tests.bat smoke

# Run with Firefox
run_tests.bat all firefox

# Run headed mode
run_tests.bat smoke chromium true
```

### Using Makefile (Linux/Mac)

```bash
# Run smoke tests
make smoke

# Run all tests in parallel
make parallel

# Run headed mode
make headed

# Generate report
make report

# Clean all reports
make clean
```

## 🐳 Docker Commands

```bash
# Build image
docker-compose build

# Run smoke tests
docker-compose run playwright-tests

# Run in parallel
docker-compose run playwright-parallel

# Start Allure service
docker-compose up allure
# Then visit http://localhost:5050
```

## 📊 Understanding Results

### Test Output
- ✅ Green dot (.) = Passed
- ❌ Red F = Failed
- ⚠️  Yellow s = Skipped

### Reports Location
- Allure: `reports/allure-results/`
- HTML: `reports/html-report/report.html`
- Screenshots: `reports/screenshots/`
- Videos: `reports/videos/`
- Traces: `reports/traces/`
- Logs: `logs/`

## 🎯 Next Steps

1. **Write Your First Test**
   - Copy an existing test
   - Modify for your use case
   - Run and verify

2. **Create Page Objects**
   - Identify your web pages
   - Create new page objects in `pages/`
   - Follow the BasePage pattern

3. **Add Test Data**
   - Add JSON/YAML files to `data/`
   - Use TestDataManager to load data
   - Or use FakeDataGenerator

4. **Customize Configuration**
   - Edit `config/config.py`
   - Update `.env` file
   - Adjust `pytest.ini`

## ❓ Troubleshooting

### Tests not finding elements?
- Check if selectors are correct
- Increase timeout in config
- Use `--headed` to see browser

### Import errors?
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### Browser not installing?
- Run: `playwright install --force`
- Check internet connection

### Allure report not opening?
- Install Allure: See README installation section
- Check path: `allure serve reports/allure-results`

## 💡 Pro Tips

1. **Debug failed tests**: Check screenshots in `reports/screenshots/`
2. **View detailed trace**: `playwright show-trace reports/traces/trace_*.zip`
3. **Speed up tests**: Use `pytest -n auto` for parallel execution
4. **Focus on failures**: Use `pytest --lf` (last failed)
5. **Skip tests**: Use `pytest --sw` (stepwise)

## 📚 Learn More

- [Playwright Docs](https://playwright.dev/python/)
- [Pytest Docs](https://docs.pytest.org/)
- [Allure Docs](https://docs.qameta.io/allure/)
- Check `README.md` for full documentation

---

**Need help?** Create an issue in the repository!
