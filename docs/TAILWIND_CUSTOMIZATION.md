# Tailwind CSS Customization Guide

**For developers with CSS knowledge coming from Bootstrap/flat HTML backgrounds**

---

## What's Different from Bootstrap?

### Bootstrap Approach (What You're Used To)
```html
<!-- Bootstrap: Predefined component classes -->
<button class="btn btn-primary btn-lg">Click Me</button>
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Title</h5>
  </div>
</div>
```

### Tailwind Approach (Utility-First)
```html
<!-- Tailwind: Compose styles from utility classes -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click Me
</button>
<div class="bg-white rounded-lg shadow-lg p-6">
  <h5 class="text-xl font-bold">Title</h5>
</div>
```

**Key Difference**: Bootstrap gives you components. Tailwind gives you atomic utilities to build your own.

---

## How Tailwind Works in This Project

### The Build Process

```
tailwind-input.css  →  [Tailwind Build]  →  tailwind-output.css  →  [Browser]
   (Source)                                    (Generated)
```

1. **You edit**: `static/css/tailwind-input.css`
2. **Tailwind scans**: All `.html` files in `templates/`
3. **Tailwind generates**: `static/css/tailwind-output.css` with only the classes you use
4. **Browser loads**: The generated CSS file

**Important**: Never edit `tailwind-output.css` directly! It gets overwritten on every build.

### File Structure

```
SpookyOctober/
├── static/
│   └── css/
│       ├── tailwind-input.css    ← Edit this (your custom CSS)
│       └── tailwind-output.css   ← Generated (don't touch)
├── templates/
│   ├── base.html                 ← Use Tailwind classes here
│   ├── home.html
│   └── ...
├── tailwind.config.js            ← Configure colors, fonts, etc.
└── package.json                  ← Build commands
```

---

## Customizing Colors (Like Bootstrap $variables)

### In Bootstrap (Sass Variables)
```scss
// _variables.scss
$primary: #FF6600;
$secondary: #6B2D6B;
```

### In Tailwind (tailwind.config.js)
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'pumpkin': '#FF6600',      // Use: bg-pumpkin, text-pumpkin
        'midnight': '#1a1a1a',     // Use: bg-midnight, text-midnight
        'spooky-purple': '#6B2D6B', // Use: bg-spooky-purple
      },
    },
  },
}
```

**Using Your Custom Colors:**
```html
<div class="bg-pumpkin text-midnight">
  <p class="text-spooky-purple">Halloween vibes!</p>
</div>
```

### Adding More Colors

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      'pumpkin': '#FF6600',
      'midnight': '#1a1a1a',
      'spooky-purple': '#6B2D6B',
      // Add your custom colors here:
      'ghost-white': '#F8F8FF',
      'blood-red': '#8B0000',
      'witch-green': '#228B22',
    },
  },
}
```

After editing `tailwind.config.js`, rebuild CSS:
```bash
make css
```

---

## Creating Reusable Components (Like Bootstrap .btn)

### The Problem
Writing this everywhere gets tedious:
```html
<button class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded transition duration-300">
  Click Me
</button>
```

### The Solution: Create Component Classes

Edit `static/css/tailwind-input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  /* Primary button - like Bootstrap .btn-primary */
  .btn-primary {
    @apply bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded transition duration-300;
  }

  /* Secondary button */
  .btn-secondary {
    @apply bg-purple-800 hover:bg-purple-900 text-white font-bold py-2 px-4 rounded transition duration-300;
  }

  /* Card component - like Bootstrap .card */
  .card {
    @apply bg-white rounded-lg shadow-lg p-6;
  }

  /* Your custom component */
  .spooky-badge {
    @apply inline-block bg-pumpkin text-white text-xs font-bold px-2 py-1 rounded-full;
  }
}
```

**Now use them like Bootstrap:**
```html
<button class="btn-primary">Primary Action</button>
<button class="btn-secondary">Secondary Action</button>

<div class="card">
  <h3>Card Title</h3>
  <span class="spooky-badge">New</span>
</div>
```

---

## Common Customizations

