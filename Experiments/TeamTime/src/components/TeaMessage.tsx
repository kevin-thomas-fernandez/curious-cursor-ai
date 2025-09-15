import React, { useState } from 'react';
import { format } from 'date-fns';
import { TeaNote, FollowUpQuestion } from '../types';
import { useTea } from '../context/TeaContext';

interface TeaMessageProps {
  teaNote: TeaNote;
}

const emojiMap: Record<string, string> = {
  angry: '😠',
  star: '⭐',
  heart: '❤️',
  laugh: '😂',
  shock: '😱'
};

const emojiColors: Record<string, string> = {
  angry: 'var(--pastel-pink)',
  star: 'var(--pastel-yellow)',
  heart: 'var(--pastel-pink)',
  laugh: 'var(--pastel-yellow)',
  shock: 'var(--pastel-purple)'
};

export function TeaMessage({ teaNote }: TeaMessageProps) {
  const { dispatch } = useTea();
  const [showFollowUps, setShowFollowUps] = useState(false);
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const handleAnswerChange = (questionId: string, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const saveAnswers = () => {
    const updatedQuestions = teaNote.followUpQuestions.map(q => ({
      ...q,
      answer: answers[q.id] || q.answer
    }));

    const updatedTeaNote = {
      ...teaNote,
      followUpQuestions: updatedQuestions,
      isCompleted: true
    };

    dispatch({ type: 'UPDATE_TEA_NOTE', payload: updatedTeaNote });
    setShowFollowUps(false);
  };

  const isMyMessage = teaNote.author === 'me';
  const messageStyle = {
    alignSelf: isMyMessage ? 'flex-end' : 'flex-start',
    maxWidth: '70%',
    marginBottom: '12px'
  };

  const bubbleStyle = {
    background: isMyMessage ? 'var(--pastel-purple)' : 'white',
    color: isMyMessage ? 'white' : 'var(--text-dark)',
    padding: '12px 16px',
    borderRadius: isMyMessage ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
    boxShadow: '0 2px 8px var(--shadow-light)',
    position: 'relative' as const
  };

  return (
    <div style={messageStyle}>
      <div style={bubbleStyle}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span style={{ fontSize: '20px' }}>{emojiMap[teaNote.emoji]}</span>
          <span style={{ fontSize: '12px', opacity: 0.8 }}>
            {format(teaNote.timestamp, 'HH:mm')}
          </span>
        </div>
        
        <div style={{ marginBottom: '8px' }}>
          {teaNote.content}
        </div>

        {teaNote.reminderTime && (
          <div style={{ 
            fontSize: '11px', 
            opacity: 0.8, 
            marginBottom: '8px',
            background: 'rgba(255,255,255,0.2)',
            padding: '4px 8px',
            borderRadius: '8px',
            display: 'inline-block'
          }}>
            ⏰ Remind at {format(teaNote.reminderTime, 'MMM dd, HH:mm')}
          </div>
        )}

        {!teaNote.isCompleted && (
          <button
            onClick={() => setShowFollowUps(!showFollowUps)}
            style={{
              background: 'rgba(255,255,255,0.2)',
              border: 'none',
              borderRadius: '8px',
              padding: '6px 12px',
              fontSize: '12px',
              cursor: 'pointer',
              color: 'inherit'
            }}
          >
            {showFollowUps ? 'Hide' : 'Answer'} Follow-ups
          </button>
        )}

        {teaNote.isCompleted && (
          <div style={{ 
            fontSize: '11px', 
            opacity: 0.8,
            background: 'rgba(255,255,255,0.2)',
            padding: '4px 8px',
            borderRadius: '8px',
            display: 'inline-block'
          }}>
            ✅ Discussed
          </div>
        )}
      </div>

      {showFollowUps && !teaNote.isCompleted && (
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '16px',
          marginTop: '8px',
          boxShadow: '0 4px 12px var(--shadow-light)',
          border: '2px solid var(--pastel-lavender)'
        }}>
          <h4 style={{ 
            marginBottom: '12px', 
            color: 'var(--text-dark)',
            fontSize: '14px',
            fontWeight: '600'
          }}>
            Follow-up Questions:
          </h4>
          
          {teaNote.followUpQuestions.map((question) => (
            <div key={question.id} style={{ marginBottom: '12px' }}>
              <label style={{ 
                display: 'block', 
                marginBottom: '4px', 
                fontSize: '12px',
                fontWeight: '500',
                color: 'var(--text-dark)'
              }}>
                {question.question}
              </label>
              <input
                type="text"
                value={answers[question.id] || question.answer || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                placeholder={`Answer about ${question.type}...`}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  border: '2px solid var(--pastel-lavender)',
                  borderRadius: '8px',
                  fontSize: '12px',
                  outline: 'none',
                  background: 'var(--pastel-mint)'
                }}
              />
            </div>
          ))}
          
          <button
            onClick={saveAnswers}
            style={{
              background: 'var(--pastel-green)',
              color: 'var(--text-dark)',
              border: 'none',
              borderRadius: '8px',
              padding: '8px 16px',
              fontSize: '12px',
              fontWeight: '600',
              cursor: 'pointer',
              width: '100%'
            }}
          >
            Save Answers & Mark Complete
          </button>
        </div>
      )}
    </div>
  );
}
