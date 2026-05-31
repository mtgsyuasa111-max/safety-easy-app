import hashlib

hashes = {
    "U001": ("ผู้ดูแลระบบ", "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42"),
    "U002": ("หัวหน้างาน", "4e6881d86eea85fa73a4c3bc4e6514eaba5c0417e6ad3ac61d5ed240366e578e"),
    "U003": ("วิทยา แพงศรี", "9980dd775dc6f0fcfefbeb099c64ede7555a46cc7ae3cfc4e4848c448989bde3"),
}

print("Trying various hashing combinations...")
for i in range(10000):
    pin_str = f"{i:04d}"
    
    # Check simple algorithms
    for uid, (name, target_hash) in hashes.items():
        # Combinations:
        # 1. raw PIN
        # 2. uid + pin
        # 3. name + pin
        # 4. pin + uid
        # 5. pin + name
        combos = [
            pin_str,
            f"{uid}{pin_str}",
            f"{name}{pin_str}",
            f"{pin_str}{uid}",
            f"{pin_str}{name}"
        ]
        for combo in combos:
            h = hashlib.sha256(combo.encode('utf-8')).hexdigest()
            if h == target_hash:
                print(f"MATCH! User: {name} ({uid}) -> PIN: {pin_str} (combo: '{combo}')")
                break
print("Finished complex cracking.")
