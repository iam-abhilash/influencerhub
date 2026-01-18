# MVP Execution Checklist: InfluencerHub

This document tracks the step-by-step execution plan to reach MVP Launch.

## 🏁 Phase 1: Foundation & Authentication
**Dependencies**: None
- [ ] **Database Connection**: Initialize `backend/app/core/database.py` (SQLAlchemy engine).
- [ ] **User Models**: Implement SQLAlchemy models in `backend/app/models/user.py`.
- [ ] **Dependency Injection**: Finish `backend/app/api/deps.py` (DB Session, Current User).
- [ ] **Auth Endpoints**: Verify Token validation works with Supabase.
- [ ] **Milestone Validation**: 
    - `curl localhost:8000/health` -> 200 OK.
    - Valid JWT allows access to protected routes.

## 🏗️ Phase 2: Core Logic (Users & Campaigns)
**Dependencies**: Phase 1
- [ ] **Profile API**: Build endpoints for Brand/Influencer onboarding (`POST /api/v1/users/onboard`).
- [ ] **Campaign Models**: Implement `models/campaign.py`.
- [ ] **Campaign CRUD**: Create/Read/Update campaigns APIs.
- [ ] **Milestone Validation**: 
    - Can register as a Brand.
    - Can create a "Summer Sale" campaign and see it in the DB.

## 💰 Phase 3: Financial Layer (Payments & Chain)
**Dependencies**: Phase 2
- [ ] **Razorpay Service**: Complete `services/payment/razorpay_service.py` (Order creation).
- [ ] **Webhook Security**: Implement signature verification in `api/v1/endpoints/payment.py`.
- [ ] **Blockchain Service**: Connect Web3.py to Polygon Mumbai (or local Mock).
- [ ] **Milestone Validation**: 
    - Make a test payment -> Database updates to `PAID`.
    - Background task triggers -> Database updates with `tx_hash`.

## 🧠 Phase 4: AI & Data
**Dependencies**: Phase 2
- [ ] **Ingestion Logic**: Implement CSV parser in `services/ingestion/`.
- [ ] **AI Categorizer**: Connect `services/ai/engine.py` to the Onboarding flow.
- [ ] **Milestone Validation**: 
    - Upload CSV of 10 influencers -> All receive correct Tags (Fitness, Tech, etc).

## 🖥️ Phase 5: Frontend Interface
**Dependencies**: Phases 1-4
- [ ] **Login Screen**: Streamlit form exchanging credentials for JWT.
- [ ] **Dashboard**: View "My Campaigns" table.
- [ ] **Discovery**: Search page using Backend API filters.
- [ ] **Milestone Validation**: Full user journey (Login -> Browse -> Create Campaign).

## 🛡️ Phase 6: Security & Production Readiness
**Dependencies**: Phase 5
- [ ] **RLS Audit**: Manually attempt to fetch another brand's data (Should fail).
- [ ] **Secrets Check**: Ensure no API keys are in git history.
- [ ] **Docker Compose**: Polish `docker-compose.yml` for reliable startup.
- [ ] **Go-Live Decision**: All P0 items in `docs/security/hardening_checklist.md` checked.
