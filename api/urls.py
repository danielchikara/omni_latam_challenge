from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    #  User
    path('register/client/', RegisterClientView.as_view()),
    path('update/client/', UpdateInfoClientView.as_view()),
    path('info/client/', GetInfoClientView.as_view()),
    path('delete/client/', DeleteUserView.as_view()),
    #Login and logout
    path('login/client/', LoginView.as_view()),
    path('logout/client/', LogoutView.as_view()),
    # Product
    


]
