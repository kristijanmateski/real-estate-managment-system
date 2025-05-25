from django import forms

from app.models import RealState


class RealStateForm(forms.ModelForm):
    class Meta:
        model = RealState
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RealStateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(field_name)
            if field_name not in ["reserved", "sold"]:
                field.widget.attrs['class'] = 'form-control'
