import faust
from json import loads


class MyKey(faust.Record, serializer='json'):
    id: str


class Order(faust.Record, serializer='json'):
    country_origin: str
    amount: int


app = faust.App(
    'orders_cs_447',
    broker='kafka://localhost:9092',
)


topic_name = 'orders_new'
orders_topic = app.topic(topic_name, value_type=Order, key_type=MyKey)
orders_out = app.topic('orders_out', value_type=Order, key_type=MyKey)

# process inbound messages, do something, push to a new topic
@app.agent(orders_topic)
async def process(orders_stream):
    async for e in orders_stream.events():
        e.value.amount = 999
        await orders_out.send(key=e.key,value=e.value)

