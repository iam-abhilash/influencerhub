-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ENUMS for Type Safety
CREATE TYPE user_role AS ENUM ('admin', 'brand', 'influencer');
CREATE TYPE campaign_status AS ENUM ('draft', 'active', 'completed', 'cancelled');
CREATE TYPE transaction_status AS ENUM ('pending', 'paid', 'failed', 'verified_on_chain');

-- 2. USERS (Base Identity - Links to Supabase Auth)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    role user_role NOT NULL DEFAULT 'influencer',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. BRANDS (Profile Data)
CREATE TABLE public.brands (
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT,
    website TEXT,
    verified BOOLEAN DEFAULT FALSE
);

-- 4. INFLUENCERS (Profile Data)
CREATE TABLE public.influencers (
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE PRIMARY KEY,
    username TEXT NOT NULL,
    bio TEXT,
    niche TEXT[],  -- Array of tags for AI matching
    metrics JSONB DEFAULT '{}', -- Flexible metrics (follower count, engagement rate)
    wallet_address TEXT -- For Blockchain verification
);

-- 5. CAMPAIGNS (Owned by Brands)
CREATE TABLE public.campaigns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    brand_id UUID REFERENCES public.brands(user_id) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    budget DECIMAL(10, 2) NOT NULL,
    status campaign_status DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. TRANSACTIONS (Financial & Blockchain Record)
CREATE TABLE public.transactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    campaign_id UUID REFERENCES public.campaigns(id),
    influencer_id UUID REFERENCES public.influencers(user_id),
    amount DECIMAL(10, 2) NOT NULL,
    razorpay_payment_id TEXT, -- Payment Gateway Reference
    blockchain_tx_hash TEXT UNIQUE, -- Immutable Blockchain Record
    status transaction_status DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- ROW LEVEL SECURITY (RLS)
-- ==========================================

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.influencers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;

-- POLICY: Users can only read/edit their own base user data
CREATE POLICY "Users view own data" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- POLICY: Brands can only update their own profile
CREATE POLICY "Brands update own profile" ON public.brands
    FOR UPDATE USING (auth.uid() = user_id);
-- (Public read access might be needed for discovery, but strictest is owner-only)
CREATE POLICY "Brands view own profile" ON public.brands
    FOR SELECT USING (auth.uid() = user_id);

-- POLICY: Influencers can only update their own profile
CREATE POLICY "Influencers update own profile" ON public.influencers
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Influencers view own profile" ON public.influencers
    FOR SELECT USING (auth.uid() = user_id);

-- POLICY: Brands see only their own campaigns
CREATE POLICY "Brands view own campaigns" ON public.campaigns
    FOR ALL USING (auth.uid() = brand_id);

-- POLICY: Transactions visible to involved parties only
CREATE POLICY "View transactions involved in" ON public.transactions
    FOR SELECT USING (
        auth.uid() = influencer_id OR 
        auth.uid() IN (SELECT brand_id FROM public.campaigns WHERE id = campaign_id)
    );

-- ==========================================
-- INDEXING STRATEGY
-- ==========================================
-- Accelerate joins on foreign keys
CREATE INDEX idx_campaigns_brand ON public.campaigns(brand_id);
CREATE INDEX idx_transactions_campaign ON public.transactions(campaign_id);
CREATE INDEX idx_transactions_influencer ON public.transactions(influencer_id);

-- Search optimization for Influencer discovery
CREATE INDEX idx_influencers_niche ON public.influencers USING GIN(niche);
CREATE INDEX idx_influencers_metrics ON public.influencers USING GIN(metrics);