### 1. Custom Fonts

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        'creepster': ['Creepster', 'cursive'],
        'halloween': ['Nosifer', 'cursive'],
      },
    },
  },
}
```

```html
<!-- Usage -->
<h1 class="font-creepster text-4xl">Spooky Title</h1>
```

Don't forget to load fonts in `templates/base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=Creepster&family=Nosifer&display=swap" rel="stylesheet">
```

### 2. Custom Spacing

```javascript
// tailwind.config.js
theme: {
  extend: {
    spacing: {
      '128': '32rem',  // Use: p-128, m-128, w-128
      '144': '36rem',
    },
  },
}
```

### 3. Custom Breakpoints (Like Bootstrap Grid)

```javascript
// tailwind.config.js
theme: {
  screens: {
    'xs': '475px',
    'sm': '640px',   // Default
    'md': '768px',   // Default
    'lg': '1024px',  // Default
    'xl': '1280px',  // Default
    '2xl': '1536px', // Default
    '3xl': '1920px', // Custom
  },
}
```

```html
<!-- Usage: Show on mobile, hide on desktop -->
<div class="block lg:hidden">Mobile Menu</div>
<div class="hidden lg:block">Desktop Menu</div>
```

### 4. Custom Shadows

```javascript
// tailwind.config.js
theme: {
  extend: {
    boxShadow: {
      'spooky': '0 10px 30px -15px rgba(255, 102, 0, 0.5)',
      'glow': '0 0 20px rgba(255, 102, 0, 0.8)',
    },
  },
}
```

```html
<div class="shadow-spooky">Spooky card</div>
<button class="shadow-glow">Glowing button</button>
```

### 5. Custom Animations

```javascript
// tailwind.config.js
theme: {
  extend: {
    animation: {
      'float': 'float 3s ease-in-out infinite',
      'wiggle': 'wiggle 1s ease-in-out infinite',
    },
    keyframes: {
      float: {
        '0%, 100%': { transform: 'translateY(0)' },
        '50%': { transform: 'translateY(-20px)' },
      },
      wiggle: {
        '0%, 100%': { transform: 'rotate(-3deg)' },
        '50%': { transform: 'rotate(3deg)' },
      },
    },
  },
}
```

```html
<div class="animate-float">👻 Floating ghost</div>
<div class="animate-wiggle">🎃 Wiggling pumpkin</div>
```

---

## Adding Custom CSS (When Tailwind Isn't Enough)

Sometimes you need custom CSS that doesn't fit into utility classes:

```css
/* static/css/tailwind-input.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

/* Your custom CSS */
@layer base {
  /* Global element styling */
  body {
    @apply bg-gray-50;
  }

  h1 {
    @apply text-4xl font-bold mb-4;
  }
}

@layer components {
  /* Complex component with pseudo-elements */
  .halloween-card::before {
    content: "🎃";
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 2rem;
  }

  /* Hover effects that need multiple states */
  .ghost-hover {
    @apply transition-all duration-300;
  }

  .ghost-hover:hover {
    @apply transform scale-110;
    filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
  }
}

@layer utilities {
  /* Custom utility classes */
  .text-shadow-glow {
    text-shadow: 0 0 10px rgba(255, 102, 0, 0.8);
  }
}
```

---

## Development Workflow

### Option 1: Manual Build (Like Compiling Sass)
```bash
make css
# Or: npm run build:css
```

Use this when:
- Making config changes (`tailwind.config.js`)
- Adding new component classes
- Before committing code

### Option 2: Watch Mode (Live Reload)
```bash
make css-watch
# Or: npm run watch:css
```

**Leave this running in a terminal while you develop!**

Changes to templates or CSS → Automatic rebuild → Refresh browser

### Full Development Setup
```bash
# Terminal 1: Django server
make run

# Terminal 2: Tailwind watcher
make css-watch
```

---

## Common Tailwind Utilities (Quick Reference)

### Layout
```html
<!-- Flexbox (like Bootstrap d-flex) -->
<div class="flex justify-between items-center">

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">

<!-- Container (like Bootstrap .container) -->
<div class="container mx-auto px-4">
```

### Spacing
```html
<!-- Padding: p-4 = 1rem = 16px -->
<div class="p-4">           <!-- all sides -->
<div class="px-4 py-2">     <!-- x=horizontal, y=vertical -->
<div class="pt-4 pb-2">     <!-- top/bottom individually -->

<!-- Margin: same pattern as padding -->
<div class="m-4 mx-auto">
```

### Typography
```html
<!-- Size -->
<p class="text-sm">Small</p>
<p class="text-base">Normal</p>
<p class="text-lg">Large</p>
<p class="text-2xl">2X Large</p>

<!-- Weight -->
<p class="font-normal">Normal</p>
<p class="font-bold">Bold</p>

<!-- Color -->
<p class="text-gray-900">Dark gray</p>
<p class="text-pumpkin">Custom color</p>
```

### Colors
```html
<!-- Background -->
<div class="bg-gray-100">Light gray bg</div>
<div class="bg-pumpkin">Custom color</div>

<!-- Hover states -->
<button class="bg-blue-500 hover:bg-blue-700">
```

### Responsive Design
```html
<!-- Mobile first: Default → then override at breakpoints -->
<div class="text-sm md:text-base lg:text-lg xl:text-xl">
  Small on mobile, larger on desktop
