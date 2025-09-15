import { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { TeaProvider, useTea } from './context/TeaContext';
import { TeaNoteForm } from './components/TeaNoteForm';
import { TeaMessage } from './components/TeaMessage';
import { ConnectionManager } from './components/ConnectionManager';
import { WeeklyQuizComponent } from './components/WeeklyQuiz';
import { UserSwitcher } from './components/UserSwitcher';
import { Login } from './components/Login';
import { TeaNote } from './types';

function App() {
  return (
    <AuthProvider>
      <TeaProvider>
        <AppContent />
      </TeaProvider>
    </AuthProvider>
  );
}

function AppContent() {
  const { state: authState, login } = useAuth();
  const [showConnectionManager, setShowConnectionManager] = useState(false);
  const [selectedTeaNote, setSelectedTeaNote] = useState<TeaNote | null>(null);
  const [activeTab, setActiveTab] = useState<'chat' | 'quiz'>('chat');

  const openConnectionManager = (teaNote: TeaNote) => {
    setSelectedTeaNote(teaNote);
    setShowConnectionManager(true);
  };

  const closeConnectionManager = () => {
    setShowConnectionManager(false);
    setSelectedTeaNote(null);
  };

  // Show loading screen while checking authentication
  if (authState.isLoading) {
    return (
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '40px',
          textAlign: 'center',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
        }}>
          <h1 style={{
            color: 'var(--pastel-purple)',
            fontSize: '32px',
            marginBottom: '16px'
          }}>
            ☕ Tea Time
          </h1>
          <p style={{
            color: 'var(--text-light)',
            fontSize: '16px'
          }}>
            Loading...
          </p>
        </div>
      </div>
    );
  }

  // Show login screen if not authenticated
  if (!authState.isAuthenticated) {
    return <Login onLogin={login} />;
  }

  // Show main app if authenticated
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      padding: '20px'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        background: 'white',
        borderRadius: '20px',
        boxShadow: '0 8px 32px var(--shadow-light)',
        overflow: 'hidden'
      }}>
        {/* Header */}
        <div style={{
          background: 'linear-gradient(135deg, var(--pastel-purple) 0%, var(--pastel-pink) 100%)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <h1 style={{
            color: 'white',
            fontSize: '28px',
            fontWeight: 'bold',
            marginBottom: '8px',
            textShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            ☕ Tea Time
          </h1>
          <p style={{
            color: 'rgba(255,255,255,0.9)',
            fontSize: '16px',
            fontWeight: '500'
          }}>
            Share your daily tea and stay connected
          </p>
        </div>

        {/* Tab Navigation */}
        <div style={{
          display: 'flex',
          background: 'var(--pastel-lavender)',
          borderBottom: '1px solid var(--pastel-purple)'
        }}>
          <button
            onClick={() => setActiveTab('chat')}
            style={{
              flex: 1,
              padding: '12px',
              border: 'none',
              background: activeTab === 'chat' ? 'white' : 'transparent',
              color: activeTab === 'chat' ? 'var(--text-dark)' : 'var(--text-light)',
              fontSize: '14px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setActiveTab('quiz')}
            style={{
              flex: 1,
              padding: '12px',
              border: 'none',
              background: activeTab === 'quiz' ? 'white' : 'transparent',
              color: activeTab === 'quiz' ? 'var(--text-dark)' : 'var(--text-light)',
              fontSize: '14px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            🧠 Quiz
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '20px' }}>
          {activeTab === 'chat' ? (
            <ChatTab 
              onOpenConnectionManager={openConnectionManager}
            />
          ) : (
            <WeeklyQuizComponent />
          )}
        </div>
      </div>

      {/* Connection Manager Modal */}
      {showConnectionManager && selectedTeaNote && (
        <ConnectionManager
          teaNote={selectedTeaNote}
          onClose={closeConnectionManager}
        />
      )}
    </div>
  );
}

function ChatTab({ onOpenConnectionManager }: { onOpenConnectionManager: (teaNote: TeaNote) => void }) {
  const { state } = useTea();

  // Sort tea notes by timestamp (newest first)
  const sortedTeaNotes = [...state.teaNotes].sort((a, b) => 
    b.timestamp.getTime() - a.timestamp.getTime()
  );

  return (
    <div>
      <UserSwitcher />
      <TeaNoteForm />
      
      <div style={{
        background: 'var(--pastel-mint)',
        borderRadius: '12px',
        padding: '16px',
        marginBottom: '20px'
      }}>
        <h3 style={{ 
          color: 'var(--text-dark)', 
          marginBottom: '12px',
          fontSize: '16px',
          fontWeight: '600'
        }}>
          💬 Tea Messages
        </h3>
        
        {sortedTeaNotes.length === 0 ? (
          <p style={{ 
            color: 'var(--text-light)', 
            fontSize: '14px',
            textAlign: 'center',
            padding: '20px'
          }}>
            No tea shared yet! Start the conversation! ☕
          </p>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            maxHeight: '400px',
            overflowY: 'auto',
            padding: '8px'
          }}>
            {sortedTeaNotes.map(teaNote => (
              <div key={teaNote.id} style={{ position: 'relative' }}>
                <TeaMessage teaNote={teaNote} />
                {teaNote.isCompleted && (
                  <button
                    onClick={() => onOpenConnectionManager(teaNote)}
                    style={{
                      position: 'absolute',
                      top: '8px',
                      right: '8px',
                      background: 'var(--pastel-green)',
                      border: 'none',
                      borderRadius: '6px',
                      padding: '4px 8px',
                      fontSize: '10px',
                      cursor: 'pointer',
                      color: 'var(--text-dark)',
                      fontWeight: '600'
                    }}
                  >
                    🔗 Connect
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
