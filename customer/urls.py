from django.urls import path
from customer import views

urlpatterns = [
    path('customers/', views.CustomerViewSet.as_view()),
    # path('vendors/<int:pk>', views.vendor_detail),
]