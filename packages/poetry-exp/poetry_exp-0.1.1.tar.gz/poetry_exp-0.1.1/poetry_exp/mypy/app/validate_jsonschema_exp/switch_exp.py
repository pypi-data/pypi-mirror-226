import jsonschema

schema = {

    "type": "object",
    "additionalProperties": False,
    "required": ["asset-group"],
    "properties": {
        "asset-group": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "hostId": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 36
                },
                "sqlInstance": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 255,
                            "oneOf": [
                                {"pattern": "^[a-zA-Z0-9-_]+$"},
                                {"pattern": "^[a-zA-Z0-9-_]+\\\\[a-zA-Z0-9-_]+$"}
                            ]
                        },
                    }
                },
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 255
                },
                "description": {
                    "type": "string",
                    "minLength": 0,
                    "maxLength": 255
                },
                "assets":{
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "name"]
                    },
                    "properties": {
                        "id": {
                            "type": "string",
                            "minLength": 36,
                            "maxLength": 36
                        },
                        "name": {
                           "enum": ["Database", "VirtualMachine", "Datastore", "VolumeSet", "FileSystem", "AssetGroup"]
                        }
                    }
                }
            },
            "switch": [
                {
                    "if": {
                        "properties": {"sqlInstance": {"constants": "boolean"}}
                    },
                    "then": {
                        "required": ["hostId"]
                    }
                },
                {
                    "if": {
                        "properties": {"assets": {"constants": "boolean"}}
                    },
                    "then": {
                        "required": ["name"]
                    }
                },
            ]


        }

    }


}

body1 = {
  "asset-group": {
      "sqlInstance": {
        "name": "mssql"
      },
      "hostId": "aad62763-855f-4ba9-b69e-228bd6f446dc",
      "description": "Hello",

  }
}


body2 = {
  "asset-group": {
     "name": "name1",
     "description": "Hello",
     "assets": [
          {
              "id": "aad62763-855f-4ba9-b69e-228bd6f446dc",
              "name": "Datastore1"
          }
      ]
  }
}

if __name__ == '__main__':
    validator = jsonschema.Draft7Validator(schema=schema)
    errors = validator.iter_errors(body1)
    for error in errors:
        print(error.message)

    print("Validating body2")
    errors = validator.iter_errors(body2)
    for error in errors:
        print(error.message)