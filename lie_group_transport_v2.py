"""
Lie Group Structure — Full Coupling Version
=============================================
Uses the full Kantorovich coupling (not argmax Monge) to compute
continuous displacement fields between consecutive time windows.

The "generator" v(i) = expected displacement of mass at bin i:
    v(i) = E_π[j - i | source = i] = Σ_j P(i,j) * (j - i) / Σ_j P(i,j)

This gives a continuous vector field on the spectral grid,
avoiding the discretization artifacts of argmax Monge maps.
"""

import numpy as np
import pandas as pd
import os
import ot as pot

SPEC_COLS = ['raw_F1_415', 'raw_F2_445', 'raw_F3_480', 'raw_F4_515', 'raw_F5_555',
             'raw_F6_590', 'raw_F7_630', 'raw_F8_680', 'raw_Clear', 'raw_NIR']

LOG_DIR = os.path.expanduser('~/Downloads/luces/paper3/logs')


def to_dist(arr):
    arr = np.maximum(arr, 1e-8).astype(float)
    return arr / arr.sum()


def coupling_generator(source_dist, target_dist, M):
    """Compute continuous displacement field from full coupling.
    v(i) = expected target displacement given source bin i.
    Returns v as float array (continuous, not integer)."""
    P = pot.emd(source_dist, target_dist, M)
    N = len(source_dist)
    v = np.zeros(N)
    for i in range(N):
        row_mass = P[i, :].sum()
        if row_mass > 1e-10:
            # Expected displacement: weighted average of (j - i)
            v[i] = np.sum(P[i, :] * (np.arange(N) - i)) / row_mass
        else:
            v[i] = 0.0
    return v, P


