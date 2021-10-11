from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    #  User
    path('register/client/', RegisterClientView.as_view()),
    path('update/client/', UpdateInfoClientView.as_view()),
    path('detail/client/', GetInfoClientView.as_view()),
    path('delete/client/', DeleteUserView.as_view()),
    #Login and logout
    path('login/client/', LoginView.as_view()),
    path('logout/client/', LogoutView.as_view()),
    # Product
    path('create/product/', CreateProductView.as_view()),
    path('update/product/<int:pk>/', UpdateProductView.as_view()),
    path('detail/product/<int:pk>/', DetailProductView.as_view()),
    path('list/product/', ListProductView.as_view()),
    path('delete/product/<int:pk>/', DeleteProductView.as_view()),
    #Order
    path('create/order/',CreateOrder.as_view()),
    path('detail/order/<int:pk>/', DetailOrderView.as_view()),
    path('update/order/<int:pk>/', UpdateOrderView.as_view()),
    path('delete/order/<int:pk>/', DeleteOrderView.as_view()),
    #OrderProduct
    path('create/order-product/',CreateOrderProductView.as_view()),
    path('detail/order-product/<int:pk>/', DetailOrderProductView.as_view()),
    path('update/order-product/<int:pk>/', UpdateOrderProductView.as_view()),
    path('delete/order-product/<int:pk>/', DeleteOrderProductView.as_view()),
    #Payment
    path('create/payment/',CreatePaymentView.as_view())


]
