# User Management Application (TypeScript)

This is a TypeScript version of the user management application that fetches and displays user data from JSONPlaceholder API.

## Features

- Fetch and display user data
- Filter users by name using regex patterns
- Multiple display formats (Standard, JSON, Table, Compact)
- Error handling and input validation
- Interactive command-line interface

## Prerequisites

- Node.js (v14 or higher)
- npm (Node Package Manager)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
npm install
```

## Running the Application

You can run the application in different modes:

1. Development mode (with auto-reload):
```bash
npm run dev
```

2. Production mode:
```bash
npm start
```

3. Build and run:
```bash
npm run build
node dist/task3.js
```

## Usage

The application provides an interactive menu with the following options:

1. Show all users
2. Filter users by name (supports regex)
3. Change display format
4. Exit

When filtering users by name, you can use regular expressions or literal text search:
- For regex search: Enter the pattern directly (e.g., `^A` for names starting with A)
- For literal search: Add `\` before the text (e.g., `\John` to search for "John") 