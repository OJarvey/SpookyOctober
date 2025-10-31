# ShriekedIn Accessibility Audit & Implementation Plan

**Date:** October 31, 2025
**Auditor:** Claude Code
**WCAG Target:** Level AA (2.1)

---

## Executive Summary

This audit evaluates the ShriekedIn platform against WCAG 2.1 Level AA standards. The site has a solid foundation with semantic HTML in places, but requires significant improvements to meet accessibility standards. Priority issues include missing ARIA labels, insufficient keyboard navigation support, unlabeled form controls, and inadequate screen reader announcements.

**Current Compliance Estimate:** ~40% WCAG AA compliant
**Target Compliance:** 95%+ WCAG AA compliant

---

## Critical Issues (Priority 1)

### 1. Form Control Labels
**WCAG Criterion:** 1.3.1 Info and Relationships, 2.4.6 Headings and Labels, 3.3.2 Labels or Instructions

**Issues Found:**
- Search inputs throughout the site use placeholders without proper labels
- Select dropdowns in filter sections lack labels
- Users relying on screen readers cannot identify form control purposes

**Files Affected:**
- `templates/events_list.html` (lines 47-62)
- `templates/businesses_list.html` (search section)
- `templates/haunted_places.html` (search section)

**Impact:** High - Forms are completely unusable for screen reader users

**Solution:**
```html
<!-- BEFORE (inaccessible) -->
<input type="text" id="events-search-input" placeholder="Search events...">
<select class="...">
    <option value="">All Categories</option>
</select>

<!-- AFTER (accessible) -->
<label for="events-search-input" class="sr-only">Search events</label>
<input type="text"
       id="events-search-input"
       placeholder="Search events..."
       aria-describedby="search-hint">
<span id="search-hint" class="sr-only">Enter keywords to search for Halloween events</span>

<label for="category-filter" class="sr-only">Filter by category</label>
<select id="category-filter"
        name="category"
        aria-label="Event category filter"
        class="...">
    <option value="">All Categories</option>
</select>
```

**Implementation Steps:**
1. Add `.sr-only` utility class to Tailwind CSS for visually hidden labels
2. Add `<label>` elements for all form controls
3. Add `aria-describedby` for additional context where needed
4. Test with NVDA/JAWS/VoiceOver

**Estimated Time:** 3-4 hours

---

### 2. Keyboard Navigation & Focus Management
**WCAG Criterion:** 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.4.7 Focus Visible

**Issues Found:**
- Mobile menu toggle lacks keyboard accessibility
- No visible focus indicators for all interactive elements
- No skip navigation link for keyboard users
- Tab order may be illogical in complex layouts

**Files Affected:**
- `templates/base.html` (lines 50-91)
- `static/css/tailwind-output.css` (focus styles)

**Impact:** High - Keyboard-only users cannot navigate the site effectively

**Solution:**
```html
<!-- Add skip navigation link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Improve mobile menu button -->
<button id="mobile-menu-button"
        class="md:hidden text-white focus:outline-none"
        aria-expanded="false"
        aria-controls="mobile-menu"
        aria-label="Toggle navigation menu">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
    </svg>
</button>

<!-- Mobile menu with proper attributes -->
<nav id="mobile-menu"
     class="hidden md:hidden pb-4"
     aria-label="Mobile navigation">
    <!-- menu items -->
</nav>
```

**CSS for Focus Indicators:**
```css
/* Add to Tailwind config or custom CSS */
.skip-link {
    position: absolute;
    left: -9999px;
    z-index: 999;
}

.skip-link:focus {
    left: 50%;
    transform: translateX(-50%);
    top: 0;
    padding: 1rem 2rem;
    background: #fff;
    color: #000;
    text-decoration: none;
    border: 2px solid #f97316;
    border-radius: 0 0 0.5rem 0.5rem;
}

/* Enhanced focus styles */
a:focus, button:focus, input:focus, select:focus, textarea:focus {
    outline: 3px solid #f97316;
    outline-offset: 2px;
}

/* Remove default outline and use custom ring */
.btn-primary:focus, .btn-secondary:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.5);
}
```

**Implementation Steps:**
1. Add skip navigation link to base template
2. Update mobile menu button with ARIA attributes
3. Add JavaScript to toggle aria-expanded state
4. Implement custom focus indicators
5. Test keyboard navigation flow through all pages

**Estimated Time:** 4-5 hours

---

### 3. ARIA Labels for Interactive Elements
**WCAG Criterion:** 4.1.2 Name, Role, Value

