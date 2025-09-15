import React from 'react';
import { useTea } from '../context/TeaContext';
import { useAuth } from '../context/AuthContext';

export function UserSwitcher() {
  const { currentUser } = useTea();
  const { state: authState, logout } = useAuth();

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: '12px 16px',
      marginBottom: '20px',
      boxShadow: '0 2px 8px var(--shadow-light)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <div style={{
          width: '12px',
          height: '12px',
          borderRadius: '50%',
          background: currentUser === 'me' ? 'var(--pastel-pink)' : 'var(--pastel-blue)'
        }} />
        <span style={{ 
          fontSize: '14px', 
          fontWeight: '600',
          color: 'var(--text-dark)'
        }}>
          {currentUser === 'me' ? '👩 You' : '👨 Boyfriend'} ({authState.user?.displayName})
        </span>
      </div>
      
      <button
        onClick={logout}
        style={{
          background: 'var(--pastel-lavender)',
          border: 'none',
          borderRadius: '8px',
          padding: '6px 12px',
          fontSize: '12px',
          cursor: 'pointer',
          color: 'var(--text-dark)',
          transition: 'all 0.2s ease'
        }}
        onMouseOver={(e) => e.currentTarget.style.background = 'var(--pastel-purple)'}
        onMouseOut={(e) => e.currentTarget.style.background = 'var(--pastel-lavender)'}
      >
        Logout
      </button>
    </div>
  );
}
