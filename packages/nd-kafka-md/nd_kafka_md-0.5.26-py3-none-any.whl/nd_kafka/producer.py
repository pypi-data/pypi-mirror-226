import argparse
import subprocess as subp
from nd_kafka.base import BaseNDKafka


class Producer(BaseNDKafka):

    def __init__(self, kafka_server, topic, configs, kafka_path):
        super().__init__(kafka_server, topic, configs, kafka_path)
        self.producer = None


    def create_producer(self):
        error_list = []

        # Check if all required items have values
        for item in self.required_items:
            if getattr(self, item) is None:
                error_list.append(f"Error: {item} is missing!")
        
        if error_list:
            return error_list

        # Create a dictionary of arguments
        arguments = {
            "kafka_servers": {
                "option_strings": ["--kafka-servers"],
                "dest": "kafka_servers",
                "type": str,
                "default": self.kafka_server,
                "help": "kafka servers (comma separated)",
            },
            "pub_topic": {
                "option_strings": ["--pub-topic"],
                "dest": "pub_topic",
                "type": str,
                "default": self.topic,
                "help": "topic where to publish data to",
            },
            "configs": {
                "option_strings": ["--configs"],
                "dest": "configs",
                "type": str,
                "default": self.configs,
                "help": "custom client properties to enable IAM auth enabled kafka cluster.",
            },
            "kafka_path": {
                "option_strings": ["--kafka-path"],
                "dest": "kafka_path",
                "type": str,
                "default": self.kafka_path,
                "help": "ocation where kafka is installed",
            },
        }


        parser = argparse.ArgumentParser()
        # Add the arguments from the dictionary to the parser
        for key, value in arguments.items():
            parser.add_argument(*value["option_strings"], **value)

        # Parse the arguments
        args = parser.parse_args()

        # Create the producer process in a separate thread
        self.producer = self.__create_cli_producer(args)
        return self.producer


    def __create_cli_producer(self, arguments):
        print(f"Initializing kafka producer for servers: {arguments.kafka_servers}")
        print(f"topic: {arguments.pub_topic}")

        kafka_producer_init_cmd = [
            f"{arguments.kafka_path}/bin/kafka-console-producer.sh",
            "--topic", arguments.pub_topic,
            "--bootstrap-server", arguments.kafka_servers
        ]

        if arguments.configs:
            kafka_producer_init_cmd = kafka_producer_init_cmd + ["--producer.config", arguments.configs]

        try:
            proc = subp.Popen(kafka_producer_init_cmd, stdin=subp.PIPE)
            print("kafka producer init done.")
            return proc
        except Exception as e:
            print(f"Error creating producer: {e}")
            return None


    def produce_message(self, msg):
        # Publish the received message to the producer
        try:
            print(f"Publishing message: {msg}")
            if not isinstance(msg, bytes):
                msg = f"{msg}".encode()

            self.producer.stdin.write(msg + b"\n")
            self.producer.stdin.flush()
            return True, "Message Published successfully"
        except Exception as e:
            return False, f"Error sending message: {e}"