**Issues Found:**
- Buttons lack descriptive labels (e.g., "Search" button needs context)
- Icon-only buttons have no text alternatives
- Links with vague text ("Click here", "#")
- Status indicators (Featured, Verified badges) lack screen reader text

**Files Affected:**
- All list page templates
- `templates/dashboard.html` (management cards)
- `templates/base.html` (navigation)

**Impact:** High - Screen readers cannot communicate button/link purposes

**Solution:**
```html
<!-- Icon buttons -->
<button class="btn-primary px-6 py-2"
        aria-label="Search for Halloween events">
    Search
</button>

<!-- Featured badge -->
<span class="absolute top-3 right-3 text-4xl"
      aria-label="Featured event"
      role="img">⭐</span>

<!-- Verified badge -->
<span class="bg-green-100 text-green-800 px-2 py-1 rounded"
      role="status"
      aria-label="Verified business">
    ✅ Verified
</span>

<!-- Card links -->
<a href="{% url 'core:event_detail' event.id %}"
   class="..."
   aria-label="View details for {{ event.title }}">
    View Details →
</a>

<!-- Decorative emoji -->
<span class="text-6xl" aria-hidden="true">🎃</span>
```

**Implementation Steps:**
1. Audit all interactive elements (buttons, links, form controls)
2. Add aria-label or aria-labelledby to elements lacking descriptive text
3. Add aria-hidden="true" to decorative elements
4. Use role="img" with aria-label for meaningful emoji
5. Test with screen reader to verify announcements

**Estimated Time:** 5-6 hours

---

### 4. Semantic HTML & Landmarks
**WCAG Criterion:** 1.3.1 Info and Relationships, 2.4.1 Bypass Blocks

**Issues Found:**
- Overuse of `<div>` instead of semantic elements
- Missing or incorrect ARIA landmarks
- Cards should use `<article>` elements
- Search sections should be wrapped in `<form>` or `<search>` landmarks

**Files Affected:**
- All template files

**Impact:** Medium-High - Screen reader users lose document structure navigation

**Solution:**
```html
<!-- Use semantic HTML5 elements -->
<main id="main-content">
    <section aria-labelledby="events-heading">
        <h2 id="events-heading">Halloween Events</h2>

        <!-- Search as form with search role -->
        <form role="search"
              method="GET"
              aria-label="Search and filter events">
            <div class="flex gap-4">
                <!-- form controls -->
            </div>
        </form>

        <!-- Event cards as articles -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <article class="event-card" aria-labelledby="event-{{ event.id }}-title">
                <h3 id="event-{{ event.id }}-title">{{ event.title }}</h3>
                <!-- event content -->
            </article>
        </div>
    </section>
</main>

<!-- Sidebar content -->
<aside aria-label="Additional information">
    <!-- sidebar content -->
</aside>
```

**Implementation Steps:**
1. Replace generic divs with semantic elements (article, section, aside, nav)
2. Add ARIA landmarks where HTML5 semantics aren't sufficient
3. Add id attributes to section headings and use aria-labelledby
4. Wrap search interfaces in form/search elements
5. Validate HTML structure

**Estimated Time:** 6-8 hours

---

## High Priority Issues (Priority 2)

### 5. Dynamic Content Announcements
**WCAG Criterion:** 4.1.3 Status Messages

**Issues Found:**
- Search results update without screen reader announcement
- Filter changes don't announce result count changes
- Success/error messages may not be properly announced
- Loading states not communicated

**Solution:**
```html
<!-- Live region for search results -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
    <span id="search-status"></span>
</div>

<!-- Stats with proper announcement -->
<div class="bg-gradient-to-r from-orange-100 to-purple-100 rounded-lg p-4 mb-8 text-center"
     role="status"
     aria-live="polite">
    <p class="text-gray-700">
        <strong>{{ events.count }}</strong> event{{ events.count|pluralize }} found
    </p>
</div>

<!-- Loading state -->
<div role="status" aria-live="polite" aria-busy="true" class="sr-only">
    <span>Loading events...</span>
</div>
```

**JavaScript Updates:**
```javascript
// Update search status for screen readers
function updateSearchStatus(count) {
    const status = document.getElementById('search-status');
    status.textContent = `${count} events found`;
}

// Announce filter changes
function announceFilterChange(filterType, value) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = `Filter applied: ${filterType} set to ${value}`;
    document.body.appendChild(announcement);

    setTimeout(() => announcement.remove(), 1000);
}
```

**Estimated Time:** 4-5 hours

---

### 6. Color Contrast Compliance
**WCAG Criterion:** 1.4.3 Contrast (Minimum)