def cosine_sim(a, b):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def analyze_boot(csv_path, label):
    df = pd.read_csv(csv_path)

    night = df[df['elevation'] < -3]
    transition = df[(df['elevation'] > -3) & (df['elevation'] < 8)]
    day = df[df['elevation'] > 8]

    if len(night) < 10 or len(transition) < 20 or len(day) < 10:
        print(f'  {label}: insufficient data')
        return None

    N = len(SPEC_COLS)
    M = pot.dist(np.arange(N).reshape(-1, 1).astype(float), metric='sqeuclidean')
    M = M / M.max()

    a_night = to_dist(night[SPEC_COLS].mean().values)
    a_day = to_dist(day[SPEC_COLS].mean().values)

    # Full generator NIGHT → DAY
    v_full, _ = coupling_generator(a_night, a_day, M)

    # Split transition into windows
    n_win = 5
    ws = len(transition) // n_win
    windows = []
    for i in range(n_win):
        chunk = transition.iloc[i * ws:(i + 1) * ws]
        windows.append(to_dist(chunk[SPEC_COLS].mean().values))

    # Incremental generators between consecutive distributions
    all_dists = [a_night] + windows + [a_day]
    generators = []
    for i in range(len(all_dists) - 1):
        v_inc, _ = coupling_generator(all_dists[i], all_dists[i + 1], M)
        generators.append(v_inc)

    # Cosine similarity between all pairs of generators
    n_gen = len(generators)
    cosines = []
    for i in range(n_gen):
        for j in range(i + 1, n_gen):
            if np.linalg.norm(generators[i]) > 1e-6 and np.linalg.norm(generators[j]) > 1e-6:
                cosines.append(cosine_sim(generators[i], generators[j]))

    mean_cos = np.mean(cosines) if cosines else 0.0
    min_cos = np.min(cosines) if cosines else 0.0
    max_cos = np.max(cosines) if cosines else 0.0

    # Speed profile
    magnitudes = [np.linalg.norm(g) for g in generators]
    nonzero_mags = [m for m in magnitudes if m > 1e-6]
    speed_ratio = max(nonzero_mags) / min(nonzero_mags) if len(nonzero_mags) >= 2 else 0.0

    # Direction stability: cosine of each generator vs full generator
    cos_vs_full = [cosine_sim(g, v_full) for g in generators if np.linalg.norm(g) > 1e-6]
    mean_cos_full = np.mean(cos_vs_full) if cos_vs_full else 0.0

    # Classification
    is_geodesic = mean_cos > 0.85 and speed_ratio < 3.0
    is_same_direction = mean_cos_full > 0.85

    print(f'  {label}')
    print(f'    Full generator v (continuous): [{", ".join(f"{x:+.3f}" for x in v_full)}]')
    print(f'    ||v_full|| = {np.linalg.norm(v_full):.4f}')
    print(f'')
    print(f'    Incremental generators (6 segments):')
    print(f'    {"Seg":>4} {"||v||":>7} {"cos(v,full)":>11} v[0:5]')
    for i, g in enumerate(generators):
        cos_f = cosine_sim(g, v_full)
        print(f'    {i+1:>4} {np.linalg.norm(g):>7.4f} {cos_f:>11.4f}   [{g[0]:+.3f},{g[1]:+.3f},{g[2]:+.3f},{g[3]:+.3f},{g[4]:+.3f}]')
    print(f'')
    print(f'    Pairwise cosine (inter-segment): mean={mean_cos:.4f} min={min_cos:.4f} max={max_cos:.4f}')
    print(f'    Cosine vs full generator:        mean={mean_cos_full:.4f}')
    print(f'    Speed ratio (max/min non-zero):  {speed_ratio:.2f}x')
    print(f'')
    print(f'    Direction stability: {"STABLE" if is_same_direction else "ROTATING"} (cos_full>0.85)')
    print(f'    Geodesic on group:   {"YES" if is_geodesic else "NO"} (cos>0.85 + speed<3x)')
    print()

    # ── C20: Generator Coherence ──
    # From lie_generator_structure.pvs: coherent?(p) iff all segments aligned
    # Threshold: cos_full > 0.7 = PASS, > 0.85 = STRONG
    c20_threshold = 0.7
    c20_pass = mean_cos_full > c20_threshold
    c20_status = 'PASS' if c20_pass else 'FAIL'
    if mean_cos_full > 0.85:
        c20_status = 'STRONG'
    print(f'    C20 Generator Coherence: {c20_status} (cos_full={mean_cos_full:.3f}, threshold={c20_threshold})')

    # ── C21: Exponential Structure ──
    # From lie_generator_structure.pvs + Hall Thm 2.14:
    # exponential?(p) iff coherent AND slow (cos_pair > 0.85 AND speed < 5.0)
    c21_cos_threshold = 0.85
    c21_speed_threshold = 5.0
    c21_pass = mean_cos > c21_cos_threshold and speed_ratio < c21_speed_threshold
    c21_status = 'PASS' if c21_pass else 'FAIL'
    print(f'    C21 Exponential:         {c21_status} (cos_pair={mean_cos:.3f}, speed={speed_ratio:.1f}x, need cos>{c21_cos_threshold} & speed<{c21_speed_threshold})')

    # ── C22: Shape-Direction Consistency ──
    # Generator coherence is lost when the normalized spectral-shape tangent
    # reverses inside the active transition zone.
    # Compute: normalized shape at each segment, then cos between consecutive
    # shape-direction vectors. min_cos < 0 = reversal = FAIL.
    shape_directions = []
    for i in range(len(all_dists) - 1):
        s_start = all_dists[i] / all_dists[i].sum()
        s_end = all_dists[i+1] / all_dists[i+1].sum()
        shape_directions.append(s_end - s_start)

    # Cosines between consecutive shape directions (active segments only: skip last 2)
    n_active = max(1, len(shape_directions) - 2)  # exclude DAY tail
    shape_cos_pairs = []
    for i in range(min(n_active - 1, len(shape_directions) - 1)):
        d1 = shape_directions[i]
        d2 = shape_directions[i + 1]
        if np.linalg.norm(d1) > 1e-8 and np.linalg.norm(d2) > 1e-8:
            shape_cos_pairs.append(cosine_sim(d1, d2))

    min_cos_active = min(shape_cos_pairs) if shape_cos_pairs else 0.0
    c22_status = 'FAIL' if min_cos_active < 0 else 'PASS'
    if min_cos_active > 0.85:
        c22_status = 'STRONG'
    print(f'    C22 Shape-Direction:     {c22_status} (min_cos={min_cos_active:.3f}, reversal={min_cos_active < 0})')
    print()

    return {
        'label': label,
        'mean_cos': mean_cos,
        'mean_cos_full': mean_cos_full,
        'speed_ratio': speed_ratio,
        'is_geodesic': is_geodesic,
        'is_same_direction': is_same_direction,
        'magnitudes': magnitudes,
        'c20_status': c20_status,
        'c21_status': c21_status,
        'c22_status': c22_status,
        'min_cos_active': min_cos_active
    }


