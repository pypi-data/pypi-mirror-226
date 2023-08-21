from cryptography.fernet import Fernet

fernet = Fernet(Fernet.generate_key())

enc_msg = fernet.encrypt(b"Hello")
print(enc_msg)
dec_msg = fernet.decrypt(enc_msg)
print(dec_msg)



"""
C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/security_exp/farnet_exp.py:1: CryptographyDeprecationWarning:
  Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in
  cryptography and will be removed in a future release.
  from cryptography.fernet import Fernet
b'gAAAAABi-w8KIEiQLcQail3Re6GbdN81FBnRjbvtQqNKBmySXRlnJhAp9V3eN6r2s-mpZhfQOKaeC8ydFRw04vMr-vSzqj2qTA=='
b'Hello'

"""