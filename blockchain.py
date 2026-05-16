import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block("Genesis Block", "0")

    def create_block(self, data, previous_hash):
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash
        }
        block["hash"] = self.hash_block(block)
        self.chain.append(block)
        return block

    def hash_block(self, block):
        block_copy = block.copy()
        block_copy.pop("hash", None)
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    # ✅ THIS IS THE MISSING FUNCTION
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]

            # Check hash link
            if curr["previous_hash"] != prev["hash"]:
                return False

            # Recalculate hash
            if curr["hash"] != self.hash_block(curr):
                return False

        return True
