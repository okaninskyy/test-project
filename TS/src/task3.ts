import axios from 'axios';
import { table } from 'table';
import * as os from 'os';

// Types
interface Address {
  street: string;
  city: string;
  zipcode: string;
  suite: string;
  geo: {
    lat: string;
    lng: string;
  };
}

interface User {
  id: number;
  name: string;
  email: string;
  address: Address;
  phone: string;
  website: string;
  company: {
    name: string;
    catchPhrase: string;
    bs: string;
  };
}

// Utility functions
function clearScreen(): void {
  console.clear();
}

async function fetchUsers(): Promise<User[] | null> {
  const url = "https://jsonplaceholder.typicode.com/users";
  const timeout = 10000; // 10 seconds

  try {
    console.log("\nFetching users from the API...");
    const response = await axios.get<User[]>(url, { timeout });
    
    // Validate user data
    console.log("\nValidating user data...");
    const validUsers = response.data.filter(user => {
      if (typeof user === 'object' && user.name && typeof user.name === 'string') {
        console.log(`  ✓ Valid user: ${user.name}`);
        return true;
      }
      console.log(`  × Invalid user data: ${JSON.stringify(user)}`);
      return false;
    });

    if (validUsers.length === 0) {
      console.log("\nError: No valid users found in API response");
      return null;
    }

    console.log(`\nSuccessfully loaded ${validUsers.length} valid users`);
    return validUsers;

  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === 'ECONNABORTED') {
        console.log("\nError: The request timed out. Please check your internet connection and try again.");
      } else if (error.response) {
        if (error.response.status === 404) {
          console.log("\nError: The requested resource was not found.");
        } else if (error.response.status === 403) {
          console.log("\nError: Access to the resource is forbidden.");
        } else {
          console.log(`\nError: Server returned an error (Status code: ${error.response.status})`);
        }
      } else if (error.request) {
        console.log("\nError: Could not connect to the server. Please check your internet connection.");
      }
    } else {
      console.log(`\nAn unexpected error occurred: ${error}`);
    }
    return null;
  }
}

function filterUsersByName(users: User[], searchTerm: string): User[] {
  if (!users) {
    return [];
  }

  if (!searchTerm || searchTerm.trim() === '') {
    console.log("\nWarning: Empty search term - returning all users");
    return users;
  }

  try {
    // Print available names for debugging
    console.log("\nAvailable names in database:");
    users.forEach(user => console.log(`  • ${user.name}`));

    let pattern: RegExp;
    try {
      if (searchTerm.startsWith('\\')) {
        const literalSearch = searchTerm.slice(1);
        pattern = new RegExp(literalSearch.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
        console.log(`\nUsing literal search pattern: ${literalSearch}`);
      } else {
        pattern = new RegExp(searchTerm, 'i');
        console.log(`\nUsing regex pattern: ${searchTerm}`);
      }
    } catch (e) {
      console.log(`\nInvalid regular expression: ${e}`);
      console.log("Tips:");
      console.log("- Use \\. to match a literal dot");
      console.log("- Use \\* to match a literal asterisk");
      console.log("- Use \\[ to match a literal square bracket");
      console.log("- Add \\ before any special character to match it literally");
      console.log("\nFalling back to plain text search...");
      pattern = new RegExp(searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
    }

    const filteredUsers = users.filter(user => {
      const match = pattern.exec(user.name);
      if (match) {
        console.log(`  ✓ '${user.name}' matches at position ${match.index}-${match.index + match[0].length}: '${match[0]}'`);
        return true;
      }
      console.log(`  × '${user.name}' does not match`);
      return false;
    });

    if (filteredUsers.length === 0) {
      console.log(`\nNo users found matching pattern '${searchTerm}' in their name.`);
    } else {
      console.log(`\nFound ${filteredUsers.length} user(s) matching pattern '${searchTerm}' in their name:`);
      filteredUsers.forEach(user => console.log(`  - ${user.name}`));
    }

    return filteredUsers;

  } catch (error) {
    console.log(`\nUnexpected error while filtering users: ${error}`);
    console.log("Returning all users...");
    return users;
  }
}

function displayUsers(users: User[] | null): void {
  clearScreen();
  if (!users || users.length === 0) {
    console.log("\nNo users found matching the search criteria.");
    return;
  }

  try {
    users.forEach(user => {
      console.log(`\nName: ${user.name}`);
      console.log(`Email: ${user.email}`);
      console.log(`Address: ${user.address.street}, ${user.address.city}`);
      console.log("-".repeat(50));
    });

    // Add pause at the end of display
    console.log("\nPress Enter to continue...");
    require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    }).question('', () => {
      clearScreen();
      process.stdin.resume();
    });
  } catch (error) {
    console.log(`\nError while displaying users: ${error}`);
  }
}

function displayUsersJson(users: User[]): void {
  clearScreen();
  try {
    const formattedJson = JSON.stringify(users, null, 2);
    console.log("\nUsers in JSON format:");
    console.log(formattedJson);
    console.log("\nPress Enter to continue...");
    require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    }).question('', () => {
      clearScreen();
      process.stdin.resume();
    });
  } catch (error) {
    console.log(`\nError formatting JSON: ${error}`);
  }
}

