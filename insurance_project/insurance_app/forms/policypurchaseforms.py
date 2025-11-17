
from insurance_app.models import Customer_Policy,Policy,Device
from django import forms
from django.core.exceptions import ValidationError

class PolicyPurchaseForm(forms.ModelForm):

  policy = forms.ModelChoiceField(
    queryset= Policy.objects.filter(is_active=True),
    widget=forms.Select(attrs={'class':'form-control'}),
    help_text='Select the insurance plan you want'
  )

  device = forms.ModelChoiceField(
    queryset= Device.objects.all(),
    widget=forms.Select(attrs={'class':'form-control'}),
    help_text='Select the devices for policy purchase'
  )


  class Meta:
    model = Customer_Policy
    fields = ['policy','device']


  def __init__(self, *args, user=None, **kwargs):
      super().__init__( *args, **kwargs)

      if user:
         querySet = Device.objects.filter(user=user);
         if querySet.exists():
           self.fields['device'].queryset = querySet
        

  def clean(self):
      cleaned_data = super().clean()
      device =  cleaned_data.get('device')
      # check if any active policy is running on give device
      if device and Customer_Policy.objects.filter(device=device,status = 'ACTIVE').exists():
        raise ValidationError("This device already have a running active policy")
      
      return cleaned_data

    
      

