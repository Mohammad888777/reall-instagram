from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):

    # image=forms.ImageField(label='',required=False)

    body=forms.CharField(label='',widget=forms.TextInput(attrs={
        # 'rows':1,
        'placeholder':'Add a comment ...',
        'class':'form-control'
    })) 
    class Meta:
        model=Comment
        fields=["body"]
    