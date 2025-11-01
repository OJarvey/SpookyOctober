# Inline Editing Guide for Haunted Places

## Overview

The haunted places detail page now features **in-place editing** for authorized users (staff/admin). This allows quick, seamless content updates without navigating to the Django admin panel.

## Features

### ✨ User Experience

- **Edit Icons**: Hover over any editable field to reveal a ✏️ edit icon
- **In-Place Editing**: Click the edit icon to transform the field into an editor
- **Markdown Support**: All text areas support markdown formatting
- **Real-Time Saving**: Changes are saved via AJAX without page reload
- **Visual Feedback**: Success/error notifications appear after saving
- **Clean UI**: Editors blend seamlessly with the parchment-themed design

### 🔒 Security

- **Permission-Based**: Only staff users (admins) can see and use edit icons
- **CSRF Protection**: All API requests include CSRF tokens
- **Field Validation**: Server-side validation prevents invalid data
- **Allowed Fields Only**: Only specific fields can be edited via the API

## How to Use

### For Admin Users:

1. **Navigate** to any haunted place detail page
2. **Hover** over an editable field to reveal the edit icon (✏️)
3. **Click** the edit icon to start editing
4. **Make Changes** in the editor (markdown supported for long text)
5. **Save** by clicking the 💾 Save button or **Cancel** to discard changes
6. **See Confirmation** via a notification message

### Editable Fields:

| Field | Type | Location |
|-------|------|----------|
| Story Title | Text | Page header |
| Story Content | Markdown | Main content area |
| Historical Context | Markdown | Historical section |
| Reported Phenomena | Markdown | Phenomena section |
| Famous For | Textarea | Famous For highlight box |

## Technical Details

### Architecture

```
┌─────────────────────┐
│   User Interface    │ Haunted Detail Page (haunted_detail.html)
│   (Template)        │ - Data attributes mark editable fields
└──────────┬──────────┘
           │
           │ User clicks edit icon
           │
┌──────────▼──────────┐
│   JavaScript        │ haunted-place-editor.js
│   (Client-Side)     │ - Manages UI state
│                     │ - Creates inline editors
│                     │ - Handles save/cancel
└──────────┬──────────┘
           │
           │ AJAX POST request
           │ (JSON payload)
           │
┌──────────▼──────────┐
│   Django API        │ views.update_haunted_place_field()
│   (Server-Side)     │ - Validates permissions
│                     │ - Validates data
│                     │ - Updates database
│                     │ - Returns JSON response
└─────────────────────┘
```

### Files Modified/Created

#### Created Files:

1. **`static/js/haunted-place-editor.js`** (New)
   - JavaScript class for managing inline editing
   - Handles UI transformations
   - Makes AJAX requests
   - Shows notifications

#### Modified Files:

1. **`core/views.py`**
   - Added `update_haunted_place_field()` API endpoint
   - Implements permission checks
   - Validates and saves field updates

2. **`core/urls.py`**
   - Added route: `/haunted/<int:place_id>/update/`

3. **`templates/haunted_detail.html`**
   - Added `data-editable` attributes to fields
   - Added `data-field-type` for editor type selection
   - Added `data-field-content` to identify content areas
   - Included editor JavaScript for staff users

### API Endpoint

**URL**: `/haunted/<place_id>/update/`
**Method**: POST
**Authentication**: Required (staff only)

**Request Payload**:
```json
{
  "field": "story_content",
  "value": "Updated story text with **markdown** support"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "field": "story_content",
  "value": "Updated story text with **markdown** support",
  "message": "Story Content updated successfully."
}
```

**Error Response** (400/403/404):
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Allowed Fields

The API only allows editing these specific fields:

- `story_title` - The main title
- `story_content` - The ghost story text
- `historical_context` - Historical background
- `reported_phenomena` - Paranormal activity descriptions
- `famous_for` - Notable characteristics
- `scare_level` - Scare rating (1-5)
- `year_established` - Year location was established
- `is_educational` - Educational flag (boolean)

### Field Types

The editor adapts based on the field type:

- **`text`** - Single-line text input
- **`markdown`** - Multi-line textarea with markdown support
- **`textarea`** - Multi-line textarea
- **`number`** - Number input with validation

## Markdown Support

All text fields support standard markdown formatting:

```markdown
**bold text**
*italic text*
# Heading 1
## Heading 2
- Bullet point
[Link text](https://example.com)
```

## Styling

The editors maintain the parchment theme:

- **Font**: Special Elite (matching the parchment cards)
- **Colors**: Brown borders and aged paper background
- **Buttons**: Green save button, gray cancel button
- **Notifications**: Fixed position, auto-dismiss after 3 seconds

## Browser Compatibility

- ✅ Modern Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers (with touch support)

## Keyboard Shortcuts

Currently, no keyboard shortcuts are implemented, but these could be added:

- `Ctrl+Enter` / `Cmd+Enter` - Save
- `Esc` - Cancel editing

## Future Enhancements

Potential improvements:

1. **Preview Mode**: Live markdown preview while editing
2. **Undo/Redo**: Track edit history
3. **Auto-Save**: Save drafts automatically
4. **Rich Text Editor**: WYSIWYG editor option
5. **Image Upload**: Inline image insertion
6. **Conflict Detection**: Warn if another user is editing
7. **Edit History**: Show previous versions
8. **Batch Editing**: Edit multiple fields at once

## Troubleshooting

### Edit icons not appearing?

- Ensure you're logged in as a staff user
- Check browser console for JavaScript errors
- Verify `static/js/haunted-place-editor.js` is loaded

### Save button not working?

- Check browser console for network errors
- Verify CSRF token is present in cookies
- Ensure you have staff permissions

### Changes not persisting?

- Check Django logs for validation errors
- Verify the field is in the `allowed_fields` list
- Check database permissions

## Testing

To test the inline editing functionality:

1. Create a staff/admin user:
   ```bash
   python manage.py createsuperuser
   ```

2. Log in to the site (not the admin panel)

3. Navigate to any haunted place detail page

4. Hover over fields to see edit icons

5. Test editing and saving

6. Verify changes persist after page reload

## Security Considerations

- ✅ Only staff users can edit
- ✅ CSRF protection on all requests
- ✅ Server-side validation
- ✅ Allowed fields whitelist
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (Django template escaping)

## Performance

- Lightweight JavaScript (~10KB)
- No external dependencies (pure vanilla JS)
- Lazy loading (only loads for staff users)
- Efficient DOM manipulation
- Single API request per save

## Accessibility

Current implementation could be improved for accessibility:

- Add ARIA labels to edit buttons
- Implement keyboard navigation
- Add focus management
- Improve screen reader support
- Add visual focus indicators

---

**Created**: 2025-11-01
**Version**: 1.0
**Maintainer**: ShriekedIn Development Team
