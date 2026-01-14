from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class postForm(forms.Form):
    newPost = forms.CharField(label = "New Post", required=False, max_length=300, widget= forms.TextInput(attrs={'id': 'id_post_input_text'}))

class commentForm(forms.Form):
    comment = forms.CharField(label = "Comment", required=False, max_length=300, widget= forms.TextInput(attrs={'id': 'id_comment_input_text_n'}))

class LoginForm(forms.Form):
    username = forms.CharField(required=False, max_length=20, widget= forms.TextInput(attrs={'id': 'id_username'}))
    password = forms.CharField(required=False, max_length=20, widget=forms.PasswordInput(attrs={'id': 'id_password'}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function
        # Gets a dictionary of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(required=False, max_length=20,widget= forms.TextInput(attrs={'id': 'id_username'}))
    password = forms.CharField(label = "Password", max_length=20, widget = forms.PasswordInput(attrs={'id': 'id_password'}))
    confirm = forms.CharField(label = "Confirm", max_length=20, widget = forms.PasswordInput(attrs={'id': 'id_confirm_password'}))
    email = forms.CharField(max_length=50, widget = forms.EmailInput(attrs={'id': 'id_email'}))
    first_name = forms.CharField(max_length=20, widget= forms.TextInput(attrs={'id': 'id_first_name'}))
    last_name = forms.CharField(max_length=20, widget= forms.TextInput(attrs={'id': 'id_last_name'}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function
        # Gets a dictionary of cleaned data as a result
        cleaned_data = super().clean()

        # Add an extra validation
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm')
        if password1 and password2 and password1 != password2:
            # Generates a form error (non-field error)
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
    def clean_username(self):
        # Confirms that the username is not already present in the User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            # Generates a field error specific to the field (username here)
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data dictionary
        return username