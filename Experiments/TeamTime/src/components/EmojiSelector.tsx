import React from 'react';
import { TeaEmoji } from '../types';

interface EmojiSelectorProps {
  selectedEmoji: TeaEmoji;
  onEmojiSelect: (emoji: TeaEmoji) => void;
}

const emojiMap: Record<TeaEmoji, string> = {
  angry: '😠',
  star: '⭐',
  heart: '❤️',
  laugh: '😂',
  shock: '😱'
};

const emojiColors: Record<TeaEmoji, string> = {
  angry: 'var(--pastel-pink)',
  star: 'var(--pastel-yellow)',
  heart: 'var(--pastel-pink)',
  laugh: 'var(--pastel-yellow)',
  shock: 'var(--pastel-purple)'
};

export function EmojiSelector({ selectedEmoji, onEmojiSelect }: EmojiSelectorProps) {
  return (
    <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
      {(Object.keys(emojiMap) as TeaEmoji[]).map((emoji) => (
        <button
          key={emoji}
          onClick={() => onEmojiSelect(emoji)}
          style={{
            background: selectedEmoji === emoji ? emojiColors[emoji] : 'var(--pastel-lavender)',
            border: 'none',
            borderRadius: '50%',
            width: '40px',
            height: '40px',
            fontSize: '20px',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            boxShadow: selectedEmoji === emoji ? '0 2px 8px var(--shadow-light)' : 'none',
            transform: selectedEmoji === emoji ? 'scale(1.1)' : 'scale(1)'
          }}
        >
          {emojiMap[emoji]}
        </button>
      ))}
    </div>
  );
}
