# MVP Static Site Folder

## Location

`../mvp/` (outside the main Django project)

## Purpose

A **beginner-friendly** static HTML version of the ShriekedIn site for team members with little development knowledge.

## What's Included

- ✅ **No build process** - Uses Tailwind CSS from CDN
- ✅ **No Django** - Pure HTML files
- ✅ **No database** - Static content only
- ✅ **Easy editing** - Just open HTML in any text editor

## Files

| File | Description |
|------|-------------|
| `index.html` | Home page |
| `events.html` | Events listing page |
| `TEMPLATE.html` | Copy this to create new pages |
| `COMPONENTS.html` | Copy/paste component library |
| `README.md` | Full documentation |
| `QUICK-START.md` | 5-minute getting started guide |

## How Team Members Use It

1. Navigate to `../mvp/` folder
2. Open any `.html` file in a text editor
3. Edit the HTML
4. Save and refresh browser
5. No npm, no build, no server required!

## Key Features

- **Tailwind CSS from CDN**: No compilation needed
- **Well-commented code**: Easy to understand
- **Reusable components**: Copy/paste from COMPONENTS.html
- **Halloween theming**: Matches main site aesthetic
- **Responsive design**: Works on mobile/tablet/desktop

## When to Use MVP vs Main Django Site

### Use MVP folder when:
- ✅ Quick prototyping
- ✅ Team members learning HTML/CSS
- ✅ Testing designs without Django
- ✅ Creating mockups for stakeholders

### Use Django site when:
- ✅ Need authentication
- ✅ Need database
- ✅ Need dynamic content
- ✅ Production deployment

## Syncing Designs

When a design is finalized in MVP:
1. Copy the HTML structure
2. Convert to Django template (add `{% extends %}`, `{% block %}`, etc.)
3. Replace static data with dynamic Django variables
4. Move to `templates/` folder in main project

## Team Training

Start here for new team members:
1. Read `../mvp/QUICK-START.md`
2. Make first edit to `index.html`
3. Explore `COMPONENTS.html` for examples
4. Create a new page using `TEMPLATE.html`

## Benefits

- 🚀 **Zero setup time**
- 📝 **Easy for non-developers**
- 🎨 **Fast iteration**
- 👀 **Visual feedback immediately**
- 📚 **Learning-friendly**

---

**Created**: 31 October 2025
**Maintained by**: Development team
