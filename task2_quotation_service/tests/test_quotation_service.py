"""
Tests for Quotation Service
"""

import pytest
import json
from datetime import datetime
from fastapi.testclient import TestClient

from api.main import app
from api.models import QuotationRequest, ClientInfo, QuotationItem
from api.quotation_service import QuotationService

client = TestClient(app)

class TestQuotationService:
    """Test cases for quotation service"""
    
    def setup_method(self):
        """Setup for each test"""
        self.quotation_service = QuotationService()
        
        # Sample test data
        self.sample_request = QuotationRequest(
            client=ClientInfo(
                name="Test Client",
                contact="test@client.com",
                lang="en"
            ),
            currency="SAR",
            items=[
                QuotationItem(
                    sku="ALR-SL-90W",
                    qty=120,
                    unit_cost=240.0,
                    margin_pct=22
                ),
                QuotationItem(
                    sku="ALR-OBL-12V",
                    qty=40,
                    unit_cost=95.5,
                    margin_pct=18
                )
            ],
            delivery_terms="DAP Dammam, 4 weeks",
            notes="Test quotation"
        )
    
    def test_generate_quotation_success(self):
        """Test successful quotation generation"""
        result = self.quotation_service.generate_quotation(self.sample_request)
        
        assert result.quotation_id is not None
        assert result.client.name == "Test Client"
        assert result.currency == "SAR"
        assert len(result.line_items) == 2
        assert result.total > 0
        assert result.email_draft is not None
    
    def test_calculate_line_items(self):
        """Test line item calculations"""
        items = self.sample_request.items
        line_items = self.quotation_service._calculate_line_items(items)
        
        assert len(line_items) == 2
        
        # Test first item calculation
        item1 = line_items[0]
        expected_unit_price = 240.0 * (1 + 22/100)  # 292.8
        expected_line_total = expected_unit_price * 120  # 35136
        
        assert item1.unit_price == pytest.approx(expected_unit_price, rel=1e-2)
        assert item1.line_total == pytest.approx(expected_line_total, rel=1e-2)
    
    def test_pricing_logic(self):
        """Test pricing calculations"""
        result = self.quotation_service.generate_quotation(self.sample_request)
        
        # Check subtotal
        expected_subtotal = sum(item.line_total for item in result.line_items)
        assert result.subtotal == pytest.approx(expected_subtotal, rel=1e-2)
        
        # Check tax calculation
        expected_tax = expected_subtotal * 0.15
        assert result.tax_amount == pytest.approx(expected_tax, rel=1e-2)
        
        # Check total
        expected_total = expected_subtotal + expected_tax
        assert result.total == pytest.approx(expected_total, rel=1e-2)
    
    def test_email_draft_generation(self):
        """Test email draft generation"""
        result = self.quotation_service.generate_quotation(self.sample_request)
        
        assert result.email_draft is not None
        assert len(result.email_draft) > 0
        assert "Test Client" in result.email_draft
        assert str(result.total) in result.email_draft
    
    def test_arabic_email_template(self):
        """Test Arabic email template generation"""
        arabic_request = QuotationRequest(
            client=ClientInfo(
                name="عميل تجريبي",
                contact="test@client.com",
                lang="ar"
            ),
            currency="SAR",
            items=[
                QuotationItem(
                    sku="ALR-SL-90W",
                    qty=10,
                    unit_cost=240.0,
                    margin_pct=22
                )
            ],
            delivery_terms="DAP الرياض، 2 أسبوع",
            notes="اختبار"
        )
        
        result = self.quotation_service.generate_quotation(arabic_request)
        
        assert "عرض سعر" in result.email_draft
        assert "عميل تجريبي" in result.email_draft
    
    def test_invalid_sku(self):
        """Test handling of invalid SKU"""
        invalid_request = QuotationRequest(
            client=ClientInfo(
                name="Test Client",
                contact="test@client.com",
                lang="en"
            ),
            currency="SAR",
            items=[
                QuotationItem(
                    sku="INVALID-SKU",
                    qty=1,
                    unit_cost=100.0,
                    margin_pct=20
                )
            ],
            delivery_terms="DAP Test",
            notes="Test"
        )
        
        with pytest.raises(ValueError, match="Product INVALID-SKU not found"):
            self.quotation_service.generate_quotation(invalid_request)
    
    def test_quotation_storage(self):
        """Test quotation storage and retrieval"""
        result = self.quotation_service.generate_quotation(self.sample_request)
        quotation_id = result.quotation_id
        
        # Test retrieval
        stored_quotation = self.quotation_service.get_quotation(quotation_id)
        assert stored_quotation is not None
        assert stored_quotation["quotation_id"] == quotation_id
    
    def test_quotation_listing(self):
        """Test quotation listing"""
        # Generate multiple quotations
        for i in range(3):
            request = QuotationRequest(
                client=ClientInfo(
                    name=f"Client {i}",
                    contact=f"client{i}@test.com",
                    lang="en"
                ),
                currency="SAR",
                items=[
                    QuotationItem(
                        sku="ALR-SL-90W",
                        qty=10,
                        unit_cost=240.0,
                        margin_pct=20
                    )
                ],
                delivery_terms="DAP Test",
                notes="Test"
            )
            self.quotation_service.generate_quotation(request)
        
        # Test listing
        quotations = self.quotation_service.list_quotations(limit=10)
        assert len(quotations) >= 3
    
    def test_quotation_deletion(self):
        """Test quotation deletion"""
        result = self.quotation_service.generate_quotation(self.sample_request)
        quotation_id = result.quotation_id
        
        # Test deletion
        success = self.quotation_service.delete_quotation(quotation_id)
        assert success is True
        
        # Test retrieval after deletion
        stored_quotation = self.quotation_service.get_quotation(quotation_id)
        assert stored_quotation is None
    
    def test_product_catalog(self):
        """Test product catalog"""
        products = self.quotation_service.get_products()
        
        assert len(products) > 0
        
        # Check specific product
        alr_sl_90w = next((p for p in products if p["sku"] == "ALR-SL-90W"), None)
        assert alr_sl_90w is not None
        assert alr_sl_90w["name"] == "90W Streetlight Pole"
        assert alr_sl_90w["base_price"] == 240.0

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_generate_quotation_endpoint(self):
        """Test quotation generation endpoint"""
        request_data = {
            "client": {
                "name": "Test Client",
                "contact": "test@client.com",
                "lang": "en"
            },
            "currency": "SAR",
            "items": [
                {
                    "sku": "ALR-SL-90W",
                    "qty": 120,
                    "unit_cost": 240.0,
                    "margin_pct": 22
                }
            ],
            "delivery_terms": "DAP Dammam, 4 weeks",
            "notes": "Test quotation"
        }
        
        response = client.post("/quote", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "quotation_id" in data
        assert "total" in data
        assert "email_draft" in data
    
    def test_invalid_quotation_request(self):
        """Test invalid quotation request"""
        invalid_request = {
            "client": {
                "name": "Test Client",
                "contact": "invalid-email",  # Invalid email
                "lang": "en"
            },
            "currency": "SAR",
            "items": [],  # Empty items
            "delivery_terms": "DAP Test"
        }
        
        response = client.post("/quote", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_get_quotation_endpoint(self):
        """Test get quotation endpoint"""
        # First create a quotation
        request_data = {
            "client": {
                "name": "Test Client",
                "contact": "test@client.com",
                "lang": "en"
            },
            "currency": "SAR",
            "items": [
                {
                    "sku": "ALR-SL-90W",
                    "qty": 10,
                    "unit_cost": 240.0,
                    "margin_pct": 20
                }
            ],
            "delivery_terms": "DAP Test"
        }
        
        create_response = client.post("/quote", json=request_data)
        quotation_id = create_response.json()["quotation_id"]
        
        # Test retrieval
        response = client.get(f"/quote/{quotation_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["quotation_id"] == quotation_id
    
    def test_get_nonexistent_quotation(self):
        """Test getting non-existent quotation"""
        response = client.get("/quote/NONEXISTENT")
        assert response.status_code == 404
    
    def test_list_quotations_endpoint(self):
        """Test list quotations endpoint"""
        response = client.get("/quotes")
        assert response.status_code == 200
        
        data = response.json()
        assert "quotations" in data
        assert "total" in data
    
    def test_products_endpoint(self):
        """Test products endpoint"""
        response = client.get("/products")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert len(data["products"]) > 0
        
        # Check product structure
        product = data["products"][0]
        assert "sku" in product
        assert "name" in product
        assert "base_price" in product
    
    def test_delete_quotation_endpoint(self):
        """Test delete quotation endpoint"""
        # First create a quotation
        request_data = {
            "client": {
                "name": "Test Client",
                "contact": "test@client.com",
                "lang": "en"
            },
            "currency": "SAR",
            "items": [
                {
                    "sku": "ALR-SL-90W",
                    "qty": 10,
                    "unit_cost": 240.0,
                    "margin_pct": 20
                }
            ],
            "delivery_terms": "DAP Test"
        }
        
        create_response = client.post("/quote", json=request_data)
        quotation_id = create_response.json()["quotation_id"]
        
        # Test deletion
        response = client.delete(f"/quote/{quotation_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
    
    def test_delete_nonexistent_quotation(self):
        """Test deleting non-existent quotation"""
        response = client.delete("/quote/NONEXISTENT")
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])
