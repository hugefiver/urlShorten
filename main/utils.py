from .models import LinkURL
import datetime
import hashlib

# BASE_HOST = 'http://127.0.0.1:8000/'

BASE_CODE_LEN = 4
random_seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def clean_out_time_urls():
    now = datetime.datetime.now()
    LinkURL.objects.filter(end_time__lte=now).delete()


def get_md5(string: str):
    o = hashlib.md5()
    o.update(string.encode('utf-8'))
    return o.hexdigest().upper()
