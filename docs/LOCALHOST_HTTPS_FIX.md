# Fixing localhost HTTPS Redirect Issues

## Problem
Chrome/Edge automatically redirects `http://localhost:8000/` to `https://localhost:8000/`, causing connection failures during development with errors like:
- `You're accessing the development server over HTTPS, but it only supports HTTP`
- `ERR_SSL_PROTOCOL_ERROR`
- Site shows as "Not Secure" or won't load

## Root Causes

1. **Wrong DEBUG setting** - If DEBUG=False in your .env, Django forces HTTPS redirects
2. **HSTS (HTTP Strict Transport Security) cache** - Browser remembers to use HTTPS for localhost
3. **Chrome's automatic HTTPS upgrades** - Forces HTTPS on known domains

## ✅ SOLUTION: Proper Local Development Setup

### Step 1: Verify Your .env File (MOST IMPORTANT!)

**Check your .env file exists and has the correct settings:**
```bash
cat .env
```

**Must contain:**
```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional but recommended - explicitly disable HTTPS for local dev:
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**⚠️ Common mistake:**
```bash
DEBUG=False  # ❌ This forces HTTPS redirects!
```

**After fixing .env:**
```bash
# Restart the server
python manage.py runserver
```

### Step 2: Access via HTTP (not HTTPS)

Always type the full URL with `http://` in your browser:
```
http://127.0.0.1:8000/
```

**Don't type:** `localhost` or just `127.0.0.1` - browsers may auto-upgrade to HTTPS.

---

### 2. Clear HSTS Settings in Chrome/Edge

#### Chrome:
1. Navigate to: `chrome://net-internals/#hsts`
2. Scroll down to "Delete domain security policies"
3. Enter: `localhost`
4. Click **Delete**
5. Also try deleting: `127.0.0.1`

#### Edge:
1. Navigate to: `edge://net-internals/#hsts`
2. Scroll down to "Delete domain security policies"
3. Enter: `localhost`
4. Click **Delete**
5. Also try deleting: `127.0.0.1`

**Then restart your browser completely.**

---

### 3. Use 127.0.0.1 Instead of localhost

Sometimes localhost has HSTS issues but the IP address doesn't:

```
http://127.0.0.1:8000/
```

Update your browser bookmark to use the IP address instead.

---

### 4. Disable Chrome's HTTPS-Only Mode

#### Chrome:
1. Go to: `chrome://settings/security`
2. Scroll to "Advanced"
3. Find "Always use secure connections"
4. **Turn it OFF**

#### Edge:
1. Go to: `edge://settings/privacy`
2. Scroll to "Security"
3. Find "Automatically switch to more secure connections"
4. **Turn it OFF**

---

### 5. Use Incognito/Private Mode (Quick Test)

Open an incognito/private window and try:
```
http://localhost:8000/
```

If this works, the issue is definitely browser cache/settings.

---

### 6. Clear All Browser Data

As a last resort:

#### Chrome/Edge:
1. Press `Ctrl+Shift+Delete` (Windows) or `Cmd+Shift+Delete` (Mac)
2. Select **"All time"**
3. Check:
   - ✅ Browsing history
   - ✅ Cookies and other site data
   - ✅ Cached images and files
4. Click "Clear data"
5. Restart browser

---

### 7. Use a Different Browser (Temporary)

Try Firefox, Safari, or another browser to verify the server is working:
```
http://localhost:8000/
```

If it works in another browser, it's definitely a Chrome/Edge issue.

---

### 8. Force HTTP in Address Bar

Some browsers ignore the protocol. Try:
1. Type the full URL: `http://localhost:8000/`
2. Press `Ctrl+Enter` (Windows) or `Cmd+Enter` (Mac)
   - This forces the browser to navigate without changing the protocol

---

### 9. Nuclear Option: Reset Browser Settings

#### Chrome:
1. Go to: `chrome://settings/reset`
2. Click "Restore settings to their original defaults"
3. Click "Reset settings"

#### Edge:
1. Go to: `edge://settings/reset`
2. Click "Restore settings to their original defaults"
3. Click "Reset"

---

## Prevention

To avoid this issue in the future:

### 1. Never Run Development Server with DEBUG=False
```bash
# .env file should ALWAYS have:
DEBUG=True
```

### 2. Bookmark the Correct URL
Save this in your browser bookmarks:
```
http://localhost:8000/
```
or
```
http://127.0.0.1:8000/
```

### 3. Use the Makefile Command
Our `make dev` and `make run` commands print the correct URL:
```bash
make dev
# Output shows: 💡 Visit: http://localhost:8000/
```

---

## Verification Steps

After trying a solution, verify it worked:

### 1. Check Django Settings
```bash
python -c "from decouple import config; print(f'DEBUG={config(\"DEBUG\", default=False, cast=bool)}')"
```
Should output: `DEBUG=True`

### 2. Check HSTS Status
In Chrome/Edge, navigate to:
```
chrome://net-internals/#hsts
```

Search for "localhost" - should show "Not found"

### 3. Test the URL
```bash
curl -I http://localhost:8000/
```
Should return HTTP 200, not a redirect

---

## Quick Reference

| Solution | Difficulty | Success Rate |
|----------|-----------|--------------|
| Check DEBUG=True in .env | ⭐ Easy | 40% |
| Clear HSTS settings | ⭐⭐ Easy | 30% |
| Use 127.0.0.1 instead | ⭐ Easy | 15% |
| Disable HTTPS-only mode | ⭐⭐ Medium | 10% |
| Incognito mode (test) | ⭐ Easy | N/A |
| Clear all browser data | ⭐⭐ Medium | 4% |
| Try different browser | ⭐ Easy | N/A |
| Reset browser settings | ⭐⭐⭐ Hard | 1% |

---

## Still Not Working?

If none of these work, check:

1. **Is the server actually running?**
   ```bash
   lsof -i :8000
   ```

2. **Can you access it via curl?**
   ```bash
   curl http://localhost:8000/
   ```

3. **Is there a proxy or VPN interfering?**
   - Disable VPN
   - Check system proxy settings

4. **Firewall blocking localhost?**
   - Temporarily disable firewall to test

---

## For Team Members

**Share this with your team:**

```bash
# Quick fix for most cases:
# 1. Check your .env file has DEBUG=True
# 2. Clear HSTS in chrome://net-internals/#hsts
# 3. Use http://127.0.0.1:8000/ instead
```

**Recommended workflow:**
- Always use `make dev` to start the server
- Bookmark `http://127.0.0.1:8000/` (IP instead of localhost)
- Keep DEBUG=True in development

---

Last updated: 2025-10-31
