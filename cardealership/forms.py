from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *
from .const import BODY_TYPE_CHOICES, FUEL_TYPE_CHOICES, TRANSMISSION_TYPES


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'  # ввод с краями, на весь контейнер
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }), required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }), required=False)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    password2 = forms.CharField(label='Confirm a password', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    pfp = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'file-input file-input-bordered w-full'
    }))

    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'Please be considerate and do not share too much of your personal information'
    }))

    contact_info = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))


    class Meta:
        model = ProfileUser
        fields = ('pfp', 'location', 'contact_info')


class EditUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ChangeUserPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full'
    }))


class CreateListingForm(forms.ModelForm):
    brand = forms.ModelChoiceField(label='Car brand', queryset=Brand.objects.all(), widget=forms.Select(attrs={
        'class': 'select select-bordered w-full'
    }))

    model = forms.CharField(label='Car model', widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    transmission = forms.ChoiceField(choices=TRANSMISSION_TYPES, label='Transmission', widget=forms.Select(attrs={
        'class': 'select select-bordered w-full'
    }))

    fuel_type = forms.ChoiceField(choices=FUEL_TYPE_CHOICES, label='Fuel type', widget=forms.Select(attrs={
        'class': 'select select-bordered w-full'
    }))

    release_date = forms.CharField(label='Release date (year)', widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    horsepower = forms.IntegerField(label='Horsepower', widget=forms.NumberInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    body_type = forms.ChoiceField(choices=BODY_TYPE_CHOICES, label='Body type', widget=forms.Select(attrs={
        'class': 'select select-bordered w-full'
    }))

    mileage = forms.IntegerField(label='Mileage', widget=forms.NumberInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class': 'textarea textarea-bordered w-full'
    }))

    colors_available = forms.CharField(label='Color', widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    price = forms.IntegerField(label='Price', widget=forms.NumberInput(attrs={
        'class': 'input input-bordered w-full'
    }))

    class Meta:
        model = Car
        fields = ('brand', 'model', 'transmission', 'fuel_type', 'release_date', 'horsepower', 'body_type', 'mileage', 'description', 'colors_available', 'price')


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):  # для принятия нескольких картинок
    def clean(self, value, initial=None):  # override the methsd
        valid = []

        for image in value or []:  # iterate over images in the list in order to validate
            image = super().clean(image, initial)  # right here
            valid.append(image)  # and add the valid image to the list

        if not valid and self.required:
            raise ValidationError("At least one photo must be uploaded")

        return valid


class CreateImageListingForm(forms.ModelForm):
    image = MultipleImageField(label='Image', widget=MultipleFileInput(attrs={
        'class': 'file-input file-input-bordered w-full',
    }))

    class Meta:
        model = CarImage
        fields = ('image',)


class EditImageListingForm(forms.ModelForm):
    image = MultipleImageField(required=False, label='Image', widget=MultipleFileInput(attrs={
        'class': 'file-input file-input-bordered w-full',
    }))

    class Meta:
        model = CarImage
        fields = ('image',)



class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Write a comment...',widget=forms.Textarea(attrs={
        'class': 'textarea textarea-bordered w-full h-20'
    }))

    class Meta:
        model = Comment
        fields = ('text',)


