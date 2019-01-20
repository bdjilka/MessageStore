<template>
  <div class="card">

    <!-- карточка сообщения -->

    <div class="grey--text note">Просмотр сообщения</div>
    <v-card class="msg-card">
      <div class="grey--text"> Автор:</div>
      <div> {{message.author.username}} </div>
      <div class="grey--text"> Текст сообщения:</div>
      <input v-model="message.text" placeholder="Текст сообщения" class="msg-input"/>
      <div class="grey--text"> Дата создания:</div>
      <div> {{message.publish_date}} </div>
      <div class="grey--text"> Дата последнего изменения:</div>
      <div> {{message.last_modify}} </div>
      <hr>

      <!-- изменение и удаление сообщения -->

      <v-btn small @click="modify_message">Изменить</v-btn>
      <v-btn small @click="delete_message">Удалить</v-btn>

      <!---->

    </v-card>

    <!---->


    <div class="grey--text note">История изменений сообщения</div>

    <!-- таблица истории изменений сообщений -->

    <v-data-table
      :headers="headers"
      :items="data"
      hide-actions
      id="msg-table"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-center">{{ props.item.text }}</td>
        <td class="text-xs-center">{{ props.item.date }}</td>
        <td class="text-xs-center">{{ props.item.user }}</td>
      </template>
    </v-data-table>

    <!---->

  </div>
</template>

<script>
  import $ from 'jquery'

  export default {
    name: "MsgCard",
    data() {
      return {

        // модель сообщения
        message: {
          author: {
            username: '',
          },
          text: '',
          publish_date: '',
          last_modify: ''
        },

        // модель истории изменений
        history: {
          text: '',
          date: ''
        },

        // идентификатор текущего открытого сообщения
        id: '',
        // заголовки таблицы истории изменений
        headers: [
          {text: 'Сообщение', align: 'center', value: 'text'},
          {text: 'Дата изменения', align: 'center', value: 'date'},
          {text: 'Пользователь', align: 'center', value: 'user'}
        ],

        // данные истории изменения сообзений
        data: []
      }
    },

    // установка ключа авторизации при создании компонента
    created() {
      $.ajaxSetup({
        "headers": {'Authorization': 'Token ' + sessionStorage.getItem('auth_token')},
      });

      //
      this.$parent.$on('show_msg', this.show_message);
    },
    methods: {

      // открыть сообщение
      show_message(id) {
        if (id != undefined) {
          this.id = id;
          $.ajax({
            url: "http://127.0.0.1:8000/api/message/" + this.id + "/",
            type: 'GET',
            success: (response) => {
              this.message = response;
              this.message.publish_date = this.message.publish_date.split('.')[0].replace('T', ' ');
              this.message.last_modify = this.message.last_modify.split('.')[0].replace('T', ' ');
              this.show_history();
            },
            error: (response) => {
              console.log(response.status);
            }
          });
        }
      },

      // изменить сообщение
      modify_message() {
        $.ajax({
          url: "http://127.0.0.1:8000/api/message/" + this.id + "/",
          type: 'PUT',
          data: {
            text: this.message.text
          },
          success: (response) => {
            alert('Текст сообщения изменен');
            console.log('Message ' + this.id + 'change to: ' + this.message.text);
            this.show_history();

            // колбэк на обновление таблицы
            this.$emit('refresh_table');
          },
          error: (response) => {
            console.log(response.status);
          }
        });
      },

      // удалить сообщение
      delete_message() {
        $.ajax({
          url: "http://127.0.0.1:8000/api/message/" + this.id + "/",
          type: 'DELETE',
          data: {
            text: this.message.text
          },
          success: (response) => {
            alert('Сообщение удалено.');
            console.log('Message ' + this.id + 'deleted');

            // колбэк на обновление таблицы
            this.$emit('refresh_table');
            this.show_history();
          },
          error: (response) => {
            console.log(response.status);
            if (response.status == 403)
              alert('Отстутсвуют права для удаления сообщения. Необходимо быть автором сообщения или суперюзером.')
          }
        });
      },

      // открыть историю
      show_history() {
        $.ajax({
          url: "http://127.0.0.1:8000/api/message/" + this.id + "/history/",
          type: 'GET',
          success: (response) => {
            this.history = response;

            this.data = [];
            for (let i = 0; i < this.history.length; i++) {
              var msg = this.history[i];
              this.data.push({
                'text': msg.text,
                'date': msg.date.split('.')[0].replace('T', ' '),
                'user': msg.user.username
              });
            }
          },
          error: (response) => {
            console.log(response.status);
          }
        });
      }
    }
  }
</script>

<style scoped>
  .card {
    position: absolute;
    top: 42px;
    right: 10px;
    width: 34%;
    height: calc(100% - 100px);
  }

  td {
    width: 30px !important;
  }

  hr {
      border-color: #6d6d6d;
  }

  .msg-card {
    border: 1px solid #6d6d6d;
    border-radius: 6px;
  }

  .note {
    font-size: 20px !important;
    padding: 10px;
  }

  .msg-card div {
    height: 23px;
    text-align: left;
    padding: 0px 10px;
  }

  .msg-input {
    /*position: absolute;*/
    /*left: 30px;*/
    /*top: 7px;*/
    line-height: 30px;
    width: calc(100% - 20px);
    border: 1px solid #6d6d6d;
    border-radius: 6px;
    padding-left: 8px;
  }

  #msg-table {
    margin-top: 5px;
    border: 1px solid #6d6d6d;
    border-radius: 6px;
    max-height: 330px !important;
    overflow-y: scroll;
    overflow-x: hidden;
  }
</style>
