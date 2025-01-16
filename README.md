# Mirasyedi - Turkish Inheritance Calculator

A web application for calculating inheritance distribution according to Turkish Civil Law.

## Project Structure

```
mirasyedi/
├── frontend/          # React + TypeScript frontend
└── backend/           # FastAPI Python backend
```

## Development Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn app.api:app --reload --port 8000
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Local Testing

1. Start both backend and frontend servers as described above.

2. The frontend will automatically connect to the local backend at `http://localhost:8000`.

3. Access the API documentation at `http://localhost:8000/docs` for testing backend endpoints directly.

## Deployment

### Backend Deployment (Google Cloud Run)

1. Install Google Cloud SDK:
   ```bash
   brew install google-cloud-sdk  # On macOS
   ```

2. Initialize and authenticate:
   ```bash
   gcloud auth login
   gcloud config set project mirasyedi-backend
   ```

3. Enable required services:
   ```bash
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
   ```

4. Build and deploy:
   ```bash
   cd backend
   gcloud builds submit --tag us-central1-docker.pkg.dev/mirasyedi-backend/mirasyedi-repo/api
   gcloud run deploy mirasyedi-api --image us-central1-docker.pkg.dev/mirasyedi-backend/mirasyedi-repo/api --platform managed --region us-central1 --allow-unauthenticated
   ```

### Frontend Deployment (Firebase)

1. Install Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```

2. Login to Firebase:
   ```bash
   firebase login
   ```

3. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

4. Deploy to Firebase:
   ```bash
   firebase deploy --only hosting
   ```

## Environment Configuration

### Frontend Environment Files

- Development (`.env.development`):
  ```
  VITE_API_URL=http://localhost:8000
  ```

- Production (`.env.production`):
  ```
  VITE_API_URL=https://mirasyedi-api-227035341689.us-central1.run.app
  ```

## Deployed URLs

- Frontend: https://mirasyedi-ec74e.web.app
- Backend: https://mirasyedi-api-227035341689.us-central1.run.app

## Troubleshooting

### CORS Issues
If you encounter CORS errors, verify that the backend's CORS configuration includes your frontend's domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://mirasyedi-ec74e.web.app",
        "https://mirasyedi-ec74e.firebaseapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Deployment Issues
- Ensure you have the correct permissions in Google Cloud and Firebase
- Verify that billing is enabled for Google Cloud services
- Check that all required APIs are enabled in Google Cloud Console
