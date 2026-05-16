from flask import Flask, render_template, request, send_file, jsonify
import os
from diffie_hellman import DiffieHellman
from blockchain import Blockchain
from crypto_utils import generate_aes_key, encrypt_data, decrypt_data

app = Flask(__name__)

# Folders
for d in ["uploads", "encrypted", "decrypted"]:
    os.makedirs(d, exist_ok=True)

# Init
blockchain = Blockchain()
userA = DiffieHellman()
userB = DiffieHellman()

# Store public keys immutably
blockchain.create_block(
    {"User": "A", "PublicKey": userA.public_key},
    blockchain.chain[-1]["hash"]
)
blockchain.create_block(
    {"User": "B", "PublicKey": userB.public_key},
    blockchain.chain[-1]["hash"]
)

# Validate chain (MITM prevention)
if not blockchain.validate_chain():
    raise SystemExit("🚨 MITM DETECTED – Blockchain tampered")

# Shared secret (same on both sides)
shared_A = userA.generate_shared_secret(userB.public_key)
shared_B = userB.generate_shared_secret(userA.public_key)
assert shared_A == shared_B

aes_key = generate_aes_key(shared_A)

# --- Proof print (show in terminal) ---
print("\n=== DIFFIE–HELLMAN (SECURE) ===")
print("p:", userA.p, "g:", userA.g)
print("A pub:", userA.public_key, "B pub:", userB.public_key)
print("Shared key:", shared_A)
print("==============================\n")

# Save shared key for demo (ONLY FOR ATTACK SIMULATION)
with open("shared_key_demo.txt", "w") as f:
    f.write(str(shared_A))

@app.route("/")
def index():
    return render_template("index.html", shared_key=shared_A, chain=blockchain.chain)

@app.route("/key-exchange")
def key_exchange():
    return jsonify({
        "p": userA.p, "g": userA.g,
        "A_public": userA.public_key,
        "B_public": userB.public_key,
        "Shared_A": shared_A, "Shared_B": shared_B
    })

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    src = os.path.join("uploads", f.filename)
    f.save(src)

    with open(src, "rb") as fp:
        enc = encrypt_data(fp.read(), aes_key)

    enc_path = os.path.join("encrypted", f.filename + ".enc")
    with open(enc_path, "wb") as fp:
        fp.write(enc)

    return """
<h3 style='color:green;'>✔ File Encrypted Successfully</h3>
<p>Your file has been securely encrypted and stored.</p>
"""

@app.route("/decrypt/<name>")
def decrypt(name):
    enc_path = os.path.join("encrypted", name)
    with open(enc_path, "rb") as fp:
        dec = decrypt_data(fp.read(), aes_key)

    out = os.path.join("decrypted", name.replace(".enc", ""))
    with open(out, "wb") as fp:
        fp.write(dec)

    return send_file(out, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
