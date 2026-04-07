from django import forms
from .models import GalleryImage

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
