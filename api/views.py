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
