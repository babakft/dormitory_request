from django.contrib import admin
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
        'full_location',
        'status',
        'assigned_expert',  # NEW FIELD
        'created_at',
        'days_since_created'
    ]
    list_filter = ['status', 'building_name', 'created_at', 'assigned_expert']  # UPDATED
    search_fields = [
        'title',
        'description',
        'student__student_name',
        'student__student_number',
        'assigned_expert__expert_name'  # NEW FIELD
    ]
    actions = ['approve_requests', 'assign_to_expert', 'mark_in_progress', 'mark_completed']
    readonly_fields = ['created_at', 'updated_at', 'days_since_created']

    # UPDATED fieldsets:
    fieldsets = (
        ('Request Details', {
            'fields': ('student', 'title', 'description', 'issue_image')
        }),
        ('Location', {
            'fields': ('building_name', 'room_number', 'floor_number')
        }),
        ('Status & Assignment', {  # UPDATED SECTION
            'fields': ('status', 'assigned_expert', 'assigned_at')
        }),
        ('Work Progress', {  # NEW SECTION
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

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'Approved {queryset.count()} maintenance requests.')

    approve_requests.short_description = "Approve selected requests"

    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f'Marked {queryset.count()} requests as in progress.')

    mark_in_progress.short_description = "Mark as in progress"

    def mark_completed(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'Marked {queryset.count()} requests as completed.')

    mark_completed.short_description = "Mark as completed"

    def assign_to_expert(self, request, queryset):
        updated = queryset.filter(status='approved').update(
            status='in_progress',
            assigned_at=timezone.now()
        )
        self.message_user(
            request,
            f'Marked {updated} requests as in progress. Please assign experts manually.'
        )

    assign_to_expert.short_description = "Mark as in progress (ready for expert assignment)"