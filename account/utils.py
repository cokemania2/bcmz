import hashlib
from random import randint


def send_meesage():
    number = randint(1000, 10000)
    return number


def make_hash(data):
    data_hash = hashlib.new('sha256')
    data_hash.update(data.encode('utf-8'))
    return data_hash.hexdigest()
