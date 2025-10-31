# DNS Configuration for shriekedin.uk

## ✅ What's Been Fixed

1. **ALLOWED_HOSTS Updated** - Heroku now accepts requests from custom domains
2. **www Subdomain Added** - www.shriekedin.uk is now configured in Heroku
3. **SSL Certificates Issued** - Both domains now have valid SSL certificates

## ⚠️ DNS Changes Required

Your DNS needs to be updated to point to the correct Heroku targets:

### Current DNS Configuration (INCORRECT)

**www.shriekedin.uk:**
- Currently points to: `hidden-passionflower-cbs00zuev3dxt62uz6rn4go8.herokudns.com`
- **This is wrong!** This is the target for the apex domain.

### Correct DNS Configuration

Configure your DNS provider with these exact records:

#### 1. Apex Domain (shriekedin.uk)
```
Type: ALIAS or ANAME
Name: @ (or shriekedin.uk)
Target: hidden-passionflower-cbs00zuev3dxt62uz6rn4go8.herokudns.com
```
✅ This appears to be configured correctly (resolves to Heroku IPs)

#### 2. WWW Subdomain (www.shriekedin.uk)
```
Type: CNAME
Name: www
Target: synthetic-lychee-xhrfx7xbdlaaxjtvqi1hj9ao.herokudns.com
```
❌ **ACTION REQUIRED:** Update your DNS to point www to the correct target above.

## Current Status

### ✅ Heroku Configuration
```
ALLOWED_HOSTS: shriekedin.uk,www.shriekedin.uk,shriekedin-266a1e320857.herokuapp.com
SSL Certificates: Both issued (less than a minute ago)

Domains:
- shriekedin.uk → hidden-passionflower-cbs00zuev3dxt62uz6rn4go8.herokudns.com
- www.shriekedin.uk → synthetic-lychee-xhrfx7xbdlaaxjtvqi1hj9ao.herokudns.com
```

### ❌ DNS Issue
The www CNAME is pointing to the wrong target. This is why you're seeing SSL errors.

## How to Fix

1. **Log into your DNS provider** (wherever shriekedin.uk is registered)
2. **Find the CNAME record** for `www.shriekedin.uk`
3. **Update the target** to: `synthetic-lychee-xhrfx7xbdlaaxjtvqi1hj9ao.herokudns.com`
4. **Save the changes** (DNS propagation may take a few minutes)

## Testing After DNS Update

Wait 5-10 minutes for DNS propagation, then test:

```bash
# Check www CNAME (should show the synthetic-lychee target)
dig www.shriekedin.uk CNAME +short

# Test HTTPS (should work without errors)
curl -I https://www.shriekedin.uk
curl -I https://shriekedin.uk
```

## Expected Behavior After Fix

- ✅ https://shriekedin.uk - Should work (already works)
- ✅ https://www.shriekedin.uk - Should work (after DNS fix)
- ✅ Valid SSL certificates for both domains
- ✅ No more 400 Bad Request errors
- ✅ No more "can't establish secure connection" errors

## DNS Propagation Time

- Minimum: 5-10 minutes
- Maximum: Up to 48 hours (typically much faster)
- Check status: https://www.whatsmydns.net/

## Quick Reference: Heroku Commands

```bash
# View current domains
heroku domains --app shriekedin

# Check SSL certificate status
heroku certs:auto --app shriekedin

# View logs
heroku logs --tail --app shriekedin

# Check config
heroku config --app shriekedin
```

---

**Summary:** The Heroku side is fully configured. You just need to update the www CNAME record in your DNS provider to point to the correct target.
