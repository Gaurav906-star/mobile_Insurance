
from django import forms
from insurance_app.models import Claim,Customer_Policy
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError

class ClaimForm(forms.ModelForm):

  incident_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        help_text="Exact incident time and date."
    )



  class Meta:
    model=Claim
    fields = (
            'customer_policy', 
            'incident_date', 
            'estimated_repair_cost', 
            'incident_description'
        )

    widgets = {
      'customer_policy':forms.Select(attrs={'class':'form-control'}),
      'incident_description':forms.Textarea(attrs={'class':'form-control','row':4}),
      'estimated_repair_cost':forms.NumberInput(attrs={'class':'form-control','min':0})

    }


  def __init__(self, *args, user=None, **kwargs):
    super().__init__( *args, **kwargs)

    if user:
      active_policies = Customer_Policy.objects.filter(user=user, status='ACTIVE')
      print('active policies',active_policies)
      self.fields['customer_policy'].queryset = active_policies

    self.fields['estimated_repair_cost'].required = True


  def clean_incident_date(self):
   incident_date = self.cleaned_data.get('incident_date')
   customer_policy = self.cleaned_data.get('customer_policy')

   incident_date_only = incident_date.date()

   if incident_date and incident_date_only > date.today():
     raise ValidationError("incident date should not be a future date")
   
   if incident_date and customer_policy:
      
      policy_start = customer_policy.start_date
      policy_end = customer_policy.end_date

      if(not policy_start <=incident_date_only <= policy_end):
        raise ValidationError(
          f"Incident date is outside the policy coverage period"
        )
     
     
   return incident_date
