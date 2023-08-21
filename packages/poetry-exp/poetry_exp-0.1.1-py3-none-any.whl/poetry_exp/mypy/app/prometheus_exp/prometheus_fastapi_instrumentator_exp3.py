# https://pypi.org/project/prometheus-fastapi-instrumentator/#adding-metrics

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from math import inf

app = FastAPI()

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=False,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "metrics"],
    inprogress_name="http_requests_inprogress",
    inprogress_labels=True)

print(dir(metrics))

#
# ['Callable', 'Counter', 'Histogram', 'Info', 'Optional', 'Request', 'Response'
#     , 'Summary', 'Tuple', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
#  '__name__', '__package__', '__spec__', '_build_label_attribute_names', 'combined_size',
#  'default', 'latency', 'request_size', 'requests', 'response_size']


#
# instrumentator.add(metrics.default(
#     metric_namespace='atlas',
#     metric_subsystem="virtmgr",
#     should_only_respect_2xx_for_highr=False))
# # here metrics name will be like atlas_virtapi_http_request_total

instrumentator.add(
        metrics.requests(
            metric_name="atlas_virtmgr_mgr_http_requests_total"
        )
    )
instrumentator.add(
    metrics.request_size(
        metric_name="atlas_virtmgr_http_request_size_bytes"
    )
)
instrumentator.add(
    metrics.response_size(
        metric_name="atlas_virtmgr_http_response_size_bytes"
    )
)

instrumentator.add(
    metrics.latency(
        metric_name="atlas_virtmgr_http_request_duration_seconds",
        buckets=(0.1, 0.2, 0.5, 1, 2, 5, 10, inf)
    )
)

# instrumentator.add(
#     metrics.Counter("atlas_virtmgr_rest_server_errors", documentation='Http Failures').count_exceptions()
# )

instrumentator.instrument(app).expose(
    app=app, should_gzip=False,
    endpoint="/api/v1/metrics",
    include_in_schema=True
)  # Browse http://localhost:8000/api/v1/metrics


num_err = metrics.Counter('api_num_errors','counts number of errors occurred')
#
# num_q = Counter('api_num_queries','counts number of requests sent to API', ['endpoint'])
# num_err = Counter('api_num_errors','counts number of errors occurred')
# latency = Histogram('api_latency', 'latency calculator')
# @latency.time()

@app.get("/")
#@num_err.count_exceptions()
async def get_users():
    a = 3/0
    return "Welcome to fast API APP"


@app.get("/users")
async def get_users():
    return [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]



"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/prometheus_exp
$ uvicorn prometheus_fastapi_instrumentator_exp2:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\prometheus_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [298592] using statreload
INFO:     Started server process [232400]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


Hit following request many times, and keep count and then match that count in matrics
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
python_gc_collections_total{generation="0"} 103.0
python_gc_collections_total{generation="1"} 9.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="5",version="3.6.5"} 1.0
# HELP atlas_virtapi_http_requests_total Total number of requests by method, status and handler.
# TYPE atlas_virtapi_http_requests_total counter
atlas_virtapi_http_requests_total{handler="/users",method="GET",status="200"} 3.0
# HELP atlas_virtapi_http_requests_created Total number of requests by method, status and handler.
# TYPE atlas_virtapi_http_requests_created gauge
atlas_virtapi_http_requests_created{handler="/users",method="GET",status="200"} 1.652941636276972e+09
# HELP atlas_virtapi_http_request_size_bytes Content length of incoming requests by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE atlas_virtapi_http_request_size_bytes summary
atlas_virtapi_http_request_size_bytes_count{handler="/users"} 3.0
atlas_virtapi_http_request_size_bytes_sum{handler="/users"} 0.0
# HELP atlas_virtapi_http_request_size_bytes_created Content length of incoming requests by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE atlas_virtapi_http_request_size_bytes_created gauge
atlas_virtapi_http_request_size_bytes_created{handler="/users"} 1.652941636276972e+09
# HELP atlas_virtapi_http_response_size_bytes Content length of outgoing responses by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE atlas_virtapi_http_response_size_bytes summary
atlas_virtapi_http_response_size_bytes_count{handler="/users"} 3.0
atlas_virtapi_http_response_size_bytes_sum{handler="/users"} 147.0
# HELP atlas_virtapi_http_response_size_bytes_created Content length of outgoing responses by handler. Only value of header is respected. Otherwise ignored. No percentile calculated. 
# TYPE atlas_virtapi_http_response_size_bytes_created gauge
atlas_virtapi_http_response_size_bytes_created{handler="/users"} 1.652941636276972e+09
# HELP atlas_virtapi_http_request_duration_highr_seconds Latency with many buckets but no API specific labels. Made for more accurate percentile calculations. 
# TYPE atlas_virtapi_http_request_duration_highr_seconds histogram
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.01"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.025"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.05"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.075"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.1"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.25"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="0.75"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="1.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="1.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="2.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="2.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="3.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="3.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="4.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="4.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="5.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="7.5"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="10.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="30.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="60.0"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_bucket{le="+Inf"} 3.0
atlas_virtapi_http_request_duration_highr_seconds_count 3.0
atlas_virtapi_http_request_duration_highr_seconds_sum 0.0034099344340348795
# HELP atlas_virtapi_http_request_duration_highr_seconds_created Latency with many buckets but no API specific labels. Made for more accurate percentile calculations. 
# TYPE atlas_virtapi_http_request_duration_highr_seconds_created gauge
atlas_virtapi_http_request_duration_highr_seconds_created 1.6529416241200159e+09
# HELP atlas_virtapi_http_request_duration_seconds Latency with only few buckets by handler. Made to be only used if aggregation by handler is important. 
# TYPE atlas_virtapi_http_request_duration_seconds histogram
atlas_virtapi_http_request_duration_seconds_bucket{handler="/users",le="0.1"} 3.0
atlas_virtapi_http_request_duration_seconds_bucket{handler="/users",le="0.5"} 3.0
atlas_virtapi_http_request_duration_seconds_bucket{handler="/users",le="1.0"} 3.0
atlas_virtapi_http_request_duration_seconds_bucket{handler="/users",le="+Inf"} 3.0
atlas_virtapi_http_request_duration_seconds_count{handler="/users"} 3.0
atlas_virtapi_http_request_duration_seconds_sum{handler="/users"} 0.0034099344340348795
# HELP atlas_virtapi_http_request_duration_seconds_created Latency with only few buckets by handler. Made to be only used if aggregation by handler is important. 
# TYPE atlas_virtapi_http_request_duration_seconds_created gauge
atlas_virtapi_http_request_duration_seconds_created{handler="/users"} 1.652941636276972e+09
# HELP http_requests_inprogress Number of HTTP requests in progress.
# TYPE http_requests_inprogress gauge
http_requests_inprogress{handler="/users",method="GET"} 0.0
"""