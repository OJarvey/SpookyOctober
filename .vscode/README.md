# VSCode Configuration for ShriekedIn

This folder contains VSCode workspace settings optimized for Django + Tailwind CSS development.

## What's Configured?

### Automatic Features
When you open this project in VSCode, you'll automatically get:

1. **Tailwind IntelliSense** - Autocomplete for Tailwind classes in HTML templates
2. **Django Template Support** - Proper syntax highlighting for `{% %}` and `{{ }}`
3. **Emmet in Templates** - Type `div.card` and press Tab to expand
4. **Python Import Suggestions** - Auto-import Django modules
5. **Hidden Clutter** - `__pycache__`, `.pyc` files hidden from sidebar
6. **Line Length Guides** - Visual guides at 88 and 120 characters

### File Types
- Files in `templates/` are treated as `django-html`
- Regular `.html` files are treated as `html`
- This enables proper syntax highlighting for Django template tags

### Recommended Extensions
When you open this project, VSCode will prompt you to install recommended extensions:

**Essential:**
- **Python** - Python language support
- **Pylance** - Fast Python IntelliSense
- **Django** - Django template syntax highlighting
- **Tailwind CSS IntelliSense** - Tailwind class autocomplete

**Helpful:**
- **GitLens** - Enhanced Git features
- **Error Lens** - Inline error messages (very helpful!)
- **Code Spell Checker** - Catch typos

## Quick Tips

### Tailwind Autocomplete in Templates
```html
<!-- Start typing class names and get autocomplete -->
<div class="bg-pumpkin text-white">
     ↑ IntelliSense shows all available classes
</div>
```

### Emmet Shortcuts
```html
<!-- Type this: -->
div.card>h3.text-2xl+p

<!-- Press Tab, get this: -->
<div class="card">
    <h3 class="text-2xl"></h3>
    <p></p>
</div>
```

### Django Template Snippets
If you install the Django extension, you get snippets like:
- `for` → `{% for item in items %}`
- `if` → `{% if condition %}`
- `url` → `{% url 'name' %}`

## Troubleshooting

### Tailwind classes not autocompleting?
1. Make sure `Tailwind CSS IntelliSense` extension is installed
2. Open `tailwind.config.js` to activate the extension
3. Restart VSCode

### Django template tags showing as errors?
1. Install the `Django` extension (batisteo.vscode-django)
2. Check that files in `templates/` are detected as `django-html`
3. Look at the bottom-right of VSCode - it should say "Django HTML"

### Python imports not working?
1. Make sure you've selected the correct Python interpreter (Cmd+Shift+P → "Python: Select Interpreter")
2. Look for `.venv` or your virtual environment
3. Restart VSCode after activating venv

## Customization

Feel free to modify `settings.json` for your preferences:

```json
{
    // Prefer Black formatting? Add:
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,

    // Want different tab sizes? Change:
    "editor.tabSize": 2,

    // Prefer no minimap?
    "editor.minimap.enabled": false
}
```

## Learn More

- [VSCode Django Tutorial](https://code.visualstudio.com/docs/python/tutorial-django)
- [Tailwind CSS IntelliSense Docs](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [VSCode Settings Reference](https://code.visualstudio.com/docs/getstarted/settings)
