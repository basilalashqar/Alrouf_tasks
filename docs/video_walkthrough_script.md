# Video Walkthrough Script (3-7 minutes)

## Introduction (30 seconds)
"Welcome to the Alrouf Lighting Technology RFQ Automation System. I'll demonstrate three complete automation solutions that handle the entire RFQ workflow from email capture to quotation generation and knowledge management."

## Task 1: No-Code RFQ Automation (2 minutes)

### Setup (30 seconds)
"First, let's look at the No-Code solution using Zapier. This is perfect for non-technical users who want powerful automation without coding."

**Show:**
- Zapier workflow blueprint
- Visual workflow diagram
- Sample data structures

### Workflow Demonstration (90 seconds)
"Let me show you how the complete workflow works with a real RFQ email."

**Demo Steps:**
1. **Email Trigger**: Show Gmail filter configuration
   - Subject contains "RFQ"
   - Body contains product codes like "ALR-"
   - External email detection

2. **Field Extraction**: Demonstrate OpenAI integration
   - Input: Raw email text
   - Output: Structured JSON data
   - Show extracted fields: client name, product, quantity, location

3. **Google Sheets**: Show automatic data entry
   - Display sample spreadsheet
   - Show real-time data population
   - Highlight organized columns

4. **Salesforce**: Demonstrate opportunity creation
   - Show mock Salesforce log
   - Display opportunity details
   - Highlight automatic account linking

5. **Drive Archiving**: Show attachment handling
   - Display folder structure
   - Show organized client folders
   - Highlight file preservation

6. **Auto-Reply**: Show multi-language responses
   - Display English template
   - Show Arabic template
   - Highlight professional formatting

7. **Slack Alert**: Show internal notifications
   - Display rich message format
   - Show all RFQ details
   - Highlight actionable information

## Task 2: Quotation Microservice (1.5 minutes)

### API Demonstration (45 seconds)
"Now let's see the Python-based quotation service with FastAPI."

**Show:**
- FastAPI documentation (http://localhost:8000/docs)
- API endpoints and schemas
- Interactive testing interface

### Quotation Generation (45 seconds)
"Let me generate a real quotation using the test data."

**Demo Steps:**
1. **Input**: Show JSON request with client and product data
2. **Processing**: Show pricing calculations
   - Unit cost: 240 SAR
   - Margin: 22%
   - Quantity: 120 units
   - Tax calculation: 15% VAT
3. **Output**: Show complete quotation response
   - Line items with pricing
   - Total calculations
   - Generated email draft
4. **Multi-language**: Show Arabic and English email templates

## Task 3: RAG Knowledge Base (1.5 minutes)

### Document Ingestion (30 seconds)
"Finally, let's see the intelligent knowledge base system."

**Show:**
- Sample documents in the system
- Document processing pipeline
- Vector database setup

### Q&A Demonstration (60 seconds)
"Let me ask some questions about our products and services."

**Demo Questions:**
1. "What products do you offer?" (English)
   - Show product catalog response
   - Display source citations
   - Highlight confidence score

2. "ما هي منتجاتكم؟" (Arabic)
   - Show Arabic response
   - Display bilingual capabilities
   - Show source attribution

3. "What is the warranty period?"
   - Show warranty information
   - Display document sources
   - Highlight relevant sections

4. "How do I install the streetlights?"
   - Show installation guide response
   - Display step-by-step instructions
   - Show technical specifications

## Key Benefits Summary (30 seconds)
"This system provides:
- **No-Code Automation**: Easy setup and maintenance
- **Intelligent Processing**: AI-powered field extraction
- **Multi-language Support**: Arabic and English
- **Complete Integration**: End-to-end workflow
- **Professional Output**: High-quality quotations and responses"

## Technical Highlights (30 seconds)
"Key technical features:
- **Mock Services**: Run locally without external dependencies
- **Error Handling**: Comprehensive error management
- **Scalability**: Production-ready architecture
- **Documentation**: Complete setup and usage guides
- **Testing**: Comprehensive test coverage"

## Conclusion (15 seconds)
"This complete automation system transforms RFQ processing from manual to intelligent, saving time and improving customer experience. All components work together seamlessly to provide a professional, efficient solution."

---

## Video Production Notes

### Screen Recording Setup
- **Resolution**: 1920x1080
- **Frame Rate**: 30fps
- **Audio**: Clear narration
- **Cursor**: Highlighted for visibility

### Key Screenshots to Capture
1. Zapier workflow visual diagram
2. Sample RFQ email
3. Extracted JSON data
4. Google Sheets populated data
5. Salesforce opportunity record
6. Auto-reply email samples
7. Slack notification format
8. FastAPI documentation page
9. Quotation generation process
10. RAG Q&A interface

### Timing Breakdown
- **Introduction**: 30 seconds
- **Task 1 Demo**: 2 minutes
- **Task 2 Demo**: 1.5 minutes
- **Task 3 Demo**: 1.5 minutes
- **Summary**: 30 seconds
- **Technical Notes**: 30 seconds
- **Conclusion**: 15 seconds
- **Total**: 6 minutes 15 seconds

### Voiceover Script
- Speak clearly and at moderate pace
- Emphasize key benefits and features
- Use professional terminology
- Highlight no-code vs. code solutions
- Show real data and results
