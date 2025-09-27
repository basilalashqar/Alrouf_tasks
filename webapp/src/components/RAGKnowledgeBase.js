import React, { useState } from 'react';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import { 
  FiMessageSquare, 
  FiSearch, 
  FiGlobe, 
  FiClock, 
  FiCheckCircle,
  FiCopy,
  FiDownload,
  FiLoader,
  FiBook,
  FiZap
} from 'react-icons/fi';
import axios from 'axios';

const Container = styled.div`
  padding: 2rem 0;
`;

const Header = styled.div`
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
`;

const Subtitle = styled.p`
  font-size: 1.125rem;
  color: #64748b;
  margin: 0;
`;

const SearchContainer = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
`;

const SearchForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const SearchSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const SearchLabel = styled.label`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
`;

const SearchIcon = styled.span`
  margin-right: 0.5rem;
  color: #667eea;
`;

const SearchInput = styled.textarea`
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const LanguageSelector = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const LanguageOption = styled.label`
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.selected ? '#667eea' : 'white'};
  color: ${props => props.selected ? 'white' : '#374151'};

  &:hover {
    border-color: #667eea;
  }
`;

const LanguageInput = styled.input`
  margin-right: 0.5rem;
`;

const SearchButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
`;

const ResultContainer = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-top: 2rem;
`;

const ResultHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
`;

const ResultTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
`;

const ResultActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background: #e2e8f0;
  }
`;

const AnswerSection = styled.div`
  margin-bottom: 2rem;
`;

const AnswerText = styled.div`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 1rem;
  margin-bottom: 1rem;
`;

const ArabicText = styled(AnswerText)`
  direction: rtl;
  text-align: right;
  font-family: 'Inter', 'Arial', 'Tahoma', sans-serif;
`;

const ConfidenceBadge = styled.div`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  background-color: ${props => props.confidence > 80 ? '#dcfce7' : props.confidence > 60 ? '#fef3c7' : '#fee2e2'};
  color: ${props => props.confidence > 80 ? '#166534' : props.confidence > 60 ? '#92400e' : '#991b1b'};
  margin-bottom: 1rem;
`;

const SourcesSection = styled.div`
  margin-top: 2rem;
`;

const SourcesTitle = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
`;

const SourcesList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`;

const SourceItem = styled.li`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border: 1px solid #e2e8f0;
  font-size: 0.875rem;
  color: #64748b;
`;

const PerformanceMetrics = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
`;

const MetricCard = styled.div`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  text-align: center;
`;

const MetricValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
`;

const MetricLabel = styled.div`
  font-size: 0.875rem;
  color: #64748b;
`;

const QuickQueries = styled.div`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid #e2e8f0;
`;

const QuickQueriesTitle = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
`;

const QuickQueryButton = styled.button`
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;

  &:hover {
    border-color: #667eea;
    background: #f8fafc;
  }
`;

const quickQueries = [
  { text: "What products do you offer?", lang: "en" },
  { text: "ما هي منتجاتكم؟", lang: "ar" },
  { text: "What is the warranty period?", lang: "en" },
  { text: "ما هي فترة الضمان؟", lang: "ar" },
  { text: "How do I install the lighting system?", lang: "en" },
  { text: "كيف أقوم بتثبيت النظام؟", lang: "ar" }
];

