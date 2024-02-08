import os
import base64

SECRET_KEY = base64.b64encode(os.urandom(60)).decode() #creates secret key
