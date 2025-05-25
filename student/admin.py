from django.contrib import admin
from django.utils import timezone
from student.models import Student, MaintenanceRequest


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_number', 'email', 'registration_status', 'created_at']
    list_filter = ['registration_status', 'building_name']
    search_fields = ['student_name', 'student_number', 'email']
    actions = ['approve_students', 'reject_students']

    def approve_students(self, request, queryset):
        queryset.update(registration_status='approved')
        self.message_user(request, f'Approved {queryset.count()} students.')

    approve_students.short_description = "Approve selected students"

    def reject_students(self, request, queryset):
        queryset.update(registration_status='rejected')
        self.message_user(request, f'Rejected {queryset.count()} students.')

    reject_students.short_description = "Reject selected students"


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'student',
        'service_type',  # Added service_type to display
        'full_location',
        'status',
        'assigned_expert',
        'created_at',
        'days_since_created'
    ]
    list_filter = ['status', 'service_type', 'building_name', 'created_at', 'assigned_expert']  # Added service_type to filters
    search_fields = [
        'title',
        'description',
        'student__student_name',
        'student__student_number',
        'assigned_expert__expert_name'
    ]
    actions = ['assign_to_expert', 'mark_completed', 'mark_approved']
    readonly_fields = ['created_at', 'updated_at', 'days_since_created']

    fieldsets = (
        ('Request Details', {
            'fields': ('student', 'title', 'description', 'service_type', 'issue_image')  # Added service_type
        }),
        ('Location', {
            'fields': ('building_name', 'room_number', 'floor_number')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_expert', 'assigned_at')
        }),
        ('Work Progress', {
            'fields': ('work_started_at', 'expert_notes', 'work_in_progress_image'),
            'classes': ('collapse',)
        }),
        ('Completion Details', {
            'fields': ('completion_image', 'completion_notes', 'completed_by', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Student Feedback', {
            'fields': ('student_rating', 'student_feedback'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'days_since_created'),
            'classes': ('collapse',)
        }),
    )


    def mark_completed(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'Marked {queryset.count()} requests as completed.')

    mark_completed.short_description = "Mark as completed"

    def assign_to_expert(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            status='in_progress',
            assigned_at=timezone.now()
        )

    assign_to_expert.short_description = "Mark as in progress (ready for expert assignment)"

    def mark_approved(self, request, queryset):
        from django.utils import timezone
        # Filter to only update pending items
        queryset.update(status='approved',)

    mark_approved.short_description = "Mark pending as approved"