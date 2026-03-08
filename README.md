# Yellow Smartphone Financing Project

This is a full-stack loan application system built for **Yellow**. It allows users to apply for smartphone financing with real-time risk-based pricing and South African ID validation.

## 🚀 Tech Stack

* **Frontend**: Vue.js 3 with **Quasar Framework** (Vite based).
* **Backend**: **FastAPI** (Python 3.11+).
* **Database**: **PostgreSQL**.
* **DevOps**: Docker & Docker Compose.

## 🛠️ System Architecture

The application is fully containerized. The frontend communicates with the FastAPI backend via an asynchronous REST API, which persists data to a PostgreSQL volume.

## 📦 How to Run with Docker

### 1. Prerequisites

* Install **Docker Desktop** and **Docker Compose**.
* Ensure ports `8000` and `9000` are free on your machine.

### 2. Configuration

Create a `.env` file in the root directory (refer to the `.gitignore` to ensure this stays local) with the following variables:

```env
DB_USER=yellow_admin
DB_PASSWORD=yellow_secure_pass
DB_NAME=yellow_db
DB_HOST=db
DB_PORT=5432

```
* Note: Normally l would never share these credentials, but since this is a demo project, I have included them here for ease of testing. 

### 3. Launch the System

Navigate to the project root and run:

```bash
docker-compose up --build
docker exec -it yellow_backend python seed.py (once the database is running sucessfully)
```

* **Frontend**: Accessible at `http://localhost:9000` (or `http://YOUR_IP:9000` for mobile testing).
- Make sure that you adjust the CORS settings in the backend if you are accessing from a different IP
* **Backend API**: Accessible at `http://localhost:8000`.
* **API Docs**: View the interactive Swagger UI at `http://localhost:8000/docs`.

## 📁 Project Structure

* `/frontend`: Quasar/Vue source code and Dockerfile.
* `/backend`: FastAPI logic, SQLAlchemy models, and loan service utilities.
* `/backend/uploads`: Local storage for "Supporting Proof" documents (ignored by Git).

---

