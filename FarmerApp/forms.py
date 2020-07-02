from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate


class FarmerForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model=Farmer
        fields=[ 'username', 'email','dob','is_farmer','aadhar_no','region','password', 'confirm_password']

        labels = {
        "dob": "Date Of Birth",
        'is_farmer': 'Register as a farmer',
        'aadhar_no':'Enter Your Aadhar card number',
        'region':'Region where your farm lies',
        }
    def clean(self):
        cleaned_data = super(FarmerForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")


class BuyerForm(ModelForm):
    	password = forms.CharField(label='Password', widget=forms.PasswordInput)
    	confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    	class Meta:
    		model=Buyer
    		fields=[ 'username', 'email','dob','is_farmer','aadhar_no','pan_no','password', 'confirm_password']

    		labels = {
            "dob": "Date Of Birth",
            'is_farmer': 'Register as a farmer',
            'aadhar_no':'Enter Your Aadhar card number',
            'pan_no':'Enter Your PAN card number',
        	}
    	def clean(self):
    		cleaned_data = super(BuyerForm, self).clean()
    		password = cleaned_data.get("password")
    		confirm_password = cleaned_data.get("confirm_password")
    		if password != confirm_password:
    			raise forms.ValidationError("Passwords don't match")


class AccountAuthenticationForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control','id':'submit','placeholder':"Username"}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control','placeholder':'Password'}),
    )
    class Meta:
        model = Account
        fields = ('username', 'password')

        def __init__(self, *args, **kwargs):
            super(Meta ,self.__init__(*args,**kwargs))
            self.fields[
                        'username'
            ].widget.attrs['class'] = 'form-control'
            self.fields[
                        'username'
            ].widget.attrs['id'] = 'submit'

    def clean(self):
        print(self.cleaned_data['username'])
        print(self.cleaned_data['password'])
        if self.is_valid():
            print("here")
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            print(password)
            print(authenticate(password=password,username=username))
            if not authenticate(password=password,username=username):
                raise forms.ValidationError("Invalid login")
