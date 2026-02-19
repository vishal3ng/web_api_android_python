"""
API Testing Examples using APIClient.

This demonstrates API testing with:
- GET, POST, PUT, DELETE requests
- Response validation
- JSON schema validation
- Status code validation
- Response time validation
"""
import pytest
import allure
from api.api_client import APIClient
from utils.soft_assert import SoftAssert


@allure.epic("API Testing")
@allure.feature("JSONPlaceholder API")
class TestAPIExamples:
    """Example API tests using public JSONPlaceholder API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup API client."""
        self.api = APIClient(base_url="https://jsonplaceholder.typicode.com")
    
    @allure.story("GET Request")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test GET all posts")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_posts(self):
        """Test GET request to fetch all posts."""
        
        with allure.step("Send GET request to /posts"):
            response = self.api.get("/posts")
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 200)
            assert self.api.validate_response_time(response, 5.0)
            
            posts = response.json()
            assert len(posts) > 0, "No posts returned"
            assert isinstance(posts, list), "Response is not a list"
    
    @allure.story("GET Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test GET single post by ID")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_post_by_id(self):
        """Test GET request to fetch a specific post."""
        
        post_id = 1
        
        with allure.step(f"Send GET request to /posts/{post_id}"):
            response = self.api.get(f"/posts/{post_id}")
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 200)
            
            post = response.json()
            assert post["id"] == post_id
            assert "title" in post
            assert "body" in post
            assert "userId" in post
    
    @allure.story("POST Request")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test POST create new post")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_post(self):
        """Test POST request to create a new post."""
        
        new_post = {
            "title": "Test Post from Automation",
            "body": "This is a test post created by automation framework",
            "userId": 1
        }
        
        with allure.step("Send POST request to /posts"):
            response = self.api.post("/posts", json_data=new_post)
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 201)
            
            created_post = response.json()
            assert created_post["title"] == new_post["title"]
            assert created_post["body"] == new_post["body"]
            assert created_post["userId"] == new_post["userId"]
            assert "id" in created_post
    
    @allure.story("PUT Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test PUT update existing post")
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_post(self):
        """Test PUT request to update a post."""
        
        post_id = 1
        updated_post = {
            "id": post_id,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1
        }
        
        with allure.step(f"Send PUT request to /posts/{post_id}"):
            response = self.api.put(f"/posts/{post_id}", json_data=updated_post)
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 200)
            
            post = response.json()
            assert post["title"] == updated_post["title"]
            assert post["body"] == updated_post["body"]
    
    @allure.story("DELETE Request")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test DELETE post")
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_post(self):
        """Test DELETE request to delete a post."""
        
        post_id = 1
        
        with allure.step(f"Send DELETE request to /posts/{post_id}"):
            response = self.api.delete(f"/posts/{post_id}")
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 200)
    
    @allure.story("Query Parameters")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test GET with query parameters")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_with_query_params(self):
        """Test GET request with query parameters."""
        
        params = {"userId": 1}
        
        with allure.step("Send GET request with query params"):
            response = self.api.get("/posts", params=params)
        
        with allure.step("Validate response"):
            assert self.api.validate_status_code(response, 200)
            
            posts = response.json()
            assert len(posts) > 0
            
            # Verify all posts belong to userId 1
            for post in posts:
                assert post["userId"] == 1
    
    @allure.story("API with Soft Assertions")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test API response with soft assertions")
    @pytest.mark.api
    @pytest.mark.regression
    def test_api_with_soft_assertions(self, soft_assert: SoftAssert):
        """Test API response using soft assertions."""
        
        with allure.step("Send GET request to /posts/1"):
            response = self.api.get("/posts/1")
        
        with allure.step("Validate response with soft assertions"):
            post = response.json()
            
            # These assertions will all be checked even if some fail
            soft_assert.assert_equal(response.status_code, 200, "Status code should be 200")
            soft_assert.assert_in("id", post, "Response should contain 'id'")
            soft_assert.assert_in("title", post, "Response should contain 'title'")
            soft_assert.assert_in("body", post, "Response should contain 'body'")
            soft_assert.assert_in("userId", post, "Response should contain 'userId'")
            soft_assert.assert_true(len(post["title"]) > 0, "Title should not be empty")
            soft_assert.assert_true(len(post["body"]) > 0, "Body should not be empty")
            soft_assert.assert_greater(post["userId"], 0, "User ID should be positive")
            
            # Check all assertions at the end
            soft_assert.assert_all()
    
    @allure.story("Response Time Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test API response time")
    @pytest.mark.api
    @pytest.mark.performance
    def test_response_time(self):
        """Test API response time."""
        
        with allure.step("Send GET request and measure time"):
            response = self.api.get("/posts")
        
        with allure.step("Validate response time is under 2 seconds"):
            assert self.api.validate_response_time(response, 2.0)
            
            allure.attach(
                str(response.elapsed.total_seconds()),
                "Response Time (seconds)",
                allure.attachment_type.TEXT
            )
    
    @allure.story("JSON Schema Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test JSON schema validation")
    @pytest.mark.api
    @pytest.mark.regression
    def test_json_schema_validation(self):
        """Test JSON schema validation."""
        
        # Define expected schema
        post_schema = {
            "type": "object",
            "properties": {
                "userId": {"type": "integer"},
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["userId", "id", "title", "body"]
        }
        
        with allure.step("Send GET request"):
            response = self.api.get("/posts/1")
        
        with allure.step("Validate JSON schema"):
            assert self.api.validate_json_schema(response, post_schema)
