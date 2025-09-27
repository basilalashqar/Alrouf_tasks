import React from 'react';
import styled from 'styled-components';
import { FiMenu, FiSun, FiMoon } from 'react-icons/fi';

const HeaderContainer = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
`;

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;

  &:hover {
    background-color: #f1f5f9;
    color: #334155;
  }

  @media (max-width: 768px) {
    display: block;
  }
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
`;

const Subtitle = styled.p`
  color: #64748b;
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;

  &:hover {
    background-color: #f1f5f9;
    color: #334155;
  }
`;

const HeaderContent = styled.div`
  display: flex;
  flex-direction: column;
`;

const HeaderActions = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

function Header({ onMenuClick }) {
  return (
    <HeaderContainer>
      <HeaderContent>
        <Title>Alrouf Lighting Technology</Title>
        <Subtitle>AI Automation Solutions</Subtitle>
      </HeaderContent>
      <HeaderActions>
        <MenuButton onClick={onMenuClick}>
          <FiMenu />
        </MenuButton>
        <ThemeToggle>
          <FiSun />
        </ThemeToggle>
      </HeaderActions>
    </HeaderContainer>
  );
}

export default Header;
