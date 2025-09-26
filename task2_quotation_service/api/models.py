"""
Pydantic models for the Quotation Service
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    ARABIC = "ar"

class Currency(str, Enum):
    """Supported currencies"""
    SAR = "SAR"
    USD = "USD"
    EUR = "EUR"
    AED = "AED"

class ClientInfo(BaseModel):
    """Client information"""
    name: str = Field(..., description="Client name", min_length=1, max_length=100)
    contact: str = Field(..., description="Contact email", regex=r'^[^@]+@[^@]+\.[^@]+$')
    lang: Language = Field(..., description="Preferred language")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Gulf Engineering",
                "contact": "omar@client.com",
                "lang": "en"
            }
        }

class QuotationItem(BaseModel):
    """Quotation item details"""
    sku: str = Field(..., description="Product SKU", min_length=1, max_length=50)
    qty: int = Field(..., description="Quantity", gt=0, le=10000)
    unit_cost: float = Field(..., description="Unit cost", gt=0)
    margin_pct: float = Field(..., description="Margin percentage", ge=0, le=100)
    
    @validator('sku')
    def validate_sku(cls, v):
        if not v.strip():
            raise ValueError('SKU cannot be empty')
        return v.strip().upper()
    
    @validator('unit_cost')
    def validate_unit_cost(cls, v):
        if v <= 0:
            raise ValueError('Unit cost must be positive')
        return round(v, 2)
    
    @validator('margin_pct')
    def validate_margin(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Margin percentage must be between 0 and 100')
        return round(v, 2)
    
    class Config:
        schema_extra = {
            "example": {
                "sku": "ALR-SL-90W",
                "qty": 120,
                "unit_cost": 240.0,
                "margin_pct": 22
            }
        }

class QuotationRequest(BaseModel):
    """Request model for quotation generation"""
    client: ClientInfo = Field(..., description="Client information")
    currency: Currency = Field(..., description="Currency for quotation")
    items: List[QuotationItem] = Field(..., description="List of items", min_items=1)
    delivery_terms: str = Field(..., description="Delivery terms", min_length=1, max_length=200)
    notes: Optional[str] = Field(None, description="Additional notes", max_length=500)
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('At least one item is required')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "client": {
                    "name": "Gulf Eng.",
                    "contact": "omar@client.com",
                    "lang": "en"
                },
                "currency": "SAR",
                "items": [
                    {
                        "sku": "ALR-SL-90W",
                        "qty": 120,
                        "unit_cost": 240.0,
                        "margin_pct": 22
                    },
                    {
                        "sku": "ALR-OBL-12V",
                        "qty": 40,
                        "unit_cost": 95.5,
                        "margin_pct": 18
                    }
                ],
                "delivery_terms": "DAP Dammam, 4 weeks",
                "notes": "Client asked for spec compliance with Tarsheed."
            }
        }

class LineItem(BaseModel):
    """Line item in quotation response"""
    sku: str
    description: str
    qty: int
    unit_cost: float
    margin_pct: float
    unit_price: float
    line_total: float
    
    class Config:
        schema_extra = {
            "example": {
                "sku": "ALR-SL-90W",
                "description": "90W Streetlight Pole",
                "qty": 120,
                "unit_cost": 240.0,
                "margin_pct": 22.0,
                "unit_price": 292.8,
                "line_total": 35136.0
            }
        }

class QuotationResponse(BaseModel):
    """Response model for quotation generation"""
    quotation_id: str = Field(..., description="Unique quotation identifier")
    client: ClientInfo = Field(..., description="Client information")
    currency: Currency = Field(..., description="Currency")
    line_items: List[LineItem] = Field(..., description="Line items")
    subtotal: float = Field(..., description="Subtotal amount")
    tax_rate: float = Field(..., description="Tax rate percentage")
    tax_amount: float = Field(..., description="Tax amount")
    total: float = Field(..., description="Total amount")
    delivery_terms: str = Field(..., description="Delivery terms")
    notes: Optional[str] = Field(None, description="Additional notes")
    email_draft: str = Field(..., description="Generated email draft")
    created_at: datetime = Field(..., description="Creation timestamp")
    valid_until: datetime = Field(..., description="Quotation validity date")
    
    class Config:
        schema_extra = {
            "example": {
                "quotation_id": "QUO-2024-001",
                "client": {
                    "name": "Gulf Eng.",
                    "contact": "omar@client.com",
                    "lang": "en"
                },
                "currency": "SAR",
                "line_items": [
                    {
                        "sku": "ALR-SL-90W",
                        "description": "90W Streetlight Pole",
                        "qty": 120,
                        "unit_cost": 240.0,
                        "margin_pct": 22.0,
                        "unit_price": 292.8,
                        "line_total": 35136.0
                    }
                ],
                "subtotal": 35136.0,
                "tax_rate": 15.0,
                "tax_amount": 5270.4,
                "total": 40406.4,
                "delivery_terms": "DAP Dammam, 4 weeks",
                "notes": "Client asked for spec compliance with Tarsheed.",
                "email_draft": "Dear Gulf Eng.,\n\nThank you for your RFQ...",
                "created_at": "2024-01-15T10:30:00Z",
                "valid_until": "2024-02-15T10:30:00Z"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Invalid request parameters",
                "error_code": "INVALID_REQUEST",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

class ProductInfo(BaseModel):
    """Product information"""
    sku: str = Field(..., description="Product SKU")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    base_price: float = Field(..., description="Base price")
    category: str = Field(..., description="Product category")
    specifications: Dict[str, Any] = Field(..., description="Product specifications")
    
    class Config:
        schema_extra = {
            "example": {
                "sku": "ALR-SL-90W",
                "name": "90W Streetlight Pole",
                "description": "High-efficiency LED streetlight pole",
                "base_price": 240.0,
                "category": "Streetlight",
                "specifications": {
                    "wattage": "90W",
                    "height": "8m",
                    "material": "Aluminum"
                }
            }
        }
