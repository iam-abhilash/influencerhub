# Local Setup & Hosting Guide

## Option 1: Docker (Recommended)
This runs the entire stack (Frontend + Backend + Database) in isolated containers.

### Prerequisites
- Docker Desktop installed and running.

### Steps
1. **Setup Environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Supabase/Razorpay keys if you have them.
   # For local testing, the defaults work for the basics.
   ```

2. **Run Everything**:
   ```bash
   docker-compose up --build
   ```

3. **Access**:
   - **Frontend**: [http://localhost:8501](http://localhost:8501)
   - **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

## Option 2: Manual (Python)
If you don't use Docker, you can run services individually.

### Prerequisites
- Python 3.10+ installed.

### 1. Setup Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Setup Frontend (New Terminal)
```bash
cd frontend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

## Troubleshooting
- **Port Conflicts**: Ensure ports `8000` and `8501` are free.
- **Database Connection**: If the backend crashes, check your `SUPABASE_URL` in `.env`.
