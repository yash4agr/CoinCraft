# CoinCraft Frontend

Vue 3 frontend for the CoinCraft financial literacy education platform with AI-powered module generation.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn package manager

### Installation

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

### 🔧 Environment Configuration

Create a `.env` file in the frontend directory:

```bash
# API Backend URL
VITE_API_URL=http://localhost:8000

# AI Integration - Get your API key from Cerebras
VITE_CEREBRAS_API_KEY=your-cerebras-api-key-here
```

### 🤖 Getting Cerebras AI API Key

1. **Visit Cerebras Cloud**
   ```
   https://cloud.cerebras.ai/
   ```

2. **Sign up for an account**
   - Create a free account or log in
   - Navigate to API Keys section

3. **Generate API Key**
   - Click "Create API Key"
   - Copy the generated key
   - Add it to your `.env` file as `VITE_CEREBRAS_API_KEY`

4. **API Key Format**
   ```bash
   VITE_CEREBRAS_API_KEY=csk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 🏃 Running the Application

```bash
# Development server with hot reload
npm run dev

# Or with yarn
yarn dev
```

Application will start at: `http://localhost:5173`

### 🏗️ Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🎯 Demo Accounts

| Role | Email | Password | Features |
|------|-------|----------|----------|
| **Teacher** | teacher@demo.com | demo123 | Create modules, AI assist, manage classes |
| **Parent** | parent@demo.com | demo123 | Monitor children, assign tasks |
| **Child** | child@demo.com | demo123 | Learn modules, play games, track goals |

## 🤖 AI Module Generation

### Features
- **AI-Powered Content**: Generate educational modules with Cerebras AI
- **Structured Output**: Automatic sections, activities, and quiz generation
- **Try Mode**: Interactive learning experience with progress tracking
- **Content Indicators**: Visual display of sections, activities, and quizzes

### Using AI Assist
1. **Login as Teacher** → Go to Module Management
2. **Click AI Assist** (purple button)
3. **Enter topic, age group, duration**
4. **Generate Full Module** (sections + activities + quiz)
5. **Save Module** → Auto-saves to backend
6. **Try Mode** → Test the generated content

## 📱 Testing Standalone AI Features

### Standalone Test File

### Running the Test

1. **Open `test_ai.html` and `test-api.html`** in the frontend directory
2. **Open in browser**: `file:///path/to/frontend/test_ai.html`
3. **Enter your Cerebras API key**
4. **Test AI module generation**

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── shared/         # Common UI components
│   │   └── teacher/        # Teacher-specific components
│   │       ├── AIAssistComponent.vue    # AI module generator
│   │       └── ModuleTryMode.vue       # Interactive learning mode
│   ├── views/              # Page components
│   │   ├── auth/          # Login/Register pages
│   │   ├── teacher/       # Teacher dashboard and tools
│   │   ├── parent/        # Parent management interface
│   │   └── child/         # Child learning interface
│   ├── stores/            # Pinia state management
│   │   ├── auth.ts        # Authentication state
│   │   ├── teacher.ts     # Teacher data and AI integration
│   │   └── user.ts        # User profile management
│   ├── services/          # API integration
│   │   └── api.ts         # Backend API calls
│   ├── router/            # Vue Router configuration
│   └── types/             # TypeScript definitions
├── public/                # Static assets
├── test_ai.html          # Standalone AI testing
└── package.json          # Dependencies and scripts
```

## 🎨 Tech Stack

- **Vue 3** - Progressive framework with Composition API
- **TypeScript** - Type-safe development
- **Vuetify** - Material Design component library
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Vite** - Fast build tool and dev server
- **Cerebras AI SDK** - AI-powered content generation

## 🔧 Key Features

### Teacher Dashboard
- **Module Management**: Create, edit, and organize learning modules
- **AI Assist**: Generate educational content with AI
- **Try Mode**: Preview and test modules interactively
- **Class Management**: Monitor student progress
- **Analytics**: View learning performance data

### AI Integration
- **Smart Content Generation**: Topic-based module creation
- **Structured Output**: Sections, activities, and quizzes
- **Age-Appropriate Content**: Tailored for different age groups
- **Interactive Learning**: Try Mode with progress tracking

### Enhanced Modules
- **📚 Sections**: Lessons, readings, videos, discussions
- **🎯 Activities**: Exercises, simulations, projects
- **❓ Quiz**: Multiple choice and true/false questions
- **🏆 Progress**: Real-time learning tracking

## 🐛 Troubleshooting

### Common Issues

**CORS Errors:**
```bash
# Check backend URL in .env
VITE_API_URL=http://localhost:8000
```

**AI API Errors:**
```bash
# Verify API key format
VITE_CEREBRAS_API_KEY=csk-xxxxxxxxxxxxx

# Check network connectivity to Cerebras
# Ensure API key has proper permissions
```

**Build Errors:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Environment Variables Not Loading:**
```bash
# Ensure .env file is in frontend root
# Restart dev server after .env changes
npm run dev
```

## 🚀 Production Deployment

### Build Configuration

```bash
# Production build
npm run build

# Check build output
npm run preview
```

### Environment Variables

Set production values:
```bash
VITE_API_URL=https://api.yourproductiondomain.com
VITE_CEREBRAS_API_KEY=your-production-api-key
```

### Deployment Options
- **Vercel**: Connect GitHub repo for auto-deployment
- **Netlify**: Drag & drop `dist` folder
- **AWS S3**: Static website hosting
- **CDN**: CloudFront or similar for global distribution

---

**Need help?** Check the [Vue 3 documentation](https://vuejs.org/) or review the component structure.
