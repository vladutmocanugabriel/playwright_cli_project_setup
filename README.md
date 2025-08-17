# Playwright Project Setup CLI Tool

A Python CLI tool that quickly scaffolds a complete Playwright test automation project with TypeScript, organized structure, and QA best practices.

## Features

- 🚀 **Quick Setup**: Creates a full Playwright project in seconds
- 📁 **Organized Structure**: Separates E2E, frontend, backend tests with POM pattern
- 🎭 **Multi-browser**: Pre-configured for Chromium, Firefox, and WebKit
- 📊 **Test Data**: Faker.js integration for dynamic test data
- 🔧 **TypeScript**: Full TypeScript support with proper configuration
- 🏗️ **Best Practices**: Includes fixtures, utilities, and Page Object Models

## Prerequisites

- Python 3.7+
- Node.js 18+
- npm

## Installation & Usage

### Option 1: Clone and Run Locally

```bash
# Clone the repository
git clone <your-repo-url>
cd qa_automation_project_setup

# Create a new Playwright project
python main.py my-test-project

# With options
python main.py my-test-project --force --dry-run
```

### Option 2: Download and Run

```bash
# Download the files
curl -O https://raw.githubusercontent.com/your-username/qa_automation_project_setup/main/main.py
curl -O https://raw.githubusercontent.com/your-username/qa_automation_project_setup/main/project_setup_helpers.py
curl -O https://raw.githubusercontent.com/your-username/qa_automation_project_setup/main/files_setup_helpers.py

# Run the tool
python main.py my-test-project
```

## Command Options

```bash
python main.py <project-name> [options]

Options:
  --force      Overwrite existing files
  --dry-run    Preview what would be created without making changes
  --clean      Remove all generated files from a project
```

## Examples

```bash
# Create a new project
python main.py awesome-qa-project

# Preview what will be created
python main.py test-project --dry-run

# Overwrite existing files
python main.py existing-project --force

# Clean up a project
python main.py old-project --clean
```

## Generated Project Structure

```
my-test-project/
├── playwright.config.ts          # Playwright configuration
├── tsconfig.json                  # TypeScript configuration
├── package.json                   # Node.js dependencies
├── .gitignore                     # Git ignore patterns
├── README.md                      # Project documentation
└── tests/
    ├── e2e/                       # End-to-end tests
    ├── front_end/feature_one/     # Frontend UI tests
    ├── back_end/feature_one/      # Backend API tests
    └── support/
        ├── POMs/feature_one/      # Page Object Models
        └── utils/                 # Test utilities
            ├── helpers.ts         # Common functions
            ├── test-data.ts       # Test data with Faker.js
            └── fixtures.ts        # Playwright fixtures
```

## What Gets Installed

The tool automatically installs these npm packages:
- `playwright` - Browser automation framework
- `@playwright/test` - Test runner and assertions
- `typescript` - TypeScript support
- `ts-node` - TypeScript execution
- `@faker-js/faker` - Dynamic test data generation
- `dotenv` - Environment variable support

## Getting Started with Your New Project

After running the tool:

```bash
cd my-test-project

# Run all tests
npx playwright test

# Run specific test suites
npx playwright test tests/front_end
npx playwright test tests/back_end

# Run in headed mode (see browser)
npx playwright test --headed

# Generate test report
npx playwright show-report
```

## Key Features of Generated Projects

### 🎯 Test ID Strategy
- Uses `data-e2e` attributes for reliable element selection
- Pre-configured in Playwright config

### 🏗️ Page Object Model Pattern
- Clear separation of locators and actions
- Organized by features for scalability

### 📊 Dynamic Test Data
- Faker.js integration for realistic test data
- Predefined user roles and data structures

### 🔐 Authentication Support
- Fixtures for handling auth tokens
- Environment variable support

### 🌐 Multi-browser Testing
- Parallel execution across browsers
- CI/CD ready configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different project setups
5. Submit a pull request

## License

MIT License - feel free to use and modify for your projects!

---

Built with ❤️ for QA Engineers who want to get testing faster 🚀