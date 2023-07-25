from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
User = get_user_model()



class UserRegistrationForm(UserCreationForm):
    username=forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'middle_name', 'last_name']
        

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about_me', "profile_picture", "phone_number", "address", "resume"]
    
    #to validate form fields all in single function
    def clean(self):
        pass


    def clean_profile_picture(self):
        pp = self.cleaned_data.get('profile_picture')
        if pp:
            extension = pp.name.split(".")[-1]
            if extension.lower() not in ['jpg', 'png', 'jpeg', 'svg']:
                raise ValidationError("Profile Picture must be in IMage FFormat")
        return pp


    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            ext = resume.name.split(".")[-1]  #resume.pdf
            if ext.lower() not in ['pdf']:
                  raise ValidationError("Resume must be in pdf format")
        return resume


