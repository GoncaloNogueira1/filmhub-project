import { render, screen, act } from '@testing-library/react';
import { AuthProvider } from './AuthProvider';
import AuthContext from './AuthProvider';
import { useContext, useEffect } from 'react';

// Configuration helper component to consume context
const TestComponent = ({ updateAuth }) => {
  const { auth, setAuth } = useContext(AuthContext);
  
  useEffect(() => {
    if (updateAuth) {
      setAuth(updateAuth);
    }
  }, [updateAuth, setAuth]);

  return (
    <div>
      <span data-testid="auth-user">{auth.user ? auth.user.username : 'No User'}</span>
      <span data-testid="auth-token">{auth.token ? 'Has Token' : 'No Token'}</span>
    </div>
  );
};

describe('AuthProvider', () => {
  it('provides default empty auth state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('auth-user')).toHaveTextContent('No User');
    expect(screen.getByTestId('auth-token')).toHaveTextContent('No Token');
  });

  it('allows updating auth state', () => {
    const user = { username: 'testuser' };
    const token = '12345';
    
    // We can't easily trigger the update from outside without a helper that does it on mount or button click
    // But since we are testing the Provider, we mainly want to ensure children can access and set state.
    // The TestComponent useEffect approach is tricky because of render cycles.
    
    // Better approach: Component with button to trigger update
    const InteractiveComponent = () => {
        const { auth, setAuth } = useContext(AuthContext);
        return (
            <div>
                <span data-testid="username">{auth.username}</span>
                <button onClick={() => setAuth({ username: 'updated' })}>Update</button>
            </div>
        );
    };

    render(
        <AuthProvider>
            <InteractiveComponent />
        </AuthProvider>
    );

    const button = screen.getByText('Update');
    act(() => {
        button.click();
    });

    expect(screen.getByTestId('username')).toHaveTextContent('updated');
  });
});
