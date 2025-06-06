# Generated by Django 5.2.1 on 2025-05-19 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('issue_image', models.ImageField(blank=True, null=True, upload_to='maintenance_requests/')),
                ('room_number', models.CharField(max_length=20)),
                ('building_name', models.CharField(max_length=50)),
                ('floor_number', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=15)),
                ('completion_image', models.ImageField(blank=True, null=True, upload_to='maintenance_completed/')),
                ('completion_notes', models.TextField(blank=True)),
                ('completed_by', models.CharField(blank=True, max_length=100)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('student_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('student_feedback', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_requests', to='student.student')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
