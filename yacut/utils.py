import random
import string
from .models import URLMap

CHARSET = string.ascii_letters + string.digits
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    while True:
        short_id = ''.join(random.choices(CHARSET, k=SHORT_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id