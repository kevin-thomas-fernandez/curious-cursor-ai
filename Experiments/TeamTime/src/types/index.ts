export interface TeaNote {
  id: string;
  content: string;
  timestamp: Date;
  reminderTime?: Date;
  followUpQuestions: FollowUpQuestion[];
  connections: Connection[];
  emoji: TeaEmoji;
  isCompleted: boolean;
  author: 'me' | 'bf';
}

export interface FollowUpQuestion {
  id: string;
  question: string;
  answer?: string;
  type: 'what' | 'who' | 'where' | 'how' | 'when' | 'why';
}

export interface Connection {
  id: string;
  type: 'person' | 'workplace' | 'location' | 'language' | 'category';
  name: string;
  color: string;
}

export type TeaEmoji = 'angry' | 'star' | 'heart' | 'laugh' | 'shock';

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
  teaNoteId: string;
}

export interface WeeklyQuiz {
  id: string;
  weekStart: Date;
  questions: QuizQuestion[];
  completed: boolean;
  score?: number;
}

export interface User {
  id: string;
  username: string;
  displayName: string;
  role: 'me' | 'bf';
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
}