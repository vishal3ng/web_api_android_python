.PHONY: help install setup test smoke regression parallel clean report

help:
	@echo "Playwright Pytest Framework Commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make setup       - Complete setup (venv + install + browsers)"
	@echo "  make test        - Run all tests"
	@echo "  make smoke       - Run smoke tests"
	@echo "  make regression  - Run regression tests"
	@echo "  make critical    - Run critical tests"
	@echo "  make parallel    - Run tests in parallel"
	@echo "  make headed      - Run tests in headed mode"
	@echo "  make report      - Generate and open Allure report"
	@echo "  make clean       - Clean reports and logs"

install:
	pip install -r requirements.txt
	playwright install

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && playwright install

test:
	pytest

smoke:
	pytest -m smoke

regression:
	pytest -m regression

critical:
	pytest -m critical

parallel:
	pytest -n auto

headed:
	pytest --headed

report:
	allure serve reports/allure-results

clean:
	rm -rf reports/allure-results/*
	rm -rf reports/allure-report/*
	rm -rf reports/screenshots/*
	rm -rf reports/videos/*
	rm -rf reports/traces/*
	rm -rf logs/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
