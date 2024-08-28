from rest_framework import serializers
from .models import MyUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'phone_number',
            'email',
            'password'
        )

    def create(self, validated_data):
        user = MyUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'phone_number',
        )

