from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from .models import AuthUser
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from food_vendor_app.helpers import decrypt

# Create your views here.

class CreateUser(APIView):

    def get_object(self, email):
        try:
            return AuthUser.objects.get(email=email)
        except AuthUser.DoesNotExist:
            raise Http404

    def get_permissions(self,):
        if self.request.method in ['PUT', 'GET']:
            return [permission() for permission in (AllowAny,)]
        return super(CreateUser, self).get_permissions()

    def get(self, request, mail):
        return Response(data=None, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, mail):
        email = decrypt(request.GET.get('mail'))
        user = self.get_object(email)
        request_data = request.data.copy()
        request_data['email'] = user.email
        serializer = UserSerializer(user, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)