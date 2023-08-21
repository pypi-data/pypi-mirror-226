PASSWD = "pbkdf2:sha256:50000$5bfhfZO5$24bc7a0698b251eb97d00f9be770cea79f9680d4662c23d766d0a9fc0ea0ea4b"

password = 'Password123!'
from werkzeug.security import generate_password_hash, check_password_hash
password_hash = generate_password_hash(password)  # everytime generates new hash for same password, so you store it in DB after generating
print password_hash
result = check_password_hash(password_hash, password) # But it will return True

print result

#print password_hash==PASSWD
