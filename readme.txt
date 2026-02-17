MLOps Assignment 2 - End-to-End Pipeline
==========================================

This project implements an end-to-end MLOps pipeline for binary image classification (Cats vs. Dogs), including data versioning, model training, containerization, and CI/CD.

## Completed Modules
✅ **M1: Model Development** (DVC Pipeline, MLflow Tracking)
✅ **M2: Model Packaging** (FastAPI, Docker)
✅ **M3: CI Pipeline** (GitHub Actions, Tests, Artifact Publishing)
✅ **M4: CD Pipeline** (Docker Compose, Automated Deployment)
✅ **M5: Monitoring** (Logging, Health Checks, Smoke Tests)

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.10+
- Docker & Docker Compose

### 1. Setup Environment
```bash
# Create virtual env
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data (DVC)
This project is configured to use a **local shared remote** at `../dvc-storage`.

**Option A: Build from Scratch (Recommended)**
If you don't have the shared storage folder, simply run:
```bash
dvc repro
```
This triggers the full pipeline:
1. **Download**: Fetches data from Kaggle
2. **Preprocess**: Resizes images & splits data
3. **Train**: Trains CNN & saves to `artifacts/models/baseline_cnn.pt`

**Option B: Pull from Storage**
If you have the `dvc-storage` folder placed in the parent directory:
```bash
dvc pull
```

### 3. Run Inference Service (Docker)
Start the API service:
```bash
docker-compose up --build
```
The API will be available at: http://localhost:8000

---

## 🧪 Testing & Verification

### Unit Tests
Run the automated test suite (preprocessing & API logic):
```bash
pytest tests/
```

### Smoke Tests (Post-Deployment)
Once the Docker container is running, execute the verification script:
```bash
python tests/smoke_test.py
```
*This script checks API health and attempts to predict on `images/Cat.jpg` and `images/Dog.jpg` if present.*

### Manual API Test
1. Open Browser: http://localhost:8000/docs
2. Upload an image to `/predict`
3. Or use curl:
```bash
curl -X POST "http://localhost:8000/predict" -F "file=@path/to/cat.jpg"
```

---

## 🛠 Features & Architecture

### 1. Data & DVC
- **Tracking**: `dvc.yaml` defines the DAG (Directed Acyclic Graph).
- **Remote**: Configured to `../dvc-storage` (simulates a shared network drive).
- **Data Location**: `data/dog-and-cat-classification-dataset` (Git ignored).

### 2. Model & Training
- **Framework**: PyTorch
- **Tracking**: MLflow (logs metrics to `mlruns/`)
- **Artifacts**: Model saved to `artifacts/models/baseline_cnn.pt`

### 3. API Service (`src/api.py`)
- **Endpoints**: `/health`, `/predict`
- **Monitoring**: Structured logging enabled.

### 4. CI/CD Pipeline (`.github/workflows/ci.yml`)
Automated via GitHub Actions:
1. **Linting**: `flake8` checks for code quality.
2. **Testing**: `pytest` runs unit tests.
3. **Reproducibility**: Runs `dvc repro`.
4. **Build & Publish**: Builds Docker image and pushes to a local registry.
