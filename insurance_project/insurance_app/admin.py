from django.contrib import admin
from .models import *

# Register your models here.



@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
  list_display = ('name','monthly_premium','max_coverage_limit','is_active')
  list_filter = ['is_active']
  search_fields = ('name','description')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
  list_display = ('name','user','brand','model','imei_number','purchase_date')
  list_filter = ('imei_number', 'model', 'user__username')
  search_fields = ('name','brand','model')
  raw_id_fields = ('user',)


@admin.register(Customer_Policy)
class CustomerPolicyAdmin(admin.ModelAdmin):
  list_display = ('user', 'policy', 'device', 'status', 'start_date', 'end_date')
  list_filter = ('status', 'start_date', 'end_date', 'policy__name')
  search_fields = ('user__username', 'device__imei_number', 'policy__name')
  raw_id_fields = ('user', 'policy', 'device')
  date_hierarchy = 'start_date' 


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
  list_display = ('id', 'customer_policy_user', 'incident_date', 'status', 'estimated_repair_cost', 'claim_amount_approved')
  list_filter = ('status', 'submission_date', 'incident_date')
  search_fields = ('customer_policy__user__username', 'incident_description')
  raw_id_fields = ('customer_policy',)
  readonly_fields = ('submission_date',)
  date_hierarchy = 'submission_date'

    
  def customer_policy_user(self, obj):
    return obj.customer_policy.user.username
  customer_policy_user.short_description = 'Customer'
  
