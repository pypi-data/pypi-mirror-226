# http://docs.python-cerberus.org/en/stable/

from cerberus import Validator

schema = {
    "name": {'type': 'string'}
}

v = Validator(schema)

# Doc/inputs to validate
document = {'name': 'Aman'}

print v.validate(document)  # True

document = {'name': 123}
'''
Unlike other validation tools, Cerberus will not halt and
raise an exception on the first validation issue. The whole document will always be processed,
and False will be returned if validation failed. You can then access the errors property
to obtain a list of issues
'''
print v.validate(document)  # False
print v.errors

schema2 = {'name': {'type': 'string'}}
doc2 = {'name': 'Aman'}
# can pass both the dictionary and the schema to the validate() method
# if your schema is changing through the life of the instance.
print v.validate(doc2, schema2)
