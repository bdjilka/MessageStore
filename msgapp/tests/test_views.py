from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from msgapp.models import StoreUser, Message, History


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Тестирование создания пользователя
        """
        data = {'username': 'test_user', 'password': 'fuckdisshit'}
        response = self.client.post('/auth/users/create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StoreUser.objects.count(), 1)
        self.assertEqual(StoreUser.objects.get().username, 'test_user')


class MessageTests(APITestCase):
    def test_create_message(self):
        """
        Тестирование создания сообщения
        """
        StoreUser.objects.create(
            username='user',
            password='password'
        )

        user = StoreUser.objects.get(username='user')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'text': 'test_message'}
        response = client.post('/api/message/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'test_message')

    def test_modify_message(self):
        """
        Тестирование изменения сообщения и сохранения измения в историю
        """
        StoreUser.objects.create(
            username='user',
            password='password'
        )

        user = StoreUser.objects.get(username='user')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'text': 'test_message'}
        data_modify = {'text': 'modified_message'}

        client.post('/api/message/', data, format='json')
        pk = str(Message.objects.get().id)

        response = client.put('/api/message/' + pk + '/', data_modify, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(History.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'modified_message')
        self.assertEqual(History.objects.get().text, 'modified_message')

    def test_permissions(self):
        """
        Тестирование разграничения прав на изменение и удаление сообщений
        """
        StoreUser.objects.create(
            username='user_1',
            password='password'
        )
        StoreUser.objects.create(
            username='user_2',
            password='password'
        )

        user = StoreUser.objects.get(username='user_1')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'text': 'test_message'}
        data_modify = {'text': 'modified_message'}

        client.post('/api/message/', data, format='json')
        pk = str(Message.objects.get().id)

        user = StoreUser.objects.get(username='user_2')
        client.force_authenticate(user=user)

        response = client.put('/api/message/' + pk + '/', data_modify, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.delete('/api/message/' + pk + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_delete(self):
        """
        Тестирование каскадного удаления данных при удалении сообщения
        """
        StoreUser.objects.create(
            username='user',
            password='password'
        )

        user = StoreUser.objects.get(username='user')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'text': 'test_message'}
        data_modify = {'text': 'modified_message'}

        client.post('/api/message/', data, format='json')
        pk = str(Message.objects.get().id)
        client.put('/api/message/' + pk + '/', data_modify, format='json')

        client.delete('/api/message/' + pk + '/')

        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(History.objects.count(), 0)


class PermissionTests(APITestCase):
    def test_get_history(self):
        """
        Тестирование получения информации неавторизованным пользователем
        """

        client = APIClient()
        response = client.get('/api/history/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
