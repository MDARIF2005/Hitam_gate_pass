from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

class Branch(models.Model):
    brach_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.branch_name

class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.year_name

class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.section_name

class Religion(models.Model):
    religion_id = models.AutoField(primary_key=True)
    religion_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.religion_name

class Gender(models.Model):
    G_id = models.AutoField(primary_key=True)
    G_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.G_name

class Faculty(models.Model):
    F_id = models.AutoField(primary_key=True)
    F_name = models.CharField(max_length=50, unique=True)
    F_email = models.EmailField()
    F_mobile = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$')],
        help_text="Enter a valid 10-digit mobile number"
    )
    F_pass = models.CharField(max_length=50)
    F_gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="faculty_gender")
    
    def __str__(self):
        return self.F_name

class Hod(models.Model):
    Hod_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='hod_id', to_field='F_id')
    Hod_name = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='hod_name', to_field='F_name')
    Hod_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='hod_branch')
    
    def __str__(self):
        return f"{self.Hod_id.F_id}, {self.Hod_name.F_name}, {self.Hod_branch.branch_name}"

class Mentor(models.Model):
    M_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='mentor_id', to_field='F_id')
    M_name = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='mentor_name', to_field='F_name')
    M_year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='mentor_year')
    M_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='mentor_branch')
    M_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='mentor_section')
    
    def __str__(self):
        return self.M_name.F_name  # Return only the mentor's name for display

class Students(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_roll = models.CharField(max_length=50,unique=True)
    s_name = models.CharField(max_length=50)
    s_email = models.EmailField()
    s_gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="student_gender")
    s_religian = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='student_religion')
    s_img = models.URLField()
    s_year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='student_year')
    s_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='student_branch')
    s_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='student_section')
    s_mentor = models.ForeignKey(
        Mentor,
        on_delete=models.CASCADE,
        related_name='students'  # Define the reverse relationship
    )
    s_attendec_present = models.DecimalField(
        max_digits=5,  # Total number of digits (e.g., 100.00 requires 5 digits)
        decimal_places=2,  # Number of decimal places
        default= Decimal('0.00')  # Default value
    )    
    def __str__(self):
        return self.s_roll  # Return only the roll number for display
    
    def get_image_url(self):
        if self.s_img:
            return self.s_img
        return "https://res.cloudinary.com/dsw0kcvkq/image/upload/c_crop,g_auto,h_800,w_800/defalt/dz4zkrnksjwcqh0mceew"


class Gatepass(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_rol = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='gatepasses_as_rol')
    g_student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='gatepasses_as_student')
    g_purpose = models.TextField()
    g_type = models.CharField(max_length=50)
    g_out_time = models.TimeField()
    g_in_time = models.TimeField()
    g_status = models.CharField(max_length=50, default="Not Approved")
    g_date = models.DateField(auto_now_add=True)
    g_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Gatepass {self.g_id} - {self.g_student.s_name} ({self.g_type})"

    def clean(self):
        if self.g_out_time >= self.g_in_time:
            raise ValidationError("Out time must be earlier than in time.")