def main():
    print('LIE GROUP STRUCTURE — FULL COUPLING (Continuous)')
    print('=' * 60)
    print()
    print('Generator: v(i) = E[j-i | source=i] from full Kantorovich coupling')
    print('Test: constant direction + bounded speed = geodesic on Diff group')
    print()

    logs = [
        ('boot293_overnight.csv', 'Boot293 (dawn, CLOUDY)'),
        ('boot301_sunrise.csv', 'Boot301 (dawn, CLEAR)'),
        ('boot305_dawn.csv', 'Boot305 (dawn, CLEAR)'),
        ('boot312_dawn.csv', 'Boot312 (dawn, CLOUDY)'),
        ('boot314_dawn.csv', 'Boot314 (dawn, MIXED 45%)'),
        ('boot320_merged_dawn.csv', 'Boot320 (dawn, CLOUDY 97% POST-FIX)'),
        ('boot330_dawn.csv', 'Boot330 (dawn, MIXED 62% POST-FIX)'),
        ('boot334_dawn.csv', 'Boot334 (dawn, CLOUDY 94% POST-FIX)'),
        ('boot347_dawn.csv', 'Boot347 (dawn, CLOUDY 100% POST-FIX)'),
        ('boot349_dawn.csv', 'Boot349 (dawn, CLEAR 2% POST-FIX)'),
        ('boot303_dusk.csv', 'Boot303 (dusk, CLEAR)'),
        ('boot298_dusk.csv', 'Boot298 (dusk, CLOUDY)'),
        ('boot322_dusk.csv', 'Boot322 (dusk, CLOUDY POST-FIX)'),
    ]

    results = []
    for fname, label in logs:
        path = os.path.join(LOG_DIR, fname)
        if os.path.exists(path):
            r = analyze_boot(path, label)
            if r:
                results.append(r)

    print('=' * 60)
    print('SUMMARY')
    print(f'  {"Boot":<30} {"cos_pair":>8} {"cos_full":>8} {"speed":>6} {"Dir":>8} {"C20":>6} {"C21":>5} {"C22":>6}')
    print(f'  {"----":<30} {"--------":>8} {"--------":>8} {"-----":>6} {"---":>8} {"---":>6} {"---":>5} {"---":>6}')
    for r in results:
        d = "STABLE" if r['is_same_direction'] else "ROT"
        c20 = r.get('c20_status', '?')
        c21 = r.get('c21_status', '?')
        c22 = r.get('c22_status', '?')
        print(f'  {r["label"]:<30} {r["mean_cos"]:>8.3f} {r["mean_cos_full"]:>8.3f} {r["speed_ratio"]:>5.1f}x {d:>8} {c20:>6} {c21:>5} {c22:>6}')

    print()
    print('KEY:')
    print('  cos_pair: mean cosine between consecutive incremental generators')
    print('  cos_full: mean cosine of each segment vs global NIGHT→DAY generator')
    print('  Dir: STABLE = all segments point same direction as full transport')
    print('  C20: Generator Coherence (cos_full > 0.7 = PASS, > 0.85 = STRONG)')
    print('  C21: Exponential structure (cos_pair > 0.85 AND speed < 5.0x)')
    print('  C22: Shape-Direction Consistency (min_cos in active zone > 0 = PASS, > 0.85 = STRONG)')

    # ── T10 VALIDATION (PVS theorem: coherent IFF observed AND NOT reversal) ──
    # Sanity check: C20 PASS should correspond exactly to C22 != FAIL
    # (C14 is not measured here, assumed PASS for post-fix logs)
    print()
    print('T10 VALIDATION (PVS: coherent ⟺ observed ∧ ¬reversal):')
    t10_violations = 0
    for r in results:
        c20 = r.get('c20_status', 'FAIL')
        c22 = r.get('c22_status', 'FAIL')
        c20_pass = c20 in ('PASS', 'STRONG')
        c22_no_reversal = c22 in ('PASS', 'STRONG')
        consistent = (c20_pass == c22_no_reversal)
        if not consistent:
            t10_violations += 1
            print(f'  ✗ VIOLATION: {r["label"]} — C20={c20}, C22={c22}')
    if t10_violations == 0:
        print(f'  ✓ T10 holds on all {len(results)} logs (C20↔C22 consistent)')
    else:
        print(f'  ⚠ {t10_violations}/{len(results)} violations detected')


if __name__ == '__main__':
    main()
