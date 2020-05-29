from rest_framework import serializers
from customer.models import Customer
from food_vendor_app.helpers import verify_phone_number

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'date_time_created']

    def validate(self, attrs):
        """
        Check that the phone number is valid.
        """

        if not verify_phone_number(attrs['phone_number']):
            raise serializers.ValidationError({"phone_number":"Invalid Phone Number"})
        return attrs
