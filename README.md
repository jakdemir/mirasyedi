# Mirasyedi - Turkish Inheritance Calculator

A modern web application that helps calculate inheritance distribution according to Turkish Civil Law.

## Tech Stack

### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **State Management**: React Context API
- **Styling**: Tailwind CSS
- **Hosting**: Firebase Hosting
- **Domain Management**: Cloudflare
- **URL**: https://mirasyedi.com

### Backend
- **Framework**: FastAPI (Python)
- **API Documentation**: OpenAPI/Swagger
- **Hosting**: Google Cloud Run
- **URL**: https://mirasyedi-api-227035341689.us-central1.run.app

## Architecture

The application follows a modern client-server architecture:
- Frontend and backend are completely decoupled
- RESTful API communication
- CORS enabled for secure cross-origin requests
- Serverless deployment for both frontend and backend

## Key Features

- Real-time inheritance calculation
- Support for complex family tree structures
- Responsive design for all devices
- Type-safe implementation
- Automated deployment pipeline

## Development Environment Setup

### Prerequisites
- Node.js (v18 or higher)
- Python 3.11 or higher
- Google Cloud SDK
- Firebase CLI
- Git

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/mirasyedi.git
   cd mirasyedi
   ```

2. **Backend Setup**
   ```bash
   # Create and activate Python virtual environment
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the development server
   uvicorn app.api:app --reload --port 8000
   ```
   The backend API will be available at `http://localhost:8000`
   API documentation will be at `http://localhost:8000/docs`

3. **Frontend Setup**
   ```bash
   # In a new terminal
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

### Environment Configuration

1. **Frontend Environment Files**
   
   Create `.env.development` in the frontend directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

   Create `.env.production` for production:
   ```env
   VITE_API_URL=https://mirasyedi-api-227035341689.us-central1.run.app
   ```

2. **Backend Environment**
   No environment variables are required for local development.

## Local Development Workflow

1. **Running Tests**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

2. **Code Formatting**
   ```bash
   # Backend
   cd backend
   black .
   
   # Frontend
   cd frontend
   npm run format
   ```

3. **Type Checking**
   ```bash
   # Frontend
   cd frontend
   npm run type-check
   ```

## Deployment Process

### Backend Deployment (Google Cloud Run)

1. **Initial Setup**
   ```bash
   # Install Google Cloud SDK
   brew install google-cloud-sdk  # On macOS
   
   # Login and set project
   gcloud auth login
   gcloud config set project mirasyedi-backend
   
   # Enable required services
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
   ```

2. **Deploy Changes**
   ```bash
   cd backend
   
   # Build and push container
   gcloud builds submit --tag us-central1-docker.pkg.dev/mirasyedi-backend/mirasyedi-repo/api
   
   # Deploy to Cloud Run
   gcloud run deploy mirasyedi-api \
     --image us-central1-docker.pkg.dev/mirasyedi-backend/mirasyedi-repo/api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Frontend Deployment (Firebase)

1. **Initial Setup**
   ```bash
   # Install Firebase CLI
   npm install -g firebase-tools
   
   # Login to Firebase
   firebase login
   
   # Initialize Firebase in the project
   cd frontend
   firebase init hosting
   ```

2. **Deploy Changes**
   ```bash
   cd frontend
   
   # Build the application
   npm run build
   
   # Deploy to Firebase
   firebase deploy
   ```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify backend CORS settings in `backend/app/api.py`
   - Check that frontend API URL matches allowed origins
   - Clear browser cache and reload

2. **Deployment Failures**
   - Ensure you have necessary permissions in Google Cloud and Firebase
   - Verify billing is enabled for Google Cloud services
   - Check if all required APIs are enabled

3. **Local Development Issues**
   - Verify both frontend and backend are running
   - Check console for error messages
   - Ensure correct Node.js and Python versions
   - Clear node_modules and reinstall if needed

### Getting Help

1. **Logs**
   - Backend logs: Available in Google Cloud Console
   - Frontend logs: Check Firebase Hosting logs
   - Local logs: Terminal output and browser console

2. **Support**
   - Create an issue in the repository
   - Check existing issues for similar problems
   - Include relevant logs and error messages

## Environment Variables

### Frontend
- `VITE_API_URL`: Backend API URL

### Backend
- No environment variables required currently

## Security

- CORS configuration for allowed origins
- Input validation on both frontend and backend
- Secure HTTPS communication
- No sensitive data storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

Feel free to submit issues and enhancement requests.
