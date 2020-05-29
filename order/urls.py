from django.urls import path
from order import views

urlpatterns = [
    path('orders/', views.OrderList.as_view()),
    path('order/<int:pk>', views.OrderDetail.as_view()),
]