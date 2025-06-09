import aiohttp
import asyncio
import json
from typing import List, Dict, Optional
import sys
import os
from tabulate import tabulate  # For table formatting
import re  # For regular expressions

def clear_screen() -> None:
    """Clear the terminal screen for both Windows and Unix-like systems"""
    os.system('cls' if os.name == 'nt' else 'clear')

async def fetch_users() -> Optional[List[Dict]]:
    """
    Asynchronously fetch users from the API with comprehensive error handling
    """
    url = "https://jsonplaceholder.typicode.com/users"
    timeout = aiohttp.ClientTimeout(total=10)  # 10 seconds timeout
    
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                # Check if the response status is OK (200)
                response.raise_for_status()
                
                # Try to parse JSON response
                return await response.json()
                
    except aiohttp.ClientTimeout:
        print("\nError: The request timed out. Please check your internet connection and try again.")
    except aiohttp.ClientConnectionError:
        print("\nError: Could not connect to the server. Please check your internet connection.")
    except aiohttp.ContentTypeError:
        print("\nError: Received invalid JSON response from the server.")
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            print("\nError: The requested resource was not found.")
        elif e.status == 403:
            print("\nError: Access to the resource is forbidden.")
        else:
            print(f"\nError: Server returned an error (Status code: {e.status})")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    
    return None

def filter_users_by_name(users: List[Dict], search_term: str) -> List[Dict]:
    """
    Filter users based on regular expression pattern (case-insensitive)
    Examples:
        - "^A" will match names starting with A
        - "a$" will match names ending with a
        - ".*son.*" will match names containing "son"
        - "[AM].*" will match names starting with A or M
    """
    if not users:
        return []
        
    # Handle empty search term
    if not search_term or search_term.isspace():
        print("\nWarning: Empty search term - returning all users")
        return users
    
    try:
        # Try to compile the regular expression pattern
        try:
            # Escape special characters if the pattern starts with a backslash
            if search_term.startswith('\\'):
                search_term = re.escape(search_term[1:])
                print(f"\nUsing literal search pattern: {search_term}")
            else:
                print(f"\nUsing regex pattern: {search_term}")
            
            pattern = re.compile(search_term, re.IGNORECASE)
            
        except re.error as e:
            print(f"\nInvalid regular expression: {str(e)}")
            print("Tips:")
            print("- Use \\. to match a literal dot")
            print("- Use \\* to match a literal asterisk")
            print("- Use \\[ to match a literal square bracket")
            print("- Add \\ before any special character to match it literally")
            print("\nFalling back to plain text search...")
            # Fallback to plain text search if regex is invalid
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        
        # Perform the search with detailed error handling
        try:
            filtered_users = []
            print("\nDebug: Matching names:")
            for user in users:
                name = user['name']
                if pattern.search(name):
                    filtered_users.append(user)
                    print(f"  ✓ '{name}' matches pattern")
                else:
                    print(f"  × '{name}' does not match pattern")
            
            # Provide feedback about the search results
            if not filtered_users:
                print(f"\nNo users found matching pattern '{search_term}' in their name.")
            else:
                print(f"\nFound {len(filtered_users)} user(s) matching pattern '{search_term}' in their name:")
                for user in filtered_users:
                    print(f"  - {user['name']}")
                
            return filtered_users
            
        except Exception as search_error:
            print(f"\nError during pattern matching: {str(search_error)}")
            print("Falling back to plain text search...")
            # Ultimate fallback - plain text contains search
            return [user for user in users if search_term.lower() in user['name'].lower()]
            
    except Exception as e:
        print(f"\nUnexpected error while filtering users: {str(e)}")
        print("Returning all users...")
        return users

def display_users(users: Optional[List[Dict]]) -> None:
    """
    Display user information with error handling
    """
    clear_screen()
    if not users:
        print("\nNo users found matching the search criteria.")
        return
    
    try:
        for user in users:
            print(f"\nName: {user['name']}")
            print(f"Email: {user['email']}")
            print(f"Address: {user['address']['street']}, {user['address']['city']}")
            print("-" * 50)
        
        # Add pause at the end of display
        input("\nPress Enter to continue...")
        clear_screen()
    except KeyError as e:
        print(f"\nError: Missing required field in user data: {str(e)}")
    except Exception as e:
        print(f"\nError while displaying users: {str(e)}")