</div>

<!-- Hidden on mobile, show on desktop -->
<div class="hidden lg:block">Desktop only</div>
```

---

## Debugging Tips

### 1. Class Not Working?

**Check if it exists in output:**
```bash
grep "your-class" static/css/tailwind-output.css
```

If not found:
- Did you rebuild? (`make css`)
- Is the class used in a `.html` file in `templates/`?
- Check `tailwind.config.js` → `content` paths

### 2. See What Classes Are Available

Open `static/css/tailwind-output.css` and search for patterns:
```css
.bg-pumpkin { background-color: #FF6600; }
.text-pumpkin { color: #FF6600; }
.border-pumpkin { border-color: #FF6600; }
```

### 3. Inspect in Browser

Use DevTools to see computed styles:
1. Right-click element → Inspect
2. See which Tailwind classes are applied
3. Check if your custom class is loaded

### 4. Purge Issues (Production)

If classes work locally but not in production:
- Ensure `collectstatic` ran after CSS build
- Check Heroku build logs for CSS compilation
- Verify `templates/` are committed to git

---

## Migration Guide: Bootstrap → Tailwind

| Bootstrap | Tailwind Equivalent |
|-----------|---------------------|
| `.container` | `.container .mx-auto .px-4` |
| `.row` | `.flex` or `.grid` |
| `.col-md-6` | `.md:w-1/2` or `.grid .grid-cols-2` |
| `.btn .btn-primary` | `.btn-primary` (custom component) |
| `.card` | `.card` (custom component) |
| `.text-center` | `.text-center` |
| `.mt-3` | `.mt-3` (similar spacing scale) |
| `.d-flex` | `.flex` |
| `.justify-content-between` | `.justify-between` |
| `.align-items-center` | `.items-center` |
| `.bg-primary` | `.bg-blue-500` or `.bg-pumpkin` |
| `.text-danger` | `.text-red-600` |
| `.rounded` | `.rounded` |
| `.shadow` | `.shadow-lg` |
| `.d-none .d-md-block` | `.hidden .md:block` |

---

## Best Practices

### 1. Use @apply for Repeated Patterns
```css
/* Don't repeat this everywhere: */
<button class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded">

/* Instead, create a component: */
@layer components {
  .btn-primary {
    @apply bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded;
  }
}
```

### 2. Keep Utilities for One-Offs
```html
<!-- Component for common pattern -->
<div class="card">
  <!-- Utilities for unique spacing -->
  <h3 class="mb-6">Title</h3>
  <p class="text-sm text-gray-600">Description</p>
</div>
```

### 3. Mobile-First Responsive Design
```html
<!-- Good: Mobile first, then enhance -->
<div class="text-sm md:text-base lg:text-lg">

<!-- Avoid: Desktop first -->
<div class="text-lg md:text-base sm:text-sm">
```

### 4. Use Semantic HTML + Tailwind
```html
<!-- Good: Semantic + styled -->
<nav class="bg-gray-900 text-white">
  <ul class="flex space-x-4">
    <li><a href="/" class="hover:text-pumpkin">Home</a></li>
  </ul>
</nav>

<!-- Avoid: Div soup -->
<div class="bg-gray-900 text-white">
  <div class="flex space-x-4">
    <div><div class="hover:text-pumpkin">Home</div></div>
  </div>
</div>
```

---

## Resources

### Official Docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Configuration**: https://tailwindcss.com/docs/configuration
- **Customization**: https://tailwindcss.com/docs/theme

### Tailwind Tools
- **Tailwind Play**: https://play.tailwindcss.com/ (online playground)
- **Color Generator**: https://uicolors.app/create
- **Component Libraries**:
  - Tailwind UI (paid): https://tailwindui.com/
  - Flowbite (free): https://flowbite.com/
  - DaisyUI (free): https://daisyui.com/

### Learning
- **Tailwind in 100 Seconds**: https://www.youtube.com/watch?v=mr15Xzb1Ook
- **Adam Wathan's YouTube**: Creator of Tailwind (screencasts)

---

## Quick Start Checklist

1. ✅ Understand the build process (`input.css` → `output.css`)
2. ✅ Know where to edit (`tailwind-input.css` and `tailwind.config.js`)
3. ✅ Learn utility class naming (`bg-`, `text-`, `p-`, `m-`, etc.)
4. ✅ Create custom components with `@apply` for reusable patterns
5. ✅ Use `make css-watch` during development
6. ✅ Check browser DevTools to debug classes
7. ✅ Think mobile-first for responsive design

**You're ready to customize! Start with `tailwind.config.js` for colors, then create components in `tailwind-input.css`.** 🎃
