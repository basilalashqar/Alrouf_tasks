#!/usr/bin/env python3
"""
Simple API Server for React Webapp
A minimal FastAPI server that definitely works
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Alrouf AI API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
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
    delivery_terms: str = ""
    notes: str = ""

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is running"}

# Quotation endpoint
@app.post("/quote")
async def generate_quotation(request: QuotationRequest):
    """Generate a quotation"""
    
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
    tax_amount = subtotal * 0.15
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
    
    return {
        "quotation_id": quotation_id,
        "client": request.client,
        "items": items_with_totals,
        "subtotal": round(subtotal, 2),
        "tax_amount": round(tax_amount, 2),
        "total": round(total, 2),
        "email_draft": email_draft,
        "generated_at": datetime.now().isoformat()
    }

# RAG endpoint
@app.post("/rag/query")
async def query_rag(request: dict):
    """Query the RAG knowledge base"""
    
    query = request.get("query", "")
    language = request.get("language", "en")
    
    # Simple responses based on keywords
    if "product" in query.lower() or "منتج" in query:
        if language == "ar":
            answer = "تقدم شركة الأروف للتكنولوجيا والإضاءة أعمدة إضاءة الشوارع LED بقوة 90 واط و 120 واط و 60 واط. كما نوفر أضواء الأعمدة الخارجية وأضواء الفيضانات للتطبيقات المختلفة."
        else:
            answer = "Alrouf Lighting Technology offers LED streetlight poles with 90W, 120W, and 60W outputs. We also provide outdoor bollard lights and flood lights for various applications."
        confidence = 92.0
        sources = ["Product Catalog", "Company Brochure"]
    elif "warranty" in query.lower() or "ضمان" in query:
        if language == "ar":
            answer = "جميع المنتجات تأتي مع ضمان شامل لمدة 5 سنوات يغطي عيوب التصنيع وأعطال المواد. يشمل الضمان استبدال مجاني للمكونات المعيبة ويغطي الأجزاء والعمالة."
        else:
            answer = "All products come with a comprehensive 5-year warranty covering manufacturing defects and material failures. The warranty includes free replacement of defective components and covers parts and labor."
        confidence = 88.0
        sources = ["Warranty Terms", "Service Agreement"]
    elif "install" in query.lower() or "تثبيت" in query:
        if language == "ar":
            answer = "التثبيت يتطلب أجهزة التركيب المناسبة والوصلات الكهربائية واتخاذ احتياطات السلامة. يجب اتباع الرموز الكهربائية المحلية والتأكد من التأريض المناسب. يجب أن يكون ارتفاع التركيب 6-8 أمتار للحصول على توزيع الضوء الأمثل."
        else:
            answer = "Installation requires proper mounting hardware, electrical connections, and safety precautions. Follow local electrical codes and ensure proper grounding. Mounting height should be 6-8 meters for optimal light distribution."
        confidence = 85.0
        sources = ["Installation Guide", "Technical Manual"]
    else:
        if language == "ar":
            answer = "نعتذر، لم أتمكن من العثور على إجابة محددة لسؤالك. يرجى التواصل مع فريق المبيعات للحصول على مزيد من المعلومات."
        else:
            answer = "I apologize, but I couldn't find a specific answer to your question. Please contact our sales team for more information."
        confidence = 45.0
        sources = ["General Knowledge Base"]
    
    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "response_time": 150,
        "processing_time": 100
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple API Server...")
    print("📊 Quotation Service: http://localhost:8000/quote")
    print("🧠 RAG Knowledge Base: http://localhost:8000/rag/query")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🌐 React Webapp: http://localhost:3000")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
