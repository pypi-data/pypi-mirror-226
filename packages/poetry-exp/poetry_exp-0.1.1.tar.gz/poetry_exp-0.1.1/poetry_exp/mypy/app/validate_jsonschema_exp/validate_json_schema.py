from jsonschema import validate
import jsonschema
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
                  "type": "array"
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
      "credentialId": "credentialId1",
      "tags": ["tag1"]
    }
}

try:
 print(validate(body, schema))
except jsonschema.exceptions.ValidationError as e:
    print(e.message)
    # print(e.schema)
    # #
    # print(e.validator_value)
    # print(e.validator)
    print("Failed validation : {0}, Required: {1}".format(e.validator, e.validator_value))
    # print(e.path)
    #print(e.args)