"""
Core Forms for ShriekedIn Platform

This file contains form definitions with built-in security protections.
"""

from django import forms
from django.core.validators import EmailValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re


class ContactForm(forms.Form):
    """
    Contact form with multiple security protections:

    Security Features:
    - Honeypot field (hidden, should remain empty)
    - Max length validation on all fields
    - Email validation
    - XSS protection via Django's form rendering
    - CSRF protection (handled by Django middleware)
    - Input sanitization
    """

    # Visible fields
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border-2 border-purple-300 rounded-lg focus:outline-none focus:border-purple-600 transition',
            'placeholder': 'Your Name',
        }),
        help_text='',
        error_messages={
            'required': 'Please enter your name.',
            'max_length': 'Name must be 200 characters or less.',
        }
    )

    email = forms.EmailField(
        max_length=254,  # RFC 5321 email max length
        required=True,
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border-2 border-purple-300 rounded-lg focus:outline-none focus:border-purple-600 transition',
            'placeholder': 'your.email@example.com',
        }),
        error_messages={
            'required': 'Please enter your email address.',
            'invalid': 'Please enter a valid email address.',
        }
    )

    subject = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border-2 border-purple-300 rounded-lg focus:outline-none focus:border-purple-600 transition',
            'placeholder': 'What is this about?',
        }),
        error_messages={
            'required': 'Please enter a subject.',
            'max_length': 'Subject must be 300 characters or less.',
        }
    )

    message = forms.CharField(
        max_length=5000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border-2 border-purple-300 rounded-lg focus:outline-none focus:border-purple-600 transition',
            'placeholder': 'Your message...',
            'rows': 8,
        }),
        error_messages={
            'required': 'Please enter your message.',
            'max_length': 'Message must be 5000 characters or less.',
        }
    )

    # Honeypot field - should be hidden and remain empty
    # Bots typically fill all fields, humans won't see/fill this
    website = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'hidden',
            'tabindex': '-1',
            'autocomplete': 'off',
        }),
        label='',
    )

    def clean_name(self):
        """
        Validate and sanitize name field.
        """
        name = self.cleaned_data.get('name', '').strip()

        # Check for minimum length
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')

        # Check for suspicious patterns (excessive special characters)
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\-\']', name))
        if special_char_count > 5:
            raise ValidationError('Name contains too many special characters.')

        return name

    def clean_subject(self):
        """
        Validate and sanitize subject field.
        """
        subject = self.cleaned_data.get('subject', '').strip()

        # Check for minimum length
        if len(subject) < 3:
            raise ValidationError('Subject must be at least 3 characters long.')

        # Check for spam patterns
        spam_patterns = [
            r'viagra', r'cialis', r'pharmacy', r'casino',
            r'lottery', r'winner', r'claim.*prize',
            r'click.*here', r'limited.*time.*offer',
            r'\$\$\$', r'make.*money.*fast',
        ]

        subject_lower = subject.lower()
        for pattern in spam_patterns:
            if re.search(pattern, subject_lower):
                raise ValidationError('Your subject contains prohibited content. Please rephrase.')

        return subject

    def clean_message(self):
        """
        Validate and sanitize message field.
        """
        message = self.cleaned_data.get('message', '').strip()

        # Check for minimum length
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')

        # Check for excessive URLs (common in spam)
        url_pattern = r'https?://|www\.'
        url_count = len(re.findall(url_pattern, message, re.IGNORECASE))
        if url_count > 3:
            raise ValidationError('Message contains too many URLs. Please limit to 3 or fewer.')

        # Check for excessive capitalization (common in spam)
        if len(message) > 20:  # Only check if message is reasonably long
            upper_count = sum(1 for c in message if c.isupper())
            upper_ratio = upper_count / len(message)
            if upper_ratio > 0.5:
                raise ValidationError('Please avoid excessive use of capital letters.')

        return message

    def clean_website(self):
        """
        Validate honeypot field.

        This field should always be empty for legitimate users.
        If it's filled, it's likely a bot.
        """
        website = self.cleaned_data.get('website', '')

        # If the honeypot field is filled, it's a bot
        if website:
            raise ValidationError('Bot detected.')

        return website

    def clean(self):
        """
        Additional form-level validation.
        """
        cleaned_data = super().clean()

        # Additional cross-field validation can go here

        return cleaned_data