function RAGKnowledgeBase() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('/rag/query', {
        query: query.trim(),
        language: language
      });
      setResult(response.data);
      toast.success('Query processed successfully!');
    } catch (error) {
      console.error('Error processing query:', error);
      toast.error('Failed to process query. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickQuery = (text, lang) => {
    setQuery(text);
    setLanguage(lang);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const downloadResult = () => {
    const content = `Query: ${query}
Language: ${language}
Confidence: ${result.confidence}%

Answer:
${result.answer}

Sources:
${result.sources.map((source, index) => `${index + 1}. ${source}`).join('\n')}

Performance Metrics:
- Response Time: ${result.response_time}ms
- Processing Time: ${result.processing_time}ms
- Generated at: ${new Date().toISOString()}`;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rag-query-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Container>
      <Header>
        <Title>RAG Knowledge Base</Title>
        <Subtitle>Intelligent Q&A system with multi-language support</Subtitle>
      </Header>

      <SearchContainer>
        <SearchForm onSubmit={handleSubmit}>
          <SearchSection>
            <SearchLabel>
              <SearchIcon><FiMessageSquare /></SearchIcon>
              Ask a Question
            </SearchLabel>
            <SearchInput
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about our products, warranty, installation, or any other topic..."
              required
            />
          </SearchSection>

          <LanguageSelector>
            <LanguageOption selected={language === 'en'}>
              <LanguageInput
                type="radio"
                name="language"
                value="en"
                checked={language === 'en'}
                onChange={(e) => setLanguage(e.target.value)}
              />
              <FiGlobe style={{ marginRight: '0.5rem' }} />
              English
            </LanguageOption>
            <LanguageOption selected={language === 'ar'}>
              <LanguageInput
                type="radio"
                name="language"
                value="ar"
                checked={language === 'ar'}
                onChange={(e) => setLanguage(e.target.value)}
              />
              <FiGlobe style={{ marginRight: '0.5rem' }} />
              العربية
            </LanguageOption>
          </LanguageSelector>

          <SearchButton type="submit" disabled={loading || !query.trim()}>
            {loading ? (
              <>
                <LoadingSpinner />
                Processing...
              </>
            ) : (
              <>
                <FiSearch style={{ marginRight: '0.5rem' }} />
                Search Knowledge Base
              </>
            )}
          </SearchButton>
        </SearchForm>
      </SearchContainer>

      <QuickQueries>
        <QuickQueriesTitle>
          <FiZap style={{ marginRight: '0.5rem' }} />
          Quick Queries
        </QuickQueriesTitle>
        {quickQueries.map((quickQuery, index) => (
          <QuickQueryButton
            key={index}
            onClick={() => handleQuickQuery(quickQuery.text, quickQuery.lang)}
          >
            {quickQuery.text}
          </QuickQueryButton>
        ))}
      </QuickQueries>

      {result && (
        <ResultContainer>
          <ResultHeader>
            <ResultTitle>
              <FiCheckCircle style={{ marginRight: '0.5rem', color: '#10b981' }} />
              Query Results
            </ResultTitle>
            <ResultActions>
              <ActionButton onClick={() => copyToClipboard(result.answer)}>
                <FiCopy />
              </ActionButton>
              <ActionButton onClick={downloadResult}>
                <FiDownload />
              </ActionButton>
            </ResultActions>
          </ResultHeader>

          <AnswerSection>
            <ConfidenceBadge confidence={result.confidence}>
              Confidence: {result.confidence}%
            </ConfidenceBadge>
            
            {language === 'ar' ? (
              <ArabicText>{result.answer}</ArabicText>
            ) : (
              <AnswerText>{result.answer}</AnswerText>
            )}
          </AnswerSection>

          {result.sources && result.sources.length > 0 && (
            <SourcesSection>
              <SourcesTitle>
                <FiBook style={{ marginRight: '0.5rem' }} />
                Sources
              </SourcesTitle>
              <SourcesList>
                {result.sources.map((source, index) => (
                  <SourceItem key={index}>
                    {index + 1}. {source}
                  </SourceItem>
                ))}
              </SourcesList>
            </SourcesSection>
          )}

          <PerformanceMetrics>
            <MetricCard>
              <MetricValue>{result.confidence}%</MetricValue>
              <MetricLabel>Confidence</MetricLabel>
            </MetricCard>
            <MetricCard>
              <MetricValue>{result.response_time}ms</MetricValue>
              <MetricLabel>Response Time</MetricLabel>
            </MetricCard>
            <MetricCard>
              <MetricValue>{result.processing_time}ms</MetricValue>
              <MetricLabel>Processing Time</MetricLabel>
            </MetricCard>
            <MetricCard>
              <MetricValue>{result.sources?.length || 0}</MetricValue>
              <MetricLabel>Sources Found</MetricLabel>
            </MetricCard>
          </PerformanceMetrics>
        </ResultContainer>
      )}
    </Container>
  );
}

export default RAGKnowledgeBase;
