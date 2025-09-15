import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { TeaNote, TeaEmoji, FollowUpQuestion } from '../types';
import { useTea } from '../context/TeaContext';
import { EmojiSelector } from './EmojiSelector';

export function TeaNoteForm() {
  const { state, dispatch, currentUser } = useTea();
  const [content, setContent] = useState('');
  const [selectedEmoji, setSelectedEmoji] = useState<TeaEmoji>('heart');
  const [reminderTime, setReminderTime] = useState('');

  const generateFollowUpQuestions = (): FollowUpQuestion[] => {
    const questions: FollowUpQuestion[] = [
      { id: uuidv4(), question: 'What exactly happened?', type: 'what' },
      { id: uuidv4(), question: 'Who was involved?', type: 'who' },
      { id: uuidv4(), question: 'Where did this take place?', type: 'where' },
      { id: uuidv4(), question: 'How did it make you feel?', type: 'how' },
      { id: uuidv4(), question: 'When did this happen?', type: 'when' }
    ];
    return questions;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    const newTeaNote: TeaNote = {
      id: uuidv4(),
      content: content.trim(),
      timestamp: new Date(),
      reminderTime: reminderTime ? new Date(reminderTime) : undefined,
      followUpQuestions: generateFollowUpQuestions(),
      connections: [],
      emoji: selectedEmoji,
      isCompleted: false,
      author: currentUser
    };

    dispatch({ type: 'ADD_TEA_NOTE', payload: newTeaNote });
    setContent('');
    setReminderTime('');
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '16px',
      padding: '20px',
      marginBottom: '20px',
      boxShadow: '0 4px 12px var(--shadow-light)'
    }}>
      <h3 style={{ 
        color: 'var(--text-dark)', 
        marginBottom: '16px',
        fontSize: '18px',
        fontWeight: '600'
      }}>
        ☕ Share Your Tea
      </h3>
      
      <form onSubmit={handleSubmit}>
        <EmojiSelector 
          selectedEmoji={selectedEmoji} 
          onEmojiSelect={setSelectedEmoji} 
        />
        
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="What's the tea? Spill it! ☕"
          style={{
            width: '100%',
            minHeight: '80px',
            padding: '12px',
            border: '2px solid var(--pastel-lavender)',
            borderRadius: '12px',
            fontSize: '14px',
            fontFamily: 'inherit',
            resize: 'vertical',
            outline: 'none',
            transition: 'border-color 0.2s ease',
            background: 'var(--pastel-mint)'
          }}
          onFocus={(e) => e.target.style.borderColor = 'var(--pastel-purple)'}
          onBlur={(e) => e.target.style.borderColor = 'var(--pastel-lavender)'}
        />
        
        <div style={{ marginTop: '12px' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '8px', 
            fontSize: '14px',
            color: 'var(--text-dark)',
            fontWeight: '500'
          }}>
            ⏰ Remind to talk about this at:
          </label>
          <input
            type="datetime-local"
            value={reminderTime}
            onChange={(e) => setReminderTime(e.target.value)}
            style={{
              padding: '8px 12px',
              border: '2px solid var(--pastel-lavender)',
              borderRadius: '8px',
              fontSize: '14px',
              outline: 'none',
              background: 'white'
            }}
          />
        </div>
        
        <button
          type="submit"
          style={{
            background: 'var(--pastel-purple)',
            color: 'white',
            border: 'none',
            borderRadius: '12px',
            padding: '12px 24px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            marginTop: '16px',
            transition: 'all 0.2s ease',
            width: '100%'
          }}
          onMouseOver={(e) => e.currentTarget.style.background = '#9999ff'}
          onMouseOut={(e) => e.currentTarget.style.background = 'var(--pastel-purple)'}
        >
          Share Tea ☕
        </button>
      </form>
    </div>
  );
}
