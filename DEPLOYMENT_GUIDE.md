# InfluencerHub Deployment Guide

This guide explains how to deploy the InfluencerHub application (Streamlit Frontend + FastAPI Backend) to the web.

## Architecture
The application consists of two parts:
1. **Backend**: FastAPI (Python) - Handles data, authentication, and logic.
2. **Frontend**: Streamlit (Python) - The user interface.

These must be deployed separately but connected via configuration.

## Prerequisites
1. **GitHub Repository**: Ensure this code is pushed to a GitHub repository.
2. **Supabase Account**: Ensure you have your Supabase project set up and credentials ready.

## Part 1: Deploying the Backend (Web Service)
We recommend using **Render** or **Railway** for free/easy hosting of Python backends.

### Using Render.com
1. Create a new **Web Service**.
2. Connect your GitHub repository.
3. Settings:
   - **Root Directory**: `influencerhub/backend` (or just `backend` if inside the repo root)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   Add the variables from your `.env` file (e.g., `SUPABASE_URL`, `SUPABASE_KEY`, `JWT_SECRET`, etc.).
5. Deploy.
6. **Copy the URL**: Once deployed, you will get a URL (e.g., `https://influencerhub-backend.onrender.com`).

## Part 2: Deploying the Frontend (Streamlit)
We recommend **Streamlit Community Cloud**.

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in with GitHub.
3. Click **New App** and select your repository.
4. Settings:
   - **Main file path**: `influencerhub/frontend/main.py`
5. **Advanced Settings (Secrets)**:
   - Go to the "Secrets" section (TOML format) or Environment Variables.
   - Add the specific variable `API_URL` pointing to your Backend URL from Part 1.
   ```toml
   API_URL = "https://your-backend-url.onrender.com"
   ```
   (Alternatively, use Environment Variables section if available).
6. Click **Deploy**.

## Part 3: Connecting Them
- Ensure the **Frontend** has the `API_URL` environment variable set to the **Backend**'s public URL.
- Ensure the **Backend** allows CORS from the Frontend domain (configured in `main.py`).

## Troubleshooting
- **Build Failures**: If backend fails to build due to `web3` or other heavy libraries, you may need to add a `packages.txt` requires setup or switch to Docker deployment on Render.
- **CORS Errors**: If the frontend says "Network Error" when calling backend, check the browser console. You might need to add the Streamlit URL to the Backend's `allow_origins`.
