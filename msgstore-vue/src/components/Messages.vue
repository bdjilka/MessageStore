<template>
  <div class="msg-layout">

    <!--  -->

    <v-data-table
      :headers="headers"
      :items="data"
      hide-actions
      id="msg-table"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-center" @click="open_msg(props.item)">{{ props.item.user }}</td>
        <td class="text-xs-center" @click="open_msg(props.item)">{{ props.item.text }}</td>
        <td class="text-xs-center" @click="open_msg(props.item)">{{ props.item.created }}</td>
        <td class="text-xs-center" @click="open_msg(props.item)">{{ props.item.modified }}</td>
      </template>

      <template slot="footer">
        <td :colspan="headers.length" class="nav-bar">

          <!-- поле и кнопка для отправки соббщения -->

          <input v-model="msg_text" type="text" placeholder="Текст сообщения" class="msg-input"/>
          <v-btn small @click="send">Отправить</v-btn>

          <!---->

          <!-- переход на предыдущую страницу -->

          <v-btn small v-if="!(prev_page == null)" @click="to_prev_page" class="prev"> <</v-btn>

          <!---->

          <!-- переход на следующую страницу -->

          <v-btn small v-if="!(next_page == null)" @click="to_next_page" class="next"> ></v-btn>

          <!---->
        </td>
      </template>

    </v-data-table>

    <div class="filter-bar">

      <!-- поля фильтров -->

      <input v-model="filter.text" type="text" placeholder="Текст сообщения" class="filter"/>
      <input v-model="filter.username" type="text" placeholder="Автор" class="filter"/>
      <!--<input v-model="filter.publish" type="text" placeholder="Дата публикации" class="filter"/>-->
      <!--<input v-model="filter.modify" type="text" placeholder="Дата изменения" class="filter"/>-->

      <!---->

      <!-- кнопка отправки запроса на фильтрацию, сброс фильтрации -->

      <v-btn small @click="get_filtered_messeges" v-if="!is_filtered"> Фильтровать</v-btn>
      <v-btn small @click="get_messages" v-if="is_filtered"> Сбросить</v-btn>

      <!---->
    </div>

    <!---->

  </div>
</template>

