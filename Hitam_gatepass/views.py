from django.shortcuts import render, redirect, get_object_or_404
from .models import Faculty, Students, Mentor, Gatepass, Hod
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from datetime import time
from django.http import HttpResponse
import smtplib
from email.mime.text import MIMEText
import logging
from email.mime.multipart import MIMEMultipart
import textile



logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'Hitam_gatepass/index.html')

def Student_enter(request):
    if request.method == 'POST':
        Student_name = request.POST.get('student_name')
        Student_roll = request.POST.get('roll_no')
        
        try:
            # Get the student object
            student = Students.objects.get(s_name=Student_name, s_roll=Student_roll)
            Hod_name = Hod.objects.get(Hod_branch=student.s_branch)
            
            # Check if the student exists in the Gatepass table
            student_gatepass_list = Gatepass.objects.filter(g_student=student,g_date=timezone.now().date())
            student_gatepass_exists = student_gatepass_list.exists()
            handle() 
            # Pass the data to the template
            context = {
                'Student_name': Student_name,
                'Roll_no': Student_roll,
                'Student': student,
                'Hod': Hod_name,
                'student_gatepass_exists': student_gatepass_exists,
                'student_gatepass_list': student_gatepass_list,
            }
            return render(request, 'Hitam_gatepass/Student.html', context)
        except Students.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Student not found'})
        except Hod.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'HOD not found'})
     
    return render(request, 'Hitam_gatepass/index.html')

def Student(request):
    if request.method == 'POST':
        # Retrieve common form data
        student_name = request.POST.get('student_name')
        student_roll = request.POST.get('roll_no')
        form_type = request.POST.get('form_type')  # Hidden field to differentiate forms

        try:
            # Get the student object
            student = Students.objects.get(s_name=student_name, s_roll=student_roll)

            # Determine gate pass type and save the data
            if form_type == 'normal':
                pass_reason = request.POST.get('normal_reason')
                pass_from = request.POST.get('normal_from')
                pass_to = request.POST.get('normal_to')
                gatepass_type = "Normal"

                # Fetch the HOD for the student's branch
                hod = Hod.objects.get(Hod_branch=student.s_branch)
                faculty = Faculty.objects.get(F_name=hod.Hod_name)  # Fetch HOD's faculty record
                hod_email = faculty.F_email  # Get HOD's email

                # Save the gate pass
                Gatepass.objects.create(
                    g_student=student,
                    g_type=gatepass_type,
                    g_purpose=pass_reason,
                    g_out_time=pass_from,
                    g_in_time=pass_to,
                    g_date=timezone.now(),
                    g_rol=student,  # Pass the student instance
                    g_status="Pending HOD Approval"
                )

                # Notify the HOD
                if hod_email:
                    subject = "New Normal Gate Pass Request"
                    body = f"""
                        Dear {hod.Hod_name},
                        A new normal gate pass request has been submitted by the student:
                        Student Name: {student.s_name}
                        Roll Number: {student.s_roll}
                        Purpose: {pass_reason}
                        From: {pass_from}
                        To: {pass_to}
                        
                        
                        Thank you."""
                    
                    send_mail(body, subject, hod_email)

            elif form_type == 'emergency':
                pass_reason = request.POST.get('emergency_reason')
                pass_from = request.POST.get('emergency_from')
                pass_to = request.POST.get('emergency_to')
                gatepass_type = "Emergency"

                # Fetch the Mentor for the student
                mentor = Mentor.objects.get(M_name=student.s_mentor.M_name)
                faculty = Faculty.objects.get(F_name=mentor.M_name)  # Fetch Mentor's faculty record
                mentor_email = faculty.F_email  # Get Mentor's email

                # Save the gate pass
                Gatepass.objects.create(
                    g_student=student,
                    g_type=gatepass_type,
                    g_purpose=pass_reason,
                    g_out_time=pass_from,
                    g_in_time=pass_to,
                    g_date=timezone.now(),
                    g_rol=student,  # Pass the student instance
                    g_status="Pending Mentor Approval"
                )

                # Notify the Mentor
                if mentor_email:
                    subject = "New Emergency Gate Pass Request"
                    body = f"""
                        Dear {mentor.M_name},
                        A new emergency gate pass request has been submitted by the student:
                        Student Name: {student.s_name}
                        Roll Number: {student.s_roll}
                        Purpose: {pass_reason}
                        From: {pass_from}
                        To: {pass_to}
                        
                        Thank you."""
                    
                    send_mail(body, subject, mentor_email)

            else:
                return render(request, 'Hitam_gatepass/Student.html', {'error': 'Invalid form type'})

            # Redirect back to the student page with a success message
            request.session['success_message'] = f"{gatepass_type} Gate pass created successfully!"
            return redirect('Hitam_gatepass:student')

        except Students.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Student not found'})
        except Hod.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'HOD not found'})
        except Mentor.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Mentor not found'})
        except Faculty.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Faculty record not found'})

    # Handle GET request
    success_message = request.session.pop('success_message', None)  # Retrieve and clear the success message
    return render(request, 'Hitam_gatepass/Student.html', {'success': success_message})

