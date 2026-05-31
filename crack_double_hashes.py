import hashlib

hashes = {
    "U001": ("ผู้ดูแลระบบ", "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"),
    "U002": ("หัวหน้างาน", "4e6881d86eea85fa73a4c3bc4e6514eaba5c0417e6ad3ac61d5ed240366e578e"),
    "U003": ("วิทยา แพงศรี", "9980dd775dc6f0fcfefbeb099c64ede7555a46cc7ae3cfc4e4848c448989bde3"),
}

print("Running double-hash cracking...")
for i in range(10000):
    pin_str = f"{i:04d}"
    
    # Precompute hashes of pin
    md5_1 = hashlib.md5(pin_str.encode('utf-8')).hexdigest()
    sha1_1 = hashlib.sha1(pin_str.encode('utf-8')).hexdigest()
    sha256_1 = hashlib.sha256(pin_str.encode('utf-8')).hexdigest()
    
    # Double-hash candidates
    candidates = [
        # md5(md5)
        hashlib.md5(md5_1.encode('utf-8')).hexdigest(),
        # sha256(sha256)
        hashlib.sha256(sha256_1.encode('utf-8')).hexdigest(),
        # sha256(md5)
        hashlib.sha256(md5_1.encode('utf-8')).hexdigest(),
        # md5(sha256)
        hashlib.md5(sha256_1.encode('utf-8')).hexdigest(),
        # sha1(sha1)
        hashlib.sha1(sha1_1.encode('utf-8')).hexdigest(),
        # sha256(sha1)
        hashlib.sha256(sha1_1.encode('utf-8')).hexdigest(),
    ]
    
    for uid, (name, target_hash) in hashes.items():
        for c in candidates:
            if c == target_hash:
                print(f"MATCH! User: {name} ({uid}) -> PIN: {pin_str}")
                break

print("Finished double-hash cracking.")
