# Security Hardening Checklist

## 🚨 High-Risk & Critical Areas
These must be addressed **before** the very first deployment, even for MVP.

### 1. API Security
- [ ] **JWT Validation (MVP)**: Ensure `backend/app/core/security.py` validates `aud` (audience) and `exp` (expiry) of every token.
- [ ] **CORS Policy (MVP)**: Change `allow_origins=["*"]` in `main.py` to the specific frontend domain (e.g., `https://influencerhub.app`).
- [ ] **Rate Limiting (Prod)**: Implement `slowapi` or Nginx rate limiting to prevent DDoS/Brute Force (e.g., 60 req/min per IP).
- [ ] **Input Sanitization (MVP)**: Pydantic handles JSON validation, but ensure no user input is passed directly to `subprocess` or `eval()`.

### 2. Database Security
- [ ] **RLS Policies (MVP)**: Verify every table in Supabase has RLS enabled. Run `SELECT * FROM table` as an anon user to test.
- [ ] **No Public Access (MVP)**: Ensure database port `5432` is NOT exposed to the public internet (use Supabase connection pooling or VPC).
- [ ] **Backup Strategy (Prod)**: Enable Point-in-Time Recovery (PITR) in Supabase.
- [ ] **Least Privilege (Prod)**: The Backend Application User should NOT be `postgres` (superuser). Create a dedicated `app_user` with only `CRUD` permissions.

### 3. Payment Security (Razorpay)
- [ ] **Webhook Signature Verification (MVP)**: CRITICAL. This is the only defense against fake payment injections.
- [ ] **Idempotency (MVP)**: specificy `payment_id` as Unique Index to prevent double-crediting if webhook fires twice.
- [ ] **HTTPS Only (MVP)**: Never allow payment processing over HTTP.

### 4. Blockchain Safety
- [ ] **Private Key Isolation (MVP)**: `WALLET_PRIVATE_KEY` must strictly be loaded from `.env` and **NEVER** logged/printed to console.
- [ ] **Chain ID Check (MVP)**: Ensure the Web3 provider connects to the correct network (Testnet vs Mainnet) before sending txs.
- [ ] **Gas Limits (Prod)**: Hardcode gas limits to prevent draining the treasury wallet if a contract bugs out.

### 5. Secrets Management
- [ ] **.gitignore (MVP)**: Confirm `.env`, `*.pem`, `secrets.json` are ignored.
- [ ] **Cloud Secret Manager (Prod)**: Move from `.env` files to AWS Secrets Manager / Azure Key Vault / GitHub Secrets for production.
- [ ] **Rotation Policy (Prod)**: Plan to rotate `JWT_SECRET` and Database passwords every 90 days.

### 6. Logging & Audit Trails
- [ ] **PII Redaction (MVP)**: Ensure `logging` configuration does NOT output emails, passwords, or full JWTs to system logs.
- [ ] **Audit Table (Prod)**: Create an `audit_logs` table tracking sensitive actions:
    - *Who* (User ID)
    - *What* (Updated Campaign Status)
    - *When* (Timestamp)
    - *IP Address*

## Summary of Priorities

| Priority | Task | Why? |
| :--- | :--- | :--- |
| 🔴 **P0** | **Webhook Signatures** | Money loss risk if hacked. |
| 🔴 **P0** | **RLS Policies** | Data leak risk (Brand A seeing Brand B). |
| 🟡 **P1** | **CORS Restriction** | Prevents malicious sites from using your API. |
| 🟢 **P2** | **Rate Limiting** | Service stability (Nice to have for MVP). |
