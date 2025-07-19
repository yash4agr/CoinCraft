# CoinCraft Frontend Setup Instructions

## Quick Setup

### 1. Create Environment File
Create a `.env` file in the frontend directory:

```bash
# Navigate to frontend directory
cd soft-engg-project-may-2025-se-May-15/frontend

# Create .env file
touch .env
```

### 2. Add Environment Variables
Add the following to your `.env` file:

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Development settings
VITE_APP_TITLE=CoinCraft
VITE_DEBUG=true
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Start Development Server
```bash
npm run dev
```

## Backend Requirements

Make sure the backend is running before starting the frontend:

```bash
# In a separate terminal, navigate to backend
cd soft-engg-project-may-2025-se-May-15/backend

# Install dependencies (if not done already)
pip install -e .

# Run the backend server
python -m uvicorn main:app --reload
```

## Testing the Integration

### 1. Test Login
Use these demo credentials:
- **Younger Child**: `luna@demo.com` / `demo123`
- **Older Child**: `harry@demo.com` / `demo123`
- **Parent**: `parent@demo.com` / `demo123`
- **Teacher**: `teacher@demo.com` / `demo123`

### 2. Check Browser Console
Open browser dev tools and check:
- Network tab for API calls
- Console for any errors
- Application tab for JWT token storage

### 3. Verify Features
- ✅ Login/Logout
- ✅ Dashboard data loading
- ✅ Goal creation
- ✅ Transaction history

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Make sure you're in the frontend directory
   - Run `npm install` to install dependencies

2. **API connection errors**
   - Verify backend is running on `http://localhost:8000`
   - Check `.env` file has correct `VITE_API_URL`
   - Ensure CORS is configured in backend

3. **Authentication errors**
   - Clear browser localStorage
   - Check JWT token in Application tab
   - Verify demo credentials are correct

4. **Import path errors**
   - The API service uses relative imports (`../services/api`)
   - Make sure the file structure is correct

### File Structure Check:
```
frontend/
├── .env                    # ← Create this file
├── src/
│   ├── services/
│   │   └── api.ts         # ← API service layer
│   └── stores/
│       ├── auth.ts        # ← Updated auth store
│       ├── dashboard.ts   # ← Updated dashboard store
│       └── child.ts       # ← Updated child store
└── package.json
```

## Development Notes

- The frontend uses relative imports for the API service
- JWT tokens are automatically managed
- Error handling includes network and server error detection
- All mock data has been replaced with real API calls
- Demo credentials are mapped to backend users

## Next Steps

After setup, you can:
1. Test all user roles and features
2. Add loading states and error boundaries
3. Implement offline functionality
4. Add unit tests for API integration 