# Parchment Effect CSS Tutorial

## Overview

This guide explains how we created an aged parchment document effect for the haunted place detail pages. The effect makes content look like it's written on old, weathered paper with a handwritten font.

**Live Example:** https://shriekedin.uk/haunted/1/

---

## Table of Contents

1. [Typography - The Handwritten Font](#1-typography---the-handwritten-font)
2. [Background - Creating Aged Paper](#2-background---creating-aged-paper)
3. [Borders - Framing the Document](#3-borders---framing-the-document)
4. [Texture - Adding Age Spots](#4-texture---adding-age-spots)
5. [Shadows - Creating Depth](#5-shadows---creating-depth)
6. [Final Touches](#6-final-touches)

---

## 1. Typography - The Handwritten Font

**Goal:** Make text look handwritten or typewritten on old paper.

### Step 1: Add Google Font

In your HTML `<head>`, import the font:

```html
<link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">
```

**What is "Special Elite"?**
It's a typewriter-style font that looks like text typed on an old typewriter, perfect for vintage documents.

### Step 2: Apply Font to Text

```css
.parchment-text {
    font-family: 'Special Elite', 'Courier New', monospace;
    color: #3a2a1a;  /* Dark brown ink color */
    line-height: 1.8;  /* Extra space between lines */
    font-size: 1.05rem;  /* Slightly larger for readability */
    letter-spacing: 0.3px;  /* Small gaps between letters */
}
```

**Breaking it down:**
- `font-family` - Uses Special Elite, falls back to Courier New if unavailable
- `color: #3a2a1a` - Dark brown color (like old ink)
- `line-height: 1.8` - Makes text easier to read (80% more space than default)
- `letter-spacing` - Tiny gaps make it look more authentic

---

## 2. Background - Creating Aged Paper

**Goal:** Create a cream-colored paper with subtle color variations.

```css
.parchment-card {
    background: linear-gradient(135deg,
        #f4e8d0 0%,
        #f0e4cc 25%,
        #ede0c8 50%,
        #f2e6ce 75%,
        #f4e8d0 100%);
}
```

**What is a linear-gradient?**
Instead of a single solid color, it smoothly transitions between multiple colors.

**Breaking it down:**
- `135deg` - Diagonal angle (top-left to bottom-right)
- `#f4e8d0`, `#f0e4cc`, etc. - Different shades of cream/tan
- `0%`, `25%`, `50%`, `75%`, `100%` - Where each color appears
- The subtle variation makes paper look aged and uneven

**Visualization:**
```
Top-left     →  Bottom-right
#f4e8d0  →  #f0e4cc  →  #ede0c8  →  #f2e6ce  →  #f4e8d0
```

---

## 3. Borders - Framing the Document

**Goal:** Add a golden-brown border that looks hand-drawn or aged.

```css
.parchment-card {
    border: 2px solid #c4a572;  /* Main border */
    border-radius: 4px;  /* Slightly rounded corners */
}
```

**What's `#c4a572`?**
A golden-brown color that looks like aged metal or leather binding.

### Adding a "Torn Edge" Effect

We use a **pseudo-element** (`::after`) to create a second decorative border:

```css
.parchment-card::after {
    content: '';  /* Empty content (required) */
    position: absolute;  /* Position relative to card */
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    border: 1px dashed rgba(139, 115, 85, 0.2);  /* Dashed line */
    border-radius: 4px;
    pointer-events: none;  /* Don't block mouse clicks */
}
```

**What is `::after`?**
A CSS "pseudo-element" that creates an invisible element you can style. Think of it as adding a second layer on top.

**Breaking it down:**
- `content: ''` - Required for pseudo-elements to appear
- `position: absolute` - Lets us position it exactly where we want
- `top/left/right/bottom: -2px` - Extends 2px beyond the card edges
- `dashed` - Makes a dotted line (torn paper effect)
- `rgba(139, 115, 85, 0.2)` - Brown color with 20% opacity (nearly transparent)
- `pointer-events: none` - Mouse clicks pass through to content below

---

## 4. Texture - Adding Age Spots

**Goal:** Add subtle brown spots like aged paper stains.

```css
.parchment-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        radial-gradient(circle at 20% 30%, rgba(139, 115, 85, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(139, 115, 85, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(139, 115, 85, 0.03) 0%, transparent 50%);
    pointer-events: none;
}
```

**What is `radial-gradient`?**
Creates a circular gradient that fades from center to edge (like a spotlight or spot).

**What is `::before`?**
Like `::after`, but appears *before* the content (underneath).

**Breaking it down:**

Each `radial-gradient` creates one age spot:

```css
radial-gradient(
    circle at 20% 30%,  /* Position: 20% from left, 30% from top */
    rgba(139, 115, 85, 0.05) 0%,  /* Center: brown at 5% opacity */
    transparent 50%  /* Edge: fades to transparent at 50% radius */
)
```

**Layering Multiple Spots:**
- First gradient: Spot at top-left (20% horizontal, 30% vertical)
- Second gradient: Spot at bottom-right (80%, 70%)
- Third gradient: Spot at center (50%, 50%)

These stack on top of each other to create a natural aged look.

---

## 5. Shadows - Creating Depth

**Goal:** Make the card look like real paper with thickness and dimension.

```css
.parchment-card {
    box-shadow:
        0 4px 6px rgba(0, 0, 0, 0.1),  /* Drop shadow */
        inset 0 0 50px rgba(139, 115, 85, 0.1),  /* Inner glow */
        0 0 0 1px rgba(139, 115, 85, 0.2);  /* Thin outline */
}
```

**What is `box-shadow`?**
Creates shadows around or inside an element. You can stack multiple shadows!

**Breaking it down:**

1. **Drop Shadow** - `0 4px 6px rgba(0, 0, 0, 0.1)`
   - `0` - No horizontal offset
   - `4px` - 4px down
   - `6px` - 6px blur radius (soft edge)
   - `rgba(0, 0, 0, 0.1)` - Black at 10% opacity
   - **Effect:** Paper lifts off the background

2. **Inset Shadow** - `inset 0 0 50px rgba(139, 115, 85, 0.1)`
   - `inset` - Shadow appears *inside* the element
   - `0 0` - No offset (centered)
   - `50px` - Large blur (spreads across surface)
   - **Effect:** Aged texture on paper surface

3. **Subtle Outline** - `0 0 0 1px rgba(139, 115, 85, 0.2)`
   - `0 0 0` - No offset, no blur
   - `1px` - Spread radius (creates a line)
   - **Effect:** Very thin brown border outline

---

## 6. Final Touches

### Heading Style

```css
.parchment-heading {
    font-family: 'Special Elite', 'Courier New', monospace;
    color: #2c1810;  /* Darker brown */
    text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.5);
    border-bottom: 2px solid #c4a572;
    padding-bottom: 0.5rem;
}
```

**What is `text-shadow`?**
Adds a shadow behind text.

**Breaking it down:**
- `1px 1px` - Shadow 1px right and 1px down
- `0px` - No blur (sharp edge)
- `rgba(255, 255, 255, 0.5)` - White at 50% opacity
- **Effect:** Creates an embossed or raised look

### Special Highlight (Famous For Section)

```css
.parchment-highlight {
    background: linear-gradient(135deg,
        #fff9e6 0%,
        #fff5dc 50%,
        #fff9e6 100%);
    border-left: 4px solid #d4af37;  /* Gold border */
}
```

Makes one section stand out with lighter paper and gold accent.

---

## Complete Code Structure

```html
<!-- HTML Structure -->
<div class="parchment-container">
    <div class="parchment-card">
        <h2 class="parchment-heading">The Story</h2>
        <div class="parchment-text">
            Story content goes here...
        </div>
    </div>
</div>
```

```css
/* Complete CSS */
.parchment-card {
    /* Background */
    background: linear-gradient(135deg,
        #f4e8d0 0%, #f0e4cc 25%, #ede0c8 50%,
        #f2e6ce 75%, #f4e8d0 100%);

    /* Border */
    border: 2px solid #c4a572;
    border-radius: 4px;

    /* Shadows */
    box-shadow:
        0 4px 6px rgba(0, 0, 0, 0.1),
        inset 0 0 50px rgba(139, 115, 85, 0.1),
        0 0 0 1px rgba(139, 115, 85, 0.2);

    /* Layout */
    padding: 2rem;
    position: relative;
    overflow: hidden;
}

/* Age spots texture */
.parchment-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 20% 30%, rgba(139, 115, 85, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(139, 115, 85, 0.04) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(139, 115, 85, 0.03) 0%, transparent 50%);
    pointer-events: none;
}

/* Torn edge decoration */
.parchment-card::after {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    border: 1px dashed rgba(139, 115, 85, 0.2);
    border-radius: 4px;
    pointer-events: none;
}

/* Typography */
.parchment-text {
    font-family: 'Special Elite', 'Courier New', monospace;
    color: #3a2a1a;
    line-height: 1.8;
    font-size: 1.05rem;
    letter-spacing: 0.3px;
    position: relative;
    z-index: 1;
}

.parchment-heading {
    font-family: 'Special Elite', 'Courier New', monospace;
    color: #2c1810;
    text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.5);
    border-bottom: 2px solid #c4a572;
    padding-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}
```

---

## Key Concepts Explained

### Z-Index

```css
position: relative;
z-index: 1;
```

**What is `z-index`?**
Controls stacking order (what appears on top).

- `z-index: 0` - Background layer (pseudo-elements)
- `z-index: 1` - Text content (appears above spots)

Think of it like layers of paper - higher numbers appear on top.

### Position: Absolute vs Relative

**Relative:**
```css
position: relative;
```
- Element stays in normal document flow
- Can use z-index
- Child elements with `position: absolute` position relative to this parent

**Absolute:**
```css
position: absolute;
```
- Element removed from normal flow
- Positioned relative to nearest `position: relative` ancestor
- Can overlap other content

### RGBA Colors

```css
rgba(139, 115, 85, 0.05)
```

**Breaking it down:**
- `139` - Red value (0-255)
- `115` - Green value (0-255)
- `85` - Blue value (0-255)
- `0.05` - Alpha (opacity, 0-1)

So `rgba(139, 115, 85, 0.05)` is brown at 5% opacity (very transparent).

---

## Customization Tips

### Change Paper Color

Adjust the background gradient values:

```css
/* Lighter paper */
background: linear-gradient(135deg,
    #faf5e8 0%, #f8f3e6 50%, #faf5e8 100%);

/* Darker, older paper */
background: linear-gradient(135deg,
    #e8dcc0 0%, #e0d4b8 50%, #e8dcc0 100%);
```

### More/Fewer Age Spots

Add more `radial-gradient` layers:

```css
background-image:
    radial-gradient(circle at 15% 20%, rgba(139, 115, 85, 0.06) 0%, transparent 40%),
    radial-gradient(circle at 85% 80%, rgba(139, 115, 85, 0.05) 0%, transparent 45%),
    radial-gradient(circle at 45% 60%, rgba(139, 115, 85, 0.04) 0%, transparent 50%),
    radial-gradient(circle at 70% 40%, rgba(139, 115, 85, 0.03) 0%, transparent 55%);
```

### Different Fonts

Try these alternatives to Special Elite:

- `'Courier Prime'` - Cleaner typewriter
- `'Permanent Marker'` - Handwritten marker
- `'Architects Daughter'` - Casual handwriting
- `'Shadows Into Light'` - Elegant script

---

## Browser Compatibility

All techniques used are widely supported:

- ✅ Linear gradients - IE 10+, all modern browsers
- ✅ Radial gradients - IE 10+, all modern browsers
- ✅ Box shadows - IE 9+, all modern browsers
- ✅ Pseudo-elements - IE 8+, all browsers
- ✅ RGBA colors - IE 9+, all modern browsers

---

## Performance Notes

**Efficient:**
- Gradients render faster than images
- No external image files to load
- Pure CSS = fast page loads

**Tip:** For many parchment cards on one page, consider creating a single reusable class rather than inline styles.

---

## Further Learning

### CSS Concepts to Explore:

1. **Pseudo-elements** - `::before` and `::after`
2. **Gradients** - `linear-gradient`, `radial-gradient`, `conic-gradient`
3. **Box shadows** - Multiple shadows, inset shadows
4. **Position** - `relative`, `absolute`, `fixed`, `sticky`
5. **Z-index** - Stacking context

### Recommended Resources:

- [MDN: CSS Gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Images/Using_CSS_gradients)
- [MDN: Box Shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow)
- [MDN: Pseudo-elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements)
- [Google Fonts](https://fonts.google.com/) - Browse free fonts

---

## Questions & Answers

**Q: Why use pseudo-elements instead of extra HTML divs?**
A: Keeps HTML clean and semantic. Decorative elements belong in CSS, not HTML.

**Q: Can I use this effect on other content?**
A: Yes! Apply the `.parchment-card` class to any container.

**Q: Why so many layers of shadows and gradients?**
A: Each layer adds a subtle detail. Together they create realism. Remove layers to see the difference!

**Q: Is this effect accessible?**
A: Yes! Text remains readable, and screen readers ignore decorative pseudo-elements.

---

## Credits

Effect created for ShriekedIn Halloween networking platform.
Live demo: https://shriekedin.uk/haunted/

Font: Special Elite by Astigmatic
License: SIL Open Font License

---

**Happy Styling! 🎃**

Feel free to experiment and make it your own!
