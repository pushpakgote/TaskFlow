from django import forms
from .models import Task
from tempus_dominus.widgets import DatePicker
from django.utils import timezone
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES
from accounts.models import Profile
from django.contrib.auth.models import User

class TaskUpdateForm(forms.ModelForm):
    # Hidden
    task_id = forms.CharField(widget=forms.HiddenInput(),required=False)

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':3,'placeholder':'Enter task description'}
        ),
        required=False
    )
    user_assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        # queryset=None,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        required=False,
        label="Assigned To"
    )
    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'class': 'datepicker'}
        ),
        required=False
    )
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'class': 'datepicker'}
        ),
        required=False
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        required=False
        )

    class Meta:
        model = Task
        fields = ['name','description','priority','start_date','due_date','user_assigned_to']

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            self.fields['user_assigned_to'].queryset = team