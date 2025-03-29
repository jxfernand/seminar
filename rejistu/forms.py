from django import forms
from .models import Registrant, AccessPass
from .institution import Institution  # Import Institution from the new file
from django.views.decorators.csrf import csrf_exempt

class RegistrantForm(forms.ModelForm):
    signature_data = forms.CharField(widget=forms.HiddenInput(), required=False)  # Add hidden field for signature data
    access_pass_code = forms.CharField(max_length=10, required=True, label="Access Pass Code")

    class Meta:
        model = Registrant
        fields = '__all__'
        exclude = ['signature', 'qr_code','access_pass']  # Exclude these fields from the form
        # exclude = ['signature','access_pass', 'qr_code']  # Exclude these fields from the form
         
        widgets = {
            'institution': forms.Select(attrs={'class': 'form-control'}),  # Use a dropdown widget
        }

    def clean_access_pass_code(self):
        access_pass_code = self.cleaned_data['access_pass_code']
        access_pass = AccessPass.objects.filter(code=access_pass_code, is_used=False).first()

        if not access_pass:
            raise forms.ValidationError("Invalid or already used Access Pass code.")

        return access_pass

    def save(self, commit=True):
        registrant = super().save(commit=False)
        registrant.access_pass = self.cleaned_data['access_pass_code']

        if commit:
            registrant.save()

        return registrant
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].queryset = Institution.objects.all()  # Populate with institutions


    def clean(self):
        cleaned_data = super().clean()
        institution = cleaned_data.get('institution')

        # Check if the institution has reached its quota
        if institution and institution.access_pass_counter >= institution.quota:
            raise forms.ValidationError(f"The institution {institution.name} has reached its quota of {institution.quota} access passes.")


        return cleaned_data
