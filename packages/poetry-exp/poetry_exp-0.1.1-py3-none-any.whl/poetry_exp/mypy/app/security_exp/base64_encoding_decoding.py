"""
Base64 encoding is the process of converting binary data into a limited character set of 64 characters.
those characters are A-Z, a-z, 0-9, +, and / (count them, did you notice they add up to 64?).
 This character set is considered the most common character set, and is referred to as MIMEs Base64.
It uses A-Z, a-z, 0-9, +, and / for the first 62 values, and +, and / for the last two values.

The Base64 encoded data ends up being longer than the original data,
so that as mentioned above, for every 3 bytes of binary data,
there are at least 4 bytes of Base64 encoded data.
This is due to the fact that we are squeezing the data into a smaller set of characters.
"""


import base64

es = base64.b64encode('admin:Password123!')  # or  base64.b64encode(b'admin:Password123!')
print str(es) # YWRtaW46UGFzc3dvcmQxMjMh   Will always return the same as many times you run it

ds = base64.b64decode(es)
print ds # admin:Password123!
