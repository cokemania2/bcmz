
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED
)
from django.contrib import auth

from account.models import User, Token
from api.serializer import (UserSerializer, TokenSerializer,
                            InfoCheckSerializer, PasswordCheckSerializer,
                            TokenAuthSerializer)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def token_check(self, phone_number):
        token = Token.objects.filter(
                    phone_number=phone_number,
                    accepted=True)
        if token.exists():
            token.delete()
            return True
        return False

    @action(detail=False, methods=['post'])
    def info_check(self, request):
        serializer = InfoCheckSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                User.objects.get(**serializer.data)
                return Response(status=HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if self.token_check(serializer.validated_data['phone_number']):
                User.objects.create_user(**serializer.validated_data)
                return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def sign_in(self, request):
        serializer = PasswordCheckSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for key in serializer.validated_data:
                if key in ['username', 'phone_number', 'email']:
                    try:
                        login_data = {key: serializer.validated_data[key]}
                        user = User.objects.get(**login_data)
                        auth_user = auth.authenticate(
                            request, username=user.username, 
                            password=serializer.validated_data['password'])
                        if auth_user is not None:
                            return Response(status=HTTP_200_OK)
                        else:
                            return Response(status=HTTP_401_UNAUTHORIZED)
                    except User.DoesNotExist:
                        return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def reset_pw(self, request):
        phone_number = request.POST.get('phone_number')
        new_pw = request.POST.get('new_password')
        if phone_number and new_pw:
            if self.token_check(phone_number):
                try:
                    user = User.objects.get(phone_number=phone_number)
                    user.set_password(new_pw)
                    return Response(status=HTTP_200_OK)
                except User.DoesNotExist:
                    return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_401_UNAUTHORIZED)


class TokenViewSet(viewsets.GenericViewSet):
    queryset = Token.objects.filter()
    serializer_class = TokenSerializer

    @action(detail=False, methods=['post'])
    def make_wait_token(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.data, status=400)

    @action(detail=False, methods=['post'])
    def auth_wait_token(self, request):
        serializer = TokenAuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = Token.objects.filter(
                token=serializer.validated_data['token'],
                phone_number=serializer.validated_data['phone_number'],
                auth_num=serializer.validated_data['auth_num'],
                accepted=False,
            )
            if token:
                token[0].accepted = True
                token[0].save()
                return Response(status=HTTP_200_OK)
        return Response(status=HTTP_404_NOT_FOUND)
