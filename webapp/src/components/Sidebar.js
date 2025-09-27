import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { 
  FiHome, 
  FiDollarSign, 
  FiMessageSquare, 
  FiSettings,
  FiX,
  FiChevronRight
} from 'react-icons/fi';

const SidebarContainer = styled.aside`
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  z-index: 1000;
  transition: transform 0.3s ease;
  transform: ${props => props.isOpen ? 'translateX(0)' : 'translateX(-100%)'};

  @media (min-width: 769px) {
    transform: translateX(0);
  }
`;

const SidebarHeader = styled.div`
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

const Logo = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
`;

const LogoSubtitle = styled.p`
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0.25rem 0 0 0;
`;

const CloseButton = styled.button`
  display: block;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease;
  margin-left: auto;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  @media (min-width: 769px) {
    display: none;
  }
`;

const Nav = styled.nav`
  padding: 1rem 0;
`;

const NavList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`;

const NavItem = styled.li`
  margin: 0;
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: ${props => props.active ? 'white' : 'rgba(255, 255, 255, 0.8)'};
  text-decoration: none;
  font-weight: ${props => props.active ? '600' : '400'};
  background-color: ${props => props.active ? 'rgba(255, 255, 255, 0.1)' : 'transparent'};
  border-right: ${props => props.active ? '3px solid white' : '3px solid transparent'};
  transition: all 0.2s ease;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
  }
`;

const NavIcon = styled.span`
  margin-right: 0.75rem;
  font-size: 1.25rem;
`;

const NavText = styled.span`
  flex: 1;
`;

const NavArrow = styled.span`
  font-size: 0.875rem;
  opacity: 0.7;
`;

const SidebarFooter = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
`;

const FooterText = styled.p`
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  text-align: center;
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: ${props => props.isOpen ? 'block' : 'none'};

  @media (min-width: 769px) {
    display: none;
  }
`;

const menuItems = [
  { path: '/', icon: FiHome, label: 'Dashboard', description: 'Overview' },
  { path: '/quotation', icon: FiDollarSign, label: 'Quotation Service', description: 'Task 2' },
  { path: '/rag', icon: FiMessageSquare, label: 'RAG Knowledge Base', description: 'Task 3' },
];

function Sidebar({ isOpen, onToggle }) {
  const location = useLocation();

  return (
    <>
      <Overlay isOpen={isOpen} onClick={onToggle} />
      <SidebarContainer isOpen={isOpen}>
        <SidebarHeader>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <Logo>Alrouf AI</Logo>
              <LogoSubtitle>Lighting Technology</LogoSubtitle>
            </div>
            <CloseButton onClick={onToggle}>
              <FiX />
            </CloseButton>
          </div>
        </SidebarHeader>
        
        <Nav>
          <NavList>
            {menuItems.map((item) => (
              <NavItem key={item.path}>
                <NavLink 
                  to={item.path} 
                  active={location.pathname === item.path ? 1 : 0}
                >
                  <NavIcon>
                    <item.icon />
                  </NavIcon>
                  <NavText>{item.label}</NavText>
                  <NavArrow>
                    <FiChevronRight />
                  </NavArrow>
                </NavLink>
              </NavItem>
            ))}
          </NavList>
        </Nav>

        <SidebarFooter>
          <FooterText>
            © 2024 Alrouf Lighting Technology
          </FooterText>
        </SidebarFooter>
      </SidebarContainer>
    </>
  );
}

export default Sidebar;
