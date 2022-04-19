import datetime

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient

from account.models import User, Token


class BaseSetUpTest(TestCase):
    def setup(self):
        self.user = User.objects.create(
            username='123', password='123',
            nickname='testman', email='test@email.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def setup_url(self, url, method):
        self.url = url
        self.method = method

    def setup_token(self, number, accept):
        finish_time = timezone.now()
        if accept:
            finish_time = finish_time + datetime.timedelta(minutes=5)
        self.token = Token(phone_number=number,
                           finish_time=finish_time,
                           accepted=accept)

    def status_code_test(self, code, message, data=None):
        if self.method == 'POST':
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, code, message)


class userViewTest(BaseSetUpTest):
    def user_setup(self, email=None, nickname=None, password=None,
                   username=None, phone_number=None):
        self.data = {
            'email': email if email else 'test@test.com',
            'nickname': nickname if nickname else 'testman',
            'password': password if password else 'pw',
            'username': username if username else 'testuser',
            'phone_number': phone_number if phone_number else '01020647744'
        }

    def test_info_check(self):
        self.setup()
        self.setup_url('/api/user/info_check/', 'POST')
        self.status_code_test(200, "존재하는 username", {'username': '123'})
        self.status_code_test(200, "존재하는 nickname", {'nickname': 'testman'})
        self.status_code_test(200, "존재하는 조합", {'username': '123', 'nickname': 'testman'})
        self.status_code_test(404, "존재하는 않는 username", {'username': '312'})
        self.status_code_test(404, "존재하는 않는 param", {'password': '312'})
        self.status_code_test(404, "존재하는 않는 param", {'ff': '312'})
        # response = self.client.post('/api/mobile_auth/')

    def test_sign_up(self):
        self.setup_url('/api/user/sign_up/', 'POST')
        self.user_setup()
        self.status_code_test(404, "토큰 없는 회원가입", self.data)
        self.setup_token('010206477444', False)
        self.status_code_test(404, "토큰 미인증 회원가입", self.data)
        self.setup_token('010206477444', True)
        self.status_code_test(201, "정상적인 회원가입", self.data)
        self.status_code_test(404, "중복 회원가입", self.data)

        self.setup_token('01011112222', True)
        self.user_setup(phone_number='01011112222')
        self.status_code_test(404, "이메일 중복 회원가입", self.data)
        self.user_setup(email='dummy@test.com')
        self.status_code_test(404, "전화번호 중복 회원가입", self.data)

        self.user_setup(email='test2@teset.com', nickname='coke', username='coke', phone_number='01012345678')
        self.setup_token('01012345678', True)
        self.status_code_test(201, "비밀번호 중복 회원가입", self.data)

        self.setup_token('01033334444', True)
        self.user_setup(email='test3@teset.com', username='coke3', phone_number='01033334444')
        self.status_code_test(201, "닉네임 중복 회원가입", self.data)

    def test_token(self):
        self.setup_url('/api/token/make_wait_token/', 'POST')
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
