# Deploy to Firebase Hosting

## Quick Deploy Steps:

1. **Open PowerShell/Terminal in this folder**

2. **Login to Firebase** (if not already logged in):
   ```
   firebase login
   ```
   This will open a browser for authentication.

3. **Initialize Firebase Hosting** (if not already done):
   ```
   firebase init hosting
   ```
   - Select your Firebase project
   - Use current directory (`.`)
   - Don't overwrite index.html (say No)
   - Single-page app: Yes

4. **Deploy**:
   ```
   firebase deploy --only hosting
   ```

5. **Your site will be live at**: `https://YOUR-PROJECT-ID.web.app`

## Alternative: Use Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project
3. Go to Hosting
4. Click "Get started"
5. Install Firebase CLI (if needed): `npm install -g firebase-tools`
6. Run `firebase init hosting` then `firebase deploy`

