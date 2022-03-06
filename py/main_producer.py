from kafka import KafkaProducer
from time import sleep
from json import dumps
from json import JSONEncoder
import jsonpickle


class Key:
    def __init__(self, id):
        self.id = id


class Order:
    def __init__(self, country_origin, amount):
        self.country_origin = country_origin
        self.amount = amount

class Country:
    def __init__(self, country_full_name):
        self.country_full_name = country_full_name


if __name__ == '__main__':


    producer = KafkaProducer\
        (bootstrap_servers=['localhost:9092'],
        #value_serializer = lambda x: dumps(x).encode('utf-8'),
        value_serializer=lambda v: jsonpickle.encode(v,unpicklable=False).encode('utf-8'),
        key_serializer = lambda k: jsonpickle.encode(k,unpicklable=False).encode('utf-8')
    )

    #topic_name = 'country'
    #print(f'producing to {topic_name} topic')
    #key_data = Key("UK")
    #value_data = Country('United Kingdom')
    #producer.send(topic_name, key=key_data, value=value_data)
    #key_data = Key("FR")
    #value_data = Country('France')
    #producer.send(topic_name, key=key_data, value=value_data)

    topic_name = 'orders_2'
    print(f'producing to {topic_name} topic')
    key_data = Key("o1")
    value_data = Order('UK', 12)
    producer.send(topic_name, key=key_data, value=value_data)
    #key_data = Key("o2")
    #value_data = Order('UK', 9)
    #producer.send(topic_name, key=key_data, value=value_data)
    #key_data = Key("o3")
    #value_data = Order('FR', 15)
    #producer.send(topic_name, key=key_data, value=value_data)



    producer.flush()

    #app.main()