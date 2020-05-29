from rest_framework import serializers
from user.models import AuthUser

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.HiddenField(default=False)
    class Meta:
        model = AuthUser
        fields = ['email', 'password', 'is_active', 'is_vendor', 'is_customer']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.is_active = True
        instance.save()
        return instance