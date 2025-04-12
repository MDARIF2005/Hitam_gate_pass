from django import forms
from .models import Hod, Mentor, Students, Gatepass, Faculty, Branch, Year, Section, Religion, Gender

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['s_roll', 's_name', 's_email', 's_religian', 's_img', 's_year', 's_branch', 's_section', 's_mentor', 's_attendec_present', 's_gender']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        if 's_year' in self.data and 's_branch' in self.data and 's_section' in self.data:
            try:
                year_id = int(self.data.get('s_year'))
                branch_id = int(self.data.get('s_branch'))
                section_id = int(self.data.get('s_section'))
                self.fields['s_mentor'].queryset = Mentor.objects.filter(M_year_id=year_id, M_branch_id=branch_id, M_section_id=section_id)
            except (ValueError, TypeError):
                pass  # Invalid input from the client; fallback to empty Mentor queryset
        elif self.instance.pk:
            # Use the explicitly defined related_name
            self.fields['s_mentor'].queryset = self.instance.s_mentor.students.all()
        self.fields['s_mentor'].label_from_instance = lambda obj: f"{obj.M_name.F_name}"

class GatepassForm(forms.ModelForm):
    class Meta:
        model = Gatepass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GatepassForm, self).__init__(*args, **kwargs)
        self.fields['g_rol'].queryset = Students.objects.all()
        self.fields['g_student'].queryset = Students.objects.all()
        
        # Display only the student's name (s_name) in the dropdown
        self.fields['g_rol'].label_from_instance = lambda obj: f"{obj.s_roll}"  # Keeps roll number for g_rol
        self.fields['g_student'].label_from_instance = lambda obj: f"{obj.s_name}"  # Only shows s_name for g_student

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MentorForm, self).__init__(*args, **kwargs)
        self.fields['M_id'].queryset = Faculty.objects.all()
        self.fields['M_name'].queryset = Faculty.objects.all()
        self.fields['M_id'].label_from_instance = lambda obj: f"{obj.F_id}"
        self.fields['M_name'].label_from_instance = lambda obj: f"{obj.F_name}"

class HodForm(forms.ModelForm):
    class Meta:
        model = Hod
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HodForm, self).__init__(*args, **kwargs)
        self.fields['Hod_id'].queryset = Faculty.objects.all()
        self.fields['Hod_name'].queryset = Faculty.objects.all()
        self.fields['Hod_id'].label_from_instance = lambda obj: f"{obj.F_id}"
        self.fields['Hod_name'].label_from_instance = lambda obj: f"{obj.F_name}"

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['branch_name']
        widgets = {
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Branch Name'}),
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['year_name']
        widgets = {
            'year_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year Name'}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_name']
        widgets = {
            'section_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Section Name'}),
        }

class ReligionForm(forms.ModelForm):
    class Meta:
        model = Religion
        fields = ['religion_name']
        widgets = {
            'religion_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Religion Name'}),
        }

class GenderForm(forms.ModelForm):
    class Meta:
        model = Gender
        fields = ['G_name']
        widgets = {
            'G_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Gender Name'}),
        }