from django import forms
from .models import Post



class PostForm(forms.ModelForm):

    picture=forms.ImageField(required=True)
    caption=forms.CharField(required=True,widget=forms.TextInput(attrs={
        "class":"input",
        "placeholder":"Caption"
        }))
    tags=forms.CharField(required=True,widget=forms.TextInput(attrs={
        "class":"input",
        "placeholder":"Tags | Seprate with comma "
    }))


    class Meta:

        model=Post
        fields=["picture","caption","tags"]