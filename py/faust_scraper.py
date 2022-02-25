import faust


class IdKey(faust.Record, serializer='json'):
    id: str


class Scrape_Request(faust.Record, serializer='json'):
    url: str  # e.g. https://www.glassdoor.co.uk/Reviews/Hastings-Direct-Reviews-E230322.htm
    destination_topic: str  # Do I need this?
    # What else?
    # How to paginate
    # How to determine the number of pages (e.g. Viewing 11 - 20 of 430 Reviews)


app = faust.App(
    'orders_cs_8',
    broker='kafka://localhost:9092',
)

topic_name = 'scrape_request'
scrape_request_topic = app.topic(topic_name, value_type=Scrape_Request, key_type=IdKey)


@app.agent(scrape_request_topic)
async def process_scrape_request(scrape_requests):
    async for r in scrape_requests:
        print(f'Go Scrape', r.url, 'put the result to', r.destination_topic)
