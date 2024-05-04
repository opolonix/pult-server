from sqlalchemy import create_engine, Column, Boolean, String, Integer, DateTime, BigInteger, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Session, relationship


import random, string, hashlib, datetime
from tools import alchemy

engine = alchemy.sclite_engine("/db/pult.db")
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

def generate_id() -> str:
    while True:
        date = datetime.datetime.now()
        date = ''.join(str(i)[-2:].rjust(2, '0') for i in [date.year, date.month, date.day])

        secret = ''.join(random.choice(string.digits) for i in range(random.randint(3,4)))

        hash_object = hashlib.sha256()
        hash_object.update(secret.encode())
        hex_hash = hash_object.hexdigest()

        value = str(int(hex_hash[:32], 16))

        additions = [int(value[i:i+3]) for i in range(0, len(value), 3) if len(value[i:i+3]) == 3]
        result = ''.join(str(encrypt(int(a), additions[i])) for i, a in enumerate(date))

        if not session.query(User).filter(User.public_id == result + secret).first():
            return result + secret


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    username = Column(String, default=None, unique=True, index=True)
    name = Column(String, nullable=False)
    public_id = Column(BigInteger, default=generate_id, unique=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.now)
    blocked = Column(Boolean, default=False)

class Auth(Base):
    __tablename__ = 'auth'

    user_id = Column(Integer, ForeignKey('user.id'))
    hash = Column(Text, nullable=False, primary_key=True)


class Session(Base):
    __tablename__ = 'session'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    token = Column(String, unique=True, index=True)
    user = Column(Integer, ForeignKey('user.id'))

    init = Column(DateTime, default=datetime.datetime.now)

def encrypt(number, key):
    encrypted_number = number + key
    return encrypted_number % 10  # Получаем остаток от деления на 10

def decrypt(number, key):
    decrypted_number = number - key
    return decrypted_number % 10  # Получаем остаток от деления на 10


# превращает закодированный юзер айди в обьект даты создания пользователя
# def get_user_date(user_id) -> datetime.date:

#     date = user_id[:6]
#     secret = user_id[6:]

#     hash_object = hashlib.sha256()
#     hash_object.update(secret.encode())
#     hex_hash = hash_object.hexdigest()

#     value = str(int(hex_hash[:32], 16))

#     additions = [int(value[i:i+3]) for i in range(0, len(value), 3) if len(value[i:i+3]) == 3]
#     date = ''.join(str(decrypt(int(a), additions[i])) for i, a in enumerate(date))
    
#     return datetime.date(year=int('20' + date[:2]), month=int(date[2:4]), day=int(date[4:6]))
