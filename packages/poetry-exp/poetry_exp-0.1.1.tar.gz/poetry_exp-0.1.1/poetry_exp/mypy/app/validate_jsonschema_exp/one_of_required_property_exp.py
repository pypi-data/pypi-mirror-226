import jsonschema

schema = {

    "type": "object",
    "additionalProperties": False,
    "required": ["database"],
    "properties": {
        "database": {
            "type": "object",
            "additionalProperties": False,
            "oneOf": [
                {
                    "required": ["snapshotId"]
                },
                {
                    "required": ["snapshotInfo"]
                }
            ],
            "properties": {
                "snapshotId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "snapshotInfo":{
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
      "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc"
  }
}

body2 = {
  "database": {
      "snapshotInfo": "aad62763-855f-4ba9-b69e-228bd6f446dc"
  }
}
body3 = {
   "database": {

   }
}

body4 = {
   "database": {
       "snapshotInfo": "aad62763-855f-4ba9-b69e-228bd6f446dc",
       "snapshotId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
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
        if e.validator == 'oneOf':
            print('comes here')
            required_props = []
            validator_value = e.validator_value
            print('.........validator_value: {0}'.format(validator_value))
            if validator_value and isinstance(validator_value, list):
                for validator_val in validator_value:
                    if isinstance(validator_val, dict) and 'required' in validator_val:
                        required_props.extend(validator_val['required'])

        print("Only one property allowed from : {0}".format(required_props))
        print(e.validator_value)
