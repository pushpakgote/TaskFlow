from django import forms
from django.contrib.auth.models import User
from .models import Team
from tempus_dominus.widgets import DatePicker

class TeamForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter Team Description"})
        , label=False
        , required=True
        )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':"Enter Team Name"})
        , label=False
        , required=True
        )
    team_lead = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        widget=forms.Select(
            attrs={"class":"form-control select2"}
        ),
        label=False, 
        required=True
        )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        widget=forms.SelectMultiple(
            attrs={"class":"form-control select2"}
        ),
        label=False, 
        required=True
        )
    
    class Meta:
        model = Team
        fields = [
            'name',
            'description',
            'team_lead',
            'members'
        ]
