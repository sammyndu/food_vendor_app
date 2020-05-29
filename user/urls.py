from django.urls import path, re_path
from user import views

urlpatterns = [
    re_path(r'^confirmsignup/(?P<mail>)$', views.CreateUser.as_view()),
    # path('vendors/<int:pk>', views.vendor_detail),
]