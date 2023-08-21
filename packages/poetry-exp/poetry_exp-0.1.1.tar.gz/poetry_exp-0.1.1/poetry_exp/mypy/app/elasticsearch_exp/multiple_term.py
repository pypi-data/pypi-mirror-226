query = {
  "query": {
    "bool": {
      "must": [

      ]
    }
  }
}


def create_term(key, value):
    term = {
        "term": {
            key + ".keyword": {
                "value": value
            }
        }
    }
    return term


if __name__ == '__main__':
    request = {
        'hostId': '123',
        'assetId': '456',
        'managed': True
    }

    for k, v in request.items():
        term = create_term(k, v)
        query['query']['bool']['must'].append(term)

    print(query)


