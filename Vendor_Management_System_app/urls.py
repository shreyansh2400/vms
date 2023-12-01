from django.urls import path
from .views import *

urlpatterns = [
    path('api/vendors/', vendor_list, name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', vendor_list, name='vendor-detail'),
    path('api/purchase_order_tracking/', purchase_order_tracking),
    path('api/purchase_order_tracking/<int:vendor_id>/', purchase_order_tracking),
    path('api/update_vendor_performance_metrics/<int:id>/', update_vendor_performance_metrics),
    path('api/show_vendor_performance/<int:id>/', show_vendor_performance),
]
