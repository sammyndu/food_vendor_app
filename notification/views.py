from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from food_vendor_app.decorators import CustomerPermission
from .serializers import NotificationSerializer
from .models import Notification
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class NotificationList(APIView):

    def get(self, request):
        notification = Notification.objects.all().filter(subjectUser=request.user.email)
        serializer = NotificationSerializer(notification, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=NotificationSerializer)
    def post(self, request):
        request_data = request.data.copy()
        request_data['message_status'] = 1
        serializer = NotificationSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class NotificationDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get_object(self, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            return notification
        except Notification.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        notification = self.get_object(pk)
        if notification.subjectUser != request.user.email:
            return Response({'message': 'you are not allowed'}, status=401)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NotificationSerializer)
    def put(self, request, pk):
        data = request.data
        notification = self.get_object(pk)
        if notification.subjectUser != request.user.email:
            return Response({'message': 'you are not allowed'}, status=401)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
    @permission_classes([CustomerPermission])
    def delete(self, request, pk):
        notification = self.get_object(pk)
        if notification.subjectUser != request.user.email:
            return Response({'message': 'you are not allowed'}, status=401)
        notification.delete()
        return Response(status=204)