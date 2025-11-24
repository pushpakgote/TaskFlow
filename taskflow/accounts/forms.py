from django import forms
from .models import Profile
from tempus_dominus.widgets import DatePicker

class ProfileUpdateForm(forms.ModelForm):
    education_level = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your educational level here ..."}
        ),
        required=False
    )

    skills = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your skills here ..."}
        ),
        required=False
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your bior here ..."}
        ),
        required=False
    )

    date_of_birth = forms.DateTimeField(
        label=False,
        required=False,
        widget=DatePicker(
            attrs = {
                # 'append': 'fa fa-calendar',
                # 'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ['job_title', 'profile_picture', 'education_level', 'skills', 'bio', 'phone_number', 'location', 'date_of_birth']

