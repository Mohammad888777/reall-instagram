from django import forms
from .models import Profile
from django.core.validators import FileExtensionValidator

class ProfileForm(forms.ModelForm):

    image = forms.ImageField(required=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class pt-2': 'input', 'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'URL'}), required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=True)


    class Meta:

        model=Profile
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for k,v in self.fields.items():
            v.widget.attrs.update({
                "class":"input"
            })
        
