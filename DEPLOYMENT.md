# 🚀 Deployment Guide - Alrouf Lighting Technology

This guide provides step-by-step instructions for deploying all three tasks in production environments.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.13+
- **Node.js**: 18+ (for frontend components)
- **Docker**: 20.10+ (optional)
- **Git**: 2.30+
- **Memory**: 4GB+ RAM
- **Storage**: 10GB+ free space

### Required Services
- **OpenAI API**: For AI-powered features
- **Zapier Account**: For Task 1 automation
- **Google Services**: Gmail, Sheets, Drive
- **Salesforce**: CRM integration
- **Slack/Teams**: Team notifications

## 🎯 Task 1: RFQ Automation (Zapier)

### Production Setup

1. **Zapier Account Configuration**
   ```bash
   # Visit: https://zapier.com
   # Create business account
   # Enable required services
   ```

2. **Service Connections**
   - **Gmail**: Connect business email
   - **OpenAI**: Add API key
   - **Google Sheets**: Connect to workspace
   - **Salesforce**: Connect CRM instance
   - **Google Drive**: Connect storage
   - **Slack**: Connect team workspace

3. **Workflow Import**
   ```bash
   # Import workflow_blueprint.json
   # Configure trigger conditions
   # Set up action parameters
   ```

4. **Testing & Validation**
   ```bash
   # Send test RFQ email
   # Verify all steps execute
   # Check data accuracy
   ```

### Monitoring
- **Zapier Dashboard**: Monitor execution logs
- **Error Alerts**: Set up notifications
- **Performance Metrics**: Track processing time

## 🎯 Task 2: Quotation Microservice

### Local Development

1. **Environment Setup**
   ```bash
   cd task2_quotation_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

3. **Start Service**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Test API**
   ```bash
   curl -X POST "http://localhost:8000/quote" \
     -H "Content-Type: application/json" \
     -d @tests/test_data.json
   ```

### Docker Deployment

1. **Build Image**
   ```bash
   docker build -t alrouf-quotation-service .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name quotation-service \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your_key_here \
     alrouf-quotation-service
   ```

3. **Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

### Production Deployment

1. **Server Setup**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.13 python3-pip nginx
   
   # Create service user
   sudo useradd -m -s /bin/bash alrouf
   sudo usermod -aG docker alrouf
   ```

2. **Application Deployment**
   ```bash
   # Clone repository
   git clone https://github.com/basilalashqar/Alrouf_tasks.git
   cd Alrouf_tasks/task2_quotation_service
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp env.example .env
   nano .env
   ```

3. **Systemd Service**
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/quotation-service.service
   ```

   ```ini
   [Unit]
   Description=Alrouf Quotation Service
   After=network.target
   
   [Service]
   Type=simple
   User=alrouf
   WorkingDirectory=/home/alrouf/Alrouf_tasks/task2_quotation_service
   Environment=PATH=/home/alrouf/Alrouf_tasks/task2_quotation_service/venv/bin
   ExecStart=/home/alrouf/Alrouf_tasks/task2_quotation_service/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable quotation-service
   sudo systemctl start quotation-service
   sudo systemctl status quotation-service
   ```

5. **Nginx Configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/quotation-service
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/quotation-service /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## 🎯 Task 3: RAG Knowledge Base

### Local Development

1. **Environment Setup**
   ```bash
   cd task3_rag_knowledge
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Initialize System**
   ```bash
   python main.py
   ```

3. **Test Queries**
   ```bash
   python -c "
   from main import RAGKnowledgeBase
   rag = RAGKnowledgeBase()
   result = rag.query('What products do you offer?', 'en')
   print(result['answer'])
   "
   ```

### Production Deployment

1. **Server Setup**
   ```bash
   # Install dependencies
   sudo apt install python3.13 python3-pip
   
   # Create directories
   mkdir -p /opt/alrouf-rag
   cd /opt/alrouf-rag
   ```

2. **Application Deployment**
   ```bash
   # Clone repository
   git clone https://github.com/basilalashqar/Alrouf_tasks.git
   cd Alrouf_tasks/task3_rag_knowledge
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp env.example .env
   nano .env
   ```

