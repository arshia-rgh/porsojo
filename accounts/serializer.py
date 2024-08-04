from rest_framework import serializers

from accounts.models import User
from accounts.models.otp_token import OtpToken
from accounts.validators import iranian_phone_number_validator


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "email",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class IranianPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, validators=[iranian_phone_number_validator])

    @staticmethod
    def validate_phone_number(value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number does not exist.")
        return value


class VerifyOtpTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, validators=[iranian_phone_number_validator])
    otp_token = serializers.CharField(max_length=4)

    @staticmethod
    def validate_otp_token(value):
        if not OtpToken.objects.filter(code=value).exists():
            raise serializers.ValidationError("Invalid OTP token.")
        return value

    @staticmethod
    def validate_phone_number(value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number does not exist.")
        return value

    def validate(self, data):
        if not OtpToken.objects.filter(code=data["otp_token"], phone_number=data["phone_number"]).exists():
            raise serializers.ValidationError(detail={"otp_token": "Invalid OTP token."})
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "email",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    class Meta:
        model = User

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(detail={"password": "The two password fields didn't match."})
        return data

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("The old password is not correct.")
        return value
