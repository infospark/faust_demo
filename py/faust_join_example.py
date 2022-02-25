import faust


class MyKey(faust.Record, serializer='json'):
    id: str


class Order(faust.Record, serializer='json'):
    country_origin: str
    amount: int


class Country(faust.Record, serializer='json'):
    country_full_name: str


app = faust.App(
    'join_012',
    broker='kafka://localhost:9092',
)


orders = app.topic('orders_2', value_type=Order, key_type=MyKey)
country = app.topic('country', value_type=Country, key_type=MyKey)
country_table = app.Table('country_table', partitions=8)
#country_table_2 = app.GlobalTable()

# Creates a table from a Topic and joins to that table

@app.agent(orders)
async def process_order(left_stream):
    async for k,v in left_stream.items():
        print('len country_table', len(country_table))

        if v.country_origin in country_table:
            print('got country:', country_table[v.country_origin])
        print ('left', k,v)


@app.agent(country)
async def process_country(right_stream):
    async for k,v in right_stream.items():
        country_table[k.id] = v
        print ('country_table', country_table)