3. **Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/rag-service.service
   ```

   ```ini
   [Unit]
   Description=Alrouf RAG Knowledge Base
   After=network.target
   
   [Service]
   Type=simple
   User=alrouf
   WorkingDirectory=/opt/alrouf-rag/task3_rag_knowledge
   Environment=PATH=/opt/alrouf-rag/task3_rag_knowledge/venv/bin
   ExecStart=/opt/alrouf-rag/task3_rag_knowledge/venv/bin/python main.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable rag-service
   sudo systemctl start rag-service
   sudo systemctl status rag-service
   ```

## 🔧 Configuration Management

### Environment Variables

Create `.env` file in each task directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/alrouf_db

# Vector Database
VECTOR_DB_TYPE=faiss
FAISS_INDEX_PATH=./data/faiss_index

# Service Configuration
USE_MOCK_SERVICES=False
MOCK_OPENAI=False
DEFAULT_LANGUAGE=en

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Security Configuration

1. **API Keys**
   ```bash
   # Store in secure location
   echo "OPENAI_API_KEY=your_key_here" >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Firewall Rules**
   ```bash
   # Allow only necessary ports
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable
   ```

3. **SSL Certificates**
   ```bash
   # Install certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Generate certificate
   sudo certbot --nginx -d your-domain.com
   ```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Health Checks**
   ```bash
   # Task 2 (FastAPI)
   curl http://localhost:8000/health
   
   # Task 3 (RAG)
   curl http://localhost:8080/health
   ```

2. **Log Monitoring**
   ```bash
   # View logs
   tail -f logs/app.log
   
   # Monitor system logs
   journalctl -u quotation-service -f
   journalctl -u rag-service -f
   ```

3. **Performance Monitoring**
   ```bash
   # System resources
   htop
   
   # Disk usage
   df -h
   
   # Memory usage
   free -h
   ```

### Alerting

1. **Email Alerts**
   ```bash
   # Configure email notifications
   sudo apt install mailutils
   echo "Service down" | mail -s "Alert" admin@alrouf.com
   ```

2. **Slack Integration**
   ```bash
   # Webhook configuration
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Service alert"}' \
     YOUR_SLACK_WEBHOOK_URL
   ```

## 🔄 Backup & Recovery

### Data Backup

1. **Database Backup**
   ```bash
   # PostgreSQL backup
   pg_dump alrouf_db > backup_$(date +%Y%m%d).sql
   
   # Restore
   psql alrouf_db < backup_20240115.sql
   ```

2. **File Backup**
   ```bash
   # Backup application files
   tar -czf alrouf_backup_$(date +%Y%m%d).tar.gz /opt/alrouf-rag/
   
   # Restore
   tar -xzf alrouf_backup_20240115.tar.gz -C /
   ```

3. **Vector Database Backup**
   ```bash
   # Backup FAISS index
   cp -r data/faiss_index backup/faiss_index_$(date +%Y%m%d)
   
   # Restore
   cp -r backup/faiss_index_20240115 data/faiss_index
   ```

### Disaster Recovery

1. **Recovery Plan**
   - Document all configurations
   - Maintain backup schedules
   - Test recovery procedures
   - Monitor system health

2. **Failover Setup**
   - Configure load balancers
   - Set up redundant servers
   - Implement health checks
   - Automate failover procedures

## 🚀 Scaling

### Horizontal Scaling

1. **Load Balancer**
   ```bash
   # Nginx load balancer
   upstream quotation_services {
       server 127.0.0.1:8000;
       server 127.0.0.1:8001;
       server 127.0.0.1:8002;
   }
   ```

2. **Container Orchestration**
   ```bash
   # Docker Compose
   version: '3.8'
   services:
     quotation-service:
       image: alrouf-quotation-service
       replicas: 3
       ports:
         - "8000-8002:8000"
   ```

### Vertical Scaling

1. **Resource Optimization**
   - Increase server memory
   - Add more CPU cores
   - Optimize database queries
   - Implement caching

2. **Performance Tuning**
   - Configure worker processes
   - Optimize database connections
   - Implement connection pooling
   - Use CDN for static content

## 📞 Support & Maintenance

### Regular Maintenance

1. **System Updates**
   ```bash
   # Update packages
   sudo apt update && sudo apt upgrade
   
   # Update Python packages
   pip install --upgrade -r requirements.txt
   ```

2. **Log Rotation**
   ```bash
   # Configure logrotate
   sudo nano /etc/logrotate.d/alrouf-services
   ```

3. **Health Monitoring**
   ```bash
   # Automated health checks
   crontab -e
   # Add: */5 * * * * curl -f http://localhost:8000/health || echo "Service down"
   ```

### Troubleshooting

1. **Common Issues**
   - Service not starting
   - API not responding
   - Database connection errors
   - Memory issues

2. **Debug Commands**
   ```bash
   # Check service status
   systemctl status quotation-service
   
   # View logs
   journalctl -u quotation-service -n 100
   
   # Test connectivity
   telnet localhost 8000
   ```

---

**For additional support, contact: basil@alrouf.com**
