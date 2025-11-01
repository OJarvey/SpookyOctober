/**
 * In-Place Editor for Haunted Places
 *
 * Provides inline editing capabilities for haunted place fields with markdown support.
 * Only available to authorized users (staff/admin).
 */

class HauntedPlaceEditor {
    constructor(placeId, csrfToken) {
        this.placeId = placeId;
        this.csrfToken = csrfToken;
        this.currentEditor = null;
        this.init();
    }

    init() {
        // Add edit icons to all editable fields
        this.addEditIcons();
    }

    addEditIcons() {
        const editableFields = document.querySelectorAll('[data-editable]');
        editableFields.forEach(field => {
            const fieldName = field.dataset.editable;
            const fieldType = field.dataset.fieldType || 'text';

            // Create edit icon
            const editIcon = document.createElement('button');
            editIcon.className = 'edit-icon';
            editIcon.innerHTML = '✏️';
            editIcon.title = `Edit ${fieldName.replace(/_/g, ' ')}`;
            editIcon.setAttribute('aria-label', `Edit ${fieldName.replace(/_/g, ' ')}`);

            // Position the icon
            field.style.position = 'relative';
            editIcon.style.cssText = `
                position: absolute;
                top: 8px;
                right: 8px;
                background: rgba(139, 69, 19, 0.9);
                color: white;
                border: none;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                cursor: pointer;
                font-size: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.2s, transform 0.2s;
                z-index: 10;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            `;

            // Show icon on hover
            field.addEventListener('mouseenter', () => {
                editIcon.style.opacity = '1';
            });

            field.addEventListener('mouseleave', () => {
                if (!field.classList.contains('editing')) {
                    editIcon.style.opacity = '0';
                }
            });

            editIcon.addEventListener('mouseenter', () => {
                editIcon.style.transform = 'scale(1.1)';
            });

            editIcon.addEventListener('mouseleave', () => {
                editIcon.style.transform = 'scale(1)';
            });

            // Handle click
            editIcon.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.enableEditing(field, fieldName, fieldType);
            });

            field.appendChild(editIcon);
        });
    }

    enableEditing(field, fieldName, fieldType) {
        // Close any existing editor
        if (this.currentEditor) {
            this.cancelEditing();
        }

        // Mark as editing
        field.classList.add('editing');
        this.currentEditor = field;

        // Get current content
        const contentElement = field.querySelector('[data-field-content]');
        const currentValue = contentElement.textContent.trim();

        // Hide the edit icon
        const editIcon = field.querySelector('.edit-icon');
        if (editIcon) {
            editIcon.style.display = 'none';
        }

        // Create editor based on field type
        let editor;
        if (fieldType === 'markdown' || fieldType === 'textarea') {
            editor = this.createMarkdownEditor(currentValue, fieldName);
        } else if (fieldType === 'number') {
            editor = this.createNumberEditor(currentValue, fieldName);
        } else {
            editor = this.createTextEditor(currentValue, fieldName);
        }

        // Create action buttons
        const actions = this.createActionButtons(field, fieldName, editor);

        // Replace content with editor
        contentElement.style.display = 'none';
        contentElement.parentNode.insertBefore(editor, contentElement.nextSibling);
        contentElement.parentNode.insertBefore(actions, editor.nextSibling);

        // Focus the editor
        if (editor.tagName === 'TEXTAREA') {
            editor.focus();
            editor.setSelectionRange(editor.value.length, editor.value.length);
        } else if (editor.tagName === 'INPUT') {
            editor.focus();
        }
    }

    createMarkdownEditor(value, fieldName) {
        const textarea = document.createElement('textarea');
        textarea.value = value;
        textarea.className = 'markdown-editor';
        textarea.rows = 10;
        textarea.style.cssText = `
            width: 100%;
            padding: 12px;
            border: 2px solid #8B4513;
            border-radius: 4px;
            font-family: 'Special Elite', 'Courier New', monospace;
            font-size: 1rem;
            line-height: 1.6;
            resize: vertical;
            background: #fff;
            color: #3a2a1a;
        `;

        // Add markdown help text
        const helpText = document.createElement('div');
        helpText.className = 'markdown-help';
        helpText.style.cssText = `
            font-size: 0.85rem;
            color: #666;
            margin-top: 8px;
            padding: 8px;
            background: #f9f9f9;
            border-radius: 4px;
            font-family: sans-serif;
        `;
        helpText.innerHTML = `
            <strong>Markdown supported:</strong>
            **bold** | *italic* | # Heading | - List | [link](url)
        `;

        const container = document.createElement('div');
        container.appendChild(textarea);
        container.appendChild(helpText);

        return container;
    }

    createTextEditor(value, fieldName) {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = value;
        input.className = 'text-editor';
        input.style.cssText = `
            width: 100%;
            padding: 12px;
            border: 2px solid #8B4513;
            border-radius: 4px;
            font-family: 'Special Elite', 'Courier New', monospace;
            font-size: 1.1rem;
            background: #fff;
            color: #3a2a1a;
        `;
        return input;
    }

    createNumberEditor(value, fieldName) {
        const input = document.createElement('input');
        input.type = 'number';
        input.value = value;
        input.className = 'number-editor';

        if (fieldName === 'scare_level') {
            input.min = 1;
            input.max = 5;
        }

        input.style.cssText = `
            width: 100%;
            padding: 12px;
            border: 2px solid #8B4513;
            border-radius: 4px;
            font-family: 'Special Elite', 'Courier New', monospace;
            font-size: 1.1rem;
            background: #fff;
            color: #3a2a1a;
        `;
        return input;
    }

    createActionButtons(field, fieldName, editor) {
        const container = document.createElement('div');
        container.className = 'editor-actions';
        container.style.cssText = `
            display: flex;
            gap: 8px;
            margin-top: 12px;
            justify-content: flex-end;
        `;

        // Save button
        const saveBtn = document.createElement('button');
        saveBtn.textContent = '💾 Save';
        saveBtn.className = 'btn-save';
        saveBtn.style.cssText = `
            background: #059669;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        `;
        saveBtn.addEventListener('mouseenter', () => {
            saveBtn.style.background = '#047857';
        });
        saveBtn.addEventListener('mouseleave', () => {
            saveBtn.style.background = '#059669';
        });
        saveBtn.addEventListener('click', () => {
            this.saveField(field, fieldName, editor);
        });

        // Cancel button
        const cancelBtn = document.createElement('button');
        cancelBtn.textContent = '❌ Cancel';
        cancelBtn.className = 'btn-cancel';
        cancelBtn.style.cssText = `
            background: #6b7280;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        `;
        cancelBtn.addEventListener('mouseenter', () => {
            cancelBtn.style.background = '#4b5563';
        });
        cancelBtn.addEventListener('mouseleave', () => {
            cancelBtn.style.background = '#6b7280';
        });
        cancelBtn.addEventListener('click', () => {
            this.cancelEditing();
        });

        container.appendChild(saveBtn);
        container.appendChild(cancelBtn);

        return container;
    }

    async saveField(field, fieldName, editorContainer) {
        // Get value from editor
        let value;
        const textarea = editorContainer.querySelector('textarea');
        const input = editorContainer.querySelector('input');

        if (textarea) {
            value = textarea.value;
        } else if (input) {
            value = input.value;
        } else {
            value = editorContainer.value;
        }

        // Show loading state
        const saveBtn = field.querySelector('.btn-save');
        const originalText = saveBtn.textContent;
        saveBtn.textContent = '⏳ Saving...';
        saveBtn.disabled = true;

        try {
            // Make API request
            const response = await fetch(`/haunted/${this.placeId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    field: fieldName,
                    value: value
                })
            });

            const data = await response.json();

            if (data.success) {
                // Update the content
                const contentElement = field.querySelector('[data-field-content]');
                contentElement.textContent = value;

                // Show success message
                this.showNotification('✅ ' + data.message, 'success');

                // Clean up editor
                this.cancelEditing();
            } else {
                // Show error message
                this.showNotification('❌ ' + data.error, 'error');
                saveBtn.textContent = originalText;
                saveBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error saving field:', error);
            this.showNotification('❌ Failed to save changes. Please try again.', 'error');
            saveBtn.textContent = originalText;
            saveBtn.disabled = false;
        }
    }

    cancelEditing() {
        if (!this.currentEditor) return;

        const field = this.currentEditor;

        // Remove editor and actions
        const editorContainer = field.querySelector('.markdown-editor')?.parentElement ||
                               field.querySelector('.text-editor') ||
                               field.querySelector('.number-editor');
        const actions = field.querySelector('.editor-actions');

        if (editorContainer) {
            editorContainer.remove();
        }
        if (actions) {
            actions.remove();
        }

        // Show content again
        const contentElement = field.querySelector('[data-field-content]');
        if (contentElement) {
            contentElement.style.display = '';
        }

        // Show edit icon again
        const editIcon = field.querySelector('.edit-icon');
        if (editIcon) {
            editIcon.style.display = '';
            editIcon.style.opacity = '0';
        }

        // Remove editing class
        field.classList.remove('editing');
        this.currentEditor = null;
    }

    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.3s ease-out;
            font-family: sans-serif;
        `;

        if (type === 'success') {
            notification.style.background = '#059669';
        } else {
            notification.style.background = '#dc2626';
        }

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
