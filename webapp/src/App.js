import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import styled from 'styled-components';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import QuotationService from './components/QuotationService';
import RAGKnowledgeBase from './components/RAGKnowledgeBase';

const AppContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
`;

const MainContent = styled.main`
  flex: 1;
  margin-left: 250px;
  padding: 2rem;
  transition: margin-left 0.3s ease;

  @media (max-width: 768px) {
    margin-left: 0;
    padding: 1rem;
  }
`;

const ContentWrapper = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <Router>
      <AppContainer>
        <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
        <MainContent>
          <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
          <ContentWrapper>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/quotation" element={<QuotationService />} />
              <Route path="/rag" element={<RAGKnowledgeBase />} />
            </Routes>
          </ContentWrapper>
        </MainContent>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </AppContainer>
    </Router>
  );
}

export default App;
