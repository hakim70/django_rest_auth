from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data.get('name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Must include both email and password")

        data['user'] = user
        return data