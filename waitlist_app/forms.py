from django import forms
from .models import WaitlistEntry
from ingabotool import is_valid_email

class WaitlistEntryForm(forms.ModelForm):
    class Meta:
        model = WaitlistEntry
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not is_valid_email(email):
            raise forms.ValidationError("Please enter a valid email format.")
        return email
