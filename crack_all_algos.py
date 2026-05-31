import hashlib

hashes = {
    "admin": "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42",
    "supervisor": "4e6881d86eea85fa73a4c3bc4e6514eaba5c0417e6ad3ac61d5ed240366e578e",
}

print("Cracking with multiple algorithms...")
for i in range(10000):
    pin_str = f"{i:04d}"
    
    # MD5
    h_md5 = hashlib.md5(pin_str.encode('utf-8')).hexdigest()
    # SHA-1
    h_sha1 = hashlib.sha1(pin_str.encode('utf-8')).hexdigest()
    # SHA-256
    h_sha256 = hashlib.sha256(pin_str.encode('utf-8')).hexdigest()
    # SHA-512
    h_sha512 = hashlib.sha512(pin_str.encode('utf-8')).hexdigest()
    
    for user, user_hash in list(hashes.items()):
        if h_md5 == user_hash:
            print(f"MATCH (MD5)! User: {user} -> PIN: {pin_str}")
            del hashes[user]
        elif h_sha1 == user_hash:
            print(f"MATCH (SHA-1)! User: {user} -> PIN: {pin_str}")
            del hashes[user]
        elif h_sha256 == user_hash:
            print(f"MATCH (SHA-256)! User: {user} -> PIN: {pin_str}")
            del hashes[user]
        elif h_sha512 == user_hash:
            print(f"MATCH (SHA-512)! User: {user} -> PIN: {pin_str}")
            del hashes[user]

print("Cracking finished!")