**Issues Found (Potential):**
- Orange/purple gradient text on colored backgrounds
- Gray text on light backgrounds
- Link colors in certain contexts
- Button text contrast on gradient backgrounds

**Testing Required:**
- Use WebAIM Contrast Checker
- Test all text/background combinations
- Verify links have 3:1 contrast with surrounding text

**Solution Approach:**
```css
/* Ensure minimum 4.5:1 contrast for normal text */
/* Ensure minimum 3:1 contrast for large text (18pt+) */

/* Example fixes */
.text-gray-600 {
    /* If on white: #4B5563 has 7.1:1 ratio - PASS */
}

.text-orange-200 {
    /* On purple-800 background may fail - test and adjust */
    /* May need to use orange-100 or white for sufficient contrast */
}

/* Links need 3:1 contrast with surrounding text */
a {
    color: #9333EA; /* purple-700 for better contrast */
    text-decoration: underline; /* Don't rely on color alone */
}
```

**Implementation Steps:**
1. Install browser extension for contrast checking (e.g., axe DevTools)
2. Check all text/background color combinations
3. Update Tailwind color classes where contrast fails
4. Ensure links are distinguishable by more than color
5. Document color palette with contrast ratios

**Estimated Time:** 3-4 hours

---

### 7. Form Validation & Error Handling
**WCAG Criterion:** 3.3.1 Error Identification, 3.3.3 Error Suggestion, 3.3.4 Error Prevention

**Issues Found:**
- Contact form errors could be more descriptive
- Error messages may not be associated with form controls
- No summary of errors at form top
- Required fields indicated only by color

**Files Affected:**
- `templates/contact.html`
- `templates/login.html`
- `core/forms.py`

**Solution:**
```html
<!-- Error summary at top of form -->
{% if form.errors %}
<div role="alert"
     class="bg-red-100 border-l-4 border-red-500 p-4 mb-6"
     aria-labelledby="form-errors-heading">
    <h3 id="form-errors-heading" class="font-bold text-red-800 mb-2">
        Please correct the following errors:
    </h3>
    <ul class="list-disc list-inside text-red-700">
        {% for field in form %}
            {% for error in field.errors %}
                <li><a href="#{{ field.id_for_label }}">{{ field.label }}: {{ error }}</a></li>
            {% endfor %}
        {% endfor %}
    </ul>
</div>
{% endif %}

<!-- Form field with proper error association -->
<div class="mb-6">
    <label for="{{ form.email.id_for_label }}" class="block text-gray-700 font-bold mb-2">
        Email Address <span class="text-red-500" aria-label="required">*</span>
    </label>
    {{ form.email }}
    {% if form.email.errors %}
        <div id="{{ form.email.id_for_label }}-error"
             class="text-red-600 text-sm mt-2"
             role="alert">
            {% for error in form.email.errors %}
                <p>{{ error }}</p>
            {% endfor %}
        </div>
    {% endif %}
</div>
```

**Update form field rendering:**
```python
# In forms.py, add aria-invalid and aria-describedby
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
        field.widget.attrs['aria-required'] = 'true' if field.required else 'false'
        if self.errors.get(field_name):
            field.widget.attrs['aria-invalid'] = 'true'
            field.widget.attrs['aria-describedby'] = f'{field_name}-error'
```

**Estimated Time:** 4-5 hours

---

## Medium Priority Issues (Priority 3)

### 8. Heading Hierarchy
**WCAG Criterion:** 1.3.1 Info and Relationships, 2.4.6 Headings and Labels

**Action Required:**
- Audit all headings on each page
- Ensure logical hierarchy (h1 → h2 → h3, no skipping)
- Verify only one h1 per page
- Add heading levels where sections lack them

**Estimated Time:** 2-3 hours

---

### 9. Link Purpose & Context
**WCAG Criterion:** 2.4.4 Link Purpose (In Context)

**Action Required:**
- Replace vague link text ("Click here", "Read more") with descriptive text
- Add aria-label to links where context is unclear
- Remove placeholder "#" href attributes
- Indicate when links open in new windows

**Estimated Time:** 2-3 hours

---

### 10. Images & Alternative Text
**WCAG Criterion:** 1.1.1 Non-text Content

**Action Required:**
- Add aria-hidden="true" to all decorative emoji
- Add aria-label to emoji conveying information
- Add alt text if moving from emoji to actual images
- Describe gradient placeholder purpose in event cards

**Estimated Time:** 2-3 hours

---

### 11. Tables (If Added)
**WCAG Criterion:** 1.3.1 Info and Relationships

