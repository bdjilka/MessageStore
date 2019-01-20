<template>
  <div>

    <!-- главная компонента приложения -->

    <h4 class="headline font-weight-regular text-uppercase">Message store</h4>

    <!-- авторизация пользователя / выход из системы-->

    <v-btn small  @click="logInUser" v-if="!auth" class="in-out">Вход</v-btn>
    <v-btn small @click="logOutUser" v-if="auth" class="in-out">Выход</v-btn>

    <!---->

    <!-- компонента, отвечающая за вывод таблицы сообщений -->

    <Messages v-if="auth" @open_message="open_message"></Messages>

    <!---->

    <!-- компонента, отвечающая за карточки сообщения и его истории-->

    <MsgCard v-if="auth" @refresh_table="refresh_table"></MsgCard>

    <!---->

    <v-footer class="pa-3">
      <v-spacer></v-spacer>
      <div>
        <strong> Система хранения сообщений </strong>
        &copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
  </div>
</template>

<script>
  import Messages from '@/components/Messages'
  import MsgCard from '@/components/MsgCard'

  export default {
    name: "Main",
    components: {
      Messages,
      MsgCard
    },
    data() {
      return {
        // текущее открытое сообщение
        msg: '',
      }
    },
    computed: {

      // проверка авторизации пользователя в системе
      auth() {
        if (sessionStorage.getItem('auth_token'))
          return true;
      else
        return false;
      }
    },
    methods: {

      // авторизация пользователя, сохранение токена для отправки запросов
      logInUser() {

        // переход на страницу авторизации
        this.$router.push({name: "login"});
      },

      // выход пользователя из системы
      logOutUser() {
        sessionStorage.removeItem('auth_token');

        // переход на главную страницу
        window.location = '/';
      },

      // открытие сообщения
      open_message(message) {
        this.msg = message;

        // колбэк на открытие сообщения в компоненте MsgCard
        this.$emit('show_msg', this.msg.id);
      },

      // обновление таблицы сообщений
      refresh_table() {

        // колбэк на обновление в компоненте Messages
        this.$emit('refresh');
      }
    }
  }
</script>

<style scoped>
  h4 {
    padding-top: 10px;
    color: #ffffffb3;
  }
  .in-out {
    position: absolute;
    top: 5px;
    right: 10px;
  }
  .pa-3 {
    position: absolute;
    bottom: 0;
    width: 100%;
  }
</style>
