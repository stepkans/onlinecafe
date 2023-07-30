from django import forms
from .models import MyUser

class MyUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean(self):
        cleaned_data = super(MyUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Password does not match!")    
        else: 
            raise forms.ValidationError("Passwords can't be blank.")       