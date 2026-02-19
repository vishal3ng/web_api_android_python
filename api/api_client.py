"""
Base API Client for API testing.
"""
import requests
import allure
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import Logger
from config.config import Config
import json

logger = Logger.get_logger(__name__)


class APIClient:
    """Base class for API testing."""
    
    def __init__(self, base_url: str = None):
        """
        Initialize API Client.
        
        Args:
            base_url: Base URL for API endpoints
        """
        self.base_url = base_url or Config.API_BASE_URL
        self.session = self._create_session()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry strategy.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def set_auth_token(self, token: str, auth_type: str = "Bearer") -> None:
        """
        Set authentication token.
        
        Args:
            token: Authentication token
            auth_type: Type of authentication (Bearer, Basic, etc.)
        """
        self.headers["Authorization"] = f"{auth_type} {token}"
        logger.info(f"Auth token set: {auth_type} {token[:10]}...")
    
    def set_header(self, key: str, value: str) -> None:
        """
        Set custom header.
        
        Args:
            key: Header key
            value: Header value
        """
        self.headers[key] = value
        logger.info(f"Header set: {key}={value}")
    
    @allure.step("GET Request: {endpoint}")
    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"GET Request: {url}")
        if params:
            logger.info(f"Params: {params}")
        
        response = self.session.get(
            url,
            params=params,
            headers=merged_headers,
            timeout=Config.API_TIMEOUT
        )
        
        self._log_response(response)
        self._attach_to_allure(response, "GET")
        
        return response
    
    @allure.step("POST Request: {endpoint}")
    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"POST Request: {url}")
        if json_data:
            logger.info(f"JSON Data: {json_data}")
        
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            headers=merged_headers,
            timeout=Config.API_TIMEOUT
        )
        
        self._log_response(response)
        self._attach_to_allure(response, "POST")
        
        return response
    
    @allure.step("PUT Request: {endpoint}")
    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        """
        Send PUT request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"PUT Request: {url}")
        
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            headers=merged_headers,
            timeout=Config.API_TIMEOUT
        )
        
        self._log_response(response)
        self._attach_to_allure(response, "PUT")
        
        return response
    
    @allure.step("DELETE Request: {endpoint}")
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        """
        Send DELETE request.
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"DELETE Request: {url}")
        
        response = self.session.delete(
            url,
            headers=merged_headers,
            timeout=Config.API_TIMEOUT
        )
        
        self._log_response(response)
        self._attach_to_allure(response, "DELETE")
        
        return response
    
    @allure.step("PATCH Request: {endpoint}")
    def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        """
        Send PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        merged_headers = {**self.headers, **(headers or {})}
        
        logger.info(f"PATCH Request: {url}")
        
        response = self.session.patch(
            url,
            data=data,
            json=json_data,
            headers=merged_headers,
            timeout=Config.API_TIMEOUT
        )
        
        self._log_response(response)
        self._attach_to_allure(response, "PATCH")
        
        return response
    
    def _log_response(self, response: requests.Response) -> None:
        """
        Log response details.
        
        Args:
            response: Response object
        """
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        
        try:
            logger.info(f"Response Body: {response.json()}")
        except:
            logger.info(f"Response Body: {response.text[:200]}")
    
    def _attach_to_allure(self, response: requests.Response, method: str) -> None:
        """
        Attach request/response to Allure report.
        
        Args:
            response: Response object
            method: HTTP method
        """
        # Attach request
        request_data = {
            "method": method,
            "url": response.request.url,
            "headers": dict(response.request.headers),
            "body": response.request.body
        }
        allure.attach(
            json.dumps(request_data, indent=2),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )
        
        # Attach response
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "response_time": f"{response.elapsed.total_seconds():.2f}s"
        }
        
        try:
            response_data["body"] = response.json()
        except:
            response_data["body"] = response.text
        
        allure.attach(
            json.dumps(response_data, indent=2),
            name="Response",
            attachment_type=allure.attachment_type.JSON
        )
    
    def validate_status_code(self, response: requests.Response, expected_code: int) -> bool:
        """
        Validate response status code.
        
        Args:
            response: Response object
            expected_code: Expected status code
            
        Returns:
            True if status code matches
        """
        actual_code = response.status_code
        is_valid = actual_code == expected_code
        
        if is_valid:
            logger.info(f"✓ Status code validated: {actual_code}")
        else:
            logger.error(f"✗ Status code mismatch: Expected {expected_code}, Got {actual_code}")
        
        return is_valid
    
    def validate_response_time(self, response: requests.Response, max_time: float) -> bool:
        """
        Validate response time.
        
        Args:
            response: Response object
            max_time: Maximum allowed time in seconds
            
        Returns:
            True if response time is within limit
        """
        actual_time = response.elapsed.total_seconds()
        is_valid = actual_time <= max_time
        
        if is_valid:
            logger.info(f"✓ Response time validated: {actual_time:.2f}s <= {max_time}s")
        else:
            logger.error(f"✗ Response time exceeded: {actual_time:.2f}s > {max_time}s")
        
        return is_valid
    
    def validate_json_schema(self, response: requests.Response, schema: Dict) -> bool:
        """
        Validate JSON response against schema.
        
        Args:
            response: Response object
            schema: JSON schema
            
        Returns:
            True if valid
        """
        from jsonschema import validate, ValidationError
        
        try:
            validate(instance=response.json(), schema=schema)
            logger.info("✓ JSON schema validated")
            return True
        except ValidationError as e:
            logger.error(f"✗ JSON schema validation failed: {e.message}")
            return False
    
    def get_json(self, response: requests.Response) -> Dict[str, Any]:
        """
        Get JSON response.
        
        Args:
            response: Response object
            
        Returns:
            JSON data
        """
        return response.json()
