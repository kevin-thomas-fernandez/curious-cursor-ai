import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { TeaNote, Connection } from '../types';
import { useTea } from '../context/TeaContext';

interface ConnectionManagerProps {
  teaNote: TeaNote;
  onClose: () => void;
}

const connectionTypes = [
  { type: 'person', label: '👤 Person', color: 'var(--pastel-pink)' },
  { type: 'workplace', label: '🏢 Workplace', color: 'var(--pastel-blue)' },
  { type: 'location', label: '📍 Location', color: 'var(--pastel-green)' },
  { type: 'language', label: '🗣️ Language', color: 'var(--pastel-yellow)' },
  { type: 'category', label: '🏷️ Category', color: 'var(--pastel-purple)' }
] as const;

export function ConnectionManager({ teaNote, onClose }: ConnectionManagerProps) {
  const { dispatch } = useTea();
  const [newConnection, setNewConnection] = useState({
    type: 'person' as Connection['type'],
    name: ''
  });

  const handleAddConnection = () => {
    if (!newConnection.name.trim()) return;

    const connection: Connection = {
      id: uuidv4(),
      type: newConnection.type,
      name: newConnection.name.trim(),
      color: connectionTypes.find(ct => ct.type === newConnection.type)?.color || 'var(--pastel-lavender)'
    };

    const updatedTeaNote = {
      ...teaNote,
      connections: [...teaNote.connections, connection]
    };

    dispatch({ type: 'UPDATE_TEA_NOTE', payload: updatedTeaNote });
    setNewConnection({ type: 'person', name: '' });
  };

  const handleRemoveConnection = (connectionId: string) => {
    const updatedTeaNote = {
      ...teaNote,
      connections: teaNote.connections.filter(conn => conn.id !== connectionId)
    };

    dispatch({ type: 'UPDATE_TEA_NOTE', payload: updatedTeaNote });
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '24px',
        maxWidth: '500px',
        width: '90%',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 8px 32px var(--shadow-light)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ color: 'var(--text-dark)', fontSize: '18px', fontWeight: '600' }}>
            🔗 Connect This Tea
          </h3>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '24px',
              cursor: 'pointer',
              color: 'var(--text-light)'
            }}
          >
            ×
          </button>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <p style={{ 
            color: 'var(--text-light)', 
            fontSize: '14px', 
            marginBottom: '16px',
            background: 'var(--pastel-mint)',
            padding: '12px',
            borderRadius: '8px'
          }}>
            "{teaNote.content}"
          </p>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ marginBottom: '12px', color: 'var(--text-dark)', fontSize: '14px', fontWeight: '600' }}>
            Add New Connection:
          </h4>
          
          <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
            <select
              value={newConnection.type}
              onChange={(e) => setNewConnection(prev => ({ ...prev, type: e.target.value as Connection['type'] }))}
              style={{
                padding: '8px 12px',
                border: '2px solid var(--pastel-lavender)',
                borderRadius: '8px',
                fontSize: '12px',
                outline: 'none',
                background: 'white'
              }}
            >
              {connectionTypes.map(ct => (
                <option key={ct.type} value={ct.type}>{ct.label}</option>
              ))}
            </select>
            
            <input
              type="text"
              value={newConnection.name}
              onChange={(e) => setNewConnection(prev => ({ ...prev, name: e.target.value }))}
              placeholder="Enter name..."
              style={{
                flex: 1,
                padding: '8px 12px',
                border: '2px solid var(--pastel-lavender)',
                borderRadius: '8px',
                fontSize: '12px',
                outline: 'none',
                background: 'var(--pastel-mint)'
              }}
            />
            
            <button
              onClick={handleAddConnection}
              style={{
                background: 'var(--pastel-purple)',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                padding: '8px 16px',
                fontSize: '12px',
                cursor: 'pointer'
              }}
            >
              Add
            </button>
          </div>
        </div>

        <div>
          <h4 style={{ marginBottom: '12px', color: 'var(--text-dark)', fontSize: '14px', fontWeight: '600' }}>
            Current Connections:
          </h4>
          
          {teaNote.connections.length === 0 ? (
            <p style={{ color: 'var(--text-light)', fontSize: '12px', fontStyle: 'italic' }}>
              No connections yet. Add some to organize your tea!
            </p>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {teaNote.connections.map(connection => (
                <div
                  key={connection.id}
                  style={{
                    background: connection.color,
                    color: 'var(--text-dark)',
                    padding: '6px 12px',
                    borderRadius: '16px',
                    fontSize: '12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  <span>{connectionTypes.find(ct => ct.type === connection.type)?.label.split(' ')[0]}</span>
                  <span>{connection.name}</span>
                  <button
                    onClick={() => handleRemoveConnection(connection.id)}
                    style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '14px',
                      cursor: 'pointer',
                      color: 'var(--text-dark)',
                      padding: '0',
                      marginLeft: '4px'
                    }}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
