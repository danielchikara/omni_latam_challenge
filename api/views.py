from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from api.serializers import *
from api.models import *
# Create your views here.


# User
class RegisterClientView(APIView):

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        success = False
        code = 400
        if user:
            success = True
            code = 201
        return Response({"success": success}, status=code)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer_user = UserClientSerializer(user)
            return Response({"token": token.key, "user": serializer_user.data}, status=200)


class UpdateInfoClientView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = (TokenAuthentication)

    def post(self, request):
        user = request.user
        serializer_info = ClientUpdateSerializer(data=request.data)
        if serializer_info.is_valid(raise_exception=True):
            serializer_info.update(
                instance=user, validated_data=serializer_info.validated_data)
        serializer_user = UserClientSerializer(user)
        return Response({'user': serializer_user.data}, status=200)


class GetInfoClientView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = (TokenAuthentication)

    def get(self, request):
        user = request.user
        serializer_user = UserClientSerializer(user)
        return Response({'user': serializer_user.data}, status=200)


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_class = (TokenAuthentication)
    serializer_class = UserClientSerializer

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.save()
        return Response({'msg': "Has desactivado tu cuenta"}, status=200)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)


# Crud Product
class CreateProductView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer


class UpdateProductView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class DetailProductView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)


class ListProductView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True).order_by('id')


class DeleteProductView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    authentication_class = (TokenAuthentication)
    queryset = Product.objects.filter(is_active=True)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "Se ha  borrado el producto"}, status=200)


# Crud  Order
class CreateOrder(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        return Response({'msg': "Orden creada"}, status=201)


class DetailOrderView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderReadSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class UpdateOrderView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderUpdateSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class DeleteOrderView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, is_active=True)
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "Se ha  borrado la  orden"}, status=200)


# Crud OrderProduct
class CreateOrderProductView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderProductSerializer

    def perform_create(self, serializer):
        print("serializer", serializer.validated_data)
        product = serializer.validated_data['product']
        order = serializer.validated_data['order']
        total_price_order_product = float(product.price) * \
            float(serializer.validated_data['amount'])
        order.total_order = float(order.total_order) + \
            total_price_order_product
        serializer.save(price_per_unit=product.price,
                        total_price=total_price_order_product)


class DetailOrderProductView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderProductReadSerializer

    def get_queryset(self):
        queryset = OrderProduct.objects.filter(
            is_active=True, order__user=self.request.user)
        return queryset


class UpdateOrderProductView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)
    serializer_class = OrderProductReadSerializer

    def get_queryset(self):
        queryset = OrderProduct.objects.filter(
            is_active=True, order__user=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"order_product": serializer.data}, status=200)


class DeleteOrderProductView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = (TokenAuthentication)

    def get_queryset(self):
        queryset = OrderProduct.objects.filter(
            user=self.request.user, is_active=True)
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'msg': "Se ha  borrado con exito"}, status=200)

