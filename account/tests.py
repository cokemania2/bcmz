import datetime

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from rest_framework.test import APIClient

from account.models import User, Token


class BaseSetUpTest(TestCase):
    def setup(self):
        settings.PRODUCTION = False
        self.user = User.objects.create(
            username='testuser', password='pw', phone_number='01020647744',
            nickname='testman', email='test@test.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def setup_url(self, url, method):
        self.url = url
        self.method = method

    def setup_token(self, number, accept):
        finish_time = timezone.now()
        if accept:
            finish_time = finish_time + datetime.timedelta(minutes=5)
        Token(phone_number=number, accepted=accept,
              finish_time=finish_time).save()

    def status_code_test(self, code, message, data=None):
        if self.method == 'POST':
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, code, message)
            return response.data 


class userViewTest(BaseSetUpTest):
    def user_setup(self, email=None, nickname=None, password=None,
                   username=None, phone_number=None):
        self.data = {
            'email': email if email else 'test2@test.com',
            'nickname': nickname if nickname else 'testman2',
            'password': password if password else 'pw',
            'username': username if username else 'testuser2',
            'phone_number': phone_number if phone_number else '01099999999'
        }

    # 중복 체크 API
    def test_info_check(self):
        self.setup()
        self.setup_url('/api/user/info_check/', 'POST')
        self.status_code_test(200, "존재하는 username", {'username': 'testuser'})
        self.status_code_test(200, "존재하는 조합", {'username': 'testuser', 'nickname': 'testman'})
        self.status_code_test(404, "존재하는 않는 username", {'username': '312'})
        self.status_code_test(400, "식별할수 없는 param", {'password': 'pw'})
        self.status_code_test(400, "식별할수 없는 param", {'nickname': 'testman'})
        self.status_code_test(400, "식별할수 없는 param", {'ff': '312'})

    # 회원가입 체크 API
    def test_sign_up(self):
        self.setup_url('/api/user/sign_up/', 'POST')
        self.user_setup()
        self.status_code_test(404, "토큰 없는 회원가입", self.data)
        self.setup_token('01099999999', False)
        self.status_code_test(404, "토큰 미인증 회원가입", self.data)
        self.setup_token('01099999999', True)
        self.status_code_test(201, "정상적인 회원가입", self.data)
        self.status_code_test(400, "중복 회원가입", self.data)
        self.setup_token('01011112222', True)
        self.user_setup(phone_number='01011112222')
        self.status_code_test(400, "이메일 중복 회원가입", self.data)
        self.user_setup(email='dummy@test.com')
        self.status_code_test(400, "전화번호 중복 회원가입", self.data)

        self.user_setup(email='test2@teset.com', nickname='coke',
                        username='coke', phone_number='01012345678')
        self.setup_token('01012345678', True)
        self.status_code_test(201, "비밀번호 중복 회원가입", self.data)

        self.setup_token('01033334444', True)
        self.user_setup(email='test3@teset.com', username='coke3',
                        phone_number='01033334444')
        self.status_code_test(201, "닉네임 중복 회원가입", self.data)

    def test_sign_in(self):
        self.setup_url('/api/user/sign_in/', 'POST')
        self.user_setup()
        User.objects.create(**self.data)
        self.status_code_test(200, "모든 데이터 로그인", self.data)
        self.status_code_test(200, "이메일 + 비밀번호 로그인", {
            'email': 'test2@test.com', 'password': 'pw'
        })
        self.status_code_test(200, "유저네임 + 비밀번호 로그인", {
            'username': 'testman2', 'password': 'pw'
        })
        self.status_code_test(200, "전화번호 + 비밀번호 로그인", {
            'phone_number': '01099999999', 'password': 'pw'
        })
        self.status_code_test(400, "닉네임 + 비밀번호 로그인", {
            'nickname': 'testman2', 'password': 'pw'
        })
        self.status_code_test(400, "전화번호 + 이메일 로그인", {
            'phone_number': '01099999999', 'email': 'test2@test.com'
        })
        self.status_code_test(400, "이메일 + 유저네임 로그인", {
            'email': 'test2@test.com', 'username': 'testman2'
        })


class tokenViewTest(BaseSetUpTest):
    def test_token(self):
        self.setup()
        self.setup_url('/api/token/make_wait_token/', 'POST')
        self.status_code_test(
            201, "토큰 생성", {'phone_number': '01020647744', 'wait_time': '5'})
        self.status_code_test(
            201, "같은번호 토큰 생성", {'phone_number': '01020647744', 'wait_time': '5'})
        self.status_code_test(
            201, "다른 번호 생성", {'phone_number': '01012345678', 'wait_time': '5'})
        self.assertEqual(len(Token.objects.all()), 2, "생성 확인")

        # 기한 지난 토큰 삭제
        finish_time = timezone.now()
        test_token = Token.objects.get(phone_number='01012345678')
        test_token.finish_time = finish_time
        test_token.save()
        test_data = self.status_code_test(
            201, "번호 생성", {'phone_number': '01000000000', 'wait_time': '5'})
        self.assertEqual(len(Token.objects.all()), 2, "기한 지한 토큰 삭제 확인")
        
        self.setup_url('/api/token/auth_wait_token/', 'POST')
        auth_num = Token.objects.get(phone_number='01000000000').auth_num
        self.status_code_test(200, "정상 토큰 인증", {
            'token': test_data['token'], 'phone_number': test_data['phone_number'],
            'auth_num': auth_num
        })
        test_token = Token.objects.get(phone_number=test_data['phone_number'])
        self.assertEqual(test_token.accepted, True, "인증 완료 확인")
        test_data = self.client.post('/api/token/make_wait_token/', {'phone_number': '01077777777', 'wait_time': '5'}).data
        self.status_code_test(404, "잘못된 인증번호 인증", {
            'token': test_data['token'], 'phone_number': test_data['phone_number'],
            'auth_num': '09'
        })
        test_token = Token.objects.get(phone_number=test_data['phone_number'])
        self.assertEqual(test_token.accepted, False, "인증 실패 확인")