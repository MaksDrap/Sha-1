import struct

def pad_message(message):
    ml = len(message) * 8  # довжина повідомлення в бітах
    message += b'\x80'  # додати біт "1" після повідомлення

    # додати необхідну кількість нулів до завершення повідомлення
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # додати довжину повідомлення в бітах у вигляді 64-бітного цілого числа
    message += ml.to_bytes(8, 'big')

    return message

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(data):
    # ініціалізація початкових значень
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    padded_data = pad_message(data)
    block_size = 64

    # обробка повідомлення по блоках
    blocks = [padded_data[i:i+block_size] for i in range(0, len(padded_data), block_size)]

    # оновлення хеш-значення для кожного блоку
    for block in blocks:
        # Розбиття блоку на 16 слів
        words = [0] * 80
        for i in range(16):
            words[i] = struct.unpack('>I', block[i*4:i*4+4])[0]

        # розрахунок решти слів
        for i in range(16, 80):
            words[i] = left_rotate(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1)

        # ініціалізація змінних
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # основний цикл обчислення
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = left_rotate(a, 5) + f + e + k + words[j]
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp & 0xFFFFFFFF

        # оновлення хеш-значення
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # фінальне хеш-значення
    hash_value = struct.pack('>5I', h0, h1, h2, h3, h4)
    return hash_value

#тести
data1 = b'Short message'
data2 = b'A longer message that spans multiple blocks'
data3 = b'A message that is larger than a single block. It needs to be split into multiple blocks for hashing.'

hashed_data1 = sha1(data1)
hashed_data2 = sha1(data2)
hashed_data3 = sha1(data3)

print(hashed_data1.hex())
print(hashed_data2.hex())
print(hashed_data3.hex())
