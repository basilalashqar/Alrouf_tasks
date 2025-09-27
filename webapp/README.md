# Alrouf Lighting Technology - React Web Application

A modern React web application providing user-friendly interfaces for Task 2 (Quotation Service) and Task 3 (RAG Knowledge Base) of the Alrouf AI automation solutions.

## 🚀 Features

### Task 2: Quotation Service Interface
- **Interactive Form**: Complete quotation generation form with client information, items, and terms
- **Real-time Calculations**: Automatic pricing calculations with margin percentages
- **Multi-language Support**: Arabic and English email generation
- **API Integration**: Direct connection to FastAPI backend service
- **Export Options**: Copy to clipboard and download functionality

### Task 3: RAG Knowledge Base Interface
- **Intelligent Q&A**: Natural language query interface
- **Multi-language Support**: Arabic and English question processing
- **Quick Queries**: Pre-defined common questions for easy access
- **Source Citations**: Display of information sources
- **Performance Metrics**: Response time and confidence scores
- **Export Options**: Copy answers and download results

## 🛠️ Technology Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Styled Components**: CSS-in-JS styling
- **Axios**: HTTP client for API communication
- **React Icons**: Icon library
- **React Toastify**: Toast notifications
- **Responsive Design**: Mobile-first approach

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend services running (Task 2 & Task 3)

### Setup Instructions

1. **Navigate to webapp directory**
   ```bash
   cd webapp
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file
   echo "REACT_APP_API_URL=http://localhost:8000" > .env
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

5. **Open in browser**
   ```
   http://localhost:3000
   ```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000  # Backend API URL
REACT_APP_TIMEOUT=30000                  # Request timeout (ms)

# Feature Flags
REACT_APP_ENABLE_QUOTATION=true         # Enable quotation service
REACT_APP_ENABLE_RAG=true               # Enable RAG knowledge base
REACT_APP_ENABLE_ANALYTICS=false       # Enable analytics
```

### Backend Services Required

#### Task 2: Quotation Service
- **URL**: `http://localhost:8000`
- **Endpoints**:
  - `POST /quote` - Generate quotation
  - `GET /quote/{id}` - Get quotation by ID
  - `GET /quotes` - List all quotations
  - `GET /health` - Health check

#### Task 3: RAG Knowledge Base
- **URL**: `http://localhost:8000`
- **Endpoints**:
  - `POST /rag/query` - Query knowledge base
  - `GET /rag/documents` - List documents
  - `POST /rag/documents` - Add document
  - `GET /rag/stats` - Get statistics
  - `GET /health/rag` - RAG health check

## 🎯 Usage

### Quotation Service
1. **Navigate to Quotation Service** (`/quotation`)
2. **Fill Client Information**:
   - Client name and contact
   - Language preference (English/Arabic)
   - Currency selection
3. **Add Items**:
   - SKU, quantity, unit cost, margin percentage
   - Add/remove items as needed
4. **Add Terms**:
   - Delivery terms and notes
5. **Generate Quotation**:
   - Click "Generate Quotation" button
   - View results with pricing breakdown
   - Copy or download email draft

### RAG Knowledge Base
1. **Navigate to RAG Knowledge Base** (`/rag`)
2. **Ask Questions**:
   - Type your question in the text area
   - Select language (English/Arabic)
   - Use quick query buttons for common questions
3. **View Results**:
   - Read AI-generated answers
   - Check confidence scores
   - Review source citations
   - View performance metrics
4. **Export Results**:
   - Copy answers to clipboard
   - Download results as text file

## 🎨 UI Components

### Layout Components
- **Header**: Application title and navigation
- **Sidebar**: Navigation menu with task links
- **Dashboard**: Overview of all tasks and statistics

### Task 2 Components
- **QuotationForm**: Complete quotation input form
- **ItemManager**: Dynamic item addition/removal
- **ResultDisplay**: Quotation results and email preview
- **ExportTools**: Copy and download functionality

### Task 3 Components
- **QueryInterface**: Question input and language selection
- **QuickQueries**: Pre-defined common questions
- **AnswerDisplay**: AI-generated answers with formatting
- **SourceCitations**: Information source references
- **PerformanceMetrics**: Response time and confidence scores

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop**: Full-featured interface
- **Tablet**: Optimized layout with collapsible sidebar
- **Mobile**: Touch-friendly interface with mobile navigation

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔌 API Integration

### Error Handling
- **Network Errors**: Automatic retry with exponential backoff
- **Server Errors**: User-friendly error messages
- **Timeout Handling**: Configurable request timeouts
- **Offline Support**: Graceful degradation when backend unavailable

### Request/Response Format
```javascript
// Quotation Request
{
  "client": {
    "name": "Gulf Engineering",
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
  "notes": "Client requested Tarsheed compliance"
}

// RAG Query Request
{
  "query": "What products do you offer?",
  "language": "en"
}
```

## 🧪 Testing

### Manual Testing
1. **Start backend services** (Task 2 & Task 3)
2. **Start React app**: `npm start`
3. **Test Quotation Service**:
   - Fill form with sample data
   - Generate quotation
   - Verify results and export
4. **Test RAG Knowledge Base**:
   - Ask questions in English and Arabic
   - Check quick queries
   - Verify source citations

### Automated Testing
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 🚀 Deployment

### Production Build
```bash
# Create production build
npm run build

# Serve build locally
npx serve -s build
```

### Environment Configuration
```bash
# Production environment
REACT_APP_API_URL=https://api.alrouf.com
REACT_APP_TIMEOUT=30000
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY build ./build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
```

## 🔧 Development

### Project Structure
```
webapp/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   ├── Dashboard.js
│   │   ├── QuotationService.js
│   │   └── RAGKnowledgeBase.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

### Available Scripts
- `npm start` - Start development server
- `npm run build` - Create production build
- `npm test` - Run test suite
- `npm run eject` - Eject from Create React App

## 📊 Performance

### Optimization Features
- **Code Splitting**: Lazy loading of components
- **Bundle Optimization**: Tree shaking and minification
- **Caching**: API response caching
- **Compression**: Gzip compression for assets

### Performance Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Check if backend services are running
   - Verify API URL in environment variables
   - Check network connectivity

2. **CORS Errors**
   - Ensure backend has CORS enabled
   - Check API URL configuration

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Debug Commands
```bash
# Check React version
npm list react

# Check for outdated packages
npm outdated

# Clear cache
npm start -- --reset-cache
```

## 📚 Documentation

- [React Documentation](https://reactjs.org/docs)
- [Styled Components](https://styled-components.com/docs)
- [React Router](https://reactrouter.com/docs)
- [Axios Documentation](https://axios-http.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 📞 Support

For support and questions:
- **Email**: basil@alrouf.com
- **GitHub Issues**: [Create an issue](https://github.com/basilalashqar/Alrouf_tasks/issues)
- **Documentation**: [Project Wiki](https://github.com/basilalashqar/Alrouf_tasks/wiki)

---

**Built with ❤️ for Alrouf Lighting Technology**
