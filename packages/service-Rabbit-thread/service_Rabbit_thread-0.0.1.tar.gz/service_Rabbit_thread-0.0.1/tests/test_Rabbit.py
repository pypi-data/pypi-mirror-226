from unittest import TestCase, mock
from rabbit_library import Rabbit
from unittest.mock import MagicMock
import time
import pytest


class TestRabbit(TestCase):
    def setUp(self):
        self.rabbit = Rabbit('localhost', 5672, 'test', 'guest', 'guest')
        self.message_handler_mock = mock.MagicMock()

    def test_getmessages_success(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                self.rabbit.getMessages(
                    'test_queue', 'test', self.message_handler_mock, 1)
                receive_message_mock.assert_called_once_with(
                    'test_queue', 'test', self.message_handler_mock, 1)

    def test_getmessages_error_message_handler(self):
        with self.assertRaises(TypeError):
            self.rabbit.getMessages('queue', 'not_callable', None, 1)

    def test_getmessages_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit.getMessages(
                None, 'not_callable', self.message_handler_mock, 1)

    def test_getmessages_success_exchange_none(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                self.rabbit.getMessages(
                    'test_queue', None, self.message_handler_mock, 1)
                receive_message_mock.assert_called_once_with(
                    'test_queue', 'test', self.message_handler_mock, 1)
                
    def test_getmessages_success_set_default_limit_get_messages(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect'):
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                self.rabbit.getMessages(
                    'test_queue', 'test', self.message_handler_mock, None)
                receive_message_mock.assert_called_once_with(
                    'test_queue', 'test', self.message_handler_mock, 1)

    def test_get_messages_with_Exception(self,):
        with mock.patch.object(self.rabbit, '_Rabbit__is_connected') as is_connected_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with self.assertLogs(level="ERROR") as log:
                    is_connected_mock.side_effect = Exception(
                        'Error receiving message from rabbit:')
                    self.rabbit.getMessages(
                        'test_queue', 'test', self.message_handler_mock, 1)
                    assert "Error receiving message from rabbit:" in log.output[0]

    def test_post_message_success(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect') as connect_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__send_message') as send_message_mock:
                result = self.rabbit.postMessage(
                    'test_queue', 'test', 'test_message')
                send_message_mock.assert_called_once_with(
                    'test_queue', 'test', 'test_message')
                self.assertTrue(result)

    def test_post_message_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit.postMessage(
                None, 'test', 'test_message')

    def test_post_message_success_exchange_none(self):
        with mock.patch.object(self.rabbit, '_Rabbit__connect') as connect_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__send_message') as send_message_mock:
                result = self.rabbit.postMessage(
                    'test_queue', None, 'test_message')
                send_message_mock.assert_called_once_with(
                    'test_queue', 'test', 'test_message')
                self.assertTrue(result)

    def test_post_message_with_Exception(self,):
        with mock.patch.object(self.rabbit, '_Rabbit__is_connected') as is_connected_mock:
            with mock.patch.object(self.rabbit, '_Rabbit__receive_message') as receive_message_mock:
                with self.assertLogs(level="ERROR") as log:
                    is_connected_mock.side_effect = Exception(
                        'Error the send message to rabbit:')
                    self.rabbit.postMessage(
                        'test_queue', 'test', 'test_message')
                    assert "Error the send message to rabbit:" in log.output[0]

    def test_is_connected(self):
        assert not self.rabbit._Rabbit__is_connected()
        self.rabbit.connection = mock.Mock()
        assert not self.rabbit._Rabbit__is_connected()
        self.rabbit.connection.is_closed = False
        assert self.rabbit._Rabbit__is_connected()

    @mock.patch('pika.SelectConnection')
    # @mock.patch.object(Rabbit, 'on_connection_open')
    def test__connect(self, select_connection_mock):
        self.__on_connection_open = MagicMock()
        self.rabbit.channel = True
        assert not self.rabbit._Rabbit__connect()

    @mock.patch('pika.SelectConnection')
    def test_wait_for_channel_open(self, select_connection_mock):
        # Cria um mock para simular o objeto channel
        mock_channel = MagicMock()

        # Cria um mock para simular o objeto SelectConnection
        mock_select_connection = MagicMock()

        # Define um método simulado para substituir o método ioloop.start do objeto SelectConnection
        def mock_ioloop_start():
            # Aguarda um tempo específico para simular a abertura do canal
            time.sleep(1)
            # Define o valor de self.channel como o objeto mock_channel
            self.rabbit.channel = mock_channel

        # Substitui o método ioloop.start do objeto SelectConnection pelo método simulado
        mock_select_connection.ioloop.start = mock_ioloop_start

        # Substitui a classe SelectConnection pelo mock criado
        select_connection_mock.return_value = mock_select_connection

        # Inicia o teste do método __connect
        self.rabbit._Rabbit__connect()

        # Verifica se o valor de self.channel foi alterado para o objeto mock_channel
        assert self.rabbit.channel == mock_channel

    @mock.patch('pika.PlainCredentials')
    def test__connect_with_Exception(self, PlainCredentials_mock):
        with self.assertLogs(level="ERROR") as log:
            PlainCredentials_mock.side_effect = Exception(
                'Failed to connect to rabbit:')
            self.rabbit._Rabbit__connect()
            assert "Failed to connect to rabbit:" in log.output[0]

    def test__on_connection_open(self,):
        mock_connection = MagicMock()
        assert not self.rabbit._Rabbit__on_connection_open(mock_connection)

    def test__on_channel_open(self):
        mock_connection = MagicMock()
        assert not self.rabbit._Rabbit__on_channel_open(mock_connection)

    def test__send_message_sucess(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock()
        self.rabbit.channel.queue_bind = MagicMock()
        self.rabbit.channel.basic_publish = MagicMock()
        self.rabbit._Rabbit__send_message(
            'teste_queue', 'teste_exchange', 'teste_message')
        assert self.rabbit._Rabbit__send_message('teste_queue', 'teste_exchange', 'teste_message')
        self.rabbit.channel.queue_declare.assert_called_with(queue='teste_queue', durable=True)
        self.rabbit.channel.basic_publish.assert_called_with(
            exchange="teste_exchange", routing_key='teste_queue', body='teste_message')

    def test__send_message_error_queue_None(self):
        with self.assertRaises(ValueError):
            self.rabbit._Rabbit__send_message(None, 'teste_exchange', 'teste_message')
    
    def test_send_message_exception(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock(side_effect=Exception('Error'))
        
        with pytest.raises(Exception):
            with self.assertLogs(level="ERROR") as log:
                assert not self.rabbit._Rabbit__send_message('teste_queue', 'teste_exchange', 'teste_message')
                assert "Error the send message to rabbit: Error" in log.output[0]

    def test_receive_message(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.queue_declare = MagicMock()
        self.rabbit.channel.queue_bind = MagicMock()
        self.rabbit.channel.basic_consume = MagicMock()
        
        message_handler = MagicMock()
        self.rabbit._Rabbit__receive_message('teste_queue', 'teste_exchange', message_handler, 1)
        self.rabbit.channel.queue_declare.assert_called_with(queue='teste_queue', durable=True)
        self.rabbit.channel.queue_bind.assert_called_with(queue='teste_queue', exchange='teste_exchange', routing_key='teste_queue')
        self.rabbit.channel.basic_consume.assert_called_once()
    
    def test_receive_message_exception(self):
        self.rabbit.channel = MagicMock()
        self.rabbit.channel.basic_qos = MagicMock(side_effect=Exception('Error'))

        with self.assertLogs(level="ERROR") as log:
            message_handler = MagicMock()
            self.rabbit._Rabbit__receive_message('teste_queue', 'teste_exchange', message_handler, 1)
            assert "Error receiving message: Error" in log.output[0]
    
    @mock.patch.object(Rabbit, '_Rabbit__is_connected')
    @mock.patch.object(Rabbit, '_Rabbit__connect')
    def test_receive_message_function_callback(self,connect_mock,is_connected_mock):
        # Set up mock objects
        ch = MagicMock()
        method = MagicMock()
        properties = MagicMock()
        body = "test message"
        message_handler = MagicMock()     
        self.rabbit.channel = MagicMock()

        self.rabbit._Rabbit__receive_message('teste_queue', 'teste_exchange', message_handler, 1)

        # Recupera a função que foi passada como callback do basic_consume call_args
        callback = self.rabbit.channel.basic_consume.call_args[1][
        "on_message_callback"
        ]
        # Invoca a função de callback
        callback(ch, method, properties, body)

        # verifica se afunção message_handler foi chamada com os argumentos corretos
        message_handler.assert_called_once_with(ch, method, properties, body)
    
    def test_close_connection(self):
        # Set up Rabbit instance
        self.rabbit.connection = MagicMock()
        self.rabbit.connection.is_closed = False
        # Call __close_connection method
        self.rabbit.close_connection()

        # Check that connection.close was called
        self.rabbit.connection.close.assert_called_once()

    def test_close_connection_exception(self):
        self.rabbit.connection = MagicMock()
        self.rabbit.connection.is_closed = False
        self.rabbit.connection.close.side_effect = Exception("test error")
        
        
        with self.assertLogs(level="ERROR") as log:
            self.rabbit.close_connection()
            assert "Error closing connection: test error" in log.output[0]