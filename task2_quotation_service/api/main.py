"""
Task 2: Quotation Microservice
FastAPI-based quotation service with OpenAI integration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Dict, List, Optional
from datetime import datetime

from models import (
    QuotationRequest, 
    QuotationResponse, 
    ClientInfo, 
    QuotationItem,
    ErrorResponse
)
from quotation_service import QuotationService
from config import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Alrouf Lighting Technology - Quotation Service",
    description="Microservice for generating quotations with OpenAI integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize quotation service
quotation_service = QuotationService()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Alrouf Lighting Technology - Quotation Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "quotation-service"
    }

@app.post("/quote", response_model=QuotationResponse)
async def generate_quotation(request: QuotationRequest):
    """
    Generate quotation based on client request
    
    Args:
        request: QuotationRequest with client info, items, and terms
        
    Returns:
        QuotationResponse with pricing details and email draft
    """
    try:
        logger.info(f"Generating quotation for client: {request.client.name}")
        
        # Validate request
        if not request.items:
            raise HTTPException(status_code=400, detail="No items provided")
        
        # Generate quotation
        result = quotation_service.generate_quotation(request)
        
        logger.info(f"Quotation generated successfully for {request.client.name}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating quotation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/quote/{quotation_id}")
async def get_quotation(quotation_id: str):
    """
    Get quotation by ID
    
    Args:
        quotation_id: Unique quotation identifier
        
    Returns:
        Quotation details
    """
    try:
        quotation = quotation_service.get_quotation(quotation_id)
        if not quotation:
            raise HTTPException(status_code=404, detail="Quotation not found")
        
        return quotation
        
    except Exception as e:
        logger.error(f"Error getting quotation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/quotes")
async def list_quotations(limit: int = 100, offset: int = 0):
    """
    List quotations with pagination
    
    Args:
        limit: Maximum number of quotations to return
        offset: Number of quotations to skip
        
    Returns:
        List of quotations
    """
    try:
        quotations = quotation_service.list_quotations(limit, offset)
        return {
            "quotations": quotations,
            "total": len(quotations),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Error listing quotations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/quote/{quotation_id}")
async def delete_quotation(quotation_id: str):
    """
    Delete quotation by ID
    
    Args:
        quotation_id: Unique quotation identifier
        
    Returns:
        Success message
    """
    try:
        success = quotation_service.delete_quotation(quotation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Quotation not found")
        
        return {"message": "Quotation deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting quotation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/products")
async def list_products():
    """
    List available products with base pricing
    
    Returns:
        List of products
    """
    try:
        products = quotation_service.get_products()
        return {"products": products}
        
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
