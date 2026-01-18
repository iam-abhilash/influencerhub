# API Design & Standards

## Overview
RESTful API design following OpenAPI 3.0 standards. All endpoints are prefixed with `/api/v1`.

## Standards

### HTTP Status Codes
| Code | Meaning | When to use |
| :--- | :--- | :--- |
| `200` | OK | Successful GET, PUT, or non-creation POST |
| `201` | Created | Successful entity creation (POST) |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Validation failure (Pydantic error) |
| `401` | Unauthorized | Valid authentication credentials missing |
| `403` | Forbidden | Authenticated but not allowed (RBAC) |
| `404` | Not Found | Resource does not exist |
| `422` | Validation Error | JSON body format correct, but content invalid |
| `500` | Server Error | Unhandled exception (bug) |

### Error Response Format
All errors return a standard JSON structure:
```json
{
  "detail": "Error message description"
}
```

## API Endpoints

### 1. Authentication (`/auth`)
Handled primarily by Supabase Client on Frontend. Backend provides:
- `POST /auth/login` (Optional proxy)
- `POST /auth/refresh` (Optional proxy)

### 2. Onboarding (`/users`)

#### Brand Onboarding
- **Endpoint**: `POST /users/brand/onboard`
- **Auth**: `Bearer <token>`
- **Payload**:
```json
{
  "company_name": "Tech Corp",
  "industry": "SaaS",
  "website": "https://tech.corp"
}
```
- **Response**: `200 OK` (User profile updated)

#### Influencer Onboarding
- **Endpoint**: `POST /users/influencer/onboard`
- **Auth**: `Bearer <token>`
- **Payload**:
```json
{
  "username": "crypto_king",
  "bio": "Blockchain enthusiast",
  "niche": ["crypto", "finance"],
  "wallet_address": "0x123..."
}
```

### 3. Campaign Lifecycle (`/campaigns`)

#### Create Campaign
- **Endpoint**: `POST /campaigns/`
- **Auth**: `Bearer <token>` (Role: Brand)
- **Payload**:
```json
{
  "title": "Summer Launch",
  "budget": 5000.00,
  "description": "Launch event promotion"
}
```
- **Response**: `201 Created` -> Returns `CampaignResponse` object

#### List My Campaigns
- **Endpoint**: `GET /campaigns/`
- **Auth**: `Bearer <token>`
- **Response**: `200 OK` -> `List[CampaignResponse]`

#### Update Status
- **Endpoint**: `PATCH /campaigns/{id}`
- **Auth**: `Bearer <token>` (Role: Owner)
- **Payload**: `{"status": "active"}`

### 4. Insights (`/insights`)

#### Get Matches (AI)
- **Endpoint**: `POST /insights/match/`
- **Auth**: `Bearer <token>` (Role: Brand)
- **Payload**:
```json
{
  "campaign_desc": "Looking for crypto influencers for new wallet launch",
  "tags": ["web3"]
}
```
- **Response**: List of `InfluencerResponse` sorted by match score.

#### Get Public Profile
- **Endpoint**: `GET /users/profile/{username}`
- **Auth**: Public or Auth
- **Response**: Limited view of Influencer profile.
