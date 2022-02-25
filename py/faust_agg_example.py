import faust
from json import loads


class MyKey(faust.Record, serializer='json'):
    id: str


class Order(faust.Record, serializer='json'):
    country_origin: str
    amount: int


app = faust.App(
    'orders_cs_8',
    broker='kafka://localhost:9092',
)

topic_name = 'orders_new'
orders_topic = app.topic(topic_name, value_type=Order, key_type=str)
orders_by_country = app.Table('orders_by_country', default=int, partitions=8)

for o in orders_by_country:
    print('got',o)

@app.agent(orders_topic)
async def process_order(orders):
    async for order in orders.group_by(Order.country_origin):
        print(f'Got Order {order}')
        country = order.country_origin
        orders_by_country[country] += order.amount
        print(f'Orders for country {country}: {orders_by_country[country]}')

