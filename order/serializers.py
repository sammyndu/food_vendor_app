from rest_framework import serializers
from django.http import Http404
from .models import Order
from menu.models import Menu

class OrderSerializer(serializers.ModelSerializer):
    # amount_paid = serializers.HiddenField(default=0)
    # amount_due = serializers.HiddenField(default=0)
    # amount_outsanding =serializers.HiddenField(default=0)
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'vendor_id', 'description',
                  'items_ordered', 'amount_due', 'amount_paid',
                  'amount_outsanding', 'order_status', 'date_and_time_of_order']

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        user = self.context.get("request_user")
        if not user:
            pass
        elif user.is_vendor:
            for field in self.fields:
                if field != 'order_status':
                    self.fields[field].read_only = True
        elif user.is_customer:
            allowed_fields = ['vendor_id', 'description', 'items_ordered']
            for field in self.fields:
                if field not in allowed_fields:
                    self.fields[field].read_only = True
        
    def create(self, validated_data):

        # First, remove following from the validated_data dict...
        validated_data.pop('amount_due', None)
        amount_due = get_amount_due(validated_data['items_ordered'])

        # Create the object instance...
        order = Order.objects.create(**validated_data)

        if amount_due:
            order.amount_due = amount_due
            order.amount_paid = 0
            order.amount_outsanding = amount_due
        return order

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        user = self.context.get("request_user")
        if user.is_vendor:
            instance.order_status = validated_data.get('order_status', instance.order_status)
            instance.save()
        if user.is_customer:
            instance.amount_paid = validated_data.get('amount_paid', instance.amount_paid)
            instance.amount_outsanding = instance.amount_due - instance.amount_paid
            if validated_data.get('order_status') and validated_data.get('order_status') not in ['Pending', 'Completed']:
                instance.order_status = validated_data.get('order_staus', instance.order_status)
            instance.save()
        return instance

def get_amount_due(menu_ids):
    price = 0
    for i in menu_ids:
        try:
            menu_item = Menu.objects.get(pk=i)
        except Menu.DoesNotExist:
            raise Http404

        price += menu_item.price
    return price
