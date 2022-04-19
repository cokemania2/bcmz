import datetime
import time

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from account.models import User, Token
from account.utils import send_meesage, make_hash


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    username = serializers.CharField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    nickname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    phone_number = serializers.CharField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['email', 'nickname', 'username', 'password', 'phone_number']


class InfoCheckSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def is_valid(self, raise_exception=False):
        for key in self.initial_data:
            if key in ['username', 'email', 'phone_number']:
                return super().is_valid(raise_exception)
        raise ValidationError()


class PasswordCheckSerializer(InfoCheckSerializer):
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    token = serializers.CharField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    finish_time = serializers.DateTimeField(read_only=True)
    wait_time = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        wait_time = validated_data.pop('wait_time')
        timestamp = str(int(time.time() * 1000))
        now = timezone.now()
        finish_time = now + datetime.timedelta(minutes=wait_time)
        token, _ = Token.objects.get_or_create(
            phone_number=validated_data['phone_number'],
            accepted=False)
        token.token = make_hash(timestamp + validated_data['phone_number'])
        token.created_time = now
        token.finish_time = finish_time
        token.auth_num = send_meesage()
        token.save()
        return token

    class Meta:
        model = Token
        fields = ['phone_number', 'token',
                  'created_time', 'finish_time', 'wait_time']


class TokenAuthSerializer(serializers.Serializer):
    token = serializers.CharField()
    phone_number = serializers.CharField()
    auth_num = serializers.IntegerField()
