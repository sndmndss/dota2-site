from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    match_id = forms.ChoiceField(choices=[])

    class Meta:
        model = Comment
        fields = ('text', 'match_id')
