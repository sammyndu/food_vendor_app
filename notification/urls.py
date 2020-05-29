from django.urls import path
from notification import views

urlpatterns = [
    path('notifications/', views.NotificationList.as_view()),
    path('notification/<int:pk>', views.NotificationDetail.as_view()),
]