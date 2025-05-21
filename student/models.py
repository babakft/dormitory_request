from django.db import models
import os

class Student(models.Model):
    REGISTRATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Basic Information
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    # Room Information
    room_number = models.CharField(max_length=20)
    building_name = models.CharField(max_length=50)
    floor_number = models.IntegerField()

    # Registration Status
    registration_status = models.CharField(
        max_length=10,
        choices=REGISTRATION_STATUS_CHOICES,
        default='pending'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_name} - {self.student_number}"

    @property
    def is_approved(self):
        return self.registration_status == 'approved'

    @property
    def full_room_address(self):
        return f"Room {self.room_number}, Floor {self.floor_number}, {self.building_name}"


class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    # Student who made the request
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='maintenance_requests')

    # Request details
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Image upload
    issue_image = models.ImageField(upload_to='maintenance_requests/', null=True, blank=True)

    # Location details
    room_number = models.CharField(max_length=20)
    building_name = models.CharField(max_length=50)
    floor_number = models.IntegerField()

    # Status tracking
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    # Completion details (filled by services team)
    completion_image = models.ImageField(upload_to='maintenance_completed/', null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    completed_by = models.CharField(max_length=100, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Student feedback (after completion)
    student_rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    student_feedback = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.student_name} ({self.get_status_display()})"

    @property
    def full_location(self):
        return f"Room {self.room_number}, Floor {self.floor_number}, {self.building_name}"

    @property
    def days_since_created(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).days