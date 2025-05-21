from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceExpert


@admin.register(ServiceExpert)
class ServiceExpertAdmin(admin.ModelAdmin):
    list_display = [
        'expert_name',
        'employee_id',
        'specialization',
        'email',
        'is_active',
        'pending_requests_count',
        'completed_requests_count',
        'total_assigned'
    ]
    list_filter = ['specialization', 'is_active', 'created_at']
    search_fields = ['expert_name', 'employee_id', 'email']
    list_editable = ['is_active']

    fieldsets = (
        ('Expert Information', {
            'fields': ('expert_name', 'employee_id', 'password', 'specialization')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def pending_requests_count(self, obj):
        """Count of pending requests assigned to this expert"""
        count = obj.assigned_requests.filter(status='in_progress').count()
        if count > 0:
            return format_html(
                '<span style="color: orange; font-weight: bold;">{}</span>',
                count
            )
        return count

    pending_requests_count.short_description = 'Pending'

    def completed_requests_count(self, obj):
        """Count of completed requests by this expert"""
        count = obj.assigned_requests.filter(status='completed').count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return count

    completed_requests_count.short_description = 'Completed'

    def total_assigned(self, obj):
        """Total requests ever assigned to this expert"""
        return obj.assigned_requests.count()

    total_assigned.short_description = 'Total Assigned'

    actions = ['activate_experts', 'deactivate_experts']

    def activate_experts(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Activated {queryset.count()} experts.')

    activate_experts.short_description = "Activate selected experts"

    def deactivate_experts(self, request, queryset):
        # Check if any have pending requests using the property
        experts_with_pending = []
        for expert in queryset:
            if expert.pending_requests.exists():
                experts_with_pending.append(expert)

        if experts_with_pending:
            names = [expert.expert_name for expert in experts_with_pending]
            self.message_user(
                request,
                f'Cannot deactivate experts with pending requests: {", ".join(names)}',
                level='error'
            )
            return

        queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {queryset.count()} experts.')