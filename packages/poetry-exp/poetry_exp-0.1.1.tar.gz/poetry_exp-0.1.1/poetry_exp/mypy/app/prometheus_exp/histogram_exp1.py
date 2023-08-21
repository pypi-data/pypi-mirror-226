from prometheus_client import start_http_server, Histogram
import random
import time


SOME_MEASURE= Histogram('some_measure_seconds', 'Some measure I am trying to graph')

list=[1,2,3,4,5,6,7,8,9,10]


def register_histo(i):
    SOME_MEASURE.observe(i)
    time.sleep(5)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        for i in list:
            #print(i)
            register_histo(i)

"""
Browse: http://localhost:8000/
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 356.0
python_gc_objects_collected_total{generation="1"} 7.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 46.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="5",version="3.6.5"} 1.0
# HELP some_measure_seconds Some measure I am trying to graph
# TYPE some_measure_seconds histogram
some_measure_seconds_bucket{le="0.005"} 0.0
some_measure_seconds_bucket{le="0.01"} 0.0
some_measure_seconds_bucket{le="0.025"} 0.0
some_measure_seconds_bucket{le="0.05"} 0.0
some_measure_seconds_bucket{le="0.075"} 0.0
some_measure_seconds_bucket{le="0.1"} 0.0
some_measure_seconds_bucket{le="0.25"} 0.0
some_measure_seconds_bucket{le="0.5"} 0.0
some_measure_seconds_bucket{le="0.75"} 0.0
some_measure_seconds_bucket{le="1.0"} 42.0
some_measure_seconds_bucket{le="2.5"} 84.0
some_measure_seconds_bucket{le="5.0"} 210.0
some_measure_seconds_bucket{le="7.5"} 294.0
some_measure_seconds_bucket{le="10.0"} 418.0
some_measure_seconds_bucket{le="+Inf"} 418.0
some_measure_seconds_count 418.0
some_measure_seconds_sum 2291.0
# HELP some_measure_seconds_created Some measure I am trying to graph
# TYPE some_measure_seconds_created gauge
some_measure_seconds_created 1.6547670272163901e+09
"""