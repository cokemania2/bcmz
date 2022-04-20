<template>
     <form class="signup_container"> 
            <div class="input">
                <span>이메일</span>
                <input type="email" name="email" v-model="email">
                <button @click="emailCheck">중복 체크</button>
            </div>
            <div class="input">
                <span>이름</span>
                <input type="text" name="username" v-model="username">
                <button @click="usernameCheck">중복 체크</button>
            </div>
            <div class="input">
                <span>전화번호</span>
                <input type="text" name="number" v-model="number">
                <button @click="numberCheck">중복 체크</button>
                <button @click="getAuthenticationNumber">인증 번호 받기</button>
            </div>
            <div class="input">
                <span>인증 번호 입력</span>
                <input type="text" name="auth_num" v-model="auth_num" :disabled="validated == 1">
                <button @click="setAuthenticationNumber">인증 하기</button>
            </div>
            <div class="input">
                <span>닉네임</span>
                <input type="text" name="nickname" v-model="nickname">
            </div>
            <div class="input">
                <span>비밀번호</span>
                <input type="password" name="password" v-model="password">
            </div>
            <div class="input">
                <span>비밀번호 확인</span>
                <input type="password" name="password_check" v-model="password_check">
            </div>
            <button @click="signUp" type="submit">signUp</button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    name : 'SignUpVue', 
    component : {

    },
    data() {
        return {
            username : '',
            email : '',
            number : '',
            nickname : '',
            password : '',
            password_check : '',
            token: '',
            auth_num : '',
            validated: 0,
        }
    },
    methods: {
        signUp(e) {
            e.preventDefault()
            axios.post('http://localhost:8000/api/user/sign_up/', {
                 email: this.email,
                 username: this.username,
                 nickname: this.nickname,
                 phone_number: this.number,
                 password: this.password 
            }).then((res)=>{
                if (res.status === 201) {
                    alert('가입 완료되었습니다.')
                } 
            }).catch(error => {
                if (error.response) {
                    if (error.response.status >= 400) {
                        alert('정확한 정보를 입력해주세요')
                    }
                }
            })
            const router = this.$router;
            router.push('/')
        },
        emailCheck(e) {
            e.preventDefault()
            axios.post('http://127.0.0.1:8000/api/user/info_check/', {
                'email': this.email,
            }).then((res) => {
                if (res.status === 200) {
                    alert('중복되는 이메일 입니다.')
                }
            }).catch(error => {
                if (error.response) {
                    if (error.response.status === 400) {
                        alert('정확한 정보를 입력해주세요')
                    } else if (error.response.status === 404) {
                        alert('사용 가능한 이메일 입니다.')
                    }
                }
            })
        },
        numberCheck(e) {
            e.preventDefault()
            axios.post('http://127.0.0.1:8000/api/user/info_check/', {
                'phone_number': this.number,
            }).then((res) => {
                if (res.status === 200) {
                    alert('중복되는 번호 입니다.')
                }
            }).catch(error => {
                if (error.response) {
                    if (error.response.status === 400) {
                        alert('정확한 정보를 입력해주세요')
                    } else if (error.response.status === 404) {
                        alert('사용 가능한 번호 입니다.')
                    }
                }
            })
        },
        usernameCheck(e) {
            e.preventDefault()
            axios.post('http://127.0.0.1:8000/api/user/info_check/', {
                'username': this.username,
            }).then((res) => {
                if (res.status === 200) {
                    alert('중복되는 이름 입니다.')
                }
            }).catch(error => {
                if (error.response) {
                    if (error.response.status === 400) {
                        alert('정확한 정보를 입력해주세요')
                    } else if (error.response.status === 404) {
                        alert('사용 가능한 이름 입니다.')
                    }
                }
            })
        },
        getAuthenticationNumber(e) {
            e.preventDefault()
            axios.post('http://127.0.0.1:8000/api/token/make_wait_token/', {
                'phone_number': this.number, 'wait_time': 5
            }).then((res) => {
                if (res.status === 201) {
                    alert('5분 안에 인증 번호를 입력해주세요')
                    this.token = res.data['token']
                }
            }).catch(error => {
                if (error.response) {
                    if (error.response.status === 400) {
                        alert('정확한 정보를 입력해주세요')
                    }
                }
            })
        },
        setAuthenticationNumber(e) {
            e.preventDefault()
            axios.post('http://127.0.0.1:8000/api/token/auth_wait_token/', {
                'auth_num': this.auth_num, 
                'phone_number': this.number, 
                'token': this.token
            }).then((res) => {
                if (res.status === 200) {
                    alert('인증에 성공하였습니다.')
                    this.validated = 0
                }
            }).catch(error => {
                if (error.response) {
                    if (error.response.status === 404) {
                        alert('인증에 실패하였습니다')
                    } else {
                        alert('정확한 정보를 입력해주세요')
                    }
                }
            })
        }
    }
}
</script>

<style>
    .signup_container {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content : center;
        align-self: center;
        align-items: center;
        background-color: white;
    }
</style>