from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from account.models import User, Token


class BaseSetUpTest(TestCase):
    def setup(self):
        self.user = User.objects.create(
            username='123', password='123',
            nickname='testman', email='test@email.com')
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
        self.url_setup('/api/user/info_check/', 'POST')
        self.status_code_test(200, "존재하는 username", {'username': '123'})
        self.status_code_test(200, "존재하는 nickname", {'nickname': 'testman'})
        self.status_code_test(200, "존재하는 조합", {'username': '123', 'nickname': 'testman'})
        self.status_code_test(404, "존재하는 않는 username", {'username': '312'})
        self.status_code_test(404, "존재하는 않는 param", {'password': '312'})
        self.status_code_test(404, "존재하는 않는 param", {'ff': '312'})
        # response = self.client.post('/api/mobile_auth/')

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
