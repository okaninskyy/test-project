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
- Java Runtime Environment (JRE) for Allure reports

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

The project includes comprehensive test coverage using pytest and Allure for beautiful test reports.

### Installing Allure

1. Install Allure command-line tool:
   - For Windows (manual instalation):
     ```download Allure from https://github.com/allure-framework/allure2/releases
        add allure binary to system path
     ```
   - For macOS:
     ```bash
     brew install allure
     ```
   - For Linux:
     ```bash
     sudo apt-add-repository ppa:qameta/allure
     sudo apt-get update
     sudo apt-get install allure
     ```

2. Install Python dependencies for testing:
```bash
pip install pytest pytest-asyncio allure-pytest
```

### Running Tests

1. Run tests with Allure report generation:
```bash
pytest tests_task3.py -v --alluredir=./allure-results
```

2. Generate and open the Allure report:
```bash
allure serve ./allure-results
```

The Allure report will open in your default web browser, showing:
- Test execution summary
- Test case descriptions and steps
- Test execution timeline
- Severity distribution
- Attachments and failure details

## System Information

- Python Version: 3.10.11 [MSC v.1929 64 bit (AMD64)]
- Platform: Windows (win32)

## Notes

For detailed information about the implementation and requirements, please refer to "Tech test.pdf" in the project documentation.
