from django import forms
from .models import MyUser, UserProfile
from .validators import allow_only_images_validator

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
        
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model =  UserProfile
        fields = ['profile_picture', 'cover_photo', 'address' , 'country', 'state', 'city','pin_code', 'latitude', 'longitude']     
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs) 
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'  