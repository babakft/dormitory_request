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
        'phone',
        'is_active',
        'created_at'
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

    actions = ['activate_experts', 'deactivate_experts']

    def activate_experts(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Activated {queryset.count()} experts.')

    activate_experts.short_description = "Activate selected experts"

    def deactivate_experts(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {queryset.count()} experts.')

    deactivate_experts.short_description = "Deactivate selected experts"