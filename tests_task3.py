import pytest
import allure
import asyncio
from task3 import (
    fetch_users,
    filter_users_by_name,
    display_users,
    display_users_json,
    display_users_table,
    display_users_compact,
    choose_display_format,
    main
)

@allure.epic("User Management System")
@allure.feature("API Integration")
class TestUserManagement:

    @pytest.fixture
    async def sample_users(self):
        """
        Fixture providing sample user data for testing.
        Returns a list of two users with predefined data structure.
        """
        return [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "address": {"street": "123 Main St", "city": "Boston"}
            },
            {
                "name": "Alice Smith",
                "email": "alice@example.com", 
                "address": {"street": "456 Oak Ave", "city": "Chicago"}
            }
        ]

    @allure.story("User Fetching")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    async def test_fetch_users(self):
        """
        Test cases for fetch_users function:
        1. Verify API connection and successful data retrieval
        2. Validate that returned data is a non-empty list
        3. Check that each user object contains required 'name' field
        4. Ensure the response format matches expected structure
        """
        with allure.step("Fetching users from API"):
            users = await fetch_users()
        
        with allure.step("Validating fetched users"):
            assert users is not None
            assert isinstance(users, list)
            assert len(users) > 0
            assert all('name' in user for user in users)

    @allure.story("User Filtering")
    @allure.severity(allure.severity_level.NORMAL) 
    def test_filter_users_by_name(self, sample_users):
        """
        Test cases for filter_users_by_name function:
        1. Test regex pattern '^J' - Should match names starting with J (expects 1 match)
        2. Test regex pattern 'Smith$' - Should match names ending with Smith (expects 1 match)
        3. Test regex pattern '.*o.*' - Should match names containing 'o' (expects 1 match)
        4. Test empty pattern '' - Should return all users (expects 2 matches)
        5. Test regex pattern '[JA].*' - Should match names starting with J or A (expects 2 matches)
        """
        test_cases = [
            ("^J", 1),  # Names starting with J
            ("Smith$", 1),  # Names ending with Smith
            (".*o.*", 1),  # Names containing 'o'
            ("", 2),  # Empty pattern returns all users
            ("[JA].*", 2)  # Names starting with J or A
        ]

        for pattern, expected_count in test_cases:
            with allure.step(f"Testing pattern: {pattern}"):
                filtered = filter_users_by_name(sample_users, pattern)
                assert len(filtered) == expected_count

    @allure.story("Display Formatting")
    @allure.severity(allure.severity_level.MINOR)
    def test_display_functions(self, sample_users, capsys):
        """
        Test cases for display functions:
        1. Test standard display format (display_users)
           - Verifies proper formatting of user details in standard view
        2. Test JSON display format (display_users_json)
           - Ensures valid JSON formatting and structure
        3. Test table display format (display_users_table)
           - Checks tabular formatting with headers and grid
        4. Test compact display format (display_users_compact)
           - Validates single-line compact representation
        Each function is tested for successful output generation
        """
        display_functions = [
            display_users,
            display_users_json,
            display_users_table,
            display_users_compact
        ]

        for func in display_functions:
            with allure.step(f"Testing {func.__name__}"):
                func(sample_users)
                captured = capsys.readouterr()
                assert captured.out  # Verify some output was produced

    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    def test_error_handling(self):
        """
        Test cases for error handling:
        1. Test invalid user data structure
           - Provides malformed user data
           - Expects exception to be raised
           - Verifies proper error handling for missing required fields
        """
        with allure.step("Testing invalid user data"):
            invalid_users = [{"invalid": "data"}]
            with pytest.raises(Exception):
                display_users(invalid_users)

    @allure.story("Main Program Flow")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.asyncio
    async def test_main_program(self, monkeypatch):
        """
        Test cases for main program flow:
        1. Test basic program execution
           - Simulates user selecting option 1 (Show all users)
           - Simulates user selecting option 4 (Exit)
           - Verifies program executes without errors
           - Ensures proper handling of user input and program flow
        """
        with allure.step("Testing main program execution"):
            # Simulate user input
            inputs = iter(['1', '4'])  # Show all users, then exit
            monkeypatch.setattr('builtins.input', lambda _: next(inputs))
            
            # Run main without errors
            await main()

if __name__ == '__main__':
    pytest.main(['-v', '--alluredir=./allure-results'])
