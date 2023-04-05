from django import forms
from django.contrib.auth.models import User
from .models import DueReceipt,Level,Department,Student,SessionYearModel
from django.db import transaction



class DueReceiptCreateForm(forms.ModelForm):
    account_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Account name",
                "class": "form-control"
            }
        ))
    account_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Account address",
                "class": "form-control"
            }
        ))
    our_reference = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "our reference",
                "class": "form-control"
            }
        ))
    transaction_amount = forms.IntegerField(
        min_value=3000,
        max_value=3000,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "transaction_amount",
                "class": "form-control"
            }
        ))
    transaction_account = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "transaction_account",
                "class": "form-control"
            }
        ))
    
    file_name = forms.ImageField()
   
    class Meta:
        model = DueReceipt
        fields = ('account_name', 'account_address', 'our_reference', 
                  'transaction_amount','transaction_account','file_name',
                  'level','department')
    



class DueReceiptUpdateForm(forms.ModelForm):
    is_validated = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                "placeholder": "validate",
                # "class": "form-control"
            }
        ))
    class Meta:
        model =DueReceipt
        fields = ('is_validated',)


