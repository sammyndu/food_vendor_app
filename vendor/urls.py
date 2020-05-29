from django.urls import path
from vendor import views

urlpatterns = [
    path('vendors/', views.VendorViewSet.as_view()),
    # path('vendors/<int:pk>', views.vendor_detail),
]