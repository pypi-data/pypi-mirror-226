from jsonschema import validate
import jsonschema
from validate_jsonschema_exp import error_messages as errors
import json

schema ={
      "type":"object",
      "required":["asset-group"],
      "properties":{
         "asset-group":{
            "type":"object",
            "required":[
               "name",
               "hosts",
               "description",
               "credentialId",
               "tags"
            ],
            "properties":{
                "additionalProperties": False,
               "name":{
                  "type":"string",
                   "minLength": 5,
                   "maxLength":10
               },
               "hosts":{
                  "type":"array"
               },
               "description":{
                  "type":"string"
               },
               "credentialId":{
                  "type":"string"
               },
               "tags":{
                  "type": "array",
                   "uniqueItems": True
               }
            }
         }
      }
   }

body = {
    "asset-group": {
      "name": "ag123433463565",
      "hosts": '["abc", "def"]',
      "description": "description1",
      "credentialId1": "credentialId1",
      "tags": ["tag1", "tag1"],
      "additionalProperty": "add1"
    }
}

schema2 ={
      "type":"object",
      "required":["asset-group"],
      "properties":{
         "asset-group":{
            "type":"object",
            "minProperties": 1,
            "properties":{
               "additionalProperties": False,
               "name":{
                  "type":"string",
                   "minLength": 5,
                   "maxLength":10
               },
               "hosts":{
                  "type":"array"
               },
               "description":{
                  "type":"string"
               },
               "credentialId":{
                  "type":"string"
               },
               "tags":{
                  "type": "array",
                   "uniqueItems": True
               }
            }
         }
      }
   }

body2 = {
    "asset-group": {
        "Hi": "Hello"
    }
}


def _(msg_key, *args):
    return msg_key.format(*args)


def get_error_message(err_obj):
    err_messages = {
        "required": _(
            errors.REQUEST_MISSING_REQUIRED_ELEMENTS,
            err_obj.validator_value
        ),
        "additionalProperties": _(
            errors.REQUEST_INVALID_ELEMENTS,
            err_obj.message
        ),
        "oneOf": _(
            errors.REQUEST_INVALID_ELEMENTS_ONEOF,
            "/".join(map(str, err_obj.path)),
            ", ".join([str(ctx.message) for ctx in err_obj.context])
        ),
        "enum": _(
            errors.REQUEST_NOT_ALLOWED_VALUE,
            "/".join(map(str, err_obj.path)),
            err_obj.validator_value
        ),
        "type": _(
            errors.REQUEST_INVALID_VALUE_TYPE,
            "/".join(map(str, err_obj.path)),
            err_obj.validator_value
        ),
        "minLength": _(
            errors.REQUEST_STRING_MIN_LENGTH,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('minLength')
        ),
        "maxLength": _(
            errors.REQUEST_STRING_MAX_LENGTH,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('maxLength')
        ),
        "minimum": _(
            errors.REQUEST_INTEGER_MIN_LENGTH,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('minimum')
        ),
        "maximum": _(
            errors.REQUEST_INTEGER_MAX_LENGTH,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('maximum')
        ),
        "maxItems": _(
            errors.REQUEST_ARRAY_MAX_ITEMS,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('maxItems')
        ),
        "minItems": _(
            errors.REQUEST_ARRAY_MIN_ITEMS,
            "/".join(map(str, err_obj.path)),
            err_obj.schema.get('minItems')
        ),
        "uniqueItems": _(
            errors.REQUEST_ARRAY_UNIQUE_ITMES,
            "/".join(map(str, err_obj.path))
        ),
        "minProperties": _(
            errors.REQUEST_MIN_ONE_PROP,
            "/".join(map(str, err_obj.path))
        )  # Keep adding here if found more cases
    }
    error_message = err_messages.get(err_obj.validator)
    if error_message is None:
        error_message = _(
            errors.REQUEST_UNKNOWN_VALIDATION_ERROR,
            err_obj.validator, "/".join(map(str, err_obj.path)),
            err_obj.validator_value
        )
    return error_message


def validate_body(body, schema):
    error_messages = []
    validator = jsonschema.Draft7Validator(schema)
    validation_errors = validator.iter_errors(body)
    for validation_error in validation_errors:
        message = get_error_message(validation_error)
        error_messages.append(message)

    if error_messages:
         for error_message in error_messages:
            print(error_message)
        #raise Exception(json.dumps(error_messages))


if __name__ == '__main__':
    #validate_body(body, schema)
    validate_body(body2, schema2)