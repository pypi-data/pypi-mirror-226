import asyncio
from datetime import datetime
import time
import requests

loop = asyncio.get_event_loop()


class RequestIterator:
    def __init__(self, urls):
        self.urls = urls

    def __iter__(self):
        return self

    def __next__(self):
        if not self.urls:
            raise StopIteration
        else:
           url = self.urls.pop()
           print('Executing request: {0}'.format(url))
           response = requests.get(url)
           print('response: {0}'.format(response.text))
           # response.status_code = 200
           return response


class AsyncRequest:
    def __init__(self, urls):
        self.urls = urls

    def __await__(self):
        return RequestIterator(self.urls)


async def get_web_page(url):
   await AsyncRequest([url])


if __name__ == '__main__':
    # first run flask_server.py
    url = "http://127.0.0.1:5000/products"
    loop.create_task(get_web_page(url))
    loop.run_forever()
    loop.close()


