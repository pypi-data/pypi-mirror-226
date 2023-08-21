from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import time
app = FastAPI()


Instrumentator().instrument(app).expose(
    app=app, should_gzip=False,
    endpoint="/api/v1/metrics",
    include_in_schema=True
)  # Browse http://localhost:8000/api/v1/metrics


@app.get("/")
async def get_users():
    return "Welcome to fast API APP"


@app.get("/users")
async def get_users():
    return [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]


@app.get("/vms")
async def get_users():
    time.sleep(0.2)
    return [{"id": 1, "name": "vm1"}, {"id": 2, "name": "vm2"}]


@app.get("/datastores")
async def get_users():
    return [{"id": 1, "name": "ds1"}, {"id": 2, "name": "ds2"}]

"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/prometheus_exp
$ uvicorn prometheus_fastapi_instrumentator_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\prometheus_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [298592] using statreload
INFO:     Started server process [232400]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


http://127.0.0.1:8000/users
[{"id":1,"name":"user1"},{"id":2,"name":"user2"}]

http://localhost:8000/api/v1/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 347.0
python_gc_objects_collected_total{generation="1"} 50.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 102.0
python_gc_collections_total{generation="1"} 9.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="5",version="3.6.5"} 1.0
# HELP http_requests_total Total number of requests by method, status and handler.
# TYPE http_requests_total counter
# HELP http_request_size_bytes Content length of incoming requests by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE http_request_size_bytes summary
# HELP http_response_size_bytes Content length of outgoing responses by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE http_response_size_bytes summary
# HELP http_request_duration_highr_seconds Latency with many buckets but no API specific labels. Made for more accurate percentile calculations. 
# TYPE http_request_duration_highr_seconds histogram
http_request_duration_highr_seconds_bucket{le="0.01"} 0.0
http_request_duration_highr_seconds_bucket{le="0.025"} 0.0
http_request_duration_highr_seconds_bucket{le="0.05"} 0.0
http_request_duration_highr_seconds_bucket{le="0.075"} 0.0
http_request_duration_highr_seconds_bucket{le="0.1"} 0.0
http_request_duration_highr_seconds_bucket{le="0.25"} 0.0
http_request_duration_highr_seconds_bucket{le="0.5"} 0.0
http_request_duration_highr_seconds_bucket{le="0.75"} 0.0
http_request_duration_highr_seconds_bucket{le="1.0"} 0.0
http_request_duration_highr_seconds_bucket{le="1.5"} 0.0
http_request_duration_highr_seconds_bucket{le="2.0"} 0.0
http_request_duration_highr_seconds_bucket{le="2.5"} 0.0
http_request_duration_highr_seconds_bucket{le="3.0"} 0.0
http_request_duration_highr_seconds_bucket{le="3.5"} 0.0
http_request_duration_highr_seconds_bucket{le="4.0"} 0.0
http_request_duration_highr_seconds_bucket{le="4.5"} 0.0
http_request_duration_highr_seconds_bucket{le="5.0"} 0.0
http_request_duration_highr_seconds_bucket{le="7.5"} 0.0
http_request_duration_highr_seconds_bucket{le="10.0"} 0.0
http_request_duration_highr_seconds_bucket{le="30.0"} 0.0
http_request_duration_highr_seconds_bucket{le="60.0"} 0.0
http_request_duration_highr_seconds_bucket{le="+Inf"} 0.0
http_request_duration_highr_seconds_count 0.0
http_request_duration_highr_seconds_sum 0.0
# HELP http_request_duration_highr_seconds_created Latency with many buckets but no API specific labels. Made for more accurate percentile calculations. 
# TYPE http_request_duration_highr_seconds_created gauge
http_request_duration_highr_seconds_created 1.6529400945482194e+09
# HELP http_request_duration_seconds Latency with only few buckets by handler. Made to be only used if aggregation by handler is important. 
# TYPE http_request_duration_seconds histogram
"""