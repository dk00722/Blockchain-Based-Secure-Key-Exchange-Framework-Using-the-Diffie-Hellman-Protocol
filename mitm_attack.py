"""
SUCCESSFUL MITM ATTACK DEMO (ACADEMIC SIMULATION)
Attacker has derived the shared secret
"""

from crypto_utils import generate_aes_key, decrypt_data

# Attacker reads the stolen shared key
with open("shared_key_demo.txt", "r") as f:
    stolen_shared_key = int(f.read())

print("\n=== MITM SUCCESS (KEY COMPROMISED) ===")
print("Attacker obtained shared key:", stolen_shared_key)

# Generate AES key
aes_key = generate_aes_key(stolen_shared_key)

# Attacker intercepts encrypted file
with open("encrypted/IMG_0180.JPG.enc", "rb") as f:
    encrypted_data = f.read()

# Decrypt successfully
decrypted = decrypt_data(encrypted_data, aes_key)

with open("mitm_decrypted.pdf", "wb") as f:
    f.write(decrypted)

print("🚨 MITM SUCCESS: Attacker decrypted the file")
print("=====================================")
