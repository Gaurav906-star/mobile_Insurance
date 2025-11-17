from django import forms
from insurance_app.models import Device
from datetime import date
from django.core.exceptions import ValidationError

# Form to register Device
class DeviceForm(forms.ModelForm):
  purchase_date = forms.DateField(
      widget= forms.DateInput(attrs={'type':'date','class':'form-control'}),
      help_text="Date you purchased this device"
    )

  class Meta:
    model = Device
    fields = ['name','brand','model','purchase_date','imei_number']
    

    widgets = {
      'name': forms.TextInput(attrs={'class':'form-control'}),
      'brand':forms.Select(attrs={'class':'form-control'}),
      'model':forms.TextInput(attrs={'class':'form-control'}),
      'imei_number':forms.TextInput(attrs={'class':'form-control'})
      }
    
  def clean_purchase_date(self):
       purchase_date =  self.cleaned_data.get('purchase_date')
       if purchase_date and purchase_date> date.today():
         raise ValidationError("Purchase date cannot be in future")
       
       return purchase_date


