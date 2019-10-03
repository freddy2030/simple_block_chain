from hashlib import sha256
from ecdsa import SigningKey, NIST384p, VerifyingKey, SECP256k1
from binascii import hexlify, unhexlify
import hashlib

private = sha256("xiaohuang".encode()).hexdigest()

print(type(private))

sk = SigningKey.from_string(unhexlify(private), curve=SECP256k1)
vk = sk.get_verifying_key()

p = hexlify(vk.to_string()).decode()

obj = hashlib.new('ripemd160', p.encode('utf-8'))
ripemd_160_value = obj.hexdigest()
print(private)
print(hexlify(vk.to_string()).decode())
print(p)
print(ripemd_160_value)



signature = sk.sign("message".encode("utf-8"))
# assert vk.verify(signature, "messa1ge".encode("utf-8"))

assert 1>2

print("1")