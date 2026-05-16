import random

class DiffieHellman:
    def __init__(self, p=23, g=5):
        self.p = p
        self.g = g
        self.private_key = random.randint(2, p - 2)
        self.public_key = pow(g, self.private_key, p)

    def generate_shared_secret(self, other_public_key):
        return pow(other_public_key, self.private_key, self.p)