function displayUsersTable(users: User[]): void {
  clearScreen();
  try {
    const headers = ["Name", "Email", "Street", "City"];
    const data = [
      headers,
      ...users.map(user => [
        user.name,
        user.email,
        user.address.street,
        user.address.city
      ])
    ];

    console.log("\nUsers in table format:");
    console.log(table(data));
    console.log("\nPress Enter to continue...");
    require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    }).question('', () => {
      clearScreen();
      process.stdin.resume();
    });
  } catch (error) {
    console.log(`\nError creating table: ${error}`);
  }
}

function displayUsersCompact(users: User[]): void {
  clearScreen();
  try {
    console.log("\nUsers in compact format:");
    users.forEach(user => {
      console.log(`${user.name} | ${user.email} | ${user.address.street}, ${user.address.city}`);
    });
    console.log("\nPress Enter to continue...");
    require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    }).question('', () => {
      clearScreen();
      process.stdin.resume();
    });
  } catch (error) {
    console.log(`\nError displaying compact format: ${error}`);
  }
}

async function chooseDisplayFormat(users: User[]): Promise<void> {
  while (true) {
    clearScreen();
    console.log("\nChoose display format:");
    console.log("1. Standard format");
    console.log("2. JSON format");
    console.log("3. Table format");
    console.log("4. Compact format");
    console.log("5. Back to main menu");

    const rl = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const choice = await new Promise<string>(resolve => {
      rl.question('\nEnter your choice (1-5): ', resolve);
    });
    rl.close();

    switch (choice.trim()) {
      case "1":
        displayUsers(users);
        break;
      case "2":
        displayUsersJson(users);
        break;
      case "3":
        displayUsersTable(users);
        break;
      case "4":
        displayUsersCompact(users);
        break;
      case "5":
        clearScreen();
        return;
      default:
        console.log("\nInvalid choice. Please enter 1-5.");
        console.log("\nPress Enter to continue...");
        await new Promise(resolve => {
          require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
          }).question('', resolve);
        });
    }
  }
}

async function main(): Promise<void> {
  // Fetch all users
  clearScreen();
  const users = await fetchUsers();

  if (!users) {
    console.log("\nCould not fetch user data. Please try again later.");
    return;
  }

  while (true) {
    try {
      console.log("\nOptions:");
      console.log("1. Show all users");
      console.log("2. Filter users by name (supports regex)");
      console.log("3. Change display format");
      console.log("4. Exit");

      const rl = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
      });

      const choice = await new Promise<string>(resolve => {
        rl.question('\nEnter your choice (1-4): ', resolve);
      });
      rl.close();

      switch (choice.trim()) {
        case "1":
          console.log("\nShowing all users:");
          displayUsers(users);
          break;

        case "2":
          clearScreen();
          console.log("\nRegex Pattern Examples:");
          console.log("  ^A        - names starting with A");
          console.log("  a$        - names ending with a");
          console.log("  .*son.*   - names containing 'son'");
          console.log("  [AM].*    - names starting with A or M");
          console.log("  \\bJohn\\b - match whole word 'John'");
          console.log("\nSpecial Characters:");
          console.log("  Add \\ before . * + ? ^ $ [ ] ( ) { } | \\ to match them literally");
          console.log("  Example: \\. matches literal dot, \\* matches literal asterisk");
          console.log("\nAvailable names for reference:");
          users.forEach(user => console.log(`  - ${user.name}`));

          const searchTerm = await new Promise<string>(resolve => {
            require('readline').createInterface({
              input: process.stdin,
              output: process.stdout
            }).question('\nEnter a regex pattern to search for (or \'\\\' followed by text for literal search): ', resolve);
          });

          if (!searchTerm) {
            console.log("\nEmpty search term - showing all users");
            displayUsers(users);
            continue;
          }

          const filteredUsers = filterUsersByName(users, searchTerm);
          if (filteredUsers.length > 0) {
            console.log(`\nShowing users matching pattern '${searchTerm}':`);
            displayUsers(filteredUsers);
          }
          break;

        case "3":
          await chooseDisplayFormat(users);
          break;

        case "4":
          clearScreen();
          console.log("\nGoodbye!");
          return;

        default:
          console.log("\nInvalid choice. Please enter 1-4.");
          console.log("\nPress Enter to continue...");
          await new Promise(resolve => {
            require('readline').createInterface({
              input: process.stdin,
              output: process.stdout
            }).question('', resolve);
          });
      }
    } catch (error) {
      if (error instanceof Error && error.name === 'SyntaxError') {
        console.log("\nInvalid input. Please try again.");
      } else {
        console.log(`\nAn unexpected error occurred: ${error}`);
        console.log("Please try again.");
      }
      console.log("\nPress Enter to continue...");
      await new Promise(resolve => {
        require('readline').createInterface({
          input: process.stdin,
          output: process.stdout
        }).question('', resolve);
      });
    }
  }
}

// Run the program
if (require.main === module) {
  main().catch(error => {
    console.log(`\nFatal error: ${error}`);
    process.exit(1);
  });
} 