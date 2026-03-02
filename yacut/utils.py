import random
import string
from .models import URLMap

CHARSET = string.ascii_letters + string.digits
MIN_LENGTH = 6
MAX_LENGTH = 10


def get_unique_short_id():
    while True:
        length = random.randint(MIN_LENGTH, MAX_LENGTH)
        short_id = ''.join(random.choices(CHARSET, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id