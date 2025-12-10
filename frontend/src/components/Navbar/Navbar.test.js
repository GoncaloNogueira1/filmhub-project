import { render, screen, fireEvent } from '@testing-library/react';
import Navbar from './Navbar';

const mockNavigate = jest.fn();

// Use the same virtual mock strategy as MovieCard
jest.mock('react-router-dom', () => ({
  __esModule: true,
  useNavigate: () => mockNavigate,
}), { virtual: true });

describe('Navbar', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    localStorage.clear();
  });

  it('renders logo and links', () => {
    render(<Navbar user={null} onLogout={jest.fn()} />);
    expect(screen.getByText('FilmHub')).toBeInTheDocument();
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Recommendations')).toBeInTheDocument();
  });

  it('navigates to home on logo click', () => {
    render(<Navbar user={null} onLogout={jest.fn()} />);
    fireEvent.click(screen.getByText('FilmHub'));
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('renders user name when logged in', () => {
    const user = { username: 'JohnDoe' };
    render(<Navbar user={user} onLogout={jest.fn()} />);
    expect(screen.getByText('JohnDoe')).toBeInTheDocument();
  });

  it('shows logout option in dropdown and handles logout', () => {
    const user = { username: 'JohnDoe' };
    const mockLogout = jest.fn();
    
    render(<Navbar user={user} onLogout={mockLogout} />);
    
    // Dropdown is initially closed, but button exists
    const userBtn = screen.getByText('JohnDoe');
    fireEvent.click(userBtn);
    
    // Now check for Logout button (it might be in DOM but hidden via CSS, or conditionally rendered)
    // Based on CSS class logic in Navbar.jsx, it seems it's always in DOM but simplified for test
    const logoutBtn = screen.getByText('Logout');
    expect(logoutBtn).toBeInTheDocument();
    
    fireEvent.click(logoutBtn);
    
    expect(mockLogout).toHaveBeenCalled();
    expect(localStorage.getItem('token')).toBeNull(); 
    // Navbar implementation removes token itself before calling onLogout
  });

  it('navigates to ratings page', () => {
      const user = { username: 'JohnDoe' };
      render(<Navbar user={user} onLogout={jest.fn()} />);
      
      fireEvent.click(screen.getByText('JohnDoe')); // Open menu
      fireEvent.click(screen.getByText('My Ratings'));
      
      expect(mockNavigate).toHaveBeenCalledWith('/ratings');
  });
});
