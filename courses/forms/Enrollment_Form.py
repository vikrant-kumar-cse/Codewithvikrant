from django import forms
from courses.models import UserCourse, Course
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = UserCourse  # Use the correct model
        fields = ['course']  # Only the course field

    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
