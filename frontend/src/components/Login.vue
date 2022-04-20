<template>
     <form class="login_container"> 
            <div class="input" >
                <span>이름</span>
                <input type="text" name="username" v-model="username">
                <span>번호</span>
                <input type="text" name="number" v-model="number">
                <span>이메일</span>
                <input type="email" name="email" v-model="email">
            </div>
            <div class="input">
                <span>비밀번호</span>
                <input type="password" name="password" v-model="password">
            </div>
            <button @click="login" type="submit">login</button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    name : 'loginVue', 
    component : {

    },
    data() {
        return {
            username : '',
            number : '',
            email : '',
            password : '',
        }
    },
    methods: {
        login(e) {
            e.preventDefault()
            const router = this.$router;
            const parm = {
                    password : this.password
                }
            if (this.username != '') {
                parm['username'] = this.username
            } else if (this.email != '') {
                parm['email'] = this.email
            } else if (this.number != '') {
                parm['phone_number'] = this.number
            }
            axios.post(`http://localhost:8000/api/user/sign_in/`, parm).then((res)=>{
                if (res.status === 200) {
                    document.cookie = 'token ='+res.data.token
                    this.$store.state.isLogin = true
                    router.push('/main')
                }
            }).catch(()=>{
                alert('잘못된 정보입니다.')
                router.push('/login')
            })
        }
    }
}
</script>

<style>
    .login_container {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content : center;
        align-self: center;
        align-items: center;
        background-color: white;
    }
</style>