def display_users_json(users: List[Dict]) -> None:
    """Display users in JSON format"""
    clear_screen()
    try:
        formatted_json = json.dumps(users, indent=2)
        print("\nUsers in JSON format:")
        print(formatted_json)
        input("\nPress Enter to continue...")
        clear_screen()
    except Exception as e:
        print(f"\nError formatting JSON: {str(e)}")

def display_users_table(users: List[Dict]) -> None:
    """Display users in table format"""
    clear_screen()
    try:
        # Prepare data for table
        table_data = []
        headers = ["Name", "Email", "Street", "City"]
        
        for user in users:
            row = [
                user['name'],
                user['email'],
                user['address']['street'],
                user['address']['city']
            ]
            table_data.append(row)
        
        print("\nUsers in table format:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        input("\nPress Enter to continue...")
        clear_screen()
    except Exception as e:
        print(f"\nError creating table: {str(e)}")

def display_users_compact(users: List[Dict]) -> None:
    """Display users in compact format"""
    clear_screen()
    try:
        print("\nUsers in compact format:")
        for user in users:
            print(f"{user['name']} | {user['email']} | {user['address']['street']}, {user['address']['city']}")
        input("\nPress Enter to continue...")
        clear_screen()
    except Exception as e:
        print(f"\nError displaying compact format: {str(e)}")

def choose_display_format(users: List[Dict]) -> None:
    """Choose and apply display format for users"""
    while True:
        clear_screen()
        print("\nChoose display format:")
        print("1. Standard format")
        print("2. JSON format")
        print("3. Table format")
        print("4. Compact format")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            display_users(users)
        elif choice == "2":
            display_users_json(users)
        elif choice == "3":
            display_users_table(users)
        elif choice == "4":
            display_users_compact(users)
        elif choice == "5":
            clear_screen()
            break
        else:
            print("\nInvalid choice. Please enter 1-5.")
            input("\nPress Enter to continue...")

async def main() -> None:
    """
    Main program loop with error handling
    """
    # Fetch all users
    clear_screen()
    print("\nFetching users from the API...")
    users = await fetch_users()
    
    if users is None:
        print("\nCould not fetch user data. Please try again later.")
        return
    
    while True:
        try:
            #clear_screen()
            print("\nOptions:")
            print("1. Show all users")
            print("2. Filter users by name (supports regex)")
            print("3. Change display format")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            
            if choice == "1":
                print("\nShowing all users:")
                display_users(users)
            
            elif choice == "2":
                clear_screen()
                print("\nRegex Pattern Examples:")
                print("  ^A        - names starting with A")
                print("  a$        - names ending with a")
                print("  .*son.*   - names containing 'son'")
                print("  [AM].*    - names starting with A or M")
                print("  \\bJohn\\b - match whole word 'John'")
                print("\nSpecial Characters:")
                print("  Add \\ before . * + ? ^ $ [ ] ( ) { } | \\ to match them literally")
                print("  Example: \\. matches literal dot, \\* matches literal asterisk")
                print("\nAvailable names for reference:")
                for user in users:
                    print(f"  - {user['name']}")
                
                search_term = input("\nEnter a regex pattern to search for (or '\\' + text for literal search): ").strip()
                if not search_term:
                    print("\nEmpty search term - showing all users")
                    display_users(users)
                    continue
                    
                #clear_screen()
                filtered_users = filter_users_by_name(users, search_term)
                if filtered_users:  # Only show users if we found any
                    print(f"\nShowing users matching pattern '{search_term}':")
                    display_users(filtered_users)
            
            elif choice == "3":
                choose_display_format(users)
            
            elif choice == "4":
                clear_screen()
                print("\nGoodbye!")
                break
            
            else:
                print("\nInvalid choice. Please enter 1-4.")
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            # Set up proper event loop policy for Windows
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        clear_screen()
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
