import React, { useState } from 'react';
import { User } from '../types';

interface LoginProps {
  onLogin: (user: User) => void;
}

// Users loaded from environment variables with fallbacks
const USERS: User[] = [
  {
    id: '1',
    username: import.meta.env.VITE_USER1_USERNAME || 'diana',
    displayName: import.meta.env.VITE_USER1_DISPLAYNAME || 'Diana',
    role: (import.meta.env.VITE_USER1_ROLE as 'gf' | 'bf') || 'gf'
  },
  {
    id: '2',
    username: import.meta.env.VITE_USER2_USERNAME || 'KTF',
    displayName: import.meta.env.VITE_USER2_DISPLAYNAME || 'KTF',
    role: (import.meta.env.VITE_USER2_ROLE as 'gf' | 'bf') || 'bf'
  }
];

// Passwords loaded from environment variables with fallbacks
const PASSWORDS: Record<string, string> = {
  [import.meta.env.VITE_USER1_USERNAME || 'diana']: import.meta.env.VITE_USER1_PASSWORD || 'FlamingoTea',
  [import.meta.env.VITE_USER2_USERNAME || 'KTF']: import.meta.env.VITE_USER2_PASSWORD || 'BullTea'
};

export function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500));

    const user = USERS.find(u => u.username === username);
    
    if (!user) {
      setError('User not found');
      setIsLoading(false);
      return;
    }

    if (PASSWORDS[username] !== password) {
      setError('Invalid password');
      setIsLoading(false);
      return;
    }

    setIsLoading(false);
    onLogin(user);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '20px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        padding: '40px',
        width: '100%',
        maxWidth: '400px'
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: '30px'
        }}>
          <h1 style={{
            color: 'var(--pastel-purple)',
            fontSize: '32px',
            fontWeight: 'bold',
            marginBottom: '8px'
          }}>
            ☕ Tea Time
          </h1>
          <p style={{
            color: 'var(--text-light)',
            fontSize: '16px'
          }}>
            Sign in to share your tea
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              color: 'var(--text-dark)',
              fontSize: '14px',
              fontWeight: '600'
            }}>
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              style={{
                width: '100%',
                padding: '12px 16px',
                border: '2px solid var(--pastel-lavender)',
                borderRadius: '12px',
                fontSize: '14px',
                outline: 'none',
                transition: 'border-color 0.2s ease',
                background: 'var(--pastel-mint)'
              }}
              onFocus={(e) => e.target.style.borderColor = 'var(--pastel-purple)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--pastel-lavender)'}
              required
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              color: 'var(--text-dark)',
              fontSize: '14px',
              fontWeight: '600'
            }}>
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              style={{
                width: '100%',
                padding: '12px 16px',
                border: '2px solid var(--pastel-lavender)',
                borderRadius: '12px',
                fontSize: '14px',
                outline: 'none',
                transition: 'border-color 0.2s ease',
                background: 'var(--pastel-mint)'
              }}
              onFocus={(e) => e.target.style.borderColor = 'var(--pastel-purple)'}
              onBlur={(e) => e.target.style.borderColor = 'var(--pastel-lavender)'}
              required
            />
          </div>

          {error && (
            <div style={{
              background: '#ffebee',
              color: '#c62828',
              padding: '12px',
              borderRadius: '8px',
              marginBottom: '20px',
              fontSize: '14px',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            style={{
              width: '100%',
              background: isLoading ? '#ccc' : 'var(--pastel-purple)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              padding: '14px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s ease'
            }}
            onMouseOver={(e) => {
              if (!isLoading) {
                e.currentTarget.style.background = '#9999ff';
              }
            }}
            onMouseOut={(e) => {
              if (!isLoading) {
                e.currentTarget.style.background = 'var(--pastel-purple)';
              }
            }}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div style={{
          marginTop: '30px',
          padding: '20px',
          background: 'var(--pastel-lavender)',
          borderRadius: '12px',
          fontSize: '12px',
          color: 'var(--text-light)'
        }}>
        </div>
      </div>
    </div>
  );
}
