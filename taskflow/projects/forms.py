from django import forms
from django.contrib.auth.models import User
from tempus_dominus.widgets import DatePicker
from .models import Project
from teams.models import Team
from .utils import STATUS_CHOICES,PRIORITY_CHOICES

class ProjectForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':3,'placeholder':'Enter project description'}
        ),
        label=False,
        required=True
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'Enter project name'}
        ),
        label=False,
        required=False
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
        )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
        )
    client_company = forms.CharField(
        label=False,
        required=True
    )
    start_date = forms.DateField(
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        ),
        label=False,
        required=True
    )
    due_date = forms.DateField(
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        ),
        label=False,
        required=True
    )
    class Meta:
        model = Project
        fields = ['name', 'owner', 'team', 'client_company', 'description', 'status', 'priority', 'start_date', 'due_date']