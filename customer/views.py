from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from customer.models import Customer
from customer.serializers import CustomerSerializer
from user.serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from food_vendor_app.helpers import encrypt

# Create your views here.

class CustomerViewSet(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in (AllowAny,)]
        return super(CustomerViewSet, self).get_permissions()

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerSerializer)
    def post(self, request):
        request_data = request.data.copy()
        serializer = CustomerSerializer(data=request_data)
        if serializer.is_valid():
            request_data['is_customer'] = True
            user_serializer = UserSerializer(data=request_data)
            if user_serializer.is_valid():
                serializer.save()
                user_serializer.save()
                email = request_data['email']
                mail = encrypt(email)
                url = 'https://food-vendors-app.herokuapp.com/confirmsignup/?mail='+mail
                send_mail('Confirm Email', 'Click the link below to complete email verification \n'+url, 'samndu2@gmail.com', [email], 
                html_message="<h4>Click <a href='"+url+"'>here</a> to complete email verification</h4>", fail_silently=False)
                return Response(serializer.data, status=201)
            return Response(user_serializer.errors, status=400)

        return Response(serializer.errors, status=400)
