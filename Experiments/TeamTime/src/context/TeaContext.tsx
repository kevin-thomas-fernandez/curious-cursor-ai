import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { TeaNote, WeeklyQuiz } from '../types';
import { useAuth } from './AuthContext';

interface TeaState {
  teaNotes: TeaNote[];
  weeklyQuizzes: WeeklyQuiz[];
}

type TeaAction =
  | { type: 'ADD_TEA_NOTE'; payload: TeaNote }
  | { type: 'UPDATE_TEA_NOTE'; payload: TeaNote }
  | { type: 'DELETE_TEA_NOTE'; payload: string }
  | { type: 'ADD_QUIZ'; payload: WeeklyQuiz }
  | { type: 'UPDATE_QUIZ'; payload: WeeklyQuiz };

const initialState: TeaState = {
  teaNotes: [],
  weeklyQuizzes: []
};

function teaReducer(state: TeaState, action: TeaAction): TeaState {
  switch (action.type) {
    case 'ADD_TEA_NOTE':
      return {
        ...state,
        teaNotes: [...state.teaNotes, action.payload]
      };
    case 'UPDATE_TEA_NOTE':
      return {
        ...state,
        teaNotes: state.teaNotes.map(note =>
          note.id === action.payload.id ? action.payload : note
        )
      };
    case 'DELETE_TEA_NOTE':
      return {
        ...state,
        teaNotes: state.teaNotes.filter(note => note.id !== action.payload)
      };
    case 'ADD_QUIZ':
      return {
        ...state,
        weeklyQuizzes: [...state.weeklyQuizzes, action.payload]
      };
    case 'UPDATE_QUIZ':
      return {
        ...state,
        weeklyQuizzes: state.weeklyQuizzes.map(quiz =>
          quiz.id === action.payload.id ? action.payload : quiz
        )
      };
    default:
      return state;
  }
}

const TeaContext = createContext<{
  state: TeaState;
  dispatch: React.Dispatch<TeaAction>;
  currentUser: 'me' | 'bf';
} | null>(null);

export function TeaProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(teaReducer, initialState);
  const { state: authState } = useAuth();

  const currentUser = authState.user?.role || 'me';

  return (
    <TeaContext.Provider value={{ state, dispatch, currentUser }}>
      {children}
    </TeaContext.Provider>
  );
}

export function useTea() {
  const context = useContext(TeaContext);
  if (!context) {
    throw new Error('useTea must be used within a TeaProvider');
  }
  return context;
}
