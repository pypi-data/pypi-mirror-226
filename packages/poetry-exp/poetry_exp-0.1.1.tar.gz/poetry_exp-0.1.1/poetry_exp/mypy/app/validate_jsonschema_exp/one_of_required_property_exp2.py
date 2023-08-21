import jsonschema

schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["database"],
    "properties": {
        "database": {
            "type": "object",
            "additionalProperties": False,
            "anyOf": [  # oneOf can't be used here because third case matching all the property
                {
                    "required": ['sourceDatabaseId', 'appInfo']
                },
                {
                    "required": ['snapshotId', 'appInfo']
                },
                {
                    "required": ['snapshotId', 'sourceDatabaseId', 'appInfo']
                }
            ],
            "properties": {
                "snapshotId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "sourceDatabaseId":{
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "appInfo": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                }
            }
        }
    }
}


body1 = {
  "database": {
      "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "appInfo": "appinfo"
  }
}

body2 = {
  "database": {
      "sourceDatabaseId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "appInfo": "appINfo"
  }
}

body3 = {
   "database": {
       "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "sourceDatabaseId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "appInfo": "appInfo"
   }
}

body4 = {
   "database": {

   }
}


if __name__ == '__main__':
    try:
      jsonschema.validate(body3, schema)
    except jsonschema.exceptions.ValidationError as e:
       # print(e.message)
       # print(e.schema_path[1])
        print(e.__dict__)
        print('.........validator: {0}'.format(e.validator))

        required_props = []
        if e.validator == 'anyOf':
            print('comes here')
            required_props = []
            validator_value = e.validator_value
            print('.........validator_value: {0}'.format(validator_value))
            if validator_value and isinstance(validator_value, list):
                for validator_val in validator_value:
                    if isinstance(validator_val, dict) and 'required' in validator_val:
                        required_props.append(validator_val['required'])

            print("Any one set of properties required from : {0}".format(required_props))


# Following case will not work with oneOf, because it is having all the combinations
'''
body3 = {
   "database": {
       "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "sourceDatabaseId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "appInfo": "appInfo"
   }
}

{'message': "{'snapshotId': 'aad62763-855f-4ba9-b69e-228bd6f446dc',
 'sourceDatabaseId': 'aad62763-855f-4ba9-b69e-228bd6f446dc', 'appInfo': 'appInfo'}
  is valid under each of {'required': ['snapshotId', 'appInfo']},
{'required': ['snapshotId', 'sourceDatabaseId', 'appInfo']},
{'required': ['sourceDatabaseId', 'appInfo']}",
 'path': deque(['database']), 'relative_path': deque(['database']),
  'schema_path': deque(['properties', 'database', 'oneOf']),
   'relative_schema_path': deque(['properties', 'database', 'oneOf']),
    'context': [], 'cause': None, 'validator': 'oneOf',
     'validator_value': [{'required': ['sourceDatabaseId', 'appInfo']},
      {'required': ['snapshotId', 'appInfo']}, {'required': ['snapshotId',
       'sourceDatabaseId', 'appInfo']}], 'instance': {'snapshotId':
        'aad62763-855f-4ba9-b69e-228bd6f446dc', 'sourceDatabaseId':
         'aad62763-855f-4ba9-b69e-228bd6f446dc', 'appInfo': 'appInfo'},
          'schema': {'type': 'object', 'additionalProperties': False,
           'oneOf': [{'required': ['sourceDatabaseId', 'appInfo']},
            {'required': ['snapshotId', 'appInfo']}, {'required':
             ['snapshotId', 'sourceDatabaseId', 'appInfo']}],
              'properties': {'snapshotId': {'type': 'string', 'minLength': 1, 'maxLength': 36},
               'sourceDatabaseId': {'type': 'string', 'minLength': 1, 'maxLength': 36},
                'appInfo': {'type': 'string', 'minLength': 1, 'maxLength': 36}}},
                 'parent': None}

'''
