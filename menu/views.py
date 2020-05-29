from rest_framework.views import APIView
from rest_framework.exceptions import APIException, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from food_vendor_app.decorators import VendorPermission
from .serializers import MenuSerializer
from .models import Menu
from vendor.models import Vendor
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

def get_vendor(email):
    try:
        vendor = Vendor.objects.get(email=email)
        return vendor
    except Vendor.DoesNotExist:
        raise APIException(detail='Vendor Not found', code=status.HTTP_404_NOT_FOUND)

class MenuList(APIView):

    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MenuSerializer)
    @permission_classes([VendorPermission])
    def post(self, request):
        request_data = request.data.copy()
        vendor = get_vendor(request.user.email)
        request_data['vendor_id'] = vendor.id
        serializer = MenuSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MenuDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """

    def get_object(self, pk):
        try:
            menu = Menu.objects.get(pk=pk)
            return menu
        except Menu.DoesNotExist:
            raise APIException(detail='Menu Not found', code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MenuSerializer)
    @permission_classes([VendorPermission])
    def put(self, request, pk):
        data = request.data
        menu = self.get_object(pk)
        vendor = get_vendor(request.user.email)
        if vendor.id != menu.vendor_id:
            raise APIException(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)
        serializer = MenuSerializer(menu, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @permission_classes([VendorPermission])
    def delete(self, request, pk):
        menu = self.get_object(pk)
        vendor = get_vendor(request.user.email)
        if vendor.id != menu.vendor_id:
            raise APIException(detail='Not Allowed', code=status.HTTP_403_FORBIDDEN)
        menu.delete()
        return Response(status=204)