import hashlib

hashes = {
    "U001": ("ผู้ดูแลระบบ", "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"),
    "U002": ("หัวหน้างาน", "4e6881d86eea85fa73a4c3bc4e6514eaba5c0417e6ad3ac61d5ed240366e578e"),
    "U003": ("วิทยา แพงศรี", "9980dd775dc6f0fcfefbeb099c64ede7555a46cc7ae3cfc4e4848c448989bde3"),
}

print("Running deep brute-force...")
for i in range(10000):
    pin_str = f"{i:04d}"
    
    for uid, (name, target_hash) in hashes.items():
        # List of candidate strings to hash
        candidates = [
            pin_str,
            f"{uid}_{pin_str}",
            f"{pin_str}_{uid}",
            f"{uid}:{pin_str}",
            f"{pin_str}:{uid}",
            f"{uid}-{pin_str}",
            f"{pin_str}-{uid}",
            f"{name}_{pin_str}",
            f"{pin_str}_{name}",
            f"{name}:{pin_str}",
            f"{pin_str}:{name}",
            f"{name}-{pin_str}",
            f"{pin_str}-{name}",
            # Maybe it uses lower case uid
            f"{uid.lower()}_{pin_str}",
            f"{pin_str}_{uid.lower()}",
            f"{uid.lower()}:{pin_str}",
            f"{pin_str}:{uid.lower()}",
        ]
        
        for c in candidates:
            # SHA-256
            h = hashlib.sha256(c.encode('utf-8')).hexdigest()
            if h == target_hash:
                print(f"MATCH SHA-256! User: {name} ({uid}) -> PIN: {pin_str} (combo: '{c}')")
                break
                
            # MD5
            h_md5 = hashlib.md5(c.encode('utf-8')).hexdigest()
            if h_md5 == target_hash:
                print(f"MATCH MD5! User: {name} ({uid}) -> PIN: {pin_str} (combo: '{c}')")
                break

print("Finished deep brute-force.")