**Action Required (for future table additions):**
- Use proper table markup (thead, tbody, th, td)
- Associate headers with data cells using scope or headers/id
- Add caption or aria-label to describe table purpose

**Estimated Time:** N/A (implement when tables are added)

---

### 12. Responsive Design & Zoom
**WCAG Criterion:** 1.4.4 Resize Text, 1.4.10 Reflow

**Action Required:**
- Test at 200% zoom
- Ensure no horizontal scrolling at mobile widths
- Verify text doesn't overflow containers
- Test with browser zoom and OS text size adjustments

**Estimated Time:** 2-3 hours

---

## Low Priority Issues (Priority 4)

### 13. Language Attributes
**WCAG Criterion:** 3.1.1 Language of Page

**Current Status:** html lang="en" is present in base.html ✅

**Action Required:**
- Add lang attributes to content in other languages (if any)

**Estimated Time:** 1 hour

---

### 14. Page Titles
**WCAG Criterion:** 2.4.2 Page Titled

**Current Status:** All pages have descriptive titles ✅

**Enhancement:**
- Consider adding page context to titles (e.g., "Search Results (15 found) - Events - ShriekedIn")

**Estimated Time:** 1-2 hours

---

### 15. Consistent Navigation
**WCAG Criterion:** 3.2.3 Consistent Navigation

**Current Status:** Navigation is consistent across pages ✅

**Action Required:**
- Maintain consistency as new pages are added
- Document navigation structure

**Estimated Time:** 1 hour

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Week 1-2)
**Goal:** Achieve 70% compliance, fix blocking issues

1. Add form control labels to all search interfaces (Priority 1.1)
2. Implement keyboard navigation improvements (Priority 1.2)
3. Add ARIA labels to interactive elements (Priority 1.3)
4. Improve semantic HTML structure (Priority 1.4)

**Total Time:** 18-23 hours

---

### Phase 2: High Priority Fixes (Week 3)
**Goal:** Achieve 85% compliance

5. Add dynamic content announcements (Priority 2.5)
6. Fix color contrast issues (Priority 2.6)
7. Improve form validation accessibility (Priority 2.7)

**Total Time:** 11-14 hours

---

### Phase 3: Medium Priority Fixes (Week 4)
**Goal:** Achieve 95% compliance

8. Audit and fix heading hierarchy (Priority 3.8)
9. Improve link purpose/context (Priority 3.9)
10. Add proper image alternatives (Priority 3.10)
11. Test responsive design (Priority 3.12)

**Total Time:** 8-12 hours

---

### Phase 4: Polishing (Week 5)
**Goal:** Achieve 95%+ compliance

12. Final testing with screen readers
13. Address any remaining issues
14. Create accessibility documentation
15. Train team on accessibility standards

**Total Time:** 8-10 hours

---

## Testing Strategy

### Automated Testing Tools
1. **axe DevTools** (Browser Extension)
   - Run on every page
   - Fix all Critical and Serious issues

2. **WAVE** (Web Accessibility Evaluation Tool)
   - Secondary validation
   - Check for missed issues

3. **Lighthouse** (Chrome DevTools)
   - Accessibility audit score
   - Performance impact check

### Manual Testing
1. **Keyboard Navigation**
   - Tab through all interactive elements
   - Test all functionality without mouse
   - Verify focus indicators are visible

2. **Screen Reader Testing**
   - **NVDA** (Windows) - Primary testing
   - **JAWS** (Windows) - Secondary validation
   - **VoiceOver** (Mac) - macOS validation
   - **TalkBack** (Android) - Mobile validation

3. **Browser Testing**
   - Chrome, Firefox, Safari, Edge
   - Test at different zoom levels
   - Test with browser accessibility features

4. **User Testing**
   - Recruit users with disabilities
   - Observe real usage patterns
   - Collect feedback on pain points

---

## Code Templates & Utilities

### Screen Reader Only CSS Class
```css
/* Add to Tailwind config or custom CSS */
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

.sr-only-focusable:focus {
    position: static;
    width: auto;
    height: auto;
    padding: 0;
    margin: 0;
    overflow: visible;
    clip: auto;
    white-space: normal;
}
```

### JavaScript Utilities
```javascript
// accessibility.js

/**
 * Announce message to screen readers
 */
function announceToScreenReader(message, priority = 'polite') {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;

    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
}

/**
 * Trap focus within modal/dialog
 */
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                lastFocusable.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                firstFocusable.focus();
                e.preventDefault();
            }
        }
    });
}

/**
 * Update ARIA expanded state
 */
function toggleAriaExpanded(button) {
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', !isExpanded);
}
```

