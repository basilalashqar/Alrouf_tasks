#!/usr/bin/env python3
"""
Mock API Server for React Webapp
Provides mock responses for Task 2 (Quotation) and Task 3 (RAG) services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time
import random
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Alrouf AI Mock API",
    description="Mock API server for React webapp testing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Client(BaseModel):
    name: str
    contact: str
    lang: str

class Item(BaseModel):
    sku: str
    qty: int
    unit_cost: float
    margin_pct: float

class QuotationRequest(BaseModel):
    client: Client
    currency: str
    items: List[Item]
    delivery_terms: Optional[str] = ""
    notes: Optional[str] = ""

class QuotationResponse(BaseModel):
    quotation_id: str
    client: Client
    items: List[dict]
    subtotal: float
    tax_amount: float
    total: float
    email_draft: str
    generated_at: str

class RAGQuery(BaseModel):
    query: str
    language: str

class RAGResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    response_time: int
    processing_time: int

# Mock data
MOCK_QUOTATIONS = []
MOCK_RAG_KNOWLEDGE = {
    "en": {
        "products": "Alrouf Lighting Technology offers LED streetlight poles with 90W, 120W, and 60W outputs. We also provide outdoor bollard lights and flood lights for various applications.",
        "warranty": "All products come with a comprehensive 5-year warranty covering manufacturing defects and material failures. The warranty includes free replacement of defective components and covers parts and labor.",
        "installation": "Installation requires proper mounting hardware, electrical connections, and safety precautions. Follow local electrical codes and ensure proper grounding. Mounting height should be 6-8 meters for optimal light distribution."
    },
    "ar": {
        "products": "تقدم شركة الأروف للتكنولوجيا والإضاءة أعمدة إضاءة الشوارع LED بقوة 90 واط و 120 واط و 60 واط. كما نوفر أضواء الأعمدة الخارجية وأضواء الفيضانات للتطبيقات المختلفة.",
        "warranty": "جميع المنتجات تأتي مع ضمان شامل لمدة 5 سنوات يغطي عيوب التصنيع وأعطال المواد. يشمل الضمان استبدال مجاني للمكونات المعيبة ويغطي الأجزاء والعمالة.",
        "installation": "التثبيت يتطلب أجهزة التركيب المناسبة والوصلات الكهربائية واتخاذ احتياطات السلامة. يجب اتباع الرموز الكهربائية المحلية والتأكد من التأريض المناسب. يجب أن يكون ارتفاع التركيب 6-8 أمتار للحصول على توزيع الضوء الأمثل."
    }
}

# Health check endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mock_api", "timestamp": datetime.now().isoformat()}

@app.get("/health/quotation")
async def quotation_health():
    return {"status": "healthy", "service": "quotation_mock", "timestamp": datetime.now().isoformat()}

@app.get("/health/rag")
async def rag_health():
    return {"status": "healthy", "service": "rag_mock", "timestamp": datetime.now().isoformat()}

# Quotation endpoints
@app.post("/quote", response_model=QuotationResponse)
async def generate_quotation(request: QuotationRequest):
    """Generate a mock quotation"""
    try:
        # Calculate pricing
        items_with_totals = []
        subtotal = 0
        
        for item in request.items:
            unit_price = item.unit_cost * (1 + item.margin_pct / 100)
            line_total = unit_price * item.qty
            subtotal += line_total
            
            items_with_totals.append({
                "sku": item.sku,
                "qty": item.qty,
                "unit_cost": item.unit_cost,
                "margin_pct": item.margin_pct,
                "unit_price": round(unit_price, 2),
                "line_total": round(line_total, 2)
            })
        
        # Calculate tax (15% VAT)
        tax_rate = 0.15
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        # Generate quotation ID
        quotation_id = f"QUO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Generate email draft
        if request.client.lang == "ar":
            email_draft = f"""الموضوع: عرض سعر - {quotation_id}

السيد/السيدة {request.client.name} المحترم/ة،

نشكركم على اهتمامكم بمنتجات شركة الأروف للتكنولوجيا والإضاءة.

نرفق لكم عرض السعر المطلوب:

رقم العرض: {quotation_id}
العملة: {request.currency}

تفاصيل المنتجات:
"""
            for item in items_with_totals:
                email_draft += f"- {item['sku']}: {item['qty']} قطعة × {item['unit_price']} = {item['line_total']} {request.currency}\n"
            
            email_draft += f"""
المجموع الفرعي: {subtotal:.2f} {request.currency}
ضريبة القيمة المضافة (15%): {tax_amount:.2f} {request.currency}
المجموع الكلي: {total:.2f} {request.currency}

