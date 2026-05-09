# Daily Current Affairs Tracker

A full-stack application to track daily current affairs status.

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Vue.js 3 (Vite, Axios, Lucide-Vue-Next, Date-fns)
- **Database:** SQLite

## How to Run

### Backend
1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python -m app.main
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at the URL provided by Vite (usually `http://localhost:5173`).

## Project Structure
- `backend/`: FastAPI application and SQLite database.
- `frontend/`: Vue.js application.
