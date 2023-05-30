import hashlib

def add_message(message):
    # Доповнення починається з біту "1", за яким слідує додаткові нулі і довжина повідомлення i завершується таким чином, щоб довжина повідомлення було кратним 512
    original_length = len(message) * 8
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += original_length.to_bytes(8, 'big')
    return message

def hash_function(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    hash_value = sha1_hash.digest()
    return hash_value

def sha1(data):
    hashed_data = b''
    padded_data = add_message(data)
    block_size = 64
    for i in range(0, len(padded_data), block_size):
        block = padded_data[i:i+block_size]
        hashed_block = hash_function(block)
        hashed_data += hashed_block
    return hashed_data

# Тести
data = b'This is a test message'
hashed_data = sha1(data)
print(hashed_data.hex())

data1 = b'Short message'
hashed_data1 = sha1(data1)
print(f"Message 1: {hashed_data1.hex()}")

data2 = b'A longer message that spans multiple blocks'
hashed_data2 = sha1(data2)
print(f"Message 2: {hashed_data2.hex()}")

data3 = b'A message that is larger than a single block. It needs to be split into multiple blocks for hashing.'
hashed_data3 = sha1(data3)
print(f"Message 3: {hashed_data3.hex()}")


