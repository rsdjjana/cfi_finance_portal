from django import forms
from finance.models import *


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class BillForm(forms.ModelForm):
    class Meta:
        model=BillDetail
        exclude= ('advance','project')
        
        
class AdvanceForm(forms.ModelForm):
    class Meta:
        model=Advance
        fields=('amount','split_up')
        
class AdvanceFormCoreApproval(forms.ModelForm):
    class Meta:
        model=Advance
        fields=('approved','disapproved','core_comment')
        
class ReimbForm(forms.ModelForm):
    class Meta:
        model=Reimb
        fields=('amount',)
        
class ReimbFormCore(forms.ModelForm):
    class Meta:
        model=Reimb
        fields=('received','received_date','submitted',)
    
