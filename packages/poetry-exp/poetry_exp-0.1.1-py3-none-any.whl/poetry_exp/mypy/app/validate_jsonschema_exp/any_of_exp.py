import jsonschema

schema = {
    "oneOf": [
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["asset-group"],
            "properties": {
                "asset-group": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "name"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 36
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
                        }
                    }

                }

            }

        },
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["asset-group"],
            "properties": {
                "asset-group": {
                    "type": "object",
                    "required": ["hostId", "name"],
                    "additionalProperties": False,
                    "properties": {
                        "hostId": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 36
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
                        }
                    }

                }

            }
        }
    ]
}

body1 = {
  "asset-group": {
      "id": "aad62763-855f-4ba9-b69e-228bd6f446dc-aafak",
      "name": "",
      "description": "Hello"
  }
}

body2 = {
  "asset-group": {
      "hostId": "abc",
      "name": "name1",
      "description": "Hello"
  }
}

if __name__ == '__main__':
    validator = jsonschema.Draft7Validator(schema=schema)
    errors = validator.iter_errors(body1)
    for error in errors:
        print(error.message)
        # print(error.schema)
        # print(error.validator)
        # print(error.validator_value)
        # print(error.args)

    print("Validating body2")
    errors = validator.iter_errors(body2)
    for error in errors:
        print(error.message)