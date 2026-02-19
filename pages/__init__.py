"""Pages package for Page Object Model."""
from .base_page import BasePage
from .login_page import LoginPage
from .products_page import ProductsPage

__all__ = ["BasePage", "LoginPage", "ProductsPage"]
