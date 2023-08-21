from fastapi import FastAPI
#from prometheus_fastapi_instrumentator import Instrumentator

from starlette_exporter import PrometheusMiddleware, handle_metrics
app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/matrics", handle_metrics)   # Browse http://localhost:8000/matrics

#Instrumentator().instrument(app).expose(app)


@app.get("/")
async def get_users():
    return "Welcome to fast API APP"


@app.get("/users")
async def get_users():
    return [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]



"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/prometheus_exp
$ uvicorn first_exp:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\prometheus_exp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [82804] using statreload
INFO:     Started server process [61856]
INFO:     Waiting for application startup.
INFO:     Application startup complete.





aafakmoh@WHDCIS4TDR MINGW64 /
$  pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 prometheus-fastapi-instrumentator
Collecting prometheus-fastapi-instrumentator
  Downloading prometheus_fastapi_instrumentator-5.7.1-py3-none-any.whl (16 kB)
Requirement already satisfied: fastapi<1.0.0,>=0.38.1 in c:\python3\lib\site-packages (from prometheus-fastapi-instrumentator) (0.68.1)
Collecting prometheus-client<1.0.0,>=0.8.0
  Downloading prometheus_client-0.14.1-py3-none-any.whl (59 kB)
Requirement already satisfied: pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2 in c:\python3\lib\site-packages (from fastapi<1.0.0,>=0.38.1->prometheus-fastapi-instrumentator) (1.8.2)
Requirement already satisfied: starlette==0.14.2 in c:\python3\lib\site-packages (from fastapi<1.0.0,>=0.38.1->prometheus-fastapi-instrumentator) (0.14.2)
Requirement already satisfied: typing-extensions>=3.7.4.3 in c:\python3\lib\site-packages (from pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2->fastapi<1.0.0,>=0.38.1->prometheus-fastapi-instrumentator) (3.10.0.2)
Requirement already satisfied: dataclasses>=0.6 in c:\python3\lib\site-packages (from pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2->fastapi<1.0.0,>=0.38.1->prometheus-fastapi-instrumentator) (0.8)
Installing collected packages: prometheus-client, prometheus-fastapi-instrumentator
Successfully installed prometheus-client-0.14.1 prometheus-fastapi-instrumentator-5.7.1

aafakmoh@WHDCIS4TDR MINGW64 /
$  pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 prometheus-client
Requirement already satisfied: prometheus-client in c:\python3\lib\site-packages (0.14.1)

aafakmoh@WHDCIS4TDR MINGW64 /



Browse http://localhost:8000/users
[{"id":1,"name":"user1"},{"id":2,"name":"user2"}]

Browse http://localhost:8000/matrics
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
# HELP starlette_requests_in_progress Total HTTP requests currently in progress
# TYPE starlette_requests_in_progress gauge
starlette_requests_in_progress{app_name="starlette",method="GET"} 1.0
# HELP starlette_requests_total Total HTTP requests
# TYPE starlette_requests_total counter
starlette_requests_total{app_name="starlette",method="GET",path="/",status_code="404"} 1.0
starlette_requests_total{app_name="starlette",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_requests_total{app_name="starlette",method="GET",path="/users",status_code="200"} 1.0
# HELP starlette_requests_created Total HTTP requests
# TYPE starlette_requests_created gauge
starlette_requests_created{app_name="starlette",method="GET",path="/",status_code="404"} 1.6529382820799663e+09
starlette_requests_created{app_name="starlette",method="GET",path="/favicon.ico",status_code="404"} 1.652938282486719e+09
starlette_requests_created{app_name="starlette",method="GET",path="/users",status_code="200"} 1.6529382864679575e+09
# HELP starlette_request_duration_seconds HTTP request duration, in seconds
# TYPE starlette_request_duration_seconds histogram
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.005",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.01",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.025",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.05",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.075",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.1",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.25",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.5",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.75",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="1.0",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="2.5",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="5.0",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="7.5",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="10.0",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="+Inf",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_count{app_name="starlette",method="GET",path="/",status_code="404"} 1.0
starlette_request_duration_seconds_sum{app_name="starlette",method="GET",path="/",status_code="404"} 0.0007684837306903312
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.005",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.01",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.025",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.05",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.075",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.1",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.25",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.5",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.75",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="1.0",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="2.5",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="5.0",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="7.5",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="10.0",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="+Inf",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_count{app_name="starlette",method="GET",path="/favicon.ico",status_code="404"} 1.0
starlette_request_duration_seconds_sum{app_name="starlette",method="GET",path="/favicon.ico",status_code="404"} 0.0009144229123545511
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.005",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.01",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.025",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.05",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.075",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.1",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.25",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.5",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="0.75",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="1.0",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="2.5",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="5.0",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="7.5",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="10.0",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_bucket{app_name="starlette",le="+Inf",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_count{app_name="starlette",method="GET",path="/users",status_code="200"} 1.0
starlette_request_duration_seconds_sum{app_name="starlette",method="GET",path="/users",status_code="200"} 0.0039064185603612245
# HELP starlette_request_duration_seconds_created HTTP request duration, in seconds
# TYPE starlette_request_duration_seconds_created gauge
starlette_request_duration_seconds_created{app_name="starlette",method="GET",path="/",status_code="404"} 1.6529382820799663e+09
starlette_request_duration_seconds_created{app_name="starlette",method="GET",path="/favicon.ico",status_code="404"} 1.652938282486719e+09
starlette_request_duration_seconds_created{app_name="starlette",method="GET",path="/users",status_code="200"} 1.6529382864679575e+09
"""