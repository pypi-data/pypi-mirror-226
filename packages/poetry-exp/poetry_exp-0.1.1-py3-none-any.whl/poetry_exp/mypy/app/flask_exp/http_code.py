from flask_api import status

print status.HTTP_200_OK
print status.HTTP_201_CREATED
print status.HTTP_202_ACCEPTED
print status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
print status.HTTP_204_NO_CONTENT


print status.HTTP_400_BAD_REQUEST  # Invalid input
print status.HTTP_401_UNAUTHORIZED
print status.HTTP_402_PAYMENT_REQUIRED
print status.HTTP_403_FORBIDDEN    # Does not have access/priveliges to do this action
print status.HTTP_404_NOT_FOUND
print status.HTTP_405_METHOD_NOT_ALLOWED
print status.HTTP_409_CONFLICT


print status.HTTP_500_INTERNAL_SERVER_ERROR
print status.HTTP_501_NOT_IMPLEMENTED
print status.HTTP_502_BAD_GATEWAY
print status.HTTP_503_SERVICE_UNAVAILABLE

