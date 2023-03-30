from django.urls import path
from .views import Record, Login, Logout , ChangePasswordAPI

urlpatterns = [
    path('addUser/', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
     path('password/change/', ChangePasswordAPI.as_view()),
]