<script>
  import $ from 'jquery'

  export default {
    name: "Messages",
    data() {
      return {

        // сообщения
        messages: '',

        // фильтрация
        filter: {
          text: '',
          username: '',
          publish: '',
          modify: '',
        },

        // флаг для определения, отфильрована таблица или нет
        is_filtered: false,

        // ссылка на предыдущую страницу
        prev_page: '',

        // ссылка на следущую страницу
        next_page: '',

        // текст для отправки запроса на создание сообщения
        msg_text: '',

        // заголовки таблицы сообщени
        headers: [
          {text: 'Автор', align: 'center', value: 'user'},
          {text: 'Сообщение', align: 'center', value: 'text'},
          {text: 'Дата создания', align: 'center', value: 'created'},
          {text: 'Последнее изменение', align: 'center', value: 'modified'}
        ],

        // данные для таблицы (обрезаны даты, для пользователя сохраен только его логин)
        data: [],
      }
    },

    // установка ключа авторизации при создании компоненты
    created() {
      $.ajaxSetup({
        "headers": {'Authorization': 'Token ' + sessionStorage.getItem('auth_token')},
      });

      // запрос сообщений
      this.get_messages();

      // установка листенера для обновления таблицы (используется в Main, инициируется в MsgCard)
      this.$parent.$on('refresh', this.get_messages);
    },
    methods: {

      // запрос для получения списка сообщений
      get_messages() {
        this.is_filtered = false;
        $.ajax({
          url: "http://127.0.0.1:8000/api/message/",
          type: 'GET',
          success: (response) => {
            this.messages = response.results;
            this.next_page = response.next;
            this.prev_page = response.previous;

            this.data = [];
            for (let i = 0; i < this.messages.length; i++) {
              var msg = this.messages[i];
              this.data.push({
                'user': msg.author.username,
                'text': msg.text,
                'created': msg.publish_date.split('.')[0].replace('T', ' '),
                'modified': msg.last_modify.split('.')[0].replace('T', ' '),
                'id': msg.id
              });
            }
          },
          error: (response) => {
            console.log(response.status);
          }
        });
      },

      // переход на предыдущюю страницу
      to_prev_page() {
        $.ajax({
          url: this.prev_page,
          type: 'GET',
          success: (response) => {
            this.messages = response.results;

            this.data = [];
            for (let i = 0; i < this.messages.length; i++) {
              var msg = this.messages[i];
              this.data.push({
                'user': msg.author.username,
                'text': msg.text,
                'created': msg.publish_date.split('.')[0].replace('T', ' '),
                'modified': msg.last_modify.split('.')[0].replace('T', ' '),
                'id': msg.id
              });
            }

            this.next_page = response.next;
            this.prev_page = response.previous;
          },
          error: (response) => {
            console.log(response.status);
          }
        })
      },

      // переход на следущую страницу
      to_next_page() {
        $.ajax({
          url: this.next_page,
          type: 'GET',
          success: (response) => {
            this.messages = response.results;

            this.data = [];
            for (let i = 0; i < this.messages.length; i++) {
              var msg = this.messages[i];
              this.data.push({
                'user': msg.author.username,
                'text': msg.text,
                'created': msg.publish_date.split('.')[0].replace('T', ' '),
                'modified': msg.last_modify.split('.')[0].replace('T', ' '),
                'id': msg.id
              });
            }

            this.next_page = response.next;
            this.prev_page = response.previous;
          },
          error: (response) => {
            console.log(response.status);
          }
        })
      },

      // отправка сообщения
      send() {
        $.ajax({
          url: 'http://127.0.0.1:8000/api/message/',
          type: 'POST',
          data: {
            text: this.msg_text
          },
          success: (response) => {
            alert('Сообщение добавлено');
            this.get_messages();
            this.msg_text = '';
          },
          error: (response) => {
            console.log(response.status);
            alert('He удалось отправить сообщение');
          }
        })
      },

      // колбэк на открытие сообщения
      open_msg(message) {
        this.$emit('open_message', message);
      },

      // фильтрация списка сообщений
      get_filtered_messeges() {
        this.is_filtered = true;
        $.ajax({
          url: "http://127.0.0.1:8000/api/message/",
          data: {
            last_modify: this.filter.modify,
            publish_date: this.filter.publish,
            text: this.filter.text,
            username: this.filter.username
          },
          type: 'GET',
          success: (response) => {
            this.messages = response.results;
            this.next_page = response.next;
            this.prev_page = response.previous;

            this.data = [];
            for (let i = 0; i < this.messages.length; i++) {
              var msg = this.messages[i];
              this.data.push({
                'user': msg.author.username,
                'text': msg.text,
                'created': msg.publish_date.split('.')[0].replace('T', ' '),
                'modified': msg.last_modify.split('.')[0].replace('T', ' '),
                'id': msg.id
              });
            }
          },
          error: (response) => {
            console.log(response.status);
            alert(response.status);
          }
        });
      }
    }
  }
</script>

<style scoped>
  .msg-layout {
    padding-top: 50px;
    height: calc(100% - 100px);
    width: 65%;
  }

  #msg-table {
    border: 1px solid #ffffffb3;
    border-radius: 6px;
    user-select: none;
    color: #ffffffb3;
  }

  .nav-bar {
    position: relative;
  }

  .next, .prev {
    position: absolute;
    top: 3px;
    min-width: 10px !important;
    width: 30px;
  }

  .next {
    right: 30px;
  }

  .prev {
    right: 60px;
  }

  .msg-input {
    position: absolute;
    left: 30px;
    top: 7px;
    line-height: 30px;
    width: 41%;
    border: 1px solid #6d6d6d;
    border-radius: 6px;
    padding-left: 8px;
  }

  .filter-bar {
    margin-top: 10px;
  }

  .filter {
    border: 1px solid #6d6d6d;
    width: 170px;
    line-height: 30px;
    margin-right: 15px;
    margin-left: 5px;
    border-radius: 6px;
    padding-left: 8px;
  }
</style>
