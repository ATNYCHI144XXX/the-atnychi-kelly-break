# Bitcoin Mining Differential Analysis: Bounded Differentials

**Author:** Brendon Joseph Kelly  
**Date:** December 13, 2025

---

## Abstract

This document analyzes bounded differential patterns in SHA-256 relevant to Bitcoin mining, exploring how local collisions in message schedule can be constructed while maintaining predictable propagation.

## 1. Bitcoin Context

In Bitcoin mining, the goal is to find a nonce such that:

$$\text{SHA256}(\text{SHA256}(\text{block\_header})) < \text{Target}$$

A differential refers to a controlled change in the input and observing the resulting change in the internal state.

## 2. Bounded Differential Construction

A 9-round local collision might follow this pattern:

| Round $t$ | $\Delta W_t$ (XOR) | Purpose |
|-----------|-------------------|---------|
| t | $\delta$ = 0x80000000 | Inject initial disturbance |
| t+1 | $\delta_1$ | Cancel $\delta$'s effect on Ch function |
| t+2 | $\delta_2$ | Cancel effect from $\Sigma_1$ and carry |
| ... | ... | Continues cancellation chain |
| t+8 | $\delta_8$ | Final cancellation, $\Delta\text{State} = 0$ |

## 3. XOR vs. Addition Ambiguity

The cancellation trick exploits:
- **XOR Difference** ($\Delta^\oplus$): Simple bit flip
- **Additive Difference** ($\Delta^+$): The difference as a signed integer

Carry propagation creates ambiguity that enables cancellation in subsequent rounds.

## 4. Reality Check

**Current Status**: No practical differential attacks exist on full SHA-256 as used in Bitcoin. The known bounded differentials are theoretical tools for understanding security margin.

---

**Navigation**: [Back to Main](../README.md)
