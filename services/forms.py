from django import forms
from student.models import MaintenanceRequest


class WorkProgressForm(forms.Form):
    """Form for expert to start work and add initial notes"""

    expert_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Add your initial assessment and work plan...'
        }),
        label='Initial Assessment',
        help_text='Describe what you found and your plan to fix it',
        required=False
    )

    work_in_progress_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Before/During Work Photo',
        help_text='Take a photo before or during the repair work',
        required=False
    )


class WorkCompletionForm(forms.Form):
    """Form for expert to complete work and submit final details"""

    completion_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Completion Photo *',
        help_text='Take a photo showing the completed repair',
        required=True
    )

    completion_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe what was fixed and any important details...'
        }),
        label='Completion Summary *',
        help_text='Explain what was done to fix the issue',
        required=True
    )

    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any additional notes, recommendations, or follow-up needed...'
        }),
        label='Additional Notes',
        help_text='Optional: Any recommendations for the student or follow-up needed',
        required=False
    )

    def clean_completion_image(self):
        """Validate completion image"""
        image = self.cleaned_data.get('completion_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large. Please keep it under 5MB.")

            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Invalid image file. Please upload a JPEG, PNG, GIF, BMP, or WebP image.")

        return image

    def clean_completion_notes(self):
        """Validate completion notes"""
        notes = self.cleaned_data.get('completion_notes')
        if notes and len(notes.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed description (at least 10 characters).")
        return notes.strip() if notes else notes