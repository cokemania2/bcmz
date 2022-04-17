
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND,
)

from account.models import User, Token
from api.serializer import (UserSerializer, TokenSerializer,
                            TokenAuthSerializer, InfoCheckSerializer)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def info_check(self, request):
        serializer = InfoCheckSerializer(data=request.data)
        if serializer.is_valid():
            try:
                User.objects.get(**serializer.data)
                return Response(status=HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        pass


class TokenViewSet(viewsets.GenericViewSet):
    queryset = Token.objects.all()
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
                token=serializer.data['token'],
                phone_number=serializer.data['phone_number'],
                auth_num=serializer.data['auth_num'],
                accepted=False,
            )
            if token.exists():
                token[0].accepted = True
                token[0].save()
                return Response(status=HTTP_200_OK)
        return Response(status=HTTP_404_NOT_FOUND)


