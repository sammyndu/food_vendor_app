from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from user.serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from food_vendor_app.helpers import encrypt

# Create your views here.

# class VendorViewSet(generics.ListCreateAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

class VendorViewSet(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in (AllowAny,)]
        return super(CustomerViewSet, self).get_permissions()

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=VendorSerializer)
    def post(self, request):
        request_data = request.data.copy()
        serializer = VendorSerializer(data=request_data)
        if serializer.is_valid():
            request_data['is_vendor'] = True
            user_serializer = UserSerializer(data=request_data)
            if user_serializer.is_valid():
                serializer.save()
                user_serializer.save()
                email = request_data['email']
                mail = encrypt(email)
                url = 'http://localhost:8000/confirmsignup/?mail='+mail
                send_mail('Confirm Email', 'Click the link below to complete email verification \n'+url, 'samndu2@gmail.com', [email], 
                html_message="<h4>Click <a href='"+url+"'>here</a> to complete email verification</h4>", fail_silently=False)
                return Response(serializer.data, status=201)
            return Response(user_serializer.errors, status=400)

        return Response(serializer.errors, status=400)

# @csrf_exempt
# @permission_classes(IsAuthenticated,)
# def vendor_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         vendors = Vendor.objects.all()
#         serializer = VendorSerializer(vendors, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = VendorSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def vendor_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         vendor = Vendor.objects.get(pk=pk)
#     except Vendor.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = VendorSerializer(vendor)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = VendorSerializer(vendor, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         vendor.delete()
#         return HttpResponse(status=204)
