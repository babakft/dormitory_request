from django.db import models


class ServiceExpert(models.Model):
    """Expert/technician who handles maintenance requests"""

    SPECIALIZATION_CHOICES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('hvac', 'HVAC/Air Conditioning'),
        ('carpentry', 'Carpentry'),
        ('general', 'General Maintenance'),
        ('cleaning', 'Cleaning'),
        ('security', 'Security Systems'),
    ]

    # Expert details
    expert_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Simple password like students
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Status
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expert_name} - {self.get_specialization_display()}"

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'