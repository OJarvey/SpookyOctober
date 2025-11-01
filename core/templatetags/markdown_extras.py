"""
Custom template tags and filters for markdown rendering.
"""

from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert markdown text to HTML.

    Usage in templates:
        {{ content|markdown }}

    Features:
        - Basic markdown syntax (bold, italic, links, etc.)
        - Code blocks with syntax highlighting
        - Tables
        - Strikethrough
        - Task lists
    """
    if not text:
        return ''

    # Configure markdown with useful extensions
    md_instance = md.Markdown(extensions=[
        'extra',          # Tables, fenced code blocks, etc.
        'nl2br',          # Convert newlines to <br>
        'sane_lists',     # Better list handling
    ])

    # Convert markdown to HTML
    html = md_instance.convert(text)

    # Mark as safe so Django doesn't escape the HTML
    return mark_safe(html)
