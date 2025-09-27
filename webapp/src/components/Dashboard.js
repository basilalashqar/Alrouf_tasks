import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { 
  FiDollarSign, 
  FiMessageSquare, 
  FiZap, 
  FiTrendingUp,
  FiUsers,
  FiClock,
  FiCheckCircle
} from 'react-icons/fi';

const DashboardContainer = styled.div`
  padding: 2rem 0;
`;

const WelcomeSection = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  border-radius: 1rem;
  margin-bottom: 3rem;
  text-align: center;
`;

const WelcomeTitle = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
`;

const WelcomeSubtitle = styled.p`
  font-size: 1.25rem;
  margin: 0;
  opacity: 0.9;
`;

const TasksGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const TaskCard = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
  }
`;

const TaskHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const TaskIcon = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  background: ${props => props.bgColor};
  color: white;
  font-size: 1.5rem;
`;

const TaskInfo = styled.div`
  flex: 1;
`;

const TaskTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #1e293b;
`;

const TaskSubtitle = styled.p`
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
`;

const TaskDescription = styled.p`
  color: #64748b;
  margin-bottom: 1.5rem;
  line-height: 1.6;
`;

const TaskFeatures = styled.ul`
  list-style: none;
  margin: 0 0 1.5rem 0;
  padding: 0;
`;

const TaskFeature = styled.li`
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
`;

const FeatureIcon = styled.span`
  color: #10b981;
  margin-right: 0.5rem;
  font-size: 1rem;
`;

const TaskButton = styled(Link)`
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
`;

const StatIcon = styled.div`
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  background: ${props => props.bgColor};
  color: white;
  font-size: 1.25rem;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: #dcfce7;
  color: #166534;
  margin-left: auto;
`;

function Dashboard() {
  return (
    <DashboardContainer>
      <WelcomeSection>
        <WelcomeTitle>Welcome to Alrouf AI</WelcomeTitle>
        <WelcomeSubtitle>
          Advanced AI automation solutions for lighting technology
        </WelcomeSubtitle>
      </WelcomeSection>

      <TasksGrid>
        <TaskCard>
          <TaskHeader>
            <TaskIcon bgColor="linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">
              <FiZap />
            </TaskIcon>
            <TaskInfo>
              <TaskTitle>Task 1: RFQ Automation</TaskTitle>
              <TaskSubtitle>No-Code Zapier Solution</TaskSubtitle>
            </TaskInfo>
            <StatusBadge>Completed</StatusBadge>
          </TaskHeader>
          <TaskDescription>
            Automated RFQ processing pipeline using Zapier workflows. 
            Captures emails, extracts data, creates CRM opportunities, 
            and sends auto-replies in Arabic and English.
          </TaskDescription>
          <TaskFeatures>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Gmail email trigger
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              AI field extraction
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Google Sheets integration
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Salesforce CRM
            </TaskFeature>
          </TaskFeatures>
          <TaskButton to="/quotation">
            View Documentation
          </TaskButton>
        </TaskCard>

        <TaskCard>
          <TaskHeader>
            <TaskIcon bgColor="linear-gradient(135deg, #10b981 0%, #059669 100%)">
              <FiDollarSign />
            </TaskIcon>
            <TaskInfo>
              <TaskTitle>Task 2: Quotation Service</TaskTitle>
              <TaskSubtitle>FastAPI Microservice</TaskSubtitle>
            </TaskInfo>
            <StatusBadge>Ready</StatusBadge>
          </TaskHeader>
          <TaskDescription>
            Intelligent quotation generation with AI-powered email drafting. 
            Supports multi-language responses and automated pricing calculations 
            with comprehensive API documentation.
          </TaskDescription>
          <TaskFeatures>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              FastAPI framework
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              AI email generation
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Multi-language support
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Docker deployment
            </TaskFeature>
          </TaskFeatures>
          <TaskButton to="/quotation">
            Use Quotation Service
          </TaskButton>
        </TaskCard>

        <TaskCard>
          <TaskHeader>
            <TaskIcon bgColor="linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)">
              <FiMessageSquare />
            </TaskIcon>
            <TaskInfo>
              <TaskTitle>Task 3: RAG Knowledge Base</TaskTitle>
              <TaskSubtitle>AI Q&A System</TaskSubtitle>
            </TaskInfo>
            <StatusBadge>Ready</StatusBadge>
          </TaskHeader>
          <TaskDescription>
            Intelligent knowledge base with document processing, vector search, 
            and multi-language Q&A capabilities. Supports Arabic and English 
            queries with source citations.
          </TaskDescription>
          <TaskFeatures>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Document processing
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Vector search
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Multi-language Q&A
            </TaskFeature>
            <TaskFeature>
              <FeatureIcon>✓</FeatureIcon>
              Source citations
            </TaskFeature>
          </TaskFeatures>
          <TaskButton to="/rag">
            Use Knowledge Base
          </TaskButton>
        </TaskCard>
      </TasksGrid>

      <StatsGrid>
        <StatCard>
          <StatHeader>
            <StatIcon bgColor="linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)">
              <FiTrendingUp />
            </StatIcon>
            <div>
              <StatValue>95%</StatValue>
              <StatLabel>Accuracy Rate</StatLabel>
            </div>
          </StatHeader>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon bgColor="linear-gradient(135deg, #10b981 0%, #059669 100%)">
              <FiClock />
            </StatIcon>
            <div>
              <StatValue>&lt;1s</StatValue>
              <StatLabel>Response Time</StatLabel>
            </div>
          </StatHeader>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon bgColor="linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">
              <FiUsers />
            </StatIcon>
            <div>
              <StatValue>3</StatValue>
              <StatLabel>AI Solutions</StatLabel>
            </div>
          </StatHeader>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatIcon bgColor="linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)">
              <FiCheckCircle />
            </StatIcon>
            <div>
              <StatValue>100%</StatValue>
              <StatLabel>Success Rate</StatLabel>
            </div>
          </StatHeader>
        </StatCard>
      </StatsGrid>
    </DashboardContainer>
  );
}

export default Dashboard;
