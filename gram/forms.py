from django import forms
from . models import Image, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm


class ImageForm(forms.ModelForm): 
    class Meta:
        model = Image
        fields = ['image','image_name','caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class ProfileUpdateForm(forms.Form):
    username = forms.CharField(label='Username',max_length = 30)
    profile_photo = forms.ImageField(label = 'Image Field') 
    bio = forms.CharField(label='Caption',max_length=500)

class UpdateCaption(forms.Form):
    caption = forms.CharField(label='Caption',max_length=300)