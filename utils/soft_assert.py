"""
Soft Assertions utility for continuing test execution even after assertion failures.
"""
import allure
from typing import Any, Callable
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class SoftAssert:
    """
    Soft assertion class that collects assertion failures
    and reports them at the end.
    """
    
    def __init__(self):
        """Initialize soft assert."""
        self.errors = []
        self.assertion_count = 0
    
    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> None:
        """
        Assert that two values are equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert actual == expected, message or f"Expected '{expected}', but got '{actual}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: {actual} == {expected}")
            
            with allure.step(f"✓ Assert Equal: {actual} == {expected}"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Equal Failed: {actual} != {expected}"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_not_equal(self, actual: Any, expected: Any, message: str = "") -> None:
        """
        Assert that two values are not equal.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert actual != expected, message or f"Values should not be equal: '{actual}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: {actual} != {expected}")
            
            with allure.step(f"✓ Assert Not Equal: {actual} != {expected}"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Not Equal Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_true(self, condition: bool, message: str = "") -> None:
        """
        Assert that condition is True.
        
        Args:
            condition: Boolean condition
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert condition is True, message or f"Expected True, but got {condition}"
            logger.info(f"✓ Assertion {self.assertion_count} passed: condition is True")
            
            with allure.step(f"✓ Assert True"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert True Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_false(self, condition: bool, message: str = "") -> None:
        """
        Assert that condition is False.
        
        Args:
            condition: Boolean condition
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert condition is False, message or f"Expected False, but got {condition}"
            logger.info(f"✓ Assertion {self.assertion_count} passed: condition is False")
            
            with allure.step(f"✓ Assert False"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert False Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_in(self, item: Any, container: Any, message: str = "") -> None:
        """
        Assert that item is in container.
        
        Args:
            item: Item to check
            container: Container
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert item in container, message or f"'{item}' not found in '{container}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: '{item}' in container")
            
            with allure.step(f"✓ Assert In: '{item}' in container"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert In Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_not_in(self, item: Any, container: Any, message: str = "") -> None:
        """
        Assert that item is not in container.
        
        Args:
            item: Item to check
            container: Container
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert item not in container, message or f"'{item}' should not be in '{container}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: '{item}' not in container")
            
            with allure.step(f"✓ Assert Not In: '{item}' not in container"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Not In Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_is_none(self, obj: Any, message: str = "") -> None:
        """
        Assert that object is None.
        
        Args:
            obj: Object to check
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert obj is None, message or f"Expected None, but got '{obj}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: object is None")
            
            with allure.step(f"✓ Assert Is None"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Is None Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_is_not_none(self, obj: Any, message: str = "") -> None:
        """
        Assert that object is not None.
        
        Args:
            obj: Object to check
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert obj is not None, message or "Object should not be None"
            logger.info(f"✓ Assertion {self.assertion_count} passed: object is not None")
            
            with allure.step(f"✓ Assert Is Not None"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Is Not None Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_greater(self, actual: Any, expected: Any, message: str = "") -> None:
        """
        Assert that actual is greater than expected.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert actual > expected, message or f"Expected {actual} > {expected}"
            logger.info(f"✓ Assertion {self.assertion_count} passed: {actual} > {expected}")
            
            with allure.step(f"✓ Assert Greater: {actual} > {expected}"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Greater Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_less(self, actual: Any, expected: Any, message: str = "") -> None:
        """
        Assert that actual is less than expected.
        
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert actual < expected, message or f"Expected {actual} < {expected}"
            logger.info(f"✓ Assertion {self.assertion_count} passed: {actual} < {expected}")
            
            with allure.step(f"✓ Assert Less: {actual} < {expected}"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Less Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_contains(self, text: str, substring: str, message: str = "") -> None:
        """
        Assert that text contains substring.
        
        Args:
            text: Text to search in
            substring: Substring to find
            message: Custom error message
        """
        self.assertion_count += 1
        try:
            assert substring in text, message or f"'{substring}' not found in '{text}'"
            logger.info(f"✓ Assertion {self.assertion_count} passed: text contains '{substring}'")
            
            with allure.step(f"✓ Assert Contains: '{substring}' in text"):
                pass
                
        except AssertionError as e:
            error_msg = f"Assertion {self.assertion_count} failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            
            with allure.step(f"✗ Assert Contains Failed"):
                allure.attach(str(e), "Error", allure.attachment_type.TEXT)
    
    def assert_all(self) -> None:
        """
        Check all collected assertions and raise if any failed.
        This should be called at the end of the test.
        """
        if self.errors:
            error_summary = f"\n{'='*60}\n"
            error_summary += f"SOFT ASSERTION FAILURES: {len(self.errors)} out of {self.assertion_count}\n"
            error_summary += f"{'='*60}\n"
            
            for i, error in enumerate(self.errors, 1):
                error_summary += f"{i}. {error}\n"
            
            error_summary += f"{'='*60}"
            
            logger.error(error_summary)
            
            with allure.step(f"❌ {len(self.errors)} Soft Assertions Failed"):
                allure.attach(error_summary, "Assertion Failures", allure.attachment_type.TEXT)
            
            # Clear errors for next test
            self.errors.clear()
            self.assertion_count = 0
            
            raise AssertionError(error_summary)
        
        else:
            logger.info(f"✓ All {self.assertion_count} soft assertions passed")
            self.assertion_count = 0
    
    def get_error_count(self) -> int:
        """
        Get number of failed assertions.
        
        Returns:
            Number of errors
        """
        return len(self.errors)
    
    def has_errors(self) -> bool:
        """
        Check if there are any errors.
        
        Returns:
            True if errors exist
        """
        return len(self.errors) > 0
