from django.urls import path
from menu import views

urlpatterns = [
    path('menus/', views.MenuList.as_view()),
    path('menu/<int:pk>', views.MenuDetail.as_view()),
]