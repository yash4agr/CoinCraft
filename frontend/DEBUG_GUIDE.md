# Debug Guide for CoinCraft API Issues

## Current Status
✅ Login endpoint working (200 OK)  
❓ "Network error" appearing despite successful requests

## Debugging Steps

### 1. Check Backend Status
```bash
cd soft-engg-project-may-2025-se-May-15/backend
python -m uvicorn main:app --reload
```

**Expected output:**
- Application startup complete
- Server running on http://127.0.0.1:8000

### 2. Test API Endpoints Manually

#### Test Health Check
```bash
curl http://localhost:8000/health
```
**Expected:** `{"status":"OK"}`

#### Test New Debug Endpoint
```bash
curl http://localhost:8000/api/test
```
**Expected:** `{"message":"API is working","timestamp":"2025-01-01T00:00:00Z"}`

#### Test Login (Manual)
```bash
curl -X POST "http://localhost:8000/api/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=luna@demo.com&password=demo123"
```
**Expected:** JWT token response

#### Test Get User (with token)
```bash
# First get token from login, then:
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 3. Browser Console Debugging

Open browser dev tools and check for these logs during login:

```
🔐 Starting login process... luna@demo.com
📡 Calling API login...
🔍 Login response: {data: {access_token: "...", user: {...}}}
✅ Login successful, processing user data...
👤 User data processed: {id: "...", fullName: "...", ...}
🎉 Login completed successfully!
```

**If you see errors, check:**
- Network tab for failed requests
- Console for specific error messages
- Application tab for JWT token storage

### 4. Common Issues and Solutions

#### Issue: "Network error on /api/users/me"
**Cause:** FastAPI Users endpoint not properly configured
**Solution:** Backend has been updated with `get_users_router`

#### Issue: CORS errors
**Cause:** Missing frontend origin in CORS config
**Solution:** Added comprehensive CORS origins including all dev server ports

#### Issue: 401 Unauthorized after login
**Cause:** JWT token not being sent or invalid
**Check:**
1. Token stored in localStorage: `localStorage.getItem('auth_token')`
2. Token format: Should start with `eyJ`
3. Token in Authorization header: Check Network tab

#### Issue: 404 Not Found on endpoints
**Cause:** API prefix mismatch
**Solution:** All endpoints now use `/api` prefix

### 5. Backend Log Analysis

Check backend logs for these patterns:

**Successful login:**
```
INFO: 127.0.0.1:XXXXX - "POST /api/auth/jwt/login HTTP/1.1" 200 OK
```

**User fetch after login:**
```
INFO: 127.0.0.1:XXXXX - "GET /api/users/me HTTP/1.1" 200 OK
```

**Database queries:**
```
SELECT users.id, users.email, ... FROM users WHERE lower(users.email) = lower(?)
```

### 6. Frontend Network Tab Inspection

Check Network tab for these requests:

1. **OPTIONS /api/auth/jwt/login** → Should be 200 OK or 204 No Content
2. **POST /api/auth/jwt/login** → Should be 200 OK with JWT token
3. **GET /api/users/me** → Should be 200 OK with user data

### 7. Quick Tests in Browser Console

```javascript
// Test API connection
await apiService.testConnection()
// Expected: {data: {message: "API is working"}}

// Test authentication status
apiService.isAuthenticated()
// Expected: true/false

// Test token
apiService.getToken()
// Expected: JWT token string or null

// Test manual login
await apiService.login({email: 'luna@demo.com', password: 'demo123'})
```

### 8. Environment Variables Check

Frontend `.env` file should contain:
```
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

### 9. Troubleshooting Network Errors

If you see "Network error" despite 200 OK responses:

1. **Check the actual error:**
   - Look for detailed error logs in console
   - Check if it's a specific endpoint failing

2. **Check token validity:**
   - JWT might be malformed or expired
   - Backend might not be validating token correctly

3. **Check response parsing:**
   - Response might not match expected format
   - JSON parsing might be failing

4. **Check CORS configuration:**
   - Preflight requests might be failing
   - Headers might not be allowed

## Expected Working Flow

1. User enters credentials
2. Frontend calls `/api/auth/jwt/login` with FormData
3. Backend returns JWT token (200 OK)
4. Frontend stores token and calls `/api/users/me`
5. Backend returns user data (200 OK)
6. Frontend processes user data and updates state
7. User is logged in successfully

## Debug Commands Summary

```bash
# Backend logs
cd backend && python -m uvicorn main:app --reload

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/test

# Frontend logs
# Open browser console and check for emoji logs 🔐📡🔍✅👤🎉
```

## Current Fixes Applied

✅ Added FastAPI Users `/api/users/me` endpoint  
✅ Enhanced error handling with detailed logging  
✅ Added fallback user data if user fetch fails  
✅ Added debug endpoints and logging  
✅ Fixed FormData content-type handling  
✅ Updated all API endpoints with `/api` prefix  

The system should now work correctly! 🚀 