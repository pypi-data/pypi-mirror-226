class BaseNDKafka:

    def __init__(self, kafka_server, topic, configs, kafka_path):
        self.kafka_server = kafka_server
        self.topic = topic
        self.configs = configs
        self.kafka_path = kafka_path
        self.required_items = ["kafka_server", "topic", "configs", "kafka_path"]