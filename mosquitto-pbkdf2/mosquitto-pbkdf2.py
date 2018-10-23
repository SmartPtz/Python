import hashlib
from base64 import b64encode, b64decode

def verify(password, pbkf2):
    """Verify username functions, for mosquitto-auth-plug password hash, stored as PBKDF2 format"""
    if isinstance(password, str) and  isinstance(pbkf2, str):
            pbkf, sha, iter, salt, h_pw = (pbkf2.split('$'))
            keylen = len(b64decode(h_pw))
            saltlen = len(salt)
            password=password.encode()
            salt=salt.encode()
            h_pw=h_pw.encode()
            dk = hashlib.pbkdf2_hmac(sha, password, salt, int(iter), int(keylen))
            blen = b64encode(dk)
            if h_pw == blen:
                return True
            else:
                return False

    else:
        print("password and pbkf2 - must be a string object !")
        return False
