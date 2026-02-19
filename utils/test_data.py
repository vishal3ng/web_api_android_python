"""
Test data management utilities.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from faker import Faker
from utils.logger import Logger

logger = Logger.get_logger(__name__)
fake = Faker()


class TestDataManager:
    """Manage test data from various sources."""
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dictionary containing JSON data
        """
        logger.info(f"Loading JSON data from: {file_path}")
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """
        Load data from YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Dictionary containing YAML data
        """
        logger.info(f"Loading YAML data from: {file_path}")
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """
        Save data to JSON file.
        
        Args:
            data: Dictionary to save
            file_path: Path to save JSON file
        """
        logger.info(f"Saving JSON data to: {file_path}")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: str) -> None:
        """
        Save data to YAML file.
        
        Args:
            data: Dictionary to save
            file_path: Path to save YAML file
        """
        logger.info(f"Saving YAML data to: {file_path}")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)


class FakeDataGenerator:
    """Generate fake test data using Faker."""
    
    @staticmethod
    def generate_user() -> Dict[str, str]:
        """
        Generate fake user data.
        
        Returns:
            Dictionary with user data
        """
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
            "username": fake.user_name(),
            "password": fake.password(length=12),
        }
    
    @staticmethod
    def generate_company() -> Dict[str, str]:
        """
        Generate fake company data.
        
        Returns:
            Dictionary with company data
        """
        return {
            "name": fake.company(),
            "email": fake.company_email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "website": fake.url(),
        }
    
    @staticmethod
    def generate_credit_card() -> Dict[str, str]:
        """
        Generate fake credit card data.
        
        Returns:
            Dictionary with credit card data
        """
        return {
            "number": fake.credit_card_number(),
            "provider": fake.credit_card_provider(),
            "expiry_date": fake.credit_card_expire(),
            "security_code": fake.credit_card_security_code(),
        }
    
    @staticmethod
    def generate_product() -> Dict[str, Any]:
        """
        Generate fake product data.
        
        Returns:
            Dictionary with product data
        """
        return {
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": round(fake.random.uniform(10.0, 1000.0), 2),
            "sku": fake.ean(length=13),
            "category": fake.word(),
        }
