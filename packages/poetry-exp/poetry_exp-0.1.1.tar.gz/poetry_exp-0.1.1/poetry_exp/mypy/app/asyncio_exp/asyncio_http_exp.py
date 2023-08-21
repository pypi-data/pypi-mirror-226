import asyncio
import aiohttp # Asynchronous HTTP Client/Server for asyncio and Python.
from datetime import datetime
import time
loop = asyncio.get_event_loop()


async def fetch_page(url, url_response):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            details = await response.text()
            print('{0}: URL: {1}, Response: {2}'.format(datetime.now(), url, details))
            url_response[url] = details


async def get_url_response():
    url_response = {}
    tasks = []
    # 80 urls
    urls = [
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
        'http://localhost:5000/home',
        'http://localhost:5000/index',
        'http://localhost:5000/admin',
        'http://localhost:5000/products',
    ]
    print('No of URLS # {0}'.format(len(urls)))
    for i, url in enumerate(urls, 1):
        print('{0}: URL No.# {1}, Fetching URL: {2}'.format(datetime.now(), i, url))

        task = loop.create_task(fetch_page(url, url_response))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(url_response)


if __name__ == '__main__':
    # First run the flask_server.py
    s = time.perf_counter()
    loop.run_until_complete(get_url_response())
    total_time = time.perf_counter() - s
    print('{0}: total_time: {1}'.format(datetime.now(), total_time)) # total_time: 81.294096
    # where as if you use request module withoutusing thread/process, it will take just double time
    # 161 sec, see without_asyncio_http_exp.py


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/asyncio_http_exp.py"
No of URLS # 80
2019-12-09 11:24:45.631355: URL No.# 1, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 2, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 3, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 4, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 5, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 6, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 7, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 8, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 9, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 10, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 11, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 12, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 13, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 14, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 15, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 16, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 17, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 18, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 19, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 20, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 21, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 22, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 23, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 24, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 25, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 26, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 27, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 28, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.631355: URL No.# 29, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.631355: URL No.# 30, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.631355: URL No.# 31, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.631355: URL No.# 32, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.632392: URL No.# 33, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.632392: URL No.# 34, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.632392: URL No.# 35, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.632392: URL No.# 36, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.632392: URL No.# 37, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.632392: URL No.# 38, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.632392: URL No.# 39, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.632392: URL No.# 40, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.632392: URL No.# 41, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.632392: URL No.# 42, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.632392: URL No.# 43, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.632392: URL No.# 44, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.632392: URL No.# 45, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.632392: URL No.# 46, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.632392: URL No.# 47, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.632392: URL No.# 48, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.632392: URL No.# 49, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 50, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 51, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 52, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 53, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 54, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 55, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 56, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 57, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 58, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 59, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 60, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 61, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 62, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 63, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 64, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 65, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 66, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 67, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 68, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 69, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 70, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 71, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 72, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 73, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 74, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 75, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 76, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:45.634393: URL No.# 77, Fetching URL: http://localhost:5000/home
2019-12-09 11:24:45.634393: URL No.# 78, Fetching URL: http://localhost:5000/index
2019-12-09 11:24:45.634393: URL No.# 79, Fetching URL: http://localhost:5000/admin
2019-12-09 11:24:45.634393: URL No.# 80, Fetching URL: http://localhost:5000/products
2019-12-09 11:24:47.753367: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:24:48.765660: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:24:49.767925: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:24:50.779191: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:24:51.781077: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:24:52.782231: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:24:53.783917: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:24:54.785520: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:24:55.787399: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:24:56.789184: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:24:57.790733: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:24:58.792637: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:24:59.794324: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:00.796167: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:01.797850: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:02.798957: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:03.800051: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:04.801127: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:05.802784: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:06.804459: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:07.805717: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:08.808702: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:09.810362: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:10.812027: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:11.813688: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:12.828562: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:13.829604: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:14.832271: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:15.833934: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:16.836600: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:17.840270: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:18.841934: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:19.843602: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:20.845263: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:21.847933: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:22.849555: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:23.851278: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:24.852826: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:25.853833: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:26.855711: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:27.857426: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:28.858543: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:29.859635: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:30.861211: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:31.862643: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:32.864293: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:33.865586: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:34.866557: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:35.867987: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:36.869176: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:37.869643: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:38.872573: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:39.873959: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:40.875195: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:41.876937: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:42.878634: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:43.880474: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:44.882077: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:45.883391: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:46.885021: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:47.886496: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:25:48.888041: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:49.889276: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:50.890364: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:51.891728: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:52.892571: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:53.904239: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:54.905359: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:25:55.907295: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:56.908663: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:25:57.910835: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:58.912542: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:25:59.914224: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:26:00.916210: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:26:01.917435: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:26:02.918664: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:26:03.920443: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:26:04.921685: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:26:05.922935: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:26:06.924749: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
{'http://localhost:5000/home': 'Welcome to Home Page', 'http://localhost:5000/admin': 'Welcome to Admin Page', 'http://localhost:5000/index': 'Welcome to Index Page', 'http://localhost:5000/products': 'Welcome to Product Page'}
2019-12-09 11:26:06.924749: total_time: 81.294096


"""