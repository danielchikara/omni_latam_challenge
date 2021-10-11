from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


# Create your models here.


class SocialUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True,
                          is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField('email address',  unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = SocialUserManager()

    def __str__(self):
        return self.email


class Order(models.Model):
    user = models.ForeignKey(User, related_name=(
        "user_order"), on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    PENDING = 'pe'
    PAYMENT = 'pa'
    PRODUCTION = 'pr'
    ROUTE = 'ro'
    DELIVERED = 'de'
    STATUS_CHOICE = (
        (PENDING, 'Pendiente de pago'),
        (PAYMENT, 'Pago'),
        (ROUTE, 'En camino'),
        (DELIVERED, 'Entregado'),
    )
    order_status = models.CharField(choices=STATUS_CHOICE,
                                    max_length=2, null=True, blank=True)
    total_order = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    paid_value_order = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)


class Product (models.Model):
    product_name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)


class OrderProduct (models.Model):
    product = models.ForeignKey(
        Product, related_name="orders_product", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, related_name="order_products", on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2)
    ROUTE = 'ro'
    DELIVERED = 'de'
    STATUS_CHOICE = (
        (ROUTE, 'En camino'),
        (DELIVERED, 'Entregado'),
    )
    order_product_status = models.CharField(choices=STATUS_CHOICE,
                                            max_length=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)


class Payment(models.Model):
    user = models.ForeignKey(
        User, related_name="user_payments", on_delete=models.CASCADE)
    order = models.ManyToManyField(Order, related_name="payment_orders")
    paid_value = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
