from cerberus import Validator

# By default only keys defined in the schema are allowed:
schema = {'name': {'type': 'string', 'maxlength': 10}}
v = Validator()
doc = {'name': 'john', 'sex': 'M'}  # unknown field sex
print v.validate(doc, schema)   # False
print v.errors   # {'sex': ['unknown field']}


# Allow unknown
v.allow_unknown = True
print v.validate(doc, schema)   # True

# Allow specific fields only
v.allow_unknown = {'type': 'string'}
doc = {'name': 'john', 'age': 123}  # unknown field age of type int
print v.validate(doc, schema)   # False
print v.errors # {'age': ['must be of string type']}

doc = {'name': 'john', 'age': '123'}  # unknown field age of type str
print v.validate(doc, schema)   # True

# allow_unknown can also be set at initialization:
v = Validator(allow_unknown=True)
doc = {'name': 'john', 'age': '123'}  # unknown field age of type str
print v.validate(doc, schema)   # True


# allow_unknown can also be set as rule to configure a
# validator for a nested mapping that is checked against the schema rule:
v = Validator() # Default allow_unknown is False
schema = {
   'name': {'type': 'string'},
   'a_dict': {
    'type': 'dict',
    'allow_unknown': True,  # this overrides the behaviour(Global schema) for
    'schema': {             # the validation of this definition
       'address': {'type': 'string'}
    }
   }
 }

doc = {'name': 'john',
       'a_dict': {'an_unknown_field': 'is allowed'}
      }
print v.validate(doc, schema) # True, By default all keys in a document are optional unless the required-rule is set for a key.

doc = {'name': 'john',
       'a_dict': {'an_unknown_field': 'is allowed', 'address': 123}
      }
print v.validate(doc, schema)  # False
print v.errors # {'a_dict': [{'address': ['must be of string type']}]}

doc = {'name': 'john',
       'a_dict': {'an_unknown_field': 'is allowed', 'address': 'abc'}
      }
print v.validate(doc, schema)  # True

# this fails as allow_unknown is still False for the parent document.
doc = {'name': 'john',
       'an_unknown_field': 'is not allowed',
       'a_dict':{'an_unknown_field': 'is allowed'}
      }
print v.validate(doc, schema)  # False