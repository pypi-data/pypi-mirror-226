import jsonschema

schema = {

    "type": "object",
    "additionalProperties": False,
    "required": ["database"],
    "properties": {
        "database": {
            "type": "object",
            "additionalProperties": False,
            "anyOf": [
                {
                    "required": ["sourceDatabaseId"]
                },
                {
                    "required": ["snapshotId"]
                }
            ],
            "dependencies": {
                "snapshotId": {"not": {"required": ["snapshotInfo"]}}
            },
            "properties": {
                "hostId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },

                "sourceDatabaseId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 255
                },
                "snapshotId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "snapshotInfo":{
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "description": {
                    "type": "string",
                    "minLength": 0,
                    "maxLength": 255
                }
            }

        }
    }
}


body1 = {
  "database": {

      "hostId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "sourceDatabaseId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      #"snapshotInfo": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "description": "Hello"

  }
}


body2 = {
   "database": {
       "sourceDatabaseId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "snapshotInfo": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "hostId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "description": "Hello"
   }
}

if __name__ == '__main__':
    try:
      jsonschema.validate(body1, schema)
    except jsonschema.exceptions.ValidationError as e:
        print (e.message)
        print (e.schema_path[1])
        print (e.validator)
        print( e.validator_value)
        print(type(e.validator_value))
        #required_value = e.validator_value['required'] if 'required' in e.validator_value else e.validator_value
        #print('{0} can not have element {1}'.format(e.path, required_value))
        #print(e.schema.get('required'))

    # jsonschema.validate(body2, schema)