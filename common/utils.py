import hashlib

MAX_INT = 2**32

def hash_for_identification(info):
    return int(hashlib.md5(info.encode()).hexdigest(), 16) % MAX_INT