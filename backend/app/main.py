from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import logging
import time
from datetime import datetime
import json
from fastapi.responses import JSONResponse
from starlette.responses import Response
import copy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request
    start_time = time.time()
    request_id = str(int(time.time() * 1000))
    
    # Log request details
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    logger.info(f"Request {request_id} Headers: {dict(request.headers)}")
    
    # Log request body
    try:
        body = await request.body()
        if body:
            body_str = body.decode()
            logger.info(f"Request {request_id} Body: {body_str}")
            # Reset request body for downstream handlers
            await request.body()
    except Exception as e:
        logger.error(f"Error reading request body: {str(e)}")
    
    # Get response
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response {request_id}: Status {response.status_code}")
    
    # Log response body
    try:
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        # Try to decode and log the response body
        try:
            body_str = response_body.decode()
            if body_str:
                try:
                    # Try to parse and pretty print if it's JSON
                    parsed_body = json.loads(body_str)
                    logger.info(f"Response {request_id} Body: {json.dumps(parsed_body, indent=2)}")
                except json.JSONDecodeError:
                    # If not JSON, log as plain text
                    logger.info(f"Response {request_id} Body: {body_str}")
        except UnicodeDecodeError:
            logger.info(f"Response {request_id} Body: <binary content>")
        
        # Create new response with the same body
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
    except Exception as e:
        logger.error(f"Error logging response body: {str(e)}")
        return response
    finally:
        logger.info(f"Response {request_id}: Completed in {process_time:.3f}s")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
