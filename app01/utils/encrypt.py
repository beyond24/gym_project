from  django.conf import settings
import hashlib

def md5(data_string):
    # django项目自动生成的KEY做盐
    salt = settings.SECRET_KEY.encode('utf-8')
    obj = hashlib.md5(salt)
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()