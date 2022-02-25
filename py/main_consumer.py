from kafka import KafkaConsumer
from json import loads

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'orders_out',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='orders_out_23',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for m in consumer:
        print('m:', m.key, m.value)