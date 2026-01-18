# Payment & Settlement Flow

## 1. Flow Overview
We use a **Two-Phase Commit** strategy where the Blockchain recording happens *only* after a successful Fiat payment is confirmed via Webhook.

```mermaid
sequenceDiagram
    participant B as Brand (Frontend)
    participant API as Backend
    participant RP as Razorpay
    participant BC as Blockchain Service
    
    Note over B, API: Phase 1: Initiation
    B->>API: 1. "Fund Campaign"
    API->>RP: 2. Create Order (amount, notes={campaign_id})
    RP-->>B: 3. Return order_id
    
    B->>RP: 4. User Enters Credit Card info
    RP-->>B: 5. Payment Success

    Note over RP, API: Phase 2: Verification (Webhook)
    RP->>API: 6. POST /api/v1/payment/webhook (Event: payment.captured)
    
    API->>API: 7. Verify Signature (HMAC)
    API->>API: 8. Update DB: Transaction Status = 'Paid'
    
    Note over API, BC: Phase 3: Blockchain Record
    API->>BC: 9. Create Immutable Record (CampaignUUID + Amount)
    BC-->>API: 10. Return TX Hash
    API->>DB: 11. Update DB: blockchain_hash = '0x...'
```

## 2. Webhook Handling Logic
**Endpoint**: `/api/v1/payment/webhook`

1.  **Read Headers**: Extract `X-Razorpay-Signature`.
2.  **Verify**: Compute `HMAC_SHA256(payload, secret)`. If dispatch != signature, **ABORT** (400 Bad Request). This prevents attackers from faking payments.
3.  **Idempotency**: Check if `payment_id` already exists in `transactions` table. If yes, return 200 OK (ignore duplicate).
4.  **Process**:
    -   Parse `payload.payment.entity.notes.campaign_id`.
    -   Update Campaign status to `ACTIVE`.
    -   Trigger Background Task: `blockchain_service.create_record(...)`.

## 3. Failure Scenarios

| Scenario | Handling |
| :--- | :--- |
| **User closes window after paying** | No impact. The **Webhook** is server-to-server and reliable. |
| **Blockchain Transaction Fails** | Payment is effectively "captured" in Fiat but missing on-chain. <br> **Mitigation**: A nightly Cron Job scans for 'Paid' transactions with `blockchain_hash=NULL` and retries the blockchain write. |
| **Webhook delayed** | The UI polls the status every 5s. Eventually, the status flips to 'Paid'. |

## 4. Security Criticals
- **Never trust the Frontend success callback** for fulfilling the order. An attacker can manipulate client-side JS to call `onSuccess()`.
- **Always use Webhooks** as the source of truth for money.
