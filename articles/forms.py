from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'}) 
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows' : '5'})

    class Meta:
        model = Comment
        fields = ('name', 'text')