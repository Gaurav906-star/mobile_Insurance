from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Policy,Customer_Policy,Device,Claim
from .forms.policypurchaseforms import PolicyPurchaseForm
from .forms.claimform import ClaimForm
from .forms.deviceform import DeviceForm
from django.urls import reverse_lazy
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings

class PolicyListView(ListView):

  model = Policy
  template_name = 'insurance_app/policy_list.html'
  context_object_name = 'policies'

  def get_queryset(self):
    return Policy.objects.filter(is_active=True)
  

class PolicyPurchaseView(LoginRequiredMixin, CreateView):

  model = Customer_Policy
  form_class = PolicyPurchaseForm
  template_name = 'insurance_app/policy_purchase.html'
  success_url = reverse_lazy('my_policies') 

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.start_date = date.today()
    form.instance.end_date = date.today()+timedelta(days=365)

    form.instance.status = 'ACTIVE'

    return super().form_valid(form)
  
class DeviceRegisterView(LoginRequiredMixin, CreateView):
  model = Device
  form_class = DeviceForm
  template_name = 'insurance_app/device_register.html'
  success_url = reverse_lazy('policy_purchase')


  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  

class ClaimSubmitView(LoginRequiredMixin,CreateView):

   model = Claim
   form_class = ClaimForm
   template_name = 'insurance_app/claim_submit.html'
   success_url = reverse_lazy('my_claims')


   def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs
   
   def form_valid(self, form):
       form.instance.status = 'DR'
       
       policy = form.instance.customer_policy.policy
       form.instance.claim_amount_approved = 0
       form.instance.deductible_amount = policy.deductible

       return super().form_valid(form)
   
class MyPoliciesView(LoginRequiredMixin,ListView):
  model = Customer_Policy
  template_name = 'insurance_app/my_policies.html'
  context_object_name = 'customer_policies'
  
  def get_queryset(self):
    return Customer_Policy.objects.filter(user=self.request.user).order_by('-start_date')


class MyClaimView(LoginRequiredMixin,ListView):
  model = Claim
  template_name = 'insurance_app/my_claims.html'
  context_object_name = 'my_claims'

  def get_queryset(self):
    return Claim.objects.filter(customer_policy__user = self.request.user).order_by('-submission_date')
  
  
def signup(request):
  if request.user.is_authenticated:
    return redirect('/login')
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request,user)
      return redirect('policy_list')
  else: 
    form = UserCreationForm()
  return render(request,"registration/signup.html",{'form':form})


  
