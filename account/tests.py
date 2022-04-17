from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from model_mommy import mommy

from account.models import Token


class BaseSetUpTest(TestCase):
    def setup(self):
        self.user = mommy.make(
            get_user_model(), username='123', password='123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def url_setup(self, url, method):
        self.url = url
        self.method = method

    def status_code_test(self, code, message, data=None):
        if self.method == 'POST':
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, code, message)


class userViewTest(BaseSetUpTest):
    def setup(self):
        super().setup()
        self.empty_data = {
            'username': '',
            'password': ''
        }
        self.data = {
            'username': 'test_username',
            'password': 'test_password',
        }

    def test_auth(self):
        self.setup()
        response = self.client.post('/api/user/id_check/', {'username': '123'})
        self.assertEqual(response.status_code, 200, "존재하는 아이디")
        response = self.client.post('/api/user/id_check/', {'username': '312'})
        self.assertEqual(response.status_code, 402,  "존재하지 않는 아이디")
        response = self.client.post('/api/mobile_auth/')

    def test_token(self):
        self.url_setup('/api/token/make_wait_token/', 'POST')
        self.status_code_test(
            201, "토큰 생성", {'phone_number': '01020647744', 'wait_time': '5'})
        self.status_code_test(
            201, "같은번호 토큰 생성", {'phone_number': '01020647744', 'wait_time': '5'})
        self.status_code_test(
            201, "다른 번호 생성", {'phone_number': '01012345678', 'wait_time': '5'})
        self.assertEqual(len(Token.objects.all()), 2, "생성 확인")
        finish_time = timezone.now()
        test_token = Token.objects.get(phone_number='01012345678')
        test_token.finish_time = finish_time
        test_token.save()
        self.status_code_test(
            201, "번호 생성", {'phone_number': '01093939393', 'wait_time': '5'})
        self.assertEqual(len(Token.objects.all()), 2, "기한 지한 토큰 삭제 확인")