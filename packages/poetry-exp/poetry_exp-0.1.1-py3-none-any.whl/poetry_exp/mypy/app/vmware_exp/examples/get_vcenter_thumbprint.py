import OpenSSL
import ssl
# vCenter
vc_cert = ssl.get_server_certificate(("172.17.29.162", int(443)))
vc_pem = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                         vc_cert)
print(vc_pem)
print(vc_pem.digest('sha1'))  # A7:2D:E9:30:46:0E:BD:B3:79:C1:C8:74:2A:45:DA:5F:C0:F1:9D:23



# ESX
import OpenSSL
import ssl
esx_cert = ssl.get_server_certificate(("172.17.6.221", int(443)))
esx_pem = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                         esx_cert)
print(esx_pem)
print(esx_pem.digest('sha1'))  # b'5C:35:11:16:4F:18:07:71:19:FE:21:4B:13:40:BF:D3:6A:65:C9:60'

