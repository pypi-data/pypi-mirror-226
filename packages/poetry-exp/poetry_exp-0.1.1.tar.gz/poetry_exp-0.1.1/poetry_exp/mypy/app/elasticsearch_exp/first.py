from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200/'])
doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }
res = es.search(index='', body=doc,scroll='1m')
