from django.db import models
from django.conf import settings

class Policy(models.Model):
  name = models.CharField(max_length=100,unique=True)
  description = models.TextField(max_length=500,help_text="details about policy")
  monthly_premium = models.DecimalField(max_digits=10,decimal_places=2,help_text="premium pay per month")
  is_active = models.BooleanField(default=True)
  deductible = models.DecimalField(max_digits=10,decimal_places=2,help_text="amount user have to pay")
  max_coverage_limit = models.DecimalField(max_digits=10,decimal_places=2,help_text="maximum amout company will pay")

  def __str__(self):
    return self.name
  

class Device(models.Model):
   
   DEVICE_BRAND = [('Apple','Apple'),('Google','Google'),('Samsung','Samsung'),('OnePlus','OnePlus')] 


   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='devices',help_text="the owner details")
   name = models.CharField(max_length=100, help_text="your device name")
   brand = models.CharField(choices=DEVICE_BRAND,max_length=50,default='Apple',help_text='device brand name')
   model = models.CharField( max_length=50,help_text="your device model like iphone 15 pro ")
   purchase_date = models.DateField()
   imei_number = models.CharField(max_length=50,help_text="enter your mobile IMEI number", unique=True)

   def __str__(self):
     return f"{self.name} - {self.brand}"
   



class Customer_Policy(models.Model):
    
    STATUS = [('ACTIVE','ACTIVE'),('EXPIRE','EXPIRED'),('CANCELLED','CANCELLED')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='customer_policies',help_text='customer belongs to this policy')

    policy = models.ForeignKey(Policy,on_delete=models.PROTECT,help_text="policy belongs to this customer",related_name="purchased_policies")

    device = models.ForeignKey(Device,on_delete=models.PROTECT, related_name = 'coverage_contracts', help_text="specific mobile device cover")

    
    start_date = models.DateField()
    end_date = models.DateField()
    status =  models.CharField(max_length=10,choices=STATUS,help_text='Contract status')

    def __str__(self):
       return f"{self.policy.name}-{self.status}"

    


   

class Claim(models.Model):
   
   STATUS = [('DR','Draft'),('RV','Review'),('AP','Approved'),('RJ','Rejected')]

   customer_policy = models.ForeignKey(Customer_Policy,on_delete=models.PROTECT,related_name='claims')
   
   incident_date = models.DateTimeField(help_text='incident date and time')

   status =  models.CharField(max_length=2,choices=STATUS,help_text='policy status')

   deductible_amount = models.DecimalField(max_digits=10,decimal_places=2,help_text='amount that is deducted')

   claim_amount_approved = models.DecimalField(max_digits=10,decimal_places=2,help_text='amount apprvoed in claim')

   submission_date = models.DateTimeField(auto_now_add=True)

   incident_description = models.TextField(max_length=500, help_text='detail about incident')
   
   estimated_repair_cost = models.DecimalField(max_digits=10, decimal_places=2,help_text='total repair cost')


   def __str__(self):
      return f"{self.id}-{self.customer_policy.user.username}-{self.status}"




   
 
     


