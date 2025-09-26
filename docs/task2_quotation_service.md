# Task 2: Quotation Microservice

## Overview
A FastAPI-based microservice for generating quotations with OpenAI integration, comprehensive pricing logic, and multi-language support.

## Features

### Core Functionality
- **Quotation Generation**: Complete quotation processing with pricing calculations
- **Multi-language Support**: Arabic and English email generation
- **OpenAI Integration**: Intelligent email draft generation
- **Product Catalog**: Comprehensive product database with specifications
- **Pricing Logic**: Advanced pricing calculations with margins and taxes

### API Endpoints

#### POST /quote
Generate a new quotation based on client requirements.

**Request Example:**
```json
{
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
    }
  ],
  "delivery_terms": "DAP Dammam, 4 weeks",
  "notes": "Client asked for spec compliance with Tarsheed."
}
```

**Response Example:**
```json
{
  "quotation_id": "QUO-2024-001",
  "client": {...},
  "currency": "SAR",
  "line_items": [...],
  "subtotal": 35136.0,
  "tax_rate": 15.0,
  "tax_amount": 5270.4,
  "total": 40406.4,
  "email_draft": "Dear Gulf Eng.,\n\nThank you for your RFQ...",
  "created_at": "2024-01-15T10:30:00Z",
  "valid_until": "2024-02-15T10:30:00Z"
}
```

#### GET /quote/{quotation_id}
Retrieve a specific quotation by ID.

#### GET /quotes
List all quotations with pagination support.

#### DELETE /quote/{quotation_id}
Delete a quotation by ID.

#### GET /products
List available products with specifications.

## Pricing Logic

### Calculation Formula
```
Unit Price = Unit Cost × (1 + Margin Percentage / 100)
Line Total = Unit Price × Quantity
Subtotal = Sum of all Line Totals
Tax Amount = Subtotal × Tax Rate / 100
Total = Subtotal + Tax Amount
```

### Example Calculation
```
Item: ALR-SL-90W
Unit Cost: 240.0 SAR
Margin: 22%
Quantity: 120 units

Unit Price = 240.0 × (1 + 22/100) = 292.8 SAR
Line Total = 292.8 × 120 = 35,136 SAR
Tax (15%) = 35,136 × 0.15 = 5,270.4 SAR
Total = 35,136 + 5,270.4 = 40,406.4 SAR
```

## Product Catalog

### Available Products
- **ALR-SL-60W**: 60W Streetlight Pole (180 SAR base price)
- **ALR-SL-90W**: 90W Streetlight Pole (240 SAR base price)
- **ALR-SL-120W**: 120W Streetlight Pole (320 SAR base price)
- **ALR-OBL-12V**: 12V Outdoor Bollard Light (95.5 SAR base price)
- **ALR-FL-50W**: 50W Flood Light (150 SAR base price)

### Product Specifications
Each product includes:
- Technical specifications
- Material information
- Performance characteristics
- Application guidelines

## OpenAI Integration

### Email Generation
The service uses OpenAI to generate professional quotation emails in both Arabic and English.

**Arabic Example:**
```
الموضوع: عرض سعر - Gulf Eng.

السيد/ة Gulf Eng. المحترم/ة،

نشكركم على اهتمامكم بمنتجات شركة الأروف للتكنولوجيا والإضاءة.

نرفق لكم عرض السعر المطلوب:
• المنتج: ALR-SL-90W - 90W Streetlight Pole
• الكمية: 120 وحدة
• السعر للوحدة: 292.8 ريال
• المجموع: 35136 ريال

المجموع الكلي: 40406.4 ريال
```

**English Example:**
```
Subject: Quotation - Gulf Eng.

Dear Gulf Eng.,

Thank you for your interest in Alrouf Lighting Technology products.

Please find below our quotation for your requirements:
• Product: ALR-SL-90W - 90W Streetlight Pole
• Quantity: 120 units
• Unit Price: 292.8 SAR
• Line Total: 35136 SAR

Total: 40406.4 SAR
```

## Testing

### Unit Tests
Comprehensive test suite covering:
- Pricing calculations
- Email generation
- API endpoints
- Error handling
- Mock services

### Test Coverage
- **Pricing Logic**: All calculation scenarios
- **API Endpoints**: All CRUD operations
- **Error Handling**: Invalid inputs and edge cases
- **Mock Services**: Safe testing without external dependencies

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest task2_quotation_service/tests/

# Run with coverage
pytest --cov=task2_quotation_service tests/
```

## Docker Support

### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Commands
```bash
# Build image
docker build -t alrouf-quotation-service .

# Run container
docker run -p 8000:8000 alrouf-quotation-service

# Run with environment variables
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key alrouf-quotation-service
```

## API Documentation

### OpenAPI/Swagger
The service includes comprehensive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Schema
All request/response models are fully documented with:
- Field descriptions
- Validation rules
- Example values
- Type information

## Configuration

### Environment Variables
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo

# Database
DATABASE_URL=sqlite:///./quotations.db

# Mock Services
USE_MOCK_SERVICES=True
```

### Mock Services
The service includes comprehensive mock functionality:
- **Mock OpenAI**: Template-based email generation
- **Mock Database**: In-memory storage for testing
- **Mock Responses**: Simulated API responses

## Performance

### Optimization Features
- **Async Operations**: Non-blocking API calls
- **Connection Pooling**: Efficient database connections
- **Caching**: Response caching for repeated requests
- **Batch Processing**: Efficient bulk operations

### Monitoring
- **Health Checks**: `/health` endpoint for monitoring
- **Metrics**: Request/response timing
- **Logging**: Comprehensive operation logging
- **Error Tracking**: Detailed error reporting

## Security

### Security Features
- **Input Validation**: Comprehensive request validation
- **SQL Injection Protection**: Parameterized queries
- **Rate Limiting**: API rate limiting (configurable)
- **CORS Support**: Cross-origin request handling

### Best Practices
- **Environment Variables**: Secure credential management
- **No Hardcoded Secrets**: All sensitive data externalized
- **Input Sanitization**: All inputs validated and sanitized
- **Error Handling**: Secure error messages

## Deployment

### Production Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export DEBUG=False

# Run with production server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```bash
# Build production image
docker build -t alrouf-quotation-service:latest .

# Run with docker-compose
docker-compose up -d
```

## Maintenance

### Regular Tasks
- **Dependency Updates**: Regular package updates
- **Security Patches**: Timely security updates
- **Performance Monitoring**: Regular performance reviews
- **Log Analysis**: Daily log review and analysis

### Troubleshooting
- **Common Issues**: Documented solutions
- **Debug Procedures**: Step-by-step debugging
- **Recovery Procedures**: System recovery guides
- **Support Contacts**: Technical support information
