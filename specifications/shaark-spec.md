# SHAARK Algorithm Specification

**Algorithm**: Structured Harmonic Authentication & Adaptive Resonant Keying  
**Author:** Brendon Joseph Kelly  
**Runtime ID:** 1410-426-4743  
**Version:** 1.0  
**Date:** August 30, 2025

---

## 1. Overview

SHAARK is a cryptographic hash function designed to resist resonant-state attacks. It incorporates lessons learned from ancient undeciphered scripts and modern cryptanalysis.

### 1.1 Parameters

- **Output Size**: 256 bits
- **State Size**: 512 bits (16 × 32-bit words)
- **Capacity**: 256 bits
- **Rate**: 256 bits
- **Rounds**: 80
- **Block Size**: Variable (256-1024 bits)

### 1.2 Security Claims

- **Collision Resistance**: 2¹²⁸ operations
- **Preimage Resistance**: 2²⁵⁶ operations
- **Second Preimage Resistance**: 2²⁵⁶ operations

## 2. Algorithm Specification

### 2.1 Main Function

```python
def SHAARK(message, key, time_window=60):
    """
    Compute SHAARK hash of message.
    
    Args:
        message (bytes): Input message
        key (bytes): Secret key (32 bytes)
        time_window (int): Temporal validity window in seconds
    
    Returns:
        bytes: 256-bit hash value
    """
    # Initialize state
    state = initialize_state(key, time_window)
    
    # Pad message
    padded = pad_message(message)
    
    # Absorb phase
    for block in chunk_message(padded, rate=32):
        state = absorb_block(state, block)
        state = permutation(state, key, time_window)
    
    # Squeeze phase
    hash_value = squeeze(state, output_length=32)
    
    return hash_value
```

### 2.2 State Initialization

```python
def initialize_state(key, time_window):
    """
    Initialize 512-bit state from key and temporal context.
    """
    # Generate base seed using Ω° operator
    seed = omega_operator(key, get_entropy(), time_window)
    
    # Initialize 16 32-bit words
    state = [0] * 16
    for i in range(16):
        state[i] = seed[i*4:(i+1)*4]
    
    return state
```

### 2.3 Permutation Function

```python
def permutation(state, key, time_window):
    """
    Apply 80-round permutation to state.
    """
    for round_num in range(80):
        # Generate round-specific constant
        round_constant = generate_round_constant(key, round_num, time_window)
        
        # Apply transformation layers
        state = omega_mixing_layer(state, round_constant)
        state = lambda_transform_layer(state, key)
        state = psidelta_diffusion(state)
        
        # Inject entropy every 10 rounds
        if round_num % 10 == 0:
            entropy = glyphic_entropy_lock(key, round_num)
            state[0] ^= entropy
    
    return state
```

### 2.4 Round Constant Generation

```python
def generate_round_constant(key, round_num, time_window):
    """
    Generate procedural round constant (Phaistos principle).
    """
    device_id = get_device_identifier()
    timestamp = get_current_time()
    
    # Ω° operator creates unique constant per implementation
    constant = omega_hash(key, round_num, device_id, timestamp, time_window)
    
    return constant
```

## 3. Reference Implementation

A complete reference implementation in Python is provided in the repository.

### 3.1 Usage Example

```python
from shaark import SHAARK

# Basic usage
message = b"The quick brown fox jumps over the lazy dog"
key = b"secret_key_32_bytes_exact_len!"
hash_value = SHAARK(message, key)

# With time window
hash_value = SHAARK(message, key, time_window=60)

# Verification
is_valid = verify_SHAARK(message, hash_value, key, time_window=60)
```

## 4. Test Vectors

### Test Vector 1: Empty Message

```text
Message: ""
Key: "00000000000000000000000000000000"
Time Window: 60
Expected Output: [To be computed]
```

### Test Vector 2: Standard Test

```text
Message: "The quick brown fox jumps over the lazy dog"
Key: "secret_key_32_bytes_exact_len!"
Time Window: 60
Expected Output: [To be computed]
```

## 5. Security Analysis

See [SHA-256 Collapse Analysis](../docs/03-sha256-collapse.md) for detailed security analysis comparing SHAARK to SHA-256.

---

**Navigation**: [Back to Main](../README.md) | [Next: Migration Protocol](migration-protocol.md)