def Normal_pass(request):
    staff_name = request.session.get('staff_name')  # Retrieve staff_name from session
    if staff_name:
        try:
            faculty = Faculty.objects.get(F_name=staff_name)
            context = {}

            # Check if the faculty is an HOD
            if Hod.objects.filter(Hod_name=faculty.F_name).exists():
                hod = Hod.objects.get(Hod_name=faculty.F_name)
                context['Hod'] = hod
                context['Students'] = Students.objects.filter(s_branch=hod.Hod_branch)
                context['Gatepass'] = Gatepass.objects.filter(
                    g_student__s_branch=hod.Hod_branch, g_date=timezone.now().date(), g_status="Not Approved",g_type="Normal"
                )
                context['staff_name'] = staff_name  # Pass staff_name to the template
                return render(request, 'Hitam_gatepass/Normal_pass.html', context)

            # If the faculty is not an HOD
            return render(request, 'Hitam_gatepass/index.html', {'error': 'You are not authorized to access this page.'})

        except Faculty.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Faculty not found'})

    return render(request, 'Hitam_gatepass/index.html')

def send_mail(body, subject, to_email):
    from_email = "arif.cloud.july@gmail.com"
    from_password = "ruqh qijb fpgb spzd"  
    try:
        # Create HTML version of the email
        
        # Replace newlines with <br> tags for HTML formatting
        
        # Convert body to HTML using Textile
        html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2c3e50;">{subject}</h2>
            <div style="color: #34495e; line-height: 1.6;">{body}</div>
            <p style="color: #7f8c8d; margin-top: 20px;">
            This is an automated message from the system.
            </p>
            </body> </html> """.replace("\n","<br>") 

        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Add plain text and HTML parts
        text_part = MIMEText(body, 'plain')
        html_part = MIMEText(html_content, 'html')
        msg.attach(text_part)
        msg.attach(html_part)

        # Connect to SMTP server with explicit timeout
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        server.login(from_email, from_password)

        # Send email and log success
        server.send_message(msg)
        logger.info(f"Successfully sent email to {to_email}")

        server.quit()
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

    





@login_required
def Emergency_pass(request):
    staff_name = request.GET.get('staff_name')  # Retrieve staff_name from query parameters
    if not staff_name:
        messages.error(request, "Staff name is required.")
        print("Staff name not found in query parameters.")
        return redirect('Hitam_gatepass:index')

    try:
        # Retrieve the faculty object
        faculty = Faculty.objects.get(F_name=staff_name)
        context = {}

        # Check if the faculty is an HOD or Mentor
        hod = Hod.objects.filter(Hod_name=faculty.F_name).first()
        mentor = Mentor.objects.filter(M_name=faculty.F_name).first()

        hod_gatepasses = mentor_gatepasses = None

        # Retrieve HOD gate passes
        if hod:
            context['Hod'] = hod
            hod_gatepasses = Gatepass.objects.filter(
                g_student__s_branch=hod.Hod_branch,
                g_date=timezone.now().date(),g_status="mentor Approved"
            )

        # Retrieve Mentor gate passes
        if mentor:
            context['Mentor'] = mentor
            mentor_gatepasses = Gatepass.objects.filter(
                g_student__s_mentor=mentor,  # Use the foreign key relationship
                g_type="Emergency",
                g_status="Not Approved",
                g_date=timezone.now().date()
            )

        # Combine HOD and Mentor gate passes based on conditions
        if hod_gatepasses and mentor_gatepasses:
            context['Gatepass'] = hod_gatepasses | mentor_gatepasses  # Combine both querysets
        elif hod_gatepasses:
            context['Gatepass'] = hod_gatepasses  # Only HOD gate passes exist
        elif mentor_gatepasses:
            context['Gatepass'] = mentor_gatepasses  # Only Mentor gate passes exist
        else:
            context['Gatepass'] = None  # No gate passes exist

        context['staff_name'] = staff_name  # Pass staff_name to the template
        return render(request, 'Hitam_gatepass/Emergency_pass.html', context)

    except Faculty.DoesNotExist:
        messages.error(request, "Faculty not found.")
        return redirect('Hitam_gatepass:index')
    
def Faculty_enter(request):
    if request.method == 'POST':
        staff_name = request.POST.get('staff_name')
        password = request.POST.get('password')
        handle()
        try:
            faculty = Faculty.objects.get(F_name=staff_name, F_pass=password)
            print(f"Faculty found: {faculty}")

            # Store staff_name in the session
            request.session['staff_name'] = staff_name

            # Check if the faculty is an HOD
            if Hod.objects.filter(Hod_name=staff_name).exists():
                hod = Hod.objects.get(Hod_name=staff_name)
               
                context = {
                     'Hod' : hod,
                    'Students': Students.objects.filter(s_branch=hod.Hod_branch),
                    'Gatepass': Gatepass.objects.filter(
                        g_student__s_branch=hod.Hod_branch, g_date=timezone.now().date(), g_status="Not Approved",g_type="Normal"
                    ),
                    
                    
                    'staff_name': staff_name  # Pass staff_name to the template
                }
                return render(request, 'Hitam_gatepass/Normal_pass.html', context)

            # Check if the faculty is a Mentor
            elif Mentor.objects.filter(M_name=staff_name).exists():
                mentor = Mentor.objects.get(M_name=staff_name)
                
                
                context = {
                    'Mentor': mentor,
                    'Students': Students.objects.filter(s_mentor=mentor),
                    'Gatepass': Gatepass.objects.filter(
                        g_student__s_mentor=mentor, g_date=timezone.now().date(), g_status="Not Approved",g_type="Emergency"
                    ),
                    
                    'staff_name': staff_name  # Pass staff_name to the template
                    
                }
                return render(request, 'Hitam_gatepass/Emergency_pass.html', context)

            # If the faculty is neither an HOD nor a Mentor
            else:
                return render(request, 'Hitam_gatepass/index.html', {'error': 'You are not authorized to access this page.'})

        except Faculty.DoesNotExist:
            return render(request, 'Hitam_gatepass/index.html', {'error': 'Faculty not found'})

    return render(request, 'Hitam_gatepass/index.html')

from django.shortcuts import redirect, get_object_or_404
from .models import Gatepass

def hod_approve_gatepass(request, gatepass_id):
    gatepass = get_object_or_404(Gatepass, g_id=gatepass_id)
    gatepass.g_status = "Approved"
    gatepass.save()

    # Fetch the student's email
    student_email = gatepass.g_student.s_email  # Assuming `s_email` is a field in the Students model

    # Notify the student
    if student_email:
        subject = "Gate Pass Approved"
        body = f"""Dear {gatepass.g_student.s_name},
            Your gate pass has been approved.
            Details:
            Purpose: {gatepass.g_purpose}
            From: {gatepass.g_out_time}
            To: {gatepass.g_in_time}
            
            Thank you."""
        
        try:
            send_mail(body, subject, student_email)
            messages.success(request, f"Gate pass approved and email sent to {student_email}.")
        except Exception as e:
            messages.error(request, f"Gate pass approved, but email could not be sent: {e}")
    else:
        messages.warning(request, "Gate pass approved, but student email is not available.")

    return redirect('Hitam_gatepass:Emergency_pass')  # Redirect back to the Emergency Pass page

def mentor_approve_gatepass(request, gatepass_id):
    gatepass = get_object_or_404(Gatepass, g_id=gatepass_id)
    gatepass.g_status = "mentor Approved"
    gatepass.save()

    # Fetch the student's HOD
    try:
        student = gatepass.g_student  # Get the student object from the gatepass
        hod = Hod.objects.get(Hod_branch=student.s_branch)
        faculty = Faculty.objects.get(F_name=hod.Hod_name)
        email = faculty.F_email  # Fetch the HOD's email from the Faculty model

        # Notify the HOD
        if email:
            subject = "Gate Pass Approved by Mentor"
            body = f"""Dear {hod.Hod_name}
                The following gate pass has been approved by the mentor:
                Student Name: {student.s_name}
                Roll Number: {student.s_roll}
                Purpose: {gatepass.g_purpose}
                From: {gatepass.g_out_time}
                To: {gatepass.g_in_time}
                
                
                Thank you."""
            
            try:
                send_mail(body, subject, email)
                messages.success(request, f"Gate pass approved and email sent to HOD ({email}).")
            except Exception as e:
                messages.error(request, f"Gate pass approved, but email could not be sent to HOD: {e}")
    except Hod.DoesNotExist:
        messages.warning(request, "Gate pass approved, but HOD not found for the student's branch.")
    except Faculty.DoesNotExist:
        messages.warning(request, "Gate pass approved, but HOD's faculty record not found.")

    return redirect('Hitam_gatepass:Emergency_pass')

def normal_approve_gatepass(request, gatepass_id):
    if request.method == 'POST':
        gatepass = get_object_or_404(Gatepass, g_id=gatepass_id)
        gatepass.g_status = "Approved"
        gatepass.save()
          # Fetch the student's email
        student_email = gatepass.g_student.s_email 
        
        if student_email:
           subject = "Gate Pass Approved"
           body = f"""Dear {gatepass.g_student.s_name},
            Your gate pass has been approved.
            Details:
            Purpose: {gatepass.g_purpose}
            From: {gatepass.g_out_time}
            To: {gatepass.g_in_time}
            
            Thank you."""
        
           try:
              send_mail(body, subject, student_email)
              messages.success(request, f"Gate pass approved and email sent to {student_email}.")
           except Exception as e:
               messages.error(request, f"Gate pass approved, but email could not be sent: {e}")
    else:
        messages.warning(request, "Gate pass approved, but student email is not available.")

    return redirect('Hitam_gatepass:Normal_pass')  # Redirect back to the Emergency Pass page


def apply_gatepass(request):
    staff_name = request.GET.get('staff_name')  # Retrieve staff_name from query parameters
    if not staff_name:
        messages.error(request, "Staff name is required.")
        return redirect('Hitam_gatepass:index')
    context={'staff_name':staff_name}
    try:
        Hod_name = Hod.objects.get(Hod_name=staff_name)
        context['Hod'] = Hod_name
    except Hod.DoesNotExist:
            print("HOD not found")    
    if request.method == 'POST':
        roll_number = request.POST.get('rollNumber')
        student_name = request.POST.get('studentName')
        pass_type = request.POST.get('passType')
        purpose = request.POST.get('purpose')
        from_time = request.POST.get('fromTime')
        to_time = request.POST.get('toTime')

        # Fetch the student object based on roll number
        try:
            student = Students.objects.get(s_roll=roll_number, s_name=student_name)
        except Students.DoesNotExist:
            return HttpResponse("Student not found. Please check the roll number and name.")

        # Save the gate pass to the database
        Gatepass.objects.create(
            g_rol=student,
            g_student=student,
            g_type=pass_type,
            g_purpose=purpose,
            g_out_time=from_time,
            g_in_time=to_time,
            g_status='Not Approved'  # Default status
        )

        # Redirect to a success page or display a success message
        return HttpResponse("Gate Pass Applied Successfully!")
        

    return render(request, 'Hitam_gatepass/passapply.html',context)

def handle():
        today = now().date()
        if today.weekday() == 4:  # Check if today is Wednesday (0=Monday, 2=Wednesday)
            # Use related field lookups for ForeignKey fields
            students = Students.objects.filter(
                s_religian__religion_name='Muslim',  # Assuming `s_religian` is a ForeignKey to Religion
                s_gender__G_name='M'                 # Assuming `s_gender` is a ForeignKey to Gender
            )
            count = 0
            for student in students:
                # Check if a special pass already exists for this student today
                if not Gatepass.objects.filter(
                    g_student=student,
                    g_rol=student,  # Use the student object for g_rol
                    g_type='Special',
                    g_date=today
                ).exists():
                    Gatepass.objects.create(
                        g_student=student,
                        g_rol=student,  # Pass the student object to g_rol
                        g_type='Special',
                        g_purpose='Jumma Namaz',
                        g_out_time=time(12, 50),
                        g_in_time=time(14, 20),
                        g_date=today,
                        g_status='Approved'
                    )
                    count += 1
        
        return 1  # Return 0 if today is not Wednesday


def get_gatepasses(request):
    staff_name = request.GET.get('staff_name')  # Retrieve staff_name from query parameters
    if not staff_name:
        return redirect('Hitam_gatepass:index')

    try:
        # Retrieve the faculty object
        faculty = Faculty.objects.get(F_name=staff_name)
        context = {}

        # Check if the faculty is an HOD or Mentor
        hod = Hod.objects.filter(Hod_name=faculty.F_name).first()
        mentor = Mentor.objects.filter(M_name=faculty.F_name).first()

        hod_gatepasses = mentor_gatepasses = None

        # Retrieve HOD gate passes
        if hod:
            context['Hod'] = hod
            hod_gatepasses = Gatepass.objects.filter(
                g_student__s_branch=hod.Hod_branch,
                g_date=timezone.now().date(),
                g_status="Approved"
            )

        # Retrieve Mentor gate passes
        if mentor:
            context['Mentor'] = mentor
            mentor_gatepasses = Gatepass.objects.filter(
                g_student__s_mentor=mentor,  # Use the foreign key relationship
                g_status="Approved",
                g_date=timezone.now().date()
            )

        # Combine HOD and Mentor gate passes based on conditions
        if hod_gatepasses:
            context['Gatepass'] = hod_gatepasses  # Only HOD gate passes exist
        elif mentor_gatepasses:
            context['Gatepass'] = mentor_gatepasses  # Only Mentor gate passes exist
        else:
            context['Gatepass'] = None  # No gate passes exist

        context['staff_name'] = staff_name  # Pass staff_name to the template
        return render(request, 'Hitam_gatepass/approved.html', context)

    except Faculty.DoesNotExist:
        return redirect('Hitam_gatepass:index')

