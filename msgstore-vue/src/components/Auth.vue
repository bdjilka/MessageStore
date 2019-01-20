<template>
  <div class="log-page">

    <!--форма авторизации пользователя-->

    <v-card class="log-form">
      <h4 class="headline font-weight-regular text-uppercase title">MessageStore</h4>

      <div class="creds">
        <div class="grey--text"> Логин:</div>
        <input v-model="login" type="text" placeholder=""/>
        <div class="grey--text"> Пароль:</div>
        <input v-model="password" type="password" placeholder=""/>
      </div>
      <v-btn large id="submit" @click="validate">Войти</v-btn>
    </v-card>
  </div>
</template>

<script>
  import $ from 'jquery'

  export default {
    name: "Auth",
    data() {
      return {
        login: '',
        password: ''
      }
    },
    methods: {

      // отправка запроса на валидацию введенных данных (выполняется через Djoser)
      validate() {
        $.ajax({
          url: "http://127.0.0.1:8000/auth/token/create/",
          type: 'POST',
          data: {
            username: this.login,
            password: this.password
          },
          success: (response) => {
            sessionStorage.setItem('auth_token', response['auth_token']);
            this.$router.push({name: "home"});
          },
          error: (response) => {
            if (response.status == 400)
              alert('Ваш данные неверны. Попробуйте еще раз.');
            else
              alert('Ошибка: ' + response.status);
          }
        })
      }
    }
  }
</script>

<style scoped>
  .log-page {
    width: 100%;
    height: 100%;
    position: relative;
  }

  input {
    line-height: 30px;
    width: calc(100% - 20px);
    border: 1px solid #6d6d6d;
    border-radius: 6px;
    padding-left: 8px;
  }

  .title {
    margin-top: 10px;
    color: #ffffffd3;
  }

  .creds {
    padding: 20px;
  }

  .creds div {
    text-align: left;
    padding: 10px;
  }

  #submit {
    position: inherit;
    bottom: 10px;
    left: calc(50% - 65px);

  }

  .log-form {
    width: 500px;
    height: 300px;
    position: absolute;
    top: calc(50% - 150px);
    left: calc(50% - 250px);
    border-radius: 10px;
  }
</style>
