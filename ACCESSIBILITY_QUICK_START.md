# Accessibility Quick Start Guide

This guide provides immediate, actionable fixes for the most critical accessibility issues in ShriekedIn.

---

## 🚨 Critical Fix #1: Add Form Labels (30 minutes)

### Problem
Search inputs and select dropdowns lack labels, making them unusable for screen reader users.

### Files to Fix
- `templates/events_list.html`
- `templates/businesses_list.html`
- `templates/haunted_places.html`

### Step 1: Add `.sr-only` utility class
Add to `static/css/custom.css` or Tailwind config:

```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

### Step 2: Update Search Sections

**BEFORE:**
```html
<input type="text"
       id="events-search-input"
       placeholder="Search events..."
       class="px-4 py-2 border-2 border-purple-300 rounded-lg">

<select class="px-4 py-2 border-2 border-purple-300 rounded-lg">
    <option value="">All Categories</option>
</select>

<button class="btn-primary px-6 py-2">Search</button>
```

**AFTER:**
```html
<form role="search" method="GET" action="" class="flex flex-col sm:flex-row gap-4">
    <label for="events-search-input" class="sr-only">Search for events</label>
    <input type="text"
           id="events-search-input"
           name="search"
           placeholder="Search events..."
           aria-label="Search for Halloween events by name or location"
           class="px-4 py-2 border-2 border-purple-300 rounded-lg">

    <label for="category-filter" class="sr-only">Filter by category</label>
    <select id="category-filter"
            name="category"
            aria-label="Filter events by category"
            class="px-4 py-2 border-2 border-purple-300 rounded-lg">
        <option value="">All Categories</option>
        <!-- options -->
    </select>

    <button type="submit"
            class="btn-primary px-6 py-2"
            aria-label="Search for events">
        Search
    </button>
</form>
```

### Apply Same Pattern To:
- Businesses search (change "events" to "businesses")
- Haunted places search (change "events" to "haunted places")

---

## 🚨 Critical Fix #2: Skip Navigation Link (10 minutes)

### Problem
Keyboard users must tab through entire navigation to reach main content.

### File to Fix
`templates/base.html`

### Add Before Navigation
```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
    position: absolute;
    left: -9999px;
    z-index: 999;
    padding: 1rem 2rem;
    background: #fff;
    color: #000;
    font-weight: bold;
    text-decoration: none;
}

.skip-link:focus {
    left: 50%;
    transform: translateX(-50%);
    top: 0;
    border: 2px solid #f97316;
    border-radius: 0 0 0.5rem 0.5rem;
}
</style>
```

### Add ID to Main Content
```html
<main class="flex-grow" id="main-content" tabindex="-1">
    {% block content %}<!-- Page-specific content goes here -->{% endblock %}
</main>
```

---

## 🚨 Critical Fix #3: Mobile Menu Accessibility (20 minutes)

### Problem
Mobile menu button lacks ARIA attributes and keyboard accessibility.

### File to Fix
`templates/base.html`

### Update Mobile Menu Button
**BEFORE:**
```html
<button id="mobile-menu-button" class="md:hidden text-white focus:outline-none">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
    </svg>
</button>
```

**AFTER:**
```html
<button id="mobile-menu-button"
        class="md:hidden text-white focus:outline-none focus:ring-2 focus:ring-orange-500 rounded p-2"
        aria-expanded="false"
        aria-controls="mobile-menu"
        aria-label="Toggle navigation menu">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
    </svg>
</button>
```

### Update Mobile Menu
**BEFORE:**
```html
<div id="mobile-menu" class="hidden md:hidden pb-4">
    <div class="flex flex-col space-y-2">
        <!-- menu items -->
    </div>
</div>
```

**AFTER:**
```html
<nav id="mobile-menu"
     class="hidden md:hidden pb-4"
     aria-label="Mobile navigation">
    <div class="flex flex-col space-y-2">
        <!-- menu items -->
    </div>
</nav>
```

### Update JavaScript
**BEFORE:**
```javascript
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
});
```

**AFTER:**
```javascript
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    const menu = document.getElementById('mobile-menu');
    const isExpanded = this.getAttribute('aria-expanded') === 'true';

    // Toggle menu visibility
    menu.classList.toggle('hidden');

    // Update ARIA state
    this.setAttribute('aria-expanded', !isExpanded);
});

// Close menu on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const button = document.getElementById('mobile-menu-button');
        const menu = document.getElementById('mobile-menu');

        if (!menu.classList.contains('hidden')) {
            menu.classList.add('hidden');
            button.setAttribute('aria-expanded', 'false');
            button.focus(); // Return focus to button
        }
    }
});
```

---

## 🚨 Critical Fix #4: ARIA Labels for Cards (30 minutes)

### Problem
Event/business cards lack proper semantic structure and labels.

### Files to Fix
- `templates/events_list.html`
- `templates/businesses_list.html`
- `templates/haunted_places.html`

### Update Card Structure
**BEFORE:**
```html
<div class="event-card bg-white rounded-lg shadow-lg overflow-hidden border-2 border-purple-200">
    <div class="relative w-full h-48 bg-gradient-to-br {{ gradient }} flex items-center justify-center">
        <span class="text-6xl">🎃</span>
        {% if event.is_featured %}<span class="absolute top-3 right-3 text-4xl">⭐</span>{% endif %}
    </div>

    <div class="p-6">
        <h3 class="text-2xl font-bold text-purple-900 mb-3">{{ event.title }}</h3>
        <!-- content -->
    </div>
