<template>
     <form class="signup_container"> 
            <div class="input" >
                <span>아이디</span>
                <input type="text" name="username" v-model="username">
            </div>
            <div class="input">
                <span>비밀번호</span>
                <input type="password" name="password" v-model="password">
            </div>
            <button @click="signUp" type="submit">signUp</button>
    </form>
</template>

<script>
export default {

}
</script>

<style>

</style>