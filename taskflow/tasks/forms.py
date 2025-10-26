from django import forms
from .models import Task
from tempus_dominus.widgets import DatePicker
from django.utils import timezone
from projects.utils import STATUS_CHOICES,PRIORITY_CHOICES

class TaskUpdateForm(forms.ModelForm):
    # Hidden
    task_id = forms.CharField(widget=forms.HiddenInput(),required=True)

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':3,'placeholder':'Enter task description'}
        ),
        required=False
    )
    start_date = forms.DateField(
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        ),
        required=False
    )
    due_date = forms.DateField(
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        ),
        required=False
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        required=True
        )

    class Meta:
        model = Task
        fields = ['name','description','priority','start_date','due_date']