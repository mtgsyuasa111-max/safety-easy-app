import hashlib

hashes = {
    "admin": "4efba02990e4356fb31c65e1637a7162ccc4449870a4c26ccab052ffecae9d42",
    "supervisor": "4e6881d86eea85fa73a4c3bc4e6514eaba5c0417e6ad3ac61d5ed240366e578e",
    "วิทยา แพงศรี": "9980dd775dc6f0fcfefbeb099c64ede7555a46cc7ae3cfc4e4848c448989bde3",
    "ศิริชัย แสงวงค์": "e75d29f6840afb299cbaa0880757f868244fd606b5651e5fc6a81f79df6fbe71",
    "สนธยา วงค์สีทธิไช": "34f8a3035f6713a0988cbea498c344180e04cc96b2cd8e31be926b7ad8ab8219",
    "อุดมชัย ทศรักษา": "281b0a0a7109ed3f91bb442f796b0cac0ded5041b2f7acd4da961ac34fee0f02",
    "สุทิน รอดยิ้ม": "3ceaf06b84c8ad95239d4f20b9f4f7e7d95f1977c52f4f513958997585a7c3e9",
    "ภิพัทยา แพทพีพัฒน์": "e637e9aa21ae4783132da67161856299c26cb6adfc70ca391735ce56a381cc06",
    "พิพัฒน์พล ทอยสังข์": "c86fabb42f58aa38a815f2c08380ef4e7d280fc3b5811a06255a2611a902a788",
    "สมชาย วงษา": "ae3d04fe8a9dd70503bfa2c5eeb5113577baece660d86e39a1204f871ad52c18",
    "ณัฐพงษ์ ยะล้อม": "98163ea8a1d9967d2c46c6ab720d896bbadcd0c1bde1bcc8d4bc1b49528764a8",
    "วันชนะ แพงศรี": "e1b63e6ba5d1527dea614c06bfbaca79d1aa85f6bd1b1ad717e7200c29a37022"
}

print("Cracking PINs...")
for i in range(10000):
    pin_str = f"{i:04d}"
    # Compute SHA-256 hash
    h = hashlib.sha256(pin_str.encode('utf-8')).hexdigest()
    # Match against hashes
    for user, user_hash in list(hashes.items()):
        if h == user_hash:
            print(f"MATCH! User: {user} -> PIN: {pin_str}")
            del hashes[user]

if len(hashes) > 0:
    print("\nSome hashes could not be cracked. Checking if they are 6 digits...")
    for i in range(1000000):
        pin_str = f"{i:06d}"
        h = hashlib.sha256(pin_str.encode('utf-8')).hexdigest()
        for user, user_hash in list(hashes.items()):
            if h == user_hash:
                print(f"MATCH (6-digit)! User: {user} -> PIN: {pin_str}")
                del hashes[user]

print("Cracking finished!")
