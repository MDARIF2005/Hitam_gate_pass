from django.contrib import admin
from .models import Branch, Mentor, Year, Section, Faculty, Hod, Students, Gatepass, Religion, Gender
from .forms import StudentForm, GatepassForm, MentorForm, HodForm

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('brach_id', 'branch_name')  # Display fields in the admin list view
    search_fields = ('branch_name',)  # Add a search bar for branch_name

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year_id', 'year_name')
    search_fields = ('year_name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'section_name')
    search_fields = ('section_name',)

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display = ('religion_id', 'religion_name')
    search_fields = ('religion_name',)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('G_id', 'G_name')
    search_fields = ('G_name',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('F_id', 'F_name', 'F_email', 'F_mobile', 'F_gender', 'F_pass')

class HodAdmin(admin.ModelAdmin):
    form = HodForm
    list_display = ('Hod_id', 'Hod_branch')

class MentorAdmin(admin.ModelAdmin):
    form = MentorForm
    list_display = ('M_id', 'M_year', 'M_branch', 'M_section')

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('s_id', 's_roll', 's_name', 's_email', 's_year', 's_branch', 's_section', 's_religian', 's_mentor', 's_gender', 's_attendec_present')

class GatepassAdmin(admin.ModelAdmin):
    form = GatepassForm
    list_display = ('g_id', 'g_rol', 'g_student', 'g_date', 'g_time', 'g_purpose', 'g_out_time', 'g_in_time', 'g_status')

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('s_id', 's_roll', 's_name', 's_email', 's_year', 's_branch', 's_section', 's_mentor')
    search_fields = ('s_roll', 's_name', 's_email')

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Hod, HodAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Gatepass, GatepassAdmin)