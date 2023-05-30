import hashlib

# Повідомлення, яке складається з одного блока
message1 = b'Short message'
hash1 = hashlib.sha1(message1).hexdigest()
print(hash1)

# Повідомлення, яке складається з більше одного блока
message2 = b'A longer message that spans multiple blocks'
hash2 = hashlib.sha1(message2).hexdigest()
print(hash2)

# Повідомлення, яке складається з декількох блоків
message3 = b'A message that is larger than a single block. It needs to be split into multiple blocks for hashing.'
hash3 = hashlib.sha1(message3).hexdigest()
print(hash3)
