# Lie Group Transport — Generator Analysis

**PVS Formalization**: [lie_generator_structure.pvs](lie_generator_structure.pvs)
**Method**: Full Kantorovich coupling --> continuous displacement field
**Reference**: Hall (2015), *Lie Groups, Lie Algebras, and Representations*, GTM 222

## Generator Definition

For each source bin i, the Lie generator is the expected displacement under the full coupling:

```
v(i) = E[j - i | source = i] = sum_j P(i,j) * (j - i) / sum_j P(i,j)
```

where P is the optimal Kantorovich coupling (POT network simplex).

## Certificates

| Certificate | Definition | Threshold |
|---|---|---|
| C20 | Generator Coherence: cos(v_segment, v_full) | > 0.7 PASS, > 0.85 STRONG |
| C21 | Exponential Structure: constant direction + bounded speed | cos_pair > 0.85 AND speed < 5.0x |
| C22 | Shape-Direction Consistency: min cosine in active zone | > 0 PASS, > 0.85 STRONG |

## Results (Paper 3 Final Dataset + extended logs)

### Summary Table

| Boot | Type | Cloud | cos_pair | cos_full | speed | Dir | C20 | C21 | C22 |
|---|---|---|---|---|---|---|---|---|---|
| Boot293 | dawn | CLOUDY | 0.514 | 0.746 | 17.1x | ROT | PASS | FAIL | PASS |
| Boot301 | dawn | CLEAR | 0.332 | 0.635 | 32.9x | ROT | FAIL | FAIL | FAIL |
| Boot305 | dawn | CLEAR | 0.409 | 0.552 | 54.3x | ROT | FAIL | FAIL | FAIL |
| Boot312 | dawn | CLOUDY | 0.168 | 0.525 | 5.0x | ROT | FAIL | FAIL | FAIL |
| Boot314 | dawn | MIXED 45% | -0.041 | 0.264 | 20.5x | ROT | FAIL | FAIL | FAIL |
| Boot320 | dawn | CLOUDY 97% | 0.940 | 0.918 | 5.0x | STABLE | STRONG | FAIL | STRONG |
| Boot330 | dawn | MIXED 62% | 0.493 | 0.705 | 10.0x | ROT | PASS | FAIL | PASS |
| Boot334 | dawn | CLOUDY 94% | 0.194 | 0.502 | 7.6x | ROT | FAIL | FAIL | FAIL |
| Boot347 | dawn | CLOUDY 100% | 0.456 | 0.711 | 6.3x | ROT | PASS | FAIL | STRONG |
| Boot349 | dawn | CLEAR 2% | 0.804 | 0.892 | 14.2x | STABLE | STRONG | FAIL | PASS |
| Boot303 | dusk | CLEAR | -0.098 | 0.193 | 19.6x | ROT | FAIL | FAIL | FAIL |
| Boot298 | dusk | CLOUDY | -0.117 | 0.188 | 17.0x | ROT | FAIL | FAIL | FAIL |
| Boot322 | dusk | CLOUDY | -0.153 | -0.066 | 64.2x | ROT | FAIL | FAIL | FAIL |

### Key Findings

1. **Dawn vs Dusk asymmetry**: All dusk logs FAIL C20/C21/C22. Dusk generator reverses direction mid-transition (front-loaded deceleration).

2. **Cloud cover matters for coherence**: Cloudy 97-100% dawn (Boot320, Boot347) achieves STRONG coherence. Clear sky dawn (Boot301, Boot305) FAILS — rapid initial transport exhausts most mass in segment 1.

3. **Boot320 is the best case**: cos_pair=0.940, cos_full=0.918, C20=STRONG, C22=STRONG. Near-exponential transport under uniform cloud cover.

4. **No log achieves C21 (Exponential)**: Speed ratio always exceeds 5.0x. Even Boot320 (speed=5.0x) is borderline. True exp(tX) with constant speed is not observed — dawn always decelerates.

5. **T10 validation**: PVS theorem T10 (coherent IFF observed AND NOT reversal) holds on all 13 logs with zero violations. C20 PASS/FAIL perfectly predicts C22 PASS/FAIL.

6. **C20 vs C22 can differ in grade**: Boot347 has C20=PASS but C22=STRONG. C20 measures the mean alignment with the global generator (cos_full=0.711, above 0.7 but below 0.85). C22 measures the minimum cosine in the active zone (min_cos=0.903, above 0.85). The tangent field never reverses and has high local stability, but its average alignment with the full NIGHT-->DAY generator is only 0.711. The two certificates measure different aspects of coherence: C20 captures global direction alignment, C22 captures local tangent consistency.

### PVS Formalization

- [`lie_generator_structure.pvs`](lie_generator_structure.pvs) — 10 theorems: hierarchy exponential --> strongly_coherent --> coherent
- [`lie_pp_connection.pvs`](lie_pp_connection.pvs) — 6 theorems: PPG + Lie connection

### Hall (2015) References

| PVS Axiom/Theorem | Hall Reference |
|---|---|
| exponential?(p) | Theorem 2.14: one-parameter subgroup <--> exp(tX) |
| coherent?(p) | Corollary 3.46: g = tangent space at identity |
| ax_reversal_breaks_coherence | Theorem 2.14 contrapositive: reversal --> not exp |
| ax_exponential_requires_smooth_no_reversal | Definition 3.18 + Theorem 2.14: constant X |

### Physical Interpretation

The Lie generator v(i) describes the infinitesimal spectral flow:
- Positive v(i): energy at channel i moves to higher channels (red-shift)
- Negative v(i): energy at channel i moves to lower channels (blue-shift)
- Constant v across time: exponential flow exp(tX) on diffeomorphism group
- Reversing v: non-exponential, requires time-varying generator X(t)

Dawn: predominantly negative v (blue-shift as sun rises, energy moves from NIR to visible).
Dusk: initial negative v that reverses mid-transition (front-loaded, then rebounds).

## Author

Dragan Stosic, 2026
