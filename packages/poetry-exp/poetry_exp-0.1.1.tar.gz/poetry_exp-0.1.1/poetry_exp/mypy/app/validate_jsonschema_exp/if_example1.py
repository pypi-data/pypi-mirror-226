import jsonschema

schema = {

    "type": "object",
    "additionalProperties": False,
    "required": ["database"],
    "properties": {
        "database": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["Snapshot", "RemoteSnapshot"]
                },
                "replicationInfo":{
                    "type": "string",
                    "minLength": 1,
                },
                "description": {
                    "type": "string",
                    "minLength": 0,
                    "maxLength": 255
                }
            },
            "if": {
                "properties": {
                    "type": {
                        "enum": ['Snapshot']
                    }
                }
            },
            "then": {
                "not": {
                    "required": ['replicationInfo']
                }
            },
            "else": {
                "required": ['replicationInfo']
            }

        }
    }
}


body1 = {
  "database": {
      "type": "Snapshot",
      "description": "Local snapshot"
  }
}

body2 = {
  "database": {
      "type": "RemoteSnapshot",
      "description": "Local snapshot",
      "replicationInfo": "replinfo"
  }
}

# -ve case
body3 = {
  "database": {
      "type": "Snapshot",
      "description": "Local snapshot",
      "replicationInfo": "replinfo"
  }
}


body4 = {
  "database": {
      "type": "RemoteSnapshot",
      "description": "Local snapshot",
  }
}

if __name__ == '__main__':
    try:
      jsonschema.validate(body4, schema)
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