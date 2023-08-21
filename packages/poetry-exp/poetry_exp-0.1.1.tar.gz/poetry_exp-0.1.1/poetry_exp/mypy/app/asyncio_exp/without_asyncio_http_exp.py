from datetime import datetime
import time
import requests


def fetch_page(url, url_response):
    response = requests.get(url)
    details = response.text
    print('{0}: URL: {1}, Response: {2}'.format(datetime.now(), url, details))
    url_response[url] = details


def get_url_response():
    url_response = {}
    # 40 urls
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

        fetch_page(url, url_response)

    print(url_response)


if __name__ == '__main__':
    s = time.perf_counter()
    get_url_response()
    total_time = time.perf_counter() - s
    print('{0}: total_time: {1}'.format(datetime.now(), total_time))   # total_time: 161.11854012121213


"""
C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/asyncio_exp/without_asyncio_http_exp.py"
No of URLS # 80
2019-12-09 11:19:47.335889: URL No.# 1, Fetching URL: http://localhost:5000/home
2019-12-09 11:19:49.375307: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:19:49.375307: URL No.# 2, Fetching URL: http://localhost:5000/index
2019-12-09 11:19:51.388675: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:19:51.388675: URL No.# 3, Fetching URL: http://localhost:5000/admin
2019-12-09 11:19:53.402520: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:19:53.402520: URL No.# 4, Fetching URL: http://localhost:5000/products
2019-12-09 11:19:55.425527: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:19:55.425527: URL No.# 5, Fetching URL: http://localhost:5000/home
2019-12-09 11:19:57.436962: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:19:57.436962: URL No.# 6, Fetching URL: http://localhost:5000/index
2019-12-09 11:19:59.453374: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:19:59.453374: URL No.# 7, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:01.465565: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:01.465565: URL No.# 8, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:03.477487: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:03.477487: URL No.# 9, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:05.499159: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:05.499159: URL No.# 10, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:07.511580: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:07.511580: URL No.# 11, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:09.521622: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:09.521622: URL No.# 12, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:11.532255: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:11.532255: URL No.# 13, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:13.541804: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:13.541804: URL No.# 14, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:15.554136: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:15.554136: URL No.# 15, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:17.572142: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:17.572142: URL No.# 16, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:19.592985: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:19.592985: URL No.# 17, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:21.605856: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:21.605856: URL No.# 18, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:23.616668: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:23.616668: URL No.# 19, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:25.626027: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:25.626027: URL No.# 20, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:27.635925: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:27.635925: URL No.# 21, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:29.647692: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:29.647692: URL No.# 22, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:31.658707: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:31.658707: URL No.# 23, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:33.671128: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:33.671128: URL No.# 24, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:35.695014: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:35.695014: URL No.# 25, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:37.716543: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:37.716543: URL No.# 26, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:39.727315: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:39.727315: URL No.# 27, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:41.738953: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:41.738953: URL No.# 28, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:43.749251: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:43.749251: URL No.# 29, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:45.761043: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:45.761043: URL No.# 30, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:47.771302: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:47.772305: URL No.# 31, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:49.785265: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:49.785265: URL No.# 32, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:51.797248: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:51.797248: URL No.# 33, Fetching URL: http://localhost:5000/home
2019-12-09 11:20:53.821910: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:20:53.821910: URL No.# 34, Fetching URL: http://localhost:5000/index
2019-12-09 11:20:55.836340: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:20:55.837341: URL No.# 35, Fetching URL: http://localhost:5000/admin
2019-12-09 11:20:57.856726: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:20:57.856726: URL No.# 36, Fetching URL: http://localhost:5000/products
2019-12-09 11:20:59.875577: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:20:59.875577: URL No.# 37, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:01.891319: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:01.891319: URL No.# 38, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:03.906875: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:03.906875: URL No.# 39, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:05.917342: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:05.917342: URL No.# 40, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:07.937796: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:07.937796: URL No.# 41, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:09.947828: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:09.947828: URL No.# 42, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:11.958550: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:11.958550: URL No.# 43, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:13.970446: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:13.970446: URL No.# 44, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:15.980754: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:15.980754: URL No.# 45, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:17.991144: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:17.991144: URL No.# 46, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:20.001370: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:20.001370: URL No.# 47, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:22.015262: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:22.015262: URL No.# 48, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:24.031582: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:24.031582: URL No.# 49, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:26.043142: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:26.043142: URL No.# 50, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:28.054787: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:28.054787: URL No.# 51, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:30.066147: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:30.066147: URL No.# 52, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:32.075451: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:32.075451: URL No.# 53, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:34.085691: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:34.085691: URL No.# 54, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:36.097300: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:36.097300: URL No.# 55, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:38.108211: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:38.108211: URL No.# 56, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:40.121598: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:40.121598: URL No.# 57, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:42.136736: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:42.136736: URL No.# 58, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:44.148832: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:44.148832: URL No.# 59, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:46.157722: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:46.157722: URL No.# 60, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:48.179588: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:48.179588: URL No.# 61, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:50.191042: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:50.191042: URL No.# 62, Fetching URL: http://localhost:5000/index
2019-12-09 11:21:52.201449: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:21:52.201449: URL No.# 63, Fetching URL: http://localhost:5000/admin
2019-12-09 11:21:54.211895: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:21:54.211895: URL No.# 64, Fetching URL: http://localhost:5000/products
2019-12-09 11:21:56.223942: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:21:56.223942: URL No.# 65, Fetching URL: http://localhost:5000/home
2019-12-09 11:21:58.233918: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:21:58.233918: URL No.# 66, Fetching URL: http://localhost:5000/index
2019-12-09 11:22:00.244842: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:22:00.244842: URL No.# 67, Fetching URL: http://localhost:5000/admin
2019-12-09 11:22:02.257059: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:22:02.257059: URL No.# 68, Fetching URL: http://localhost:5000/products
2019-12-09 11:22:04.284308: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:22:04.284308: URL No.# 69, Fetching URL: http://localhost:5000/home
2019-12-09 11:22:06.295335: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:22:06.295335: URL No.# 70, Fetching URL: http://localhost:5000/index
2019-12-09 11:22:08.305162: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:22:08.305162: URL No.# 71, Fetching URL: http://localhost:5000/admin
2019-12-09 11:22:10.328721: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:22:10.328721: URL No.# 72, Fetching URL: http://localhost:5000/products
2019-12-09 11:22:12.341520: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:22:12.341520: URL No.# 73, Fetching URL: http://localhost:5000/home
2019-12-09 11:22:14.352741: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:22:14.352741: URL No.# 74, Fetching URL: http://localhost:5000/index
2019-12-09 11:22:16.362450: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:22:16.362450: URL No.# 75, Fetching URL: http://localhost:5000/admin
2019-12-09 11:22:18.373782: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:22:18.373782: URL No.# 76, Fetching URL: http://localhost:5000/products
2019-12-09 11:22:20.385068: URL: http://localhost:5000/products, Response: Welcome to Product Page
2019-12-09 11:22:20.385068: URL No.# 77, Fetching URL: http://localhost:5000/home
2019-12-09 11:22:22.403485: URL: http://localhost:5000/home, Response: Welcome to Home Page
2019-12-09 11:22:22.403485: URL No.# 78, Fetching URL: http://localhost:5000/index
2019-12-09 11:22:24.414543: URL: http://localhost:5000/index, Response: Welcome to Index Page
2019-12-09 11:22:24.414543: URL No.# 79, Fetching URL: http://localhost:5000/admin
2019-12-09 11:22:26.442781: URL: http://localhost:5000/admin, Response: Welcome to Admin Page
2019-12-09 11:22:26.442781: URL No.# 80, Fetching URL: http://localhost:5000/products
2019-12-09 11:22:28.455155: URL: http://localhost:5000/products, Response: Welcome to Product Page
{'http://localhost:5000/home': 'Welcome to Home Page', 'http://localhost:5000/index': 'Welcome to Index Page', 'http://localhost:5000/admin': 'Welcome to Admin Page', 'http://localhost:5000/products': 'Welcome to Product Page'}
2019-12-09 11:22:28.455155: total_time: 161.11854012121213
"""