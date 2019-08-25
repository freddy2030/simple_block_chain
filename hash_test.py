# -*- coding: utf-8 -*-

from hashlib import sha256


x = 98323
y = 0  # y unknown

while True:
    h=sha256(str(x * y).encode()).hexdigest()
    print(y,h)
    if h[0] == '0' and h[1] == "0" :
        break
    y += 1

