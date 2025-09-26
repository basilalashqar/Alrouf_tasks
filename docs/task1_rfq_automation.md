# Task 1: RFQ → CRM Automation

## Overview
This task implements a comprehensive RFQ (Request for Quotation) automation system that captures incoming emails, extracts relevant fields, integrates with Google Sheets and Salesforce, archives attachments, sends auto-replies, and posts internal alerts.

## Features

### Email Processing
- **Email Parsing**: Extracts subject, body, sender, and attachments
- **Field Extraction**: Uses OpenAI to extract structured data from emails
- **Language Detection**: Automatically detects Arabic/English content
- **RFQ Detection**: Identifies RFQ emails using keyword matching

### Data Extraction
- Client name and contact information
- Product model and quantity
- Delivery location and timeline
- Language preference
- Attachment information

### Integrations

#### Google Sheets
- **Automatic Data Entry**: Writes RFQ data to Google Sheets
- **Structured Format**: Organized columns for easy tracking
- **Real-time Updates**: Immediate data synchronization

#### Salesforce CRM
- **Opportunity Creation**: Automatically creates opportunities
- **Account Management**: Creates or finds existing accounts
- **Contact Management**: Links contacts to opportunities
- **Mock Implementation**: Full mock system for testing

#### Google Drive
- **Attachment Archiving**: Stores attachments in organized folders
- **Client Organization**: Separate folders per client
- **File Management**: Maintains file structure and metadata

### Auto-Reply System
- **Multi-language Support**: Arabic and English responses
- **Professional Templates**: Pre-written response templates
- **OpenAI Integration**: Dynamic email generation
- **Customization**: Client-specific information inclusion

### Internal Alerts
- **Slack Integration**: Sends alerts to Slack channels
- **Teams Integration**: Microsoft Teams notifications
- **Rich Formatting**: Structured messages with all details
- **Real-time Notifications**: Immediate team awareness

## Architecture

```
Email Input → Field Extraction → Data Processing → Multiple Integrations
     ↓              ↓                ↓                    ↓
  Email Parser → OpenAI API → Google Sheets → Salesforce
     ↓              ↓                ↓                    ↓
  Attachments → Auto-Reply → Google Drive → Slack/Teams
```

## Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo

# Google Services
GOOGLE_SHEETS_ID=your_sheets_id
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Salesforce
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token

# Email
SMTP_SERVER=smtp.gmail.com
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_password

# Notifications
SLACK_WEBHOOK_URL=your_webhook_url
TEAMS_WEBHOOK_URL=your_webhook_url
```

### Mock Services
The system includes comprehensive mock services for local development:
- Mock Google Sheets operations
- Mock Salesforce CRM
- Mock email sending
- Mock Slack/Teams notifications

## Usage

### Running the System
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your credentials

# Run the automation
python task1_rfq_automation/main.py
```

### Test Scenario
The system includes a test scenario with the provided example email:
```
Subject: RFQ — Streetlight Poles
Body: Hello Alrouf, please quote 120 pcs streetlight model ALR‑SL‑90W. 
Needed in Dammam within 4 weeks. Attach specs. 
Regards, Eng. Omar, +9665XXXX, omar@client.com
```

## Deliverables

### Scenario Blueprint
- Complete workflow documentation
- Integration architecture diagrams
- Error handling procedures

### Sample Data
- **Google Sheets**: Sample RFQ data with all fields
- **Google Drive**: Organized folder structure with attachments
- **Salesforce**: Mock opportunity records with full details
- **Auto-reply**: Sample emails in Arabic and English

### Mock Services
- **CRM Mock**: JSON logs of all Salesforce operations
- **Email Mock**: Sample auto-reply emails
- **Error Logs**: Comprehensive error tracking and logging

## Error Handling

### Robust Error Management
- **Graceful Degradation**: System continues with partial failures
- **Comprehensive Logging**: Detailed error logs for debugging
- **Retry Mechanisms**: Automatic retry for transient failures
- **Fallback Options**: Mock services when real services fail

### Monitoring
- **Real-time Logs**: Live monitoring of all operations
- **Error Alerts**: Immediate notification of critical errors
- **Performance Metrics**: Processing time and success rates
- **Audit Trails**: Complete history of all operations

## Security

### Data Protection
- **Environment Variables**: All secrets stored securely
- **No Hardcoded Credentials**: All sensitive data externalized
- **Mock Services**: Safe testing without real credentials
- **Audit Logging**: Complete operation tracking

## Testing

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Mock Testing**: Safe testing with mock services
- **Error Testing**: Failure scenario validation

### Test Data
- **Sample Emails**: Various RFQ email formats
- **Mock Responses**: Simulated service responses
- **Error Scenarios**: Network failures, API errors
- **Performance Tests**: Load and stress testing

## Maintenance

### Regular Tasks
- **Log Monitoring**: Daily log review
- **Error Analysis**: Weekly error pattern analysis
- **Performance Review**: Monthly performance assessment
- **Update Management**: Regular dependency updates

### Troubleshooting
- **Common Issues**: Documented solutions for frequent problems
- **Debug Procedures**: Step-by-step debugging guides
- **Recovery Procedures**: System recovery from failures
- **Support Contacts**: Technical support information
