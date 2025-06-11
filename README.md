# Python Asyncio Project

This is a Python implementation of an asynchronous application based on the requirements from "Tech test.pdf".

## Features

- Asynchronous operations using Python's asyncio library
- Efficient handling of concurrent tasks
- Error handling and robust implementation
- Command-line interface

## Prerequisites

- Python 3.10.11 or higher
- pip (Python Package Manager)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

You can run the application using:

```bash
python task3.py
```

## Testing

The project includes comprehensive test coverage using pytest. The tests verify various aspects of the application including:

- API integration and data fetching
- User filtering with regex patterns
- Display formatting options
- Error handling
- Main program flow

### Installing Test Dependencies

Install the required testing packages:
```bash
pip install pytest pytest-asyncio
```

### Running Tests

Run the tests using one of the following commands:

1. Run all tests:
```bash
pytest tests_task3.py -v
```

2. Run a specific test:
```bash
pytest tests_task3.py -v -k "test_name"
```

3. Run with detailed output:
```bash
pytest tests_task3.py -v -s
```

The test output will show:
- Test execution summary
- Individual test results
- Detailed error messages for failures
- Code coverage information (if configured)

## System Information

- Python Version: 3.10.11 [MSC v.1929 64 bit (AMD64)]
- Platform: Windows (win32)

## Notes

For detailed information about the implementation and requirements, please refer to "Tech test.pdf" in the project documentation.