---

## Accessibility Statement Template

Create `templates/accessibility.html`:

```html
{% extends 'base.html' %}

{% block title %}Accessibility Statement - ShriekedIn{% endblock %}

{% block content %}
<section class="py-16 bg-white">
    <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl font-bold mb-8">Accessibility Statement</h1>

            <p class="mb-4">
                ShriekedIn is committed to ensuring digital accessibility for people with disabilities.
                We are continually improving the user experience for everyone and applying the relevant
                accessibility standards.
            </p>

            <h2 class="text-2xl font-bold mt-8 mb-4">Conformance Status</h2>
            <p class="mb-4">
                The Web Content Accessibility Guidelines (WCAG) define requirements for designers and
                developers to improve accessibility for people with disabilities. It defines three levels
                of conformance: Level A, Level AA, and Level AAA. ShriekedIn is partially conformant with
                WCAG 2.1 level AA. Partially conformant means that some parts of the content do not fully
                conform to the accessibility standard.
            </p>

            <h2 class="text-2xl font-bold mt-8 mb-4">Feedback</h2>
            <p class="mb-4">
                We welcome your feedback on the accessibility of ShriekedIn. Please let us know if you
                encounter accessibility barriers:
            </p>
            <ul class="list-disc ml-8 mb-4">
                <li>E-mail: <a href="mailto:accessibility@shrieked.in" class="text-purple-600 underline">accessibility@shrieked.in</a></li>
                <li>Contact Form: <a href="{% url 'core:contact' %}" class="text-purple-600 underline">Contact Us</a></li>
            </ul>

            <h2 class="text-2xl font-bold mt-8 mb-4">Technical Specifications</h2>
            <p class="mb-4">
                Accessibility of ShriekedIn relies on the following technologies to work:
            </p>
            <ul class="list-disc ml-8 mb-4">
                <li>HTML5</li>
                <li>WAI-ARIA</li>
                <li>CSS</li>
                <li>JavaScript</li>
            </ul>

            <p class="text-sm text-gray-600 mt-8">
                This statement was last updated on October 31, 2025.
            </p>
        </div>
    </div>
</section>
{% endblock %}
```

---

## Success Metrics

### Quantitative Metrics
- **Lighthouse Accessibility Score:** Target 95+ (currently ~60)
- **axe DevTools Issues:** 0 Critical, 0 Serious
- **WAVE Errors:** 0 errors, <5 alerts
- **Keyboard Navigation:** 100% of features accessible
- **Screen Reader Compatibility:** All content accessible

### Qualitative Metrics
- User feedback from people with disabilities
- Time to complete common tasks (compare before/after)
- Support tickets related to accessibility (should decrease)

---

## Maintenance & Ongoing Compliance

### Developer Guidelines
1. Run accessibility checks before every PR merge
2. Test keyboard navigation for new features
3. Include ARIA labels in initial implementation
4. Use semantic HTML by default
5. Test with screen reader for complex components

### Regular Audits
- **Monthly:** Quick automated scan with axe/WAVE
- **Quarterly:** Full manual keyboard/screen reader testing
- **Annually:** Professional accessibility audit

### Training
- Onboard new developers with accessibility training
- Share WCAG guidelines and best practices
- Review accessibility issues in code reviews

---

## Resources

### WCAG Guidelines
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Resources](https://webaim.org/resources/)

### Testing Tools
- [axe DevTools Browser Extension](https://www.deque.com/axe/devtools/)
- [WAVE Browser Extension](https://wave.webaim.org/extension/)
- [Lighthouse (Chrome DevTools)](https://developers.google.com/web/tools/lighthouse)

### Screen Readers
- [NVDA (Free, Windows)](https://www.nvaccess.org/)
- [JAWS (Paid, Windows)](https://www.freedomscientific.com/products/software/jaws/)
- [VoiceOver (Built-in, Mac/iOS)](https://www.apple.com/accessibility/voiceover/)

### Contrast Checkers
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)

---

## Conclusion

Implementing these accessibility improvements will make ShriekedIn usable by a significantly larger audience, including people with disabilities. The estimated total implementation time is 45-59 hours, spread across 4-5 weeks. The critical issues should be addressed immediately as they prevent screen reader users from using core features.

**Next Steps:**
1. Review and approve this implementation plan
2. Begin Phase 1 (Critical Fixes)
3. Set up automated testing in CI/CD pipeline
4. Schedule regular accessibility audits

---

**Questions or concerns?** Contact the development team or file an issue in the project repository.
