# ☕ Tea Time App

A beautiful messaging app for sharing daily "tea" (gossip/stories) with your boyfriend! Built with React, TypeScript, and a delightful pastel color scheme.

## Features

### 🍵 Core Functionality
- **Tea Note Creation**: Jot down your daily tea with emoji reactions
- **Reminder System**: Set specific times to discuss each tea
- **Follow-up Questions**: Automatic "what, who, where, how, when" questions
- **User Switching**: Toggle between "me" and "boyfriend" perspectives

### 🔗 Connection System
- **Family Tree-like Connections**: Link tea to people, workplaces, locations, languages, or categories
- **Visual Organization**: Color-coded connection tags
- **Relationship Mapping**: See how different tea moments connect

### 🧠 Weekly Quiz
- **Trivia Generation**: Automatic quiz creation from weekly tea
- **Memory Testing**: See how well you remember the week's events
- **Score Tracking**: Track your tea memory skills

### 🎨 Design
- **Pastel Aesthetic**: Beautiful soft colors throughout
- **5 Emoji System**: 😠 angry, ⭐ star, ❤️ heart, 😂 laugh, 😱 shock
- **WhatsApp-like Interface**: Familiar messaging experience
- **Responsive Design**: Works on all devices

## Getting Started

### Prerequisites
- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

## How to Use

### 1. Share Tea
- Switch between "You" and "Boyfriend" using the user switcher
- Select an emoji that represents your mood about the tea
- Write your tea in the text area
- Optionally set a reminder time to discuss it later
- Click "Share Tea ☕"

### 2. Answer Follow-ups
- Click "Answer Follow-ups" on any tea message
- Fill in the automatic questions (what, who, where, how, when)
- Click "Save Answers & Mark Complete" when done

### 3. Connect Tea
- After completing follow-ups, click the "🔗 Connect" button
- Add connections to people, workplaces, locations, languages, or categories
- Organize your tea like a family tree

### 4. Weekly Quiz
- Switch to the "🧠 Quiz" tab
- Answer questions about the tea from this week
- See your score and how well you remembered the week's events

## Technical Details

### Tech Stack
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Context API** for state management
- **date-fns** for date handling
- **UUID** for unique ID generation

### Project Structure
```
src/
├── components/          # React components
│   ├── EmojiSelector.tsx
│   ├── TeaNoteForm.tsx
│   ├── TeaMessage.tsx
│   ├── ConnectionManager.tsx
│   ├── WeeklyQuiz.tsx
│   └── UserSwitcher.tsx
├── context/            # React Context for state
│   └── TeaContext.tsx
├── types/              # TypeScript type definitions
│   └── index.ts
├── App.tsx             # Main app component
├── main.tsx            # App entry point
└── index.css           # Global styles
```

### State Management
The app uses React Context for state management with the following data:
- `teaNotes`: Array of all shared tea
- `weeklyQuizzes`: Generated quizzes for each week
- `currentUser`: Currently active user ('me' or 'bf')

## Customization

### Colors
The app uses CSS custom properties for easy color customization:
```css
:root {
  --pastel-pink: #ffb3ba;
  --pastel-purple: #b3b3ff;
  --pastel-blue: #bae1ff;
  --pastel-green: #baffc9;
  --pastel-yellow: #ffffba;
  --pastel-lavender: #e6e6fa;
  --pastel-mint: #f0fff0;
  --pastel-peach: #ffdab9;
}
```

### Emojis
The 5 emoji system can be customized in `src/components/EmojiSelector.tsx`:
- 😠 angry
- ⭐ star  
- ❤️ heart
- 😂 laugh
- 😱 shock

## Future Enhancements

- Real-time synchronization between devices
- Push notifications for reminders
- Photo attachments for tea
- Export/import functionality
- Advanced analytics and insights
- Custom connection types
- Tea search and filtering

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

---

**Enjoy sharing your tea! ☕✨**
