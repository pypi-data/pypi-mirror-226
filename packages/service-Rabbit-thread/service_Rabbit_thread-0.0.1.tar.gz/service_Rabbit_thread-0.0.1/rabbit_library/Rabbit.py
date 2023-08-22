import pika
import threading
import typing
import logging


class Rabbit():
    def __init__(self, host: str, port: int, virtualhost: str, username: str, password: str):
        self.host: str = host
        self.port: int = port
        self.virtualhost: str = virtualhost
        self.username: str = username
        self.password: str = password
        self.connection = None
        self.channel = None
        self.consume_thread = None
        self.SelectConn = None
        self.confirmed_messages = set()

    def getMessages(self, queue: str, exchange: str, message_handler: typing.Callable, limit_get_messages: int) -> None:
        '''
            Get messages the queue!
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
                limit_get_messages - number of messages that will be taken from the queue
        '''
        if not callable(message_handler):
            raise TypeError(
                "Necessary implemention the message_handler must be a callable function")

        if not queue:
            raise ValueError("Queue parameter is mandatory")       

        try:

            if exchange is None or exchange.strip() == '':
                exchange = self.virtualhost

            if not self.__is_connected():
                self.__connect()

            if not bool(limit_get_messages):
                limit_get_messages = 1

            self.__receive_message(
                queue, exchange, message_handler, limit_get_messages)
        except Exception as e:
            logging.error(
                f"Error receiving message from rabbit: {str(e)} ", stack_info=True)

    def postMessage(self, queue: str, exchange: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:

            if exchange is None or exchange.strip() == '':
                exchange = self.virtualhost

            if not self.__is_connected():
                self.__connect()
            return self.__send_message(queue, exchange, message)

        except Exception as e:
            logging.error(
                f"Error the send message to rabbit: {str(e)} ", stack_info=True)

    def __is_connected(self) -> bool:
        """
            Returns True if the RabbitMQ connection is established, otherwise False.
        """
        if self.connection and not self.connection.is_closed:
            return True
        return False

    def __connect(self) -> None:
        # Method to connect to RabbitMQ
        try:
            # Create a credentials object with the provided username and password
            credentials = pika.PlainCredentials(self.username, self.password)
            # Create a connection parameters object with the provided host, port, and credentials
            parameters = pika.ConnectionParameters(
                self.host, self.port, self.virtualhost, credentials)
            # Create a SelectConnection with the provided parameters and a callback method to handle the established connection
            self.SelectConn = pika.SelectConnection(
                parameters, on_open_callback=self.__on_connection_open)
            # Start the connection's I/O loop in a separate thread
            self.consume_thread = threading.Thread(
                target=self.SelectConn.ioloop.start)
            self.consume_thread.start()

            # Wait until the channel is open
            while not self.channel:
                pass

            

        except Exception as e:
            # Log an error if the connection fails
            logging.error(
                f"Failed to connect to rabbit: {str(e)} ", stack_info=True)

    def __on_connection_open(self, connection):
        # Callback method called when the connection is established
        # Set the connection object and open a channel
        self.connection = connection
        self.connection.channel(on_open_callback=self.__on_channel_open)

    def __on_channel_open(self, channel):
        # Callback method called when the channel is open
        # Set the channel object
        self.channel = channel

    def __send_message(self, queue: str, exchange: str, message: str) -> bool:
        '''
            Send messages the rabbit
        '''
        if not queue:
            raise ValueError("Queue parameter is mandatory")
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.queue_bind(
                queue=queue, exchange=exchange, routing_key=queue)
            self.channel.basic_publish(
                exchange=exchange, routing_key=queue, body=message)
            
            return True
        except Exception as e:
            logging.error(
                f"Error the send message to rabbbit: {str(e)} ", stack_info=True)
            return False

    def __receive_message(self, queue: str, exchange: str, message_handler: typing.Callable, limit_get_messages: int) -> None:
        '''
            Connect the rabbit consume messages the queue and return message in the method "process_message"
            Recived: 
                queue - queue to get messages
                message_handler - method executed after having each message
                limit_get_messages - number of messages that will be taken from the queue
        '''
        try:

            def callback(ch, method, properties, body):
                message_handler(ch, method, properties, body)

            self.channel.basic_qos(prefetch_count=limit_get_messages)
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.queue_bind(
                queue=queue, exchange=exchange, routing_key=queue)
            self.channel.basic_consume(
                queue=queue, on_message_callback=callback, auto_ack=False)

        except Exception as e:
            logging.error(
                f"Error receiving message: {str(e)} ", stack_info=True)

    def close_connection(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception as e:
            logging.error(
                f"Error closing connection: {str(e)} ", stack_info=True)
