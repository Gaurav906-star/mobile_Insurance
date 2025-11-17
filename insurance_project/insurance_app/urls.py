from . import views
from django.urls import path

urlpatterns = [
    
    path('',views.PolicyListView.as_view(),name='policy_list'),

    path('purchase/',views.PolicyPurchaseView.as_view(),name='policy_purchase'),

    path('device/register/',views.DeviceRegisterView.as_view(),name='device_register'),

    path('claim/submit/',views.ClaimSubmitView.as_view(),name='claim_submit'),

    path('my/policies/',views.MyPoliciesView.as_view(),name= 'my_policies'),

    path('my/claims/',views.MyClaimView.as_view(),name='my_claims'),



]
