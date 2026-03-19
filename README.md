# Ecommerce Website

This project has two apps:

- `backend` (FastAPI + Uvicorn)
- `frontend` (React + Vite)

## Prerequisites

- Python 3.10+ (recommended: 3.12)
- Node.js 18+
- npm

## Run Backend

1. Open a terminal and go to backend:

```bash
cd backend
```

2. Create virtual environment (first time only):

```bash
python3 -m venv .venv
```

3. Activate virtual environment:

```bash
source .venv/bin/activate
```

4. Install Python dependencies:

```bash
pip install -r requirements.txt
```

5. Start backend with Uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at:

- `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

## Run Frontend

1. Open a second terminal and go to frontend:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start Vite dev server:

```bash
npm run dev
```

Frontend runs at:

- `http://localhost:5173`

## Run Both (Quick Sequence)

Terminal 1:

```bash
cd backend
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev
```
