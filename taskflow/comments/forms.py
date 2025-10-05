from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':3,'placeholder':'Enter comment'}
        ),
        label=False,
        required=True
    )

    class Meta:
        model = Comment
        fields = ['comment']

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return comment