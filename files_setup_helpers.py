from pathlib import Path

def write_file(dest, content, dry_run=False, force=False):
    if dry_run:
        if dest.exists():
            print(f"⚙️ [DRY RUN] Would overwrite: {dest}")
        else:
            print(f"⚙️ [DRY RUN] Would create: {dest}")
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not force:
        print(f"⏭️ Exists (skip): {dest}")
        return

    dest.write_text(content, encoding="utf-8")
    if dest.exists() and force:
        print(f"✏️ Overwrote: {dest}")
    else:
        print(f"📝 Wrote: {dest}")


FILES = {
    # Playwright config
    "playwright.config.ts": """import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  timeout: 5 * 12 * 1000,
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    testIdAttribute: 'data-e2e',
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
""",

    # TypeScript config
    "tsconfig.json": """{
  "compilerOptions": {
    "target": "ESNext",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
""",

    # Example E2E test
    "tests/e2e/example.spec.ts": """import { test, expect } from '@playwright/test';

test('homepage has Playwright in title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
""",

    # Example FrontEnd test
    "tests/front_end/feature_one/example_frontend.spec.ts": """import { test, expect } from '@playwright/test';

test('UI test - navigate and check heading', async ({ page }) => {
  await page.goto('https://playwright.dev');
  const heading = await page.locator('h1');
  await expect(heading).toHaveText(/Playwright/);
});
""",

    # Example BackEnd test
    "tests/back_end/feature_one/example_backend.spec.ts": """import { test, expect } from '@playwright/test';

test('API test - POST login', async ({ request }) => {
  const response = await request.post('https://reqres.in/api/login', {
    data: {
      email: 'eve.holt@reqres.in',
      password: 'cityslicka'
    }
  });

  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body.token).toBeTruthy();
});
""",

    # Example Page Object
    "tests/support/POMs/feature_one/example.page.ts": """import { Page } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  //////////  LOCATORS //////////

  getPageTitle = () => this.page.locator('h2', { hasText: "Test TEXT" });
  getForm = () => this.page.locator('form');

  //////////  ACTIONS //////////

  public async loginUser(email: string, password: string) {
    await this.page.locator('#email').fill(email);
    await this.page.locator('#password').fill(password);
    await this.page.locator('#login').click();
    await this.page.waitForLoadState('networkidle');
  }

  public async gotToForgotPasswordPage() {
    await this.page.locator('text=Forgot Password').click();
    await this.page.waitForLoadState('networkidle');
  }
}
""",

    # Example util
    "tests/support/utils/helpers.ts": """export function sum(a: number, b: number): number {
  return a + b;
}
""",

    # Test data
    "tests/support/utils/test-data.ts": """import * as dotenv from 'dotenv'
import { faker } from '@faker-js/faker'
dotenv.config()

interface TestData {
  auth: {
    homeowner: { email: string; password: string }
    contractor: { email: string; password: string }
    admin: { email: string; password: string }
  }
  organization: {
    name: string
    state: string
    balance: number
  }
  contact: {
    firstName: string
    lastName: string
    email: string
    phone: string
    role: string
    notes: string
  }
}

export const testData: TestData = {
  auth: {
    homeowner: {
      email: 'test.email@mail.com',
      password: '123',
    },
    contractor: {
      email: 'test.email@mail.com',
      password: '123',
    },
    admin: {
      email: 'test.email@mail.com',
      password: '123',
    },
  },
  organization: {
    name: faker.company.name(),
    state: faker.location.state(),
    balance: parseFloat(faker.finance.amount({ min: 1, max: 99999999999 })),
  },
  contact: {
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    email: faker.internet.email(),
    phone: faker.phone.number({ style: 'national' }),
    role: faker.person.jobTitle(),
    notes: faker.lorem.sentences(2),
  },
}
""",

    # Fixtures
    "tests/support/utils/fixtures.ts": """import { test as base, expect } from "@playwright/test";

type Fixtures = {
  authToken: string;
};

export const test = base.extend<Fixtures>({
  authToken: async ({}, use) => {
    await use(process.env.AUTH_TOKEN ?? "fake-token");
  },
});

export { expect };
""",

    # Gitignore
    ".gitignore": """node_modules/
test-results/
playwright-report/
.env
.DS_Store
""",

    # README
    "README.md": """# Playwright Test Automation Project

## QA Usage Guide

### Test ID Strategy
This project uses `data-e2e` attributes for reliable element selection:
```html
<button data-e2e="login-submit">Login</button>
<input data-e2e="email-field" type="email">
```

Configure in `playwright.config.ts`:
```typescript
use: {
  testIdAttribute: 'data-e2e',
  // ...
}
```

### Page Object Model (POM) Pattern
POMs separate locators from actions for maintainable tests:

**Locator Section:**
```typescript
//////////  LOCATORS //////////
getPageTitle = () => this.page.locator('h2', { hasText: "Test TEXT" });
getEmailField = () => this.page.getByTestId('email-field');
getSubmitButton = () => this.page.getByTestId('login-submit');
```

**Actions Section:**
```typescript
//////////  ACTIONS //////////
public async loginUser(email: string, password: string) {
  await this.getEmailField().fill(email);
  await this.page.getByTestId('password-field').fill(password);
  await this.getSubmitButton().click();
  await this.page.waitForLoadState('networkidle');
}
```

### Test Organization Best Practices

1. **Feature-based Structure:** Organize tests by application features
2. **Separation of Concerns:** Keep UI tests, API tests, and POMs separate
3. **Data Management:** Use `test-data.ts` for consistent test data across tests
4. **Fixtures:** Leverage fixtures for authentication tokens and shared setup

### Running Tests

```bash
# Install dependencies
npm install

# Run all tests
npx playwright test

# Run specific test suite
npx playwright test tests/front_end
npx playwright test tests/back_end

# Run tests in headed mode
npx playwright test --headed

# Run tests with specific browser
npx playwright test --project=chromium
```

### Test Data Usage
```typescript
import { testData } from '../support/utils/test-data';

// Use predefined data
await loginPage.loginUser(testData.auth.admin.email, testData.auth.admin.password);

// Use dynamic Faker data
const newContact = testData.contact; // Generates fresh data each run
```

### Authentication with Fixtures
```typescript
import { test, expect } from '../support/utils/fixtures';

test('authenticated test', async ({ page, authToken }) => {
  // authToken fixture automatically available
  await page.setExtraHTTPHeaders({
    'Authorization': `Bearer ${authToken}`
  });
});
```

Happy Testing! 🎭
"""
}

def create_files(project_root: Path, dry_run=False, force=False):
    for relative_path, content in FILES.items():
        dest = project_root / relative_path
        if dry_run:
            print(f"⚙️ [DRY RUN] Would create file: < {dest} >")
        else:
            if dest.exists() and not force:
                print(f"⚠️ Skipped (exists): {dest}")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            print(f"📄 Created: {dest}")
