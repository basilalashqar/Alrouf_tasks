import React, { useState } from 'react';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import { 
  FiDollarSign, 
  FiUser, 
  FiPackage, 
  FiMail, 
  FiFileText,
  FiLoader,
  FiCheckCircle,
  FiCopy,
  FiDownload
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

const FormContainer = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
`;

const FormSection = styled.div`
  margin-bottom: 2rem;

  &:last-child {
    margin-bottom: 0;
  }
`;

const SectionTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
`;

const SectionIcon = styled.span`
  margin-right: 0.5rem;
  color: #667eea;
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const ItemsContainer = styled.div`
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  background: #f9fafb;
`;

const ItemRow = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto;
  gap: 1rem;
  align-items: end;
  margin-bottom: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;

  &:last-child {
    margin-bottom: 0;
  }
`;

const RemoveButton = styled.button`
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #dc2626;
  }
`;

const AddButton = styled.button`
  background: #10b981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;

  &:hover {
    background: #059669;
  }
`;

const SubmitButton = styled.button`
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
  width: 100%;
  margin-top: 2rem;

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

const QuotationDetails = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const DetailCard = styled.div`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
`;

const DetailLabel = styled.div`
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
`;

const DetailValue = styled.div`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
`;

const EmailPreview = styled.div`
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  white-space: pre-wrap;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  max-height: 300px;
  overflow-y: auto;
`;

function QuotationService() {
  const [formData, setFormData] = useState({
    client: {
      name: '',
      contact: '',
      lang: 'en'
    },
    currency: 'SAR',
    items: [
      { sku: '', qty: 1, unit_cost: 0, margin_pct: 20 }
    ],
    delivery_terms: '',
    notes: ''
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleClientChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      client: {
        ...prev.client,
        [field]: value
      }
    }));
  };

  const handleItemChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { sku: '', qty: 1, unit_cost: 0, margin_pct: 20 }]
    }));
  };

  const removeItem = (index) => {
    if (formData.items.length > 1) {
      setFormData(prev => ({
        ...prev,
        items: prev.items.filter((_, i) => i !== index)
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('/quote', formData);
      setResult(response.data);
      toast.success('Quotation generated successfully!');
    } catch (error) {
      console.error('Error generating quotation:', error);
      toast.error('Failed to generate quotation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const downloadQuotation = () => {
    const content = `Quotation ID: ${result.quotation_id}
Client: ${result.client.name}
Contact: ${result.client.contact}
Currency: ${result.currency}

Items:
${result.items.map(item => 
  `${item.sku} - Qty: ${item.qty} - Unit Cost: ${item.unit_cost} - Margin: ${item.margin_pct}% - Total: ${item.line_total}`
).join('\n')}

Subtotal: ${result.subtotal}
Tax: ${result.tax_amount}
Total: ${result.total}

Email Draft:
${result.email_draft}`;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `quotation-${result.quotation_id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Container>
      <Header>
        <Title>Quotation Service</Title>
        <Subtitle>Generate intelligent quotations with AI-powered email drafting</Subtitle>
      </Header>

      <FormContainer>
        <form onSubmit={handleSubmit}>
          <FormSection>
            <SectionTitle>
              <SectionIcon><FiUser /></SectionIcon>
              Client Information
            </SectionTitle>
            <FormGrid>
              <FormGroup>
                <Label>Client Name</Label>
                <Input
                  type="text"
                  value={formData.client.name}
                  onChange={(e) => handleClientChange('name', e.target.value)}
                  placeholder="e.g., Gulf Engineering"
                  required
                />
              </FormGroup>
              <FormGroup>
                <Label>Contact Email</Label>
                <Input
                  type="email"
                  value={formData.client.contact}
                  onChange={(e) => handleClientChange('contact', e.target.value)}
                  placeholder="e.g., omar@client.com"
                  required
                />
              </FormGroup>
              <FormGroup>
                <Label>Language</Label>
                <Select
                  value={formData.client.lang}
                  onChange={(e) => handleClientChange('lang', e.target.value)}
                >
                  <option value="en">English</option>
                  <option value="ar">Arabic</option>
                </Select>
              </FormGroup>
              <FormGroup>
                <Label>Currency</Label>
                <Select
                  value={formData.currency}
                  onChange={(e) => handleInputChange('currency', e.target.value)}
                >
                  <option value="SAR">SAR</option>
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                </Select>
              </FormGroup>
            </FormGrid>
          </FormSection>

          <FormSection>
            <SectionTitle>
              <SectionIcon><FiPackage /></SectionIcon>
              Items
            </SectionTitle>
            <ItemsContainer>
              {formData.items.map((item, index) => (
                <ItemRow key={index}>
                  <FormGroup>
                    <Label>SKU</Label>
                    <Input
                      type="text"
                      value={item.sku}
                      onChange={(e) => handleItemChange(index, 'sku', e.target.value)}
                      placeholder="e.g., ALR-SL-90W"
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>Quantity</Label>
                    <Input
                      type="number"
                      value={item.qty}
                      onChange={(e) => handleItemChange(index, 'qty', parseInt(e.target.value))}
                      min="1"
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>Unit Cost</Label>
                    <Input
                      type="number"
                      value={item.unit_cost}
                      onChange={(e) => handleItemChange(index, 'unit_cost', parseFloat(e.target.value))}
                      step="0.01"
                      min="0"
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>Margin %</Label>
                    <Input
                      type="number"
                      value={item.margin_pct}
                      onChange={(e) => handleItemChange(index, 'margin_pct', parseFloat(e.target.value))}
                      step="0.1"
                      min="0"
                      max="100"
                      required
                    />
                  </FormGroup>
                  {formData.items.length > 1 && (
                    <RemoveButton onClick={() => removeItem(index)}>
                      Remove
                    </RemoveButton>
                  )}
                </ItemRow>
              ))}
              <AddButton type="button" onClick={addItem}>
                Add Item
              </AddButton>
            </ItemsContainer>
          </FormSection>

          <FormSection>
            <SectionTitle>
              <SectionIcon><FiFileText /></SectionIcon>
              Additional Information
            </SectionTitle>
            <FormGrid>
              <FormGroup>
                <Label>Delivery Terms</Label>
                <Input
                  type="text"
                  value={formData.delivery_terms}
                  onChange={(e) => handleInputChange('delivery_terms', e.target.value)}
                  placeholder="e.g., DAP Dammam, 4 weeks"
                />
              </FormGroup>
              <FormGroup>
                <Label>Notes</Label>
                <Input
                  type="text"
                  value={formData.notes}
                  onChange={(e) => handleInputChange('notes', e.target.value)}
                  placeholder="e.g., Client requested Tarsheed compliance"
                />
              </FormGroup>
            </FormGrid>
          </FormSection>

          <SubmitButton type="submit" disabled={loading}>
            {loading ? (
              <>
                <LoadingSpinner />
                Generating Quotation...
              </>
            ) : (
              <>
                <FiDollarSign style={{ marginRight: '0.5rem' }} />
                Generate Quotation
              </>
            )}
          </SubmitButton>
        </form>
      </FormContainer>

      {result && (
        <ResultContainer>
          <ResultHeader>
            <ResultTitle>
              <FiCheckCircle style={{ marginRight: '0.5rem', color: '#10b981' }} />
              Quotation Generated Successfully
            </ResultTitle>
            <ResultActions>
              <ActionButton onClick={() => copyToClipboard(result.email_draft)}>
                <FiCopy />
              </ActionButton>
              <ActionButton onClick={downloadQuotation}>
                <FiDownload />
              </ActionButton>
            </ResultActions>
          </ResultHeader>

          <QuotationDetails>
            <DetailCard>
              <DetailLabel>Quotation ID</DetailLabel>
              <DetailValue>{result.quotation_id}</DetailValue>
            </DetailCard>
            <DetailCard>
              <DetailLabel>Subtotal</DetailLabel>
              <DetailValue>{result.currency} {result.subtotal.toFixed(2)}</DetailValue>
            </DetailCard>
            <DetailCard>
              <DetailLabel>Tax Amount</DetailLabel>
              <DetailValue>{result.currency} {result.tax_amount.toFixed(2)}</DetailValue>
            </DetailCard>
            <DetailCard>
              <DetailLabel>Total</DetailLabel>
              <DetailValue>{result.currency} {result.total.toFixed(2)}</DetailValue>
            </DetailCard>
          </QuotationDetails>

          <FormSection>
            <SectionTitle>
              <SectionIcon><FiMail /></SectionIcon>
              Email Draft
            </SectionTitle>
            <EmailPreview>{result.email_draft}</EmailPreview>
          </FormSection>
        </ResultContainer>
      )}
    </Container>
  );
}

export default QuotationService;
