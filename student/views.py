from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from student.models import Student, MaintenanceRequest
from student.forms import StudentRegistrationForm, MaintenanceRequestForm


def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Save student with pending status
            student = form.save(commit=False)
            student.registration_status = 'pending'
            student.save()

            messages.success(
                request,
                'Registration submitted successfully! Your application is pending admin approval.'
            )
            return redirect('student:registration_success')
    else:
        form = StudentRegistrationForm()

    return render(request, 'student/registration_form.html', {'form': form})


def registration_success(request):
    return render(request, 'student/registration_success.html')


def student_login(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')

        if not student_number or not password:
            messages.error(request, 'Please provide both student number and password.')
            return render(request, 'student/login.html')

        try:
            # Find student by student number
            student = Student.objects.get(student_number=student_number)

            # Check if student is approved
            if student.registration_status != 'approved':
                if student.registration_status == 'pending':
                    messages.error(request, 'Your registration is still pending approval.')
                else:
                    messages.error(request, 'Your registration has been rejected. Please contact administration.')
                return render(request, 'student/login.html')

            # Verify password
            if student.password == password:
                # Create session for student
                request.session['student_id'] = student.id
                request.session['student_name'] = student.student_name
                request.session['student_number'] = student.student_number

                messages.success(request, f'Welcome back, {student.student_name}!')
                # Redirect directly to maintenance request instead of dashboard
                return redirect('student:maintenance_request')
            else:
                messages.error(request, 'Invalid student number or password.')

        except Student.DoesNotExist:
            messages.error(request, 'Invalid student number or password.')

    return render(request, 'student/login.html')


def student_logout(request):
    # Clear session
    if 'student_id' in request.session:
        del request.session['student_id']
        del request.session['student_name']
        del request.session['student_number']

    messages.success(request, 'You have been logged out successfully.')
    return redirect('student:student_login')


def maintenance_request(request):
    # Check if student is logged in
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to submit a maintenance request.')
        return redirect('student:student_login')

    # Get current student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('student:student_login')

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES, student=student)
        if form.is_valid():
            # Save maintenance request
            maintenance_req = form.save(commit=False)
            maintenance_req.student = student
            maintenance_req.status = 'pending'
            # service_type will be automatically saved from the form
            maintenance_req.save()

            messages.success(
                request,
                f'Maintenance request submitted successfully! A {maintenance_req.get_service_type_display()} expert will be assigned to handle your request.'
            )
            return redirect('student:request_success')
    else:
        # Pre-fill form with student's location data
        form = MaintenanceRequestForm(student=student)

    return render(request, 'student/maintenance_request.html', {
        'form': form,
        'student': student
    })


def request_success(request):
    # Check if student is logged in
    if 'student_id' not in request.session:
        return redirect('student:student_login')

    return render(request, 'student/request_success.html')