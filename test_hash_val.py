import hashlib

print("Calculating hashes...")
hash_0559 = hashlib.sha256(b"0559").hexdigest()
hash_1234 = hashlib.sha256(b"1234").hexdigest()

print("SHA-256 of 0559:", hash_0559)
print("SHA-256 of 1234:", hash_1234)

assert hash_0559 == "b00a470427c0ce586228d48f27b4dd5a8fee0276aecbf5afd2e08045da16b0d6", "Hash of 0559 is incorrect!"
assert hash_1234 == "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", "Hash of 1234 is incorrect!"
print("All hashes verified successfully!")
