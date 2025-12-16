import numpy as np
import hashlib
import struct

"""
LATTICE-BASED CRYPTOGRAPHY DEMONSTRATION
Based on Module Learning With Errors (MLWE) concepts used in Post-Quantum Cryptography standards.
This file contains the mathematical implementations of lattice-based encryption and standard hashing.
"""

def generate_keys_mlwe(n=512, q=12289, sigma=8.35):
    """
    Generate Public/Private keypair using MLWE parameters.
    This demonstrates the core math behind lattice cryptography: A*s + e = t
    
    Parameters:
    n (int): Dimension of the lattice
    q (int): Modulus
    sigma (float): Standard deviation for error distribution
    """
    # Secret key: random polynomial with small coefficients (-1, 0, 1)
    s = np.random.randint(-1, 2, n, dtype=np.int32)
    
    # Public key generation
    # A is a random matrix (uniform distribution)
    A = np.random.randint(0, q, (n, n), dtype=np.int32)
    # e is the error term (gaussian/normal distribution)
    e = np.round(np.random.normal(0, sigma, n)).astype(np.int32)
    # t = A * s + e (mod q)
    t = np.mod(np.dot(A, s) + e, q)
    
    return (A, t), s

def encrypt_mlwe(m, public_key, n=512, q=12289, sigma=8.35):
    """
    Basic lattice encryption of a single value.
    
    Parameters:
    m (int): Message bit (0 or 1)
    public_key (tuple): (A, t) from generate_keys_mlwe
    """
    A, t = public_key
    
    # Encode message: Map 0/1 to the lattice space
    # 0 maps to approx -q/4, 1 maps to approx q/4
    m_encoded = (m * q // 2 - q // 4) % q
    
    # Add randomness for encryption
    r = np.random.randint(0, 2, n, dtype=np.int32)
    e1 = np.round(np.random.normal(0, sigma, n)).astype(np.int32)
    e2 = np.round(np.random.normal(0, sigma)).astype(np.int32)
    
    # Ciphertext construction (u, v)
    # c1 = A^T * r + e1
    c1 = np.mod(np.dot(A.T, r) + e1, q)
    # c2 = t^T * r + e2 + encoded_message
    c2 = np.mod(np.dot(t, r) + e2 + m_encoded, q)
    
    return (c1, c2)

def standard_hashing_demo(text_inputs):
    """
    Demonstration of using text input as entropy source for SHA-3.
    This utilizes standard NIST-approved SHA-3 (SHAKE256) hashing.
    """
    seed = bytes()
    
    for text in text_inputs:
        # Standard SHA-3 (SHAKE256) hashing of inputs
        h = hashlib.shake_256()
        h.update(text.encode('utf-8'))
        # Accumulate entropy
        seed += h.digest(64)
    
    # Final mixing
    final_hash = hashlib.shake_256(seed).digest(64)
    return final_hash

if __name__ == "__main__":
    print("--- Lattice Cryptography Demonstration ---")
    print("Generating Keys (MLWE)...")
    pk, sk = generate_keys_mlwe()
    print("Keys Generated.")
    
    msg = 1
    print(f"Encrypting message bit: {msg}")
    c1, c2 = encrypt_mlwe(msg, pk)
    print("Encryption complete.")
    print(f"Ciphertext component c1 shape: {c1.shape}")
    print(f"Ciphertext component c2 (scalar): {c2}")
    
    print("\n--- Hashing Demonstration ---")
    sample_texts = ["Historical Document 1", "Linguistic Pattern A"]
    key = standard_hashing_demo(sample_texts)
    print(f"Derived Key (first 16 bytes): {key.hex()[:32]}")
