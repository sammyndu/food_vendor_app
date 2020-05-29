from rest_framework import serializers
from .models import Notification
from order.models import Order
from user.models import AuthUser

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'subjectUser', 'order_id', 'message', 'message_status', 'date_time_created']

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        try:
            order = Order.objects.get(pk=data['order_id'])
        except Order.DoesNotExist:
            raise serializers.ValidationError("order does not exist")
        vendor_id = order.vendor_id
        customer_id = order.customer_id
        user = self.context.get("request_user")

        if user.id != vendor_id and user.id != customer_id:
            raise serializers.ValidationError("You do not have permission to send notifications for this order")

        try:
            subjectUser = AuthUser.objects.get(pk=data['subjectUser'])
        except AuthUser.DoesNotExist:
            raise serializers.ValidationError("subject user does not exist")

        if user.is_customer and not subjectUser.is_vendor:
            raise serializers.ValidationError("cannot send notification to user of same usertype")
        if user.is_vendor and not subjectUser.is_customer:
            raise serializers.ValidationError("cannot send notification to user of same usertype")

        return data