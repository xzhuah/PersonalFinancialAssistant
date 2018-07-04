from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import pickle
import io
from Crypto import Random

def decrypt_obj(key, filename):
    chunksize = 64 * 1024
    out=b""
    with open(filename,"rb") as infile:
        secret = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key,AES.MODE_CBC,IV)
        while True:
            chunk = infile.read(chunksize)
            if len(chunk)==0:
                break
            out+=decryptor.decrypt(chunk)
    result = pickle.loads(out)
    return result

def obj2Bytes(obj):
    return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
def bytes2Obj(bytestream):
    return pickle.loads(bytestream)

def decrypt_obj_b(key, bytestream):
    chunksize = 64 * 1024
    out=b""
    infile = io.BytesIO(bytestream)
    IV = infile.read(16)
    decryptor = AES.new(key,AES.MODE_CBC,IV)
    while True:
        chunk = infile.read(chunksize)
        if len(chunk)==0:
            break
        out+=decryptor.decrypt(chunk)
    infile.close()
    return out

def encrypt_obj_b(key,picklyobj):
    result = b""
    chunksize = 64 * 1024
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    infile = io.BytesIO(picklyobj)
    result+=IV
    while True:
        chuck = infile.read(chunksize)
        if len(chuck) == 0:
            break
        elif len(chuck) % 16 != 0:
            chuck += b' ' * (16 - len(chuck) % 16)
        result+=encryptor.encrypt(chuck)
    infile.close()
    return result

def getKey(password):
    hasher=SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def e_obj(password,obj):
    return encrypt_obj_b(getKey(password), obj2Bytes(obj))
def d_obj(password,encode):
    return bytes2Obj(decrypt_obj_b(getKey(password), encode))

if __name__=="__main__":
    key = "123"
    testObj = {"name":"value"}
    a = e_obj(key,testObj)
    b = d_obj(key,a)
    print(a,b)