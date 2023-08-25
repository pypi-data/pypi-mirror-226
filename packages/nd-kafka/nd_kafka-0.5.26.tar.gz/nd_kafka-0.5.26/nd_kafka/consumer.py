import argparse
import subprocess as subp
from nd_kafka.base import BaseNDKafka


class Consumer(BaseNDKafka):
    
    def __init__(self, kafka_server, topic, configs, kafka_path):
        super().__init__(kafka_server, topic, configs, kafka_path)
        self.consumer = None


    def create_consumer(self):
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
            "sub_topic": {
                "option_strings": ["--pub-topic"],
                "dest": "sub_topic",
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

        # Create the consumer process in a separate thread
        self.consumer = self.__create_cli_consumer(args)
        return self.consumer
    

    def __create_cli_consumer(self, arguments):
        print(f"Initializing kafka consumer for servers: {arguments.kafka_servers}")
        print(f"topic: {arguments.sub_topic}")

        kafka_consumer_init_cmd = [
            f"{arguments.kafka_path}/bin/kafka-console-consumer.sh",
            "--topic", arguments.sub_topic,
            "--bootstrap-server", arguments.kafka_servers
        ]

        if arguments.configs:
            kafka_consumer_init_cmd = kafka_consumer_init_cmd + ["--consumer.config", arguments.configs]

        try:
            cons = subp.Popen(kafka_consumer_init_cmd, stdout=subp.PIPE, stderr=subp.PIPE)
            print("kafka consumer init done.")
            return cons
        except Exception as e:
            print(f"Error creating consumer: {e}")
            return None


    # Define a function to consume messages
    def consume_messages(self):
        # consume the received message
        try:
            for line in self.consumer.stdout:
                rcvd_msg = line.decode().strip()
                # print(f"Received: {rcvd_msg}")
                yield f"{rcvd_msg}"

        except Exception as e:
            yield str(e)