from rest_framework import serializers

from .models import MyUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "email",
            "password",
            "dob",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        dob = validated_data["dob"]

        user = MyUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            dob=dob,
        )
        return user
