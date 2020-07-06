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

class SearchForm(forms.Form):
    search_string = forms.CharField(label='search field', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_string'].widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Search', 'aria-label': 'Search'})