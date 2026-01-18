# Database Design & Security Strategy

## Overview
The InfluencerHub database is designed to be **secure-by-default** using PostgreSQL's Row Level Security (RLS) features, optimized for Supabase.

## Entities

### 1. Identity (`users`)
- **Design**: Links 1:1 with Supabase `auth.users`.
- **Purpose**: Stores global data like `email` and strictly typed `role` (Brand vs Influencer).
- **Security**: Updating role is restricted to Admin or initial setup to prevent privilege escalation.

### 2. Profiles (`brands`, `influencers`)
- **Design**: "Table-per-type" inheritance strategy.
- **Why**: Brands and Influencers have drastically different data needs (e.g., wallet address vs website).
- **Benefit**: Cleaner tables, no null-sparse columns.

### 3. Core Logic (`campaigns`)
- **Design**: Owned strictly by Brands.
- **Relationship**: 1 Brand -> Many Campaigns.
- **Access Control**: RLS policies ensure a brand user can never query another brand's campaign data (Multi-tenant isolation).

### 4. Financials (`transactions`)
- **Dual-Link**: Links to both a `campaign` and an `influencer`.
- **Hybrid Storage**:
  - `razorpay_payment_id`: Web2 audit trail.
  - `blockchain_tx_hash`: Web3 immutable proof.
- **Security**: RLS allows *both* parties (Brand and Influencer) to read the transaction record, but neither can edit the `blockchain_tx_hash` after writing (enforced by application logic and potentially trigger functions).

## Row Level Security (RLS) deep dive

We utilize `auth.uid()` which Supabase injects into the Postgres session from the User's JWT.

```sql
-- Example: Isolating Campaign Data
CREATE POLICY "Brands view own campaigns" ON public.campaigns
    FOR ALL USING (auth.uid() = brand_id);
```
**Implication**: Even if the API code has a bug and requests `SELECT * FROM campaigns`, the **Database** will only return rows belonging to that user. This is a critical defense-in-depth layer.

## Indexing Strategy for AI & Scale

1.  **GIN Indexes** on `influencers.niche` (Array) and `influencers.metrics` (JSONB).
    -   **Why**: Allows the AI/Search service to perform high-speed "Containment" queries (e.g., "Find influencers in 'Tech' niche with >10k followers").
2.  **Foreign Key Indexes**:
    -   `brand_id`, `campaign_id`, `influencer_id`.
    -   **Why**: Postgres does not auto-index FKs. Essential for performant `JOIN` operations when fetching user dashboards.
