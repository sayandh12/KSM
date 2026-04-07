from django import forms
from .models import CaseStudy

class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = ['title', 'client', 'description', 'image', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-check-input',
                })
        self.fields['description'].widget.attrs.update({'rows': 5})
