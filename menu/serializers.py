from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 
                  'quantity', 'vendor_id', 'is_recurring', 
                  'frequency_of_reoccurence', 'date_time_created']

    def validate(self, attrs):
        """
        Check that the start is before the stop.
        """
        if not attrs['is_recurring'] and attrs['frequency_of_reoccurence'] != []:
            raise serializers.ValidationError("recurring cannot be false if frequency of reoccurence has a value")
        return attrs
