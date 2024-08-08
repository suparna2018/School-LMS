# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from app_users.models import UserProfileInfo

# class UserForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta():
#         model = User
#         fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

#         # widgets = {
#         # "password":"forms.PasswordInput()",
#         # }

#         labels = {
#         'password1':'Password',
#         'password2':'Confirm Password'
#         }

# class UserProfileInfoForm(forms.ModelForm):
#     bio = forms.CharField(required=False)
#     teacher = 'teacher'
#     student = 'student'
#     parent = 'parent'
#     user_types = [
#         (student, 'student'),
#         (parent, 'parent'),
#     ]
#     user_type = forms.ChoiceField(required=True, choices=user_types)

#     class Meta():
#         model = UserProfileInfo
#         fields = ('bio', 'profile_pic', 'user_type')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import UserProfileInfo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

class UserProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    teacher = 'teacher'
    student = 'student'
    parent = 'parent'
    user_types = [
        (student, 'student'),
        (parent, 'parent'),
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)

    class Meta():
        model = UserProfileInfo
        fields = ('bio', 'profile_pic', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        

class SimpleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include fields you want to test