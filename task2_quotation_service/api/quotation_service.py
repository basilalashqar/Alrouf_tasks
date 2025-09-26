"""
Quotation service with pricing logic and OpenAI integration
"""

import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import openai
except ImportError:
    openai = None

from models import (
    QuotationRequest, 
    QuotationResponse, 
    LineItem, 
    ClientInfo,
    ProductInfo
)
from config import get_settings

logger = logging.getLogger(__name__)

@dataclass
class Product:
    """Product data structure"""
    sku: str
    name: str
    description: str
    base_price: float
    category: str
    specifications: Dict[str, Any]

class QuotationService:
    """Main quotation service with pricing logic and OpenAI integration"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.quotations = {}  # In-memory storage for demo
        self.products = self._initialize_products()
        
        if not self.settings.use_mock_services and self.settings.openai_api_key:
            try:
                self.client = openai.OpenAI(api_key=self.settings.openai_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def _initialize_products(self) -> Dict[str, Product]:
        """Initialize product catalog"""
        products = {
            "ALR-SL-90W": Product(
                sku="ALR-SL-90W",
                name="90W Streetlight Pole",
                description="High-efficiency LED streetlight pole with 90W output",
                base_price=240.0,
                category="Streetlight",
                specifications={
                    "wattage": "90W",
                    "height": "8m",
                    "material": "Aluminum",
                    "lifespan": "50000 hours",
                    "color_temp": "4000K"
                }
            ),
            "ALR-SL-120W": Product(
                sku="ALR-SL-120W",
                name="120W Streetlight Pole",
                description="High-efficiency LED streetlight pole with 120W output",
                base_price=320.0,
                category="Streetlight",
                specifications={
                    "wattage": "120W",
                    "height": "10m",
                    "material": "Aluminum",
                    "lifespan": "50000 hours",
                    "color_temp": "4000K"
                }
            ),
            "ALR-SL-60W": Product(
                sku="ALR-SL-60W",
                name="60W Streetlight Pole",
                description="High-efficiency LED streetlight pole with 60W output",
                base_price=180.0,
                category="Streetlight",
                specifications={
                    "wattage": "60W",
                    "height": "6m",
                    "material": "Aluminum",
                    "lifespan": "50000 hours",
                    "color_temp": "4000K"
                }
            ),
            "ALR-OBL-12V": Product(
                sku="ALR-OBL-12V",
                name="12V Outdoor Bollard Light",
                description="Low-voltage outdoor bollard light for pathways",
                base_price=95.5,
                category="Bollard",
                specifications={
                    "voltage": "12V",
                    "wattage": "15W",
                    "height": "1.2m",
                    "material": "Stainless Steel",
                    "lifespan": "30000 hours"
                }
            ),
            "ALR-FL-50W": Product(
                sku="ALR-FL-50W",
                name="50W Flood Light",
                description="High-power flood light for area illumination",
                base_price=150.0,
                category="Floodlight",
                specifications={
                    "wattage": "50W",
                    "beam_angle": "120°",
                    "material": "Aluminum",
                    "lifespan": "40000 hours",
                    "color_temp": "5000K"
                }
            )
        }
        return products
    
    def generate_quotation(self, request: QuotationRequest) -> QuotationResponse:
        """
        Generate quotation with pricing and email draft
        
        Args:
            request: QuotationRequest with client and item details
            
        Returns:
            QuotationResponse with complete quotation
        """
        try:
            logger.info(f"Generating quotation for {request.client.name}")
            
            # Generate unique quotation ID
            quotation_id = f"QUO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # Calculate line items
            line_items = self._calculate_line_items(request.items)
            
            # Calculate totals
            subtotal = sum(item.line_total for item in line_items)
            tax_rate = 15.0  # 15% VAT for Saudi Arabia
            tax_amount = subtotal * (tax_rate / 100)
            total = subtotal + tax_amount
            
            # Generate email draft
            email_draft = self._generate_email_draft(request, line_items, total)
            
            # Create response
            response = QuotationResponse(
                quotation_id=quotation_id,
                client=request.client,
                currency=request.currency,
                line_items=line_items,
                subtotal=round(subtotal, 2),
                tax_rate=tax_rate,
                tax_amount=round(tax_amount, 2),
                total=round(total, 2),
                delivery_terms=request.delivery_terms,
                notes=request.notes,
                email_draft=email_draft,
                created_at=datetime.now(),
                valid_until=datetime.now() + timedelta(days=30)
            )
            
            # Store quotation
            self.quotations[quotation_id] = response.dict()
            
            logger.info(f"Quotation {quotation_id} generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error generating quotation: {e}")
            raise ValueError(f"Failed to generate quotation: {str(e)}")
    
    def _calculate_line_items(self, items: List[Any]) -> List[LineItem]:
        """Calculate line items with pricing"""
        line_items = []
        
        for item in items:
            # Get product info
            product = self.products.get(item.sku)
            if not product:
                raise ValueError(f"Product {item.sku} not found")
            
            # Calculate unit price with margin
            unit_price = item.unit_cost * (1 + item.margin_pct / 100)
            line_total = unit_price * item.qty
            
            line_item = LineItem(
                sku=item.sku,
                description=product.description,
                qty=item.qty,
                unit_cost=item.unit_cost,
                margin_pct=item.margin_pct,
                unit_price=round(unit_price, 2),
                line_total=round(line_total, 2)
            )
            
            line_items.append(line_item)
        
        return line_items
    
    def _generate_email_draft(self, request: QuotationRequest, line_items: List[LineItem], total: float) -> str:
        """Generate email draft using OpenAI or template"""
        try:
            if self.client and not self.settings.use_mock_services:
                return self._generate_with_openai(request, line_items, total)
            else:
                return self._generate_template_email(request, line_items, total)
                
        except Exception as e:
            logger.error(f"Error generating email draft: {e}")
            return self._generate_template_email(request, line_items, total)
    
    def _generate_with_openai(self, request: QuotationRequest, line_items: List[LineItem], total: float) -> str:
        """Generate email draft using OpenAI"""
        prompt = f"""
        Generate a professional quotation email for Alrouf Lighting Technology.
        
        Client: {request.client.name}
        Contact: {request.client.contact}
        Language: {request.client.lang}
        Currency: {request.currency}
        Total Amount: {total}
        Delivery Terms: {request.delivery_terms}
        Notes: {request.notes or 'None'}
        
        Items:
        {json.dumps([item.dict() for item in line_items], indent=2)}
        
        The email should:
        1. Be professional and courteous
        2. Include a clear subject line
        3. Acknowledge the RFQ
        4. Present the quotation details clearly
        5. Include terms and conditions
        6. Be in the client's preferred language ({request.client.lang})
        
        Return only the email content, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a professional sales representative for Alrouf Lighting Technology. Generate professional quotation emails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI email generation failed: {e}")
            return self._generate_template_email(request, line_items, total)
    
    def _generate_template_email(self, request: QuotationRequest, line_items: List[LineItem], total: float) -> str:
        """Generate email using template"""
        if request.client.lang == "ar":
            return self._generate_arabic_template(request, line_items, total)
        else:
            return self._generate_english_template(request, line_items, total)
    
    def _generate_arabic_template(self, request: QuotationRequest, line_items: List[LineItem], total: float) -> str:
        """Generate Arabic email template"""
        subject = f"عرض سعر - {request.client.name}"
        
        body = f"""
الموضوع: عرض سعر - {request.client.name}

السيد/ة {request.client.name} المحترم/ة،

السلام عليكم ورحمة الله وبركاته،

نشكركم على اهتمامكم بمنتجات شركة الأروف للتكنولوجيا والإضاءة.

نرفق لكم عرض السعر المطلوب:

تفاصيل العرض:
"""
        
        for item in line_items:
            body += f"""
• المنتج: {item.sku} - {item.description}
• الكمية: {item.qty} وحدة
• السعر للوحدة: {item.unit_price} {request.currency}
• المجموع: {item.line_total} {request.currency}
"""
        
        body += f"""
المجموع الفرعي: {sum(item.line_total for item in line_items)} {request.currency}
ضريبة القيمة المضافة (15%): {total - sum(item.line_total for item in line_items)} {request.currency}
المجموع الكلي: {total} {request.currency}

شروط التسليم: {request.delivery_terms}

ملاحظات: {request.notes or 'لا توجد ملاحظات إضافية'}

هذا العرض صالح لمدة 30 يوماً من تاريخ الإصدار.

نتطلع للتعاون معكم.

مع أطيب التحيات،
فريق المبيعات
شركة الأروف للتكنولوجيا والإضاءة
هاتف: +966 11 123 4567
بريد إلكتروني: sales@alrouf.com
        """
        
        return f"Subject: {subject}\n\n{body.strip()}"
    
    def _generate_english_template(self, request: QuotationRequest, line_items: List[LineItem], total: float) -> str:
        """Generate English email template"""
        subject = f"Quotation - {request.client.name}"
        
        body = f"""
Subject: Quotation - {request.client.name}

Dear {request.client.name},

Thank you for your interest in Alrouf Lighting Technology products.

Please find below our quotation for your requirements:

Quotation Details:
"""
        
        for item in line_items:
            body += f"""
• Product: {item.sku} - {item.description}
• Quantity: {item.qty} units
• Unit Price: {item.unit_price} {request.currency}
• Line Total: {item.line_total} {request.currency}
"""
        
        body += f"""
Subtotal: {sum(item.line_total for item in line_items)} {request.currency}
VAT (15%): {total - sum(item.line_total for item in line_items)} {request.currency}
Total: {total} {request.currency}

Delivery Terms: {request.delivery_terms}

Notes: {request.notes or 'No additional notes'}

This quotation is valid for 30 days from the date of issue.

We look forward to working with you.

Best regards,
Sales Team
Alrouf Lighting Technology
Phone: +966 11 123 4567
Email: sales@alrouf.com
        """
        
        return f"Subject: {subject}\n\n{body.strip()}"
    
    def get_quotation(self, quotation_id: str) -> Optional[Dict]:
        """Get quotation by ID"""
        return self.quotations.get(quotation_id)
    
    def list_quotations(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List quotations with pagination"""
        quotations = list(self.quotations.values())
        return quotations[offset:offset + limit]
    
    def delete_quotation(self, quotation_id: str) -> bool:
        """Delete quotation by ID"""
        if quotation_id in self.quotations:
            del self.quotations[quotation_id]
            return True
        return False
    
    def get_products(self) -> List[Dict]:
        """Get available products"""
        return [
            {
                "sku": product.sku,
                "name": product.name,
                "description": product.description,
                "base_price": product.base_price,
                "category": product.category,
                "specifications": product.specifications
            }
            for product in self.products.values()
        ]
