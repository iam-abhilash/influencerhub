# Testing Strategy & CI/CD

## 1. Test Pyramid
We follow the standard pyramid:
- **Unit Tests (60%)**: Fast, isolated tests for Services (AI, Payment logic).
- **Integration Tests (30%)**: API Endpoint -> DB interactions.
- **E2E/UI Tests (10%)**: Playwright flows representing user journeys.

## 2. Testing Stack
| Layer | Tool | Scope |
| :--- | :--- | :--- |
| **Backend** | `pytest` | Unit, Integration, Security |
| **Async** | `pytest-asyncio` | FastAPI async route testing |
| **Frontend** | `Playwright` | Browser automation (Headless Chrome) |
| **Blockchain** | `eth-tester` / `brownie` | Mocking Ethereum nodes (Future) |

## 3. Folder Structure
```plaintext
backend/tests/
├── unit/             # Logic only (No DB)
│   └── test_ai_engine.py
├── integration/      # API + DB
│   └── test_campaign_api.py
├── security/         # RBAC & Auth exploits
│   └── test_rbac.py
└── conftest.py       # Global Fixtures (DB sessions, Client)

frontend/tests/
└── test_ui.py        # Playwright specs
```

## 4. CI/CD Pipeline (GitHub Actions)

### Step 1: Backend Quality
- **Command**: `pytest backend/tests`
- **Gate**: Must pass 100%. Blocks PR merge.

### Step 2: Security Scan
- **Tool**: `bandit` (Python SAST)
- **Command**: `bandit -r backend/`
- **Check**: Looks for hardcoded secrets, unsafe queries.

### Step 3: Frontend Smoke Test
- **Tool**: Playwright
- **Command**: `pytest frontend/tests`
- **Note**: Run on `ubuntu-latest` with headless browser.

## 5. Security & Blockchain Specifics
- **Blockchain**: We do *not* connect to real Mumbai testnet in CI. We use `Web3.py`'s `MockProvider` or `eth-tester` to simulate transaction hashes.
- **Auth**: We simulate JWTs using `python-jose` in tests to act as "fake" logged-in users. We never use real user credentials in CI.
