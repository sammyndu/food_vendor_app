from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from food_vendor_app.decorators import CustomerPermission
from .serializers import OrderSerializer
from .models import Order
from customer.models import Customer
from vendor.models import Vendor
from drf_yasg.utils import swagger_auto_schema

def get_customer(email):
    try:
        customer = Customer.objects.get(email=email)
        return customer
    except Customer.DoesNotExist:
        return Response(status=404)
        

def get_vendor(email):
    try:
        vendor = Vendor.objects.get(email=email)
        return vendor
    except Vendor.DoesNotExist:
        raise APIException(detail='Vendor Not found', code=status.HTTP_404_NOT_FOUND)

# Create your views here.
class OrderList(APIView):

    def get(self, request):
        if request.user.is_customer:
            customer = get_customer(request.user.email)
            orders = Order.objects.all().filter(customer_id = customer.id)
        elif request.user.is_vendor: 
            vendor = get_vendor(request.user.email)
            orders = Order.objects.all().filter(vendor_id = vendor.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer)
    @permission_classes([CustomerPermission])
    def post(self, request):
        request_data = request.data.copy()
        customer = get_customer(request.user.email)
        request_data['customer_id'] = customer.id
        request_data['order_id'] = 1
        serializer = OrderSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class OrderDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get_object(self, pk):
        try:
            order = Order.objects.get(pk=pk)
            return order
        except Order.DoesNotExist:
            return Response(status=404)

    def get(self, request,  pk):
        order = self.get_object(pk)
        if request.user.is_customer:
            customer = get_customer(request.user.email)
            if customer.id != order.customer_id:
                raise APIException(detail='Not Allowed', code=status.HTTP_403_FORBIDDEN)
        if request.user.is_vendor:
            vendor = get_vendor(request.user.email)
            if vendor.id != order.vendor_id:
                raise APIException(detail='Not Allowed', code=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer)
    def put(self, request, pk):
        data = request.data
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=data, context = {"request_user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
    @permission_classes([CustomerPermission])
    def delete(self, request, pk):
        order = self.get_object(pk)
        customer = get_customer(request.user.email)
        if customer.id != order.customer_id:
            raise APIException(detail='Not Allowed', code=status.HTTP_403_FORBIDDEN)
        order.delete()
        return Response(status=204)