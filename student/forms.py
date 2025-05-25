from django import forms
from student.models import Student,MaintenanceRequest


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name',
            'email',
            'password',
            'student_number',
            'room_number',
            'building_name',
            'floor_number'
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_student_number(self):
        """Check if student number already exists"""
        student_number = self.cleaned_data.get('student_number')
        if Student.objects.filter(student_number=student_number).exists():
            raise forms.ValidationError("This student number is already registered.")
        return student_number

    def clean_password(self):
        """Check password strength"""
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_student_name(self):
        """Check name is not empty or just spaces"""
        student_name = self.cleaned_data.get('student_name')
        if not student_name.strip():
            raise forms.ValidationError("Name cannot be empty.")
        return student_name.strip()


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'title',
            'description',
            'service_type',  # Added service_type field
            'issue_image',
            'room_number',
            'building_name',
            'floor_number'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of what needs to be fixed...'
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'service_type'
            }),
            'issue_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If student is provided, pre-fill location data
        if student:
            self.fields['room_number'].initial = student.room_number
            self.fields['building_name'].initial = student.building_name
            self.fields['floor_number'].initial = student.floor_number

    def clean_issue_image(self):
        """Validate image file"""
        image = self.cleaned_data.get('issue_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large. Please keep it under 5MB.")

            # Check file type using content type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Invalid image file. Please upload a JPEG, PNG, GIF, BMP, or WebP image.")

        return image