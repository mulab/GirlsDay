from django import forms
from .models import User
from image_cropping import ImageCropWidget


class ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'cropping',)
