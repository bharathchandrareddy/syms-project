from django import forms
from.models import Post,Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField()
    class Meta:
        model = Post
        fields = ('content','image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label=''
                           ,widget=forms.TextInput(attrs={'placeholder':'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)