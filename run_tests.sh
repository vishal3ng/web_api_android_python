#!/bin/bash

# Playwright Pytest Test Execution Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Playwright Test Automation${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}Virtual environment not activated. Activating...${NC}"
    source venv/bin/activate
fi

# Parse command line arguments
TEST_TYPE=${1:-all}
BROWSER=${2:-chromium}
HEADED=${3:-false}

echo -e "${GREEN}Configuration:${NC}"
echo -e "  Test Type: ${YELLOW}$TEST_TYPE${NC}"
echo -e "  Browser: ${YELLOW}$BROWSER${NC}"
echo -e "  Headed: ${YELLOW}$HEADED${NC}"
echo ""

# Run tests based on type
case $TEST_TYPE in
    smoke)
        echo -e "${GREEN}Running smoke tests...${NC}"
        pytest -m smoke --browser=$BROWSER --headed=$HEADED
        ;;
    regression)
        echo -e "${GREEN}Running regression tests...${NC}"
        pytest -m regression --browser=$BROWSER --headed=$HEADED
        ;;
    critical)
        echo -e "${GREEN}Running critical tests...${NC}"
        pytest -m critical --browser=$BROWSER --headed=$HEADED
        ;;
    login)
        echo -e "${GREEN}Running login tests...${NC}"
        pytest tests/test_login.py --browser=$BROWSER --headed=$HEADED
        ;;
    products)
        echo -e "${GREEN}Running products tests...${NC}"
        pytest tests/test_products.py --browser=$BROWSER --headed=$HEADED
        ;;
    parallel)
        echo -e "${GREEN}Running all tests in parallel...${NC}"
        pytest -n auto --browser=$BROWSER --headed=$HEADED
        ;;
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest --browser=$BROWSER --headed=$HEADED
        ;;
    *)
        echo -e "${RED}Invalid test type: $TEST_TYPE${NC}"
        echo -e "Usage: ./run_tests.sh [smoke|regression|critical|login|products|parallel|all] [chromium|firefox|webkit] [true|false]"
        exit 1
        ;;
esac

TEST_EXIT_CODE=$?

echo ""
echo -e "${GREEN}================================${NC}"

# Generate Allure report
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Tests completed successfully!${NC}"
    echo -e "${GREEN}Generating Allure report...${NC}"
    allure serve reports/allure-results
else
    echo -e "${RED}Some tests failed!${NC}"
    echo -e "${YELLOW}Generating Allure report for failed tests...${NC}"
    allure serve reports/allure-results
fi

exit $TEST_EXIT_CODE