</div>
```

**AFTER:**
```html
<article class="event-card bg-white rounded-lg shadow-lg overflow-hidden border-2 border-purple-200"
         aria-labelledby="event-{{ event.id }}-title">

    <div class="relative w-full h-48 bg-gradient-to-br {{ gradient }} flex items-center justify-center"
         aria-hidden="true">
        <span class="text-6xl" aria-hidden="true">🎃</span>
        {% if event.is_featured %}
            <span class="absolute top-3 right-3 text-4xl"
                  role="img"
                  aria-label="Featured event">⭐</span>
        {% endif %}
    </div>

    <div class="p-6">
        <h3 id="event-{{ event.id }}-title" class="text-2xl font-bold text-purple-900 mb-3">
            {{ event.title }}
        </h3>
        <!-- content -->

        <!-- Update "View Details" link -->
        <a href="{% url 'core:event_detail' event.id %}"
           class="..."
           aria-label="View details for {{ event.title }}">
            View Details <span aria-hidden="true">→</span>
        </a>
    </div>
</article>
```

### Apply Pattern to Other Cards
Repeat for:
- Business cards (use business.id, business_name)
- Haunted place cards (use place.id, story_title)

---

## 🔧 Focus Indicators (15 minutes)

### Problem
Focus indicators aren't visible enough for keyboard navigation.

### File to Update
Add to `static/css/custom.css` or inline in base.html:

```css
/* Enhanced focus styles for all interactive elements */
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus,
[tabindex]:focus {
    outline: 3px solid #f97316; /* Orange-600 */
    outline-offset: 2px;
}

/* For buttons with custom styling */
.btn-primary:focus,
.btn-secondary:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.5);
}

/* Make sure focus is never removed */
*:focus {
    outline-width: 2px;
    outline-style: solid;
    outline-color: #f97316;
}

/* Skip link styling */
.skip-link:focus {
    outline: 3px solid #000;
    outline-offset: 0;
}
```

---

## 📋 Quick Testing Checklist

After implementing fixes, test:

### Keyboard Navigation
- [ ] Press Tab key - can you reach all interactive elements?
- [ ] Press Shift+Tab - can you navigate backwards?
- [ ] Press Enter/Space on buttons - do they activate?
- [ ] Press Escape on modals/menus - do they close?
- [ ] Can you see where focus is at all times?

### Screen Reader (Use NVDA on Windows or VoiceOver on Mac)
- [ ] Turn on screen reader
- [ ] Navigate through the page with Arrow keys
- [ ] Tab through form controls - are labels announced?
- [ ] Activate search - are results announced?
- [ ] Listen to cards - is content structured logically?

### Browser Extensions
- [ ] Install axe DevTools
- [ ] Run scan on each page
- [ ] Fix all Critical and Serious issues
- [ ] Document any remaining warnings

---

## 📝 Accessibility Checklist for New Features

Before merging any PR with UI changes:

### Forms
- [ ] All inputs have associated labels (visible or sr-only)
- [ ] Required fields marked with aria-required="true"
- [ ] Error messages associated with inputs via aria-describedby
- [ ] Form has clear submit button with descriptive text

### Buttons & Links
- [ ] Button text describes action (not just "Click here")
- [ ] Icon-only buttons have aria-label
- [ ] Links have descriptive text or aria-label
- [ ] Disabled buttons have aria-disabled="true"

### Images & Icons
- [ ] Decorative images/icons have aria-hidden="true"
- [ ] Meaningful images have alt text or aria-label
- [ ] Emoji used for meaning have role="img" and aria-label

### Dynamic Content
- [ ] Status messages use role="status" or role="alert"
- [ ] Loading states announced with aria-live="polite"
- [ ] Updates to content count announced to screen readers

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab key
- [ ] Tab order is logical
- [ ] Focus indicators clearly visible
- [ ] Escape key closes modals/menus

### Semantic HTML
- [ ] Use semantic elements (nav, main, article, aside)
- [ ] Heading hierarchy is logical (h1→h2→h3)
- [ ] Lists use ul/ol/li elements
- [ ] Tables use proper structure (if applicable)

---

## 🆘 Common Mistakes to Avoid

### ❌ Don't
```html
<!-- Placeholder as only label -->
<input type="text" placeholder="Email">

<!-- Div instead of button -->
<div onclick="submit()">Submit</div>

<!-- Vague link text -->
<a href="/event/1">Click here</a>

<!-- Color-only indicators -->
<span style="color: red;">*</span>

<!-- Removing focus outline -->
button:focus { outline: none; }
```

### ✅ Do
```html
<!-- Label with placeholder -->
<label for="email" class="sr-only">Email address</label>
<input type="text" id="email" placeholder="your.email@example.com">

<!-- Semantic button -->
<button type="submit">Submit form</button>

<!-- Descriptive link -->
<a href="/event/1" aria-label="View details for Halloween Bash 2025">
    View details
</a>

<!-- Text + visual indicator -->
<span class="text-red-500" aria-label="required">*</span>

<!-- Custom focus styles -->
button:focus {
    outline: 3px solid #f97316;
    outline-offset: 2px;
}
```

---

## 📞 Getting Help

- **WCAG Reference:** https://www.w3.org/WAI/WCAG21/quickref/
- **WebAIM Guides:** https://webaim.org/resources/
- **Ask questions:** File issues in the project repo with "accessibility" label

---

## ⏱️ Time Investment Summary

| Fix | Time | Impact |
|-----|------|--------|
| Form labels | 30 min | Critical |
| Skip navigation | 10 min | High |
| Mobile menu | 20 min | High |
| Card semantics | 30 min | High |
| Focus indicators | 15 min | High |
| **Total** | **~2 hours** | **Major improvement** |

Implementing these 5 critical fixes will take approximately 2 hours and will dramatically improve accessibility for keyboard and screen reader users.

---

**Start here, test often, iterate continuously!** 🎃
