import base64
import os.path
from django.utils import timezone
import random
import string





def generate_random_string(size=5):
    return ''.join(random.choices(string.ascii_lowercase, k=size))


def text_to_base64(text):
    string_bytes = text.encode("utf-8")  
    base64_bytes = base64.b64encode(string_bytes)
    return base64_bytes.decode("utf-8")


def filename_to_base64_with_random_salt(filename, random_salt_size=5):
    # ex: foto.png => finelinitial=foto, ext=.png
    fileinitial, ext = os.path.splitext(filename)
    
    base64_filename = text_to_base64(text=fileinitial)
    random_salt = generate_random_string(size=random_salt_size)    
    
    return ''.join([base64_filename, random_salt, ext]) 


def base64_with_random_salt_to_filename(b64_filename, random_salt_size=5):
     
    fileinitial, ext = os.path.splitext(b64_filename)
        
    if len(fileinitial) > random_salt_size:
        try:
            file_with_no_random_salt = fileinitial[:-5] + '=='
            base64_bytes = file_with_no_random_salt.encode("utf-8")
            file_bytes = base64.b64decode(base64_bytes)
            fileinitial = file_bytes.decode("utf-8")
        except:
            ...
    
    return  "".join([fileinitial,ext])


def generate_uuid4_filename(instance, filename):
    return gera_estrutura_de_pastas_com_data() + filename_to_base64_with_random_salt(filename)