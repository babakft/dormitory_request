from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from student.models import MaintenanceRequest
from .models import ServiceExpert
from .forms import WorkCompletionForm, WorkProgressForm


def expert_login(request):
    """Login for service experts - similar to student login"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        if not employee_id or not password:
            messages.error(request, 'Please provide both employee ID and password.')
            return render(request, 'services/login.html')

        try:
            # Find expert by employee ID
            expert = ServiceExpert.objects.get(employee_id=employee_id)

            # Check if expert is active
            if not expert.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact administration.')
                return render(request, 'services/login.html')

            # Verify password (simple comparison like students)
            if expert.password == password:
                # Create session for expert
                request.session['expert_id'] = expert.id
                request.session['expert_name'] = expert.expert_name
                request.session['employee_id'] = expert.employee_id

                messages.success(request, f'Welcome back, {expert.expert_name}!')
                return redirect('services:expert_dashboard')
            else:
                messages.error(request, 'Invalid employee ID or password.')

        except ServiceExpert.DoesNotExist:
            messages.error(request, 'Invalid employee ID or password.')

    return render(request, 'services/login.html')


def expert_logout(request):
    """Logout for service experts"""
    # Clear session
    if 'expert_id' in request.session:
        del request.session['expert_id']
        del request.session['expert_name']
        del request.session['employee_id']

    messages.success(request, 'You have been logged out successfully.')
    return redirect('services:expert_login')


def expert_dashboard(request):
    """Dashboard showing assigned requests for the expert"""
    # Check if expert is logged in
    if 'expert_id' not in request.session:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('services:expert_login')

    # Get current expert
    try:
        expert = ServiceExpert.objects.get(id=request.session['expert_id'])
    except ServiceExpert.DoesNotExist:
        messages.error(request, 'Expert not found. Please log in again.')
        return redirect('services:expert_login')

    # Get requests in different states - FIXED THE FILTER
    pending_requests = MaintenanceRequest.objects.filter(
        assigned_expert=expert,
        status='approved'  # Changed from 'approved' to 'in_progress'
    ).order_by('-assigned_at')

    in_progress_requests = MaintenanceRequest.objects.filter(
        assigned_expert=expert,
        status='in_progress'  # Changed from 'approved' to 'in_progress'
    ).order_by('-assigned_at')

    completed_requests = MaintenanceRequest.objects.filter(
        assigned_expert=expert,
        status='completed'
    ).order_by('-completed_at')[:10]  # Last 10 completed

    context = {
        'expert': expert,
        'pending_requests': pending_requests | in_progress_requests,
        'completed_requests': completed_requests,
        'pending_count': pending_requests.count(),
        'completed_count': expert.assigned_requests.filter(status='completed').count(),
    }

    return render(request, 'services/dashboard.html', context)


def start_work(request, request_id):
    """Expert starts working on a request"""
    # Check if expert is logged in
    if 'expert_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('services:expert_login')

    # Get current expert
    try:
        expert = ServiceExpert.objects.get(id=request.session['expert_id'])
    except ServiceExpert.DoesNotExist:
        messages.error(request, 'Expert not found. Please log in again.')
        return redirect('services:expert_login')

    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        id=request_id,
        assigned_expert=expert,
        status='approved'
    )

    if request.method == 'POST':
        form = WorkProgressForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance_request.work_started_at = timezone.now()
            maintenance_request.expert_notes = form.cleaned_data['expert_notes']
            maintenance_request.status = 'in_progress'
            if form.cleaned_data['work_in_progress_image']:
                maintenance_request.work_in_progress_image = form.cleaned_data['work_in_progress_image']

            maintenance_request.save()

            messages.success(request, 'Work started successfully!')
            return redirect('services:expert_dashboard')
    else:
        form = WorkProgressForm()

    context = {
        'form': form,
        'request': maintenance_request,
        'expert': expert,
    }

    return render(request, 'services/start_work.html', context)


def complete_work(request, request_id):
    """Expert completes work and submits completion details"""
    # Check if expert is logged in
    if 'expert_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('services:expert_login')

    # Get current expert
    try:
        expert = ServiceExpert.objects.get(id=request.session['expert_id'])
    except ServiceExpert.DoesNotExist:
        messages.error(request, 'Expert not found. Please log in again.')
        return redirect('services:expert_login')

    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        id=request_id,
        assigned_expert=expert,
        status='in_progress'
    )

    if request.method == 'POST':
        form = WorkCompletionForm(request.POST, request.FILES)
        if form.is_valid():
            # Update request status
            maintenance_request.status = 'completed'
            maintenance_request.completed_at = timezone.now()
            maintenance_request.completed_by = expert.expert_name
            maintenance_request.completion_image = form.cleaned_data['completion_image']
            maintenance_request.completion_notes = form.cleaned_data['completion_notes']

            # Add any additional expert notes
            if form.cleaned_data['additional_notes']:
                if maintenance_request.expert_notes:
                    maintenance_request.expert_notes += f"\n\nCompletion Notes: {form.cleaned_data['additional_notes']}"
                else:
                    maintenance_request.expert_notes = form.cleaned_data['additional_notes']

            maintenance_request.save()

            messages.success(
                request,
                'Work completed successfully! Student will be notified to provide feedback.'
            )
            return redirect('services:expert_dashboard')
    else:
        form = WorkCompletionForm()

    context = {
        'form': form,
        'request': maintenance_request,
        'expert': expert,
    }

    return render(request, 'services/complete_work.html', context)


def request_detail(request, request_id):
    """View detailed information about a maintenance request"""
    # Check if expert is logged in
    if 'expert_id' not in request.session:
        messages.error(request, 'Please log in to access this page.')
        return redirect('services:expert_login')

    # Get current expert
    try:
        expert = ServiceExpert.objects.get(id=request.session['expert_id'])
    except ServiceExpert.DoesNotExist:
        messages.error(request, 'Expert not found. Please log in again.')
        return redirect('services:expert_login')

    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        id=request_id,
        assigned_expert=expert
    )

    context = {
        'request': maintenance_request,
        'expert': expert,
    }

    return render(request, 'services/request_detail.html', context)