شروط التسليم: {request.delivery_terms}
ملاحظات: {request.notes}

نحن في خدمتكم لأي استفسارات إضافية.

مع أطيب التحيات،
فريق المبيعات - شركة الأروف للتكنولوجيا والإضاءة
"""
        else:
            email_draft = f"""Subject: Quotation - {quotation_id}

Dear {request.client.name},

Thank you for your interest in Alrouf Lighting Technology products.

Please find below the requested quotation:

Quotation ID: {quotation_id}
Currency: {request.currency}

Product Details:
"""
            for item in items_with_totals:
                email_draft += f"- {item['sku']}: {item['qty']} pcs × {item['unit_price']} = {item['line_total']} {request.currency}\n"
            
            email_draft += f"""
Subtotal: {subtotal:.2f} {request.currency}
VAT (15%): {tax_amount:.2f} {request.currency}
Total: {total:.2f} {request.currency}

Delivery Terms: {request.delivery_terms}
Notes: {request.notes}

We are at your service for any additional inquiries.

Best regards,
Sales Team - Alrouf Lighting Technology
"""
        
        # Create response
        response = QuotationResponse(
            quotation_id=quotation_id,
            client=request.client,
            items=items_with_totals,
            subtotal=round(subtotal, 2),
            tax_amount=round(tax_amount, 2),
            total=round(total, 2),
            email_draft=email_draft,
            generated_at=datetime.now().isoformat()
        )
        
        # Store in mock database
        MOCK_QUOTATIONS.append(response.dict())
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quotation: {str(e)}")

@app.get("/quotes")
async def list_quotations():
    """List all quotations"""
    return {"quotations": MOCK_QUOTATIONS, "count": len(MOCK_QUOTATIONS)}

@app.get("/quote/{quotation_id}")
async def get_quotation(quotation_id: str):
    """Get quotation by ID"""
    for quotation in MOCK_QUOTATIONS:
        if quotation["quotation_id"] == quotation_id:
            return quotation
    raise HTTPException(status_code=404, detail="Quotation not found")

# RAG endpoints
@app.post("/rag/query", response_model=RAGResponse)
async def query_rag(request: RAGQuery):
    """Query the RAG knowledge base"""
    try:
        start_time = time.time()
        
        # Simple keyword matching for demo
        query_lower = request.query.lower()
        lang = request.language
        
        # Determine answer based on keywords
        if any(word in query_lower for word in ["product", "منتج", "offer", "تقدم"]):
            answer = MOCK_RAG_KNOWLEDGE[lang]["products"]
            confidence = 92.0
            sources = ["Product Catalog", "Company Brochure"]
        elif any(word in query_lower for word in ["warranty", "ضمان", "guarantee"]):
            answer = MOCK_RAG_KNOWLEDGE[lang]["warranty"]
            confidence = 88.0
            sources = ["Warranty Terms", "Service Agreement"]
        elif any(word in query_lower for word in ["install", "تثبيت", "setup", "تركيب"]):
            answer = MOCK_RAG_KNOWLEDGE[lang]["installation"]
            confidence = 85.0
            sources = ["Installation Guide", "Technical Manual"]
        else:
            if lang == "ar":
                answer = "نعتذر، لم أتمكن من العثور على إجابة محددة لسؤالك. يرجى التواصل مع فريق المبيعات للحصول على مزيد من المعلومات."
            else:
                answer = "I apologize, but I couldn't find a specific answer to your question. Please contact our sales team for more information."
            confidence = 45.0
            sources = ["General Knowledge Base"]
        
        processing_time = int((time.time() - start_time) * 1000)
        response_time = processing_time + random.randint(50, 150)
        
        return RAGResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
            response_time=response_time,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/rag/documents")
async def get_documents():
    """Get available documents"""
    return {
        "documents": [
            {"name": "Product Catalog", "type": "pdf", "size": "2.3 MB"},
            {"name": "Installation Guide", "type": "pdf", "size": "1.8 MB"},
            {"name": "Warranty Terms", "type": "pdf", "size": "0.9 MB"}
        ],
        "count": 3
    }

@app.get("/rag/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    return {
        "total_queries": random.randint(150, 300),
        "average_confidence": 87.5,
        "average_response_time": 245,
        "documents_processed": 3,
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Mock API Server...")
    print("📊 Quotation Service: http://localhost:8000/quote")
    print("🧠 RAG Knowledge Base: http://localhost:8000/rag/query")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print()
    print("🌐 React Webapp should connect to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
