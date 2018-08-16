from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    title = forms.CharField(label="제목", label_suffix="", widget=forms.TextInput(attrs={'class': 'form-control', 'style' : 'margin-top: 5px; margin-bottom: 5px;'}))
    content = forms.CharField(label="내용", label_suffix="", widget=forms.Textarea(attrs={'class': 'form-control', 'style' : 'margin-top: 5px; margin-bottom: 5px;'}))

    # title.label_classes = ('class_a' )
    class Meta:
        model = Post
        fields = '__all__'
