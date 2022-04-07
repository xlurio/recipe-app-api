from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a
    repeated password"""
    password_one = forms.CharField(label='Password',
                                   widget=forms.PasswordInput)
    password_two = forms.CharField(label='Verify password',
                                   widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name']

    def clean_password_two(self):
        # Check if both passwords matches
        password_one = self.cleaned_data.get('password_one')
        password_two = self.cleaned_data.get('password_two')
        if password_one and password_two and password_one != password_two:
            raise ValidationError("Passwords don't match")
        return password_two

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password_one'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user model,
    but replaces the password field with admin's disabled password hash display
    field"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'
