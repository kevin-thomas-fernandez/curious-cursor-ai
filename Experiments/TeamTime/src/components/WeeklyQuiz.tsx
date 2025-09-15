import React, { useState, useEffect } from 'react';
import { format, startOfWeek, endOfWeek, isWithinInterval } from 'date-fns';
import { v4 as uuidv4 } from 'uuid';
import { TeaNote, WeeklyQuiz, QuizQuestion } from '../types';
import { useTea } from '../context/TeaContext';

export function WeeklyQuizComponent() {
  const { state, dispatch } = useTea();
  const [currentQuiz, setCurrentQuiz] = useState<WeeklyQuiz | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, number>>({});
  const [showResults, setShowResults] = useState(false);

  const generateQuizFromTeaNotes = (teaNotes: TeaNote[]): WeeklyQuiz => {
    const thisWeekStart = startOfWeek(new Date(), { weekStartsOn: 1 });
    const thisWeekEnd = endOfWeek(new Date(), { weekStartsOn: 1 });
    
    const thisWeekTea = teaNotes.filter(tea => 
      isWithinInterval(tea.timestamp, { start: thisWeekStart, end: thisWeekEnd })
    );

    const questions: QuizQuestion[] = thisWeekTea.map(tea => {
      const questionTypes = [
        `What was the main topic of the tea shared on ${format(tea.timestamp, 'MMM dd')}?`,
        `Who was mentioned in the tea from ${format(tea.timestamp, 'MMM dd')}?`,
        `Where did the tea from ${format(tea.timestamp, 'MMM dd')} take place?`,
        `How did you feel about the tea from ${format(tea.timestamp, 'MMM dd')}?`
      ];

      const question = questionTypes[Math.floor(Math.random() * questionTypes.length)];
      
      // Generate options based on tea content and connections
      const options = [
        tea.content.substring(0, 30) + '...',
        tea.connections.find(c => c.type === 'person')?.name || 'Someone at work',
        tea.connections.find(c => c.type === 'location')?.name || 'At the office',
        'It was interesting'
      ];

      return {
        id: uuidv4(),
        question,
        options,
        correctAnswer: 0,
        teaNoteId: tea.id
      };
    });

    return {
      id: uuidv4(),
      weekStart: thisWeekStart,
      questions,
      completed: false
    };
  };

  useEffect(() => {
    const thisWeekStart = startOfWeek(new Date(), { weekStartsOn: 1 });
    const existingQuiz = state.weeklyQuizzes.find(quiz => 
      quiz.weekStart.getTime() === thisWeekStart.getTime()
    );

    if (existingQuiz) {
      setCurrentQuiz(existingQuiz);
    } else if (state.teaNotes.length > 0) {
      const newQuiz = generateQuizFromTeaNotes(state.teaNotes);
      setCurrentQuiz(newQuiz);
      dispatch({ type: 'ADD_QUIZ', payload: newQuiz });
    }
  }, [state.teaNotes, state.weeklyQuizzes, dispatch]);

  const handleAnswerSelect = (answerIndex: number) => {
    if (!currentQuiz) return;
    
    const questionId = currentQuiz.questions[currentQuestionIndex].id;
    setSelectedAnswers(prev => ({ ...prev, [questionId]: answerIndex }));
  };

  const nextQuestion = () => {
    if (!currentQuiz) return;
    
    if (currentQuestionIndex < currentQuiz.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // Quiz completed
      const score = Object.entries(selectedAnswers).reduce((acc, [questionId, answerIndex]) => {
        const question = currentQuiz.questions.find(q => q.id === questionId);
        return acc + (question && answerIndex === question.correctAnswer ? 1 : 0);
      }, 0);

      const completedQuiz = {
        ...currentQuiz,
        completed: true,
        score: Math.round((score / currentQuiz.questions.length) * 100)
      };

      dispatch({ type: 'UPDATE_QUIZ', payload: completedQuiz });
      setCurrentQuiz(completedQuiz);
      setShowResults(true);
    }
  };

  const resetQuiz = () => {
    setCurrentQuestionIndex(0);
    setSelectedAnswers({});
    setShowResults(false);
  };

  if (!currentQuiz || currentQuiz.questions.length === 0) {
    return (
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '24px',
        textAlign: 'center',
        boxShadow: '0 4px 12px var(--shadow-light)'
      }}>
        <h3 style={{ color: 'var(--text-dark)', marginBottom: '12px' }}>
          🧠 Weekly Tea Quiz
        </h3>
        <p style={{ color: 'var(--text-light)', fontSize: '14px' }}>
          No tea to quiz about this week yet! Share some tea first! ☕
        </p>
      </div>
    );
  }

  if (showResults) {
    return (
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '24px',
        textAlign: 'center',
        boxShadow: '0 4px 12px var(--shadow-light)'
      }}>
        <h3 style={{ color: 'var(--text-dark)', marginBottom: '16px' }}>
          🎉 Quiz Complete!
        </h3>
        <div style={{
          background: 'var(--pastel-green)',
          borderRadius: '12px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: 'var(--text-dark)' }}>
            {currentQuiz.score}%
          </div>
          <div style={{ fontSize: '14px', color: 'var(--text-light)' }}>
            You remembered {Math.round((currentQuiz.score || 0) / 100 * currentQuiz.questions.length)} out of {currentQuiz.questions.length} tea moments!
          </div>
        </div>
        <button
          onClick={resetQuiz}
          style={{
            background: 'var(--pastel-purple)',
            color: 'white',
            border: 'none',
            borderRadius: '12px',
            padding: '12px 24px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer'
          }}
        >
          Take Quiz Again
        </button>
      </div>
    );
  }

  const currentQuestion = currentQuiz.questions[currentQuestionIndex];
  const isAnswered = selectedAnswers[currentQuestion.id] !== undefined;

  return (
    <div style={{
      background: 'white',
      borderRadius: '16px',
      padding: '24px',
      boxShadow: '0 4px 12px var(--shadow-light)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3 style={{ color: 'var(--text-dark)', fontSize: '18px', fontWeight: '600' }}>
          🧠 Weekly Tea Quiz
        </h3>
        <div style={{ 
          background: 'var(--pastel-lavender)', 
          padding: '4px 12px', 
          borderRadius: '12px',
          fontSize: '12px',
          color: 'var(--text-dark)'
        }}>
          {currentQuestionIndex + 1} / {currentQuiz.questions.length}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ 
          color: 'var(--text-dark)', 
          marginBottom: '16px',
          fontSize: '16px',
          lineHeight: '1.4'
        }}>
          {currentQuestion.question}
        </h4>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswerSelect(index)}
              style={{
                background: selectedAnswers[currentQuestion.id] === index 
                  ? 'var(--pastel-purple)' 
                  : 'var(--pastel-lavender)',
                color: selectedAnswers[currentQuestion.id] === index 
                  ? 'white' 
                  : 'var(--text-dark)',
                border: 'none',
                borderRadius: '12px',
                padding: '12px 16px',
                fontSize: '14px',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.2s ease'
              }}
            >
              {String.fromCharCode(65 + index)}. {option}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={nextQuestion}
        disabled={!isAnswered}
        style={{
          background: isAnswered ? 'var(--pastel-green)' : 'var(--pastel-lavender)',
          color: isAnswered ? 'var(--text-dark)' : 'var(--text-light)',
          border: 'none',
          borderRadius: '12px',
          padding: '12px 24px',
          fontSize: '14px',
          fontWeight: '600',
          cursor: isAnswered ? 'pointer' : 'not-allowed',
          width: '100%',
          transition: 'all 0.2s ease'
        }}
      >
        {currentQuestionIndex < currentQuiz.questions.length - 1 ? 'Next Question' : 'Finish Quiz'}
      </button>
    </div>
  );
}
