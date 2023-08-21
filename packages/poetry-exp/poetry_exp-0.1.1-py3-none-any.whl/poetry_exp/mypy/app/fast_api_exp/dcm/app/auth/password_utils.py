from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    print(f'plain_password: {plain_password}, hashed_password:{hashed_password}')
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == '__main__':
    psw = 'test'
    hashed_psw = get_password_hash(psw)
    print(verify_password(psw, hashed_psw))
