import datetime
import time

from django.utils import timezone
from rest_framework import serializers
from account.models import User, Token
from account.utils import send_meesage, make_hash


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class InfoCheckSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)


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
