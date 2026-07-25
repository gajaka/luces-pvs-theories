# Certificate Runner — Full Results

19 certificates validated on all available logs.
Proof-preserving graph certificates (PPG, RES, DET) achieve 100% PASS rate.

---

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot293_overnight.csv
  Samples:    1173
  Duration:   5.6h
  Elevation:  [-20.7, 22.1]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=5.48e-16 W2=0.1389
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.847
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9909
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/252 (from elevation)
  C13 Voronoi Partition:    PASS   min_W2=0.0356 (DAWN↔DAY_CLOUDY) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=2.0 κ_mean=1.6

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:constant v=[553,737,732] profile=constant
  C6  OT Shadow:            N/A    No ot_error column (pre-OT-shadow firmware)
  C14 Dual Observability:   PASS   dual=50/50 spec=50 κ_ok=50
  C19 Stationarity:         FAIL   cloud_std=30.1 mean=36% range=97%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=25.3%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.065 [+0.067..+0.052]
  C12 Geodesic Additive:    FAIL   ratio=1.253 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1058 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1064 W2(N,M)=0.0988 W2(M,D)=0.0279 min=0.0279 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=9/9 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.901

═══════════════════════════════════════════════════════
  Summary: 16 PASS / 4 FAIL / 1 BORDER / 1 DIAG / 1 INFO / 1 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot298_dusk.csv
  Samples:    1588
  Duration:   7.6h
  Elevation:  [-21.8, 22.4]
  Transition: dusk

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=2.08e-17 W2=0.1370
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.828
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9785
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   decreasing violations=0/252 (from elevation)
  C13 Voronoi Partition:    PASS   min_W2=0.0176 (DAY_CLEAR↔DUSK) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    PASS   ρ=0.9909 (identity)
  C5  Fisher Boundary:      PASS   κ_max=28.7 κ_mean=15.2

  DYNAMICS
  --------
  C3  Velocity (dusk):      PASS   v=[15862,3722,1038] ratio=15.3x
  C6  OT Shadow:            N/A    No ot_error column (pre-OT-shadow firmware)
  C14 Dual Observability:   PASS   dual=50/50 spec=50 κ_ok=50
  C19 Stationarity:         PASS   cloud_std=0.0 mean=0% range=0%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      DIAG   excess=16.8% (expected for decelerating dusk)
  C10 Displ. Convexity:     PASS   MIXED excess=+0.026 [-0.033..+0.072]
  C12 Geodesic Additive:    PASS   ratio=1.168 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=3 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.2800 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1027 W2(N,M)=0.0949 W2(M,D)=0.0292 min=0.0292 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=11/11 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.903

═══════════════════════════════════════════════════════
  Summary: 21 PASS / 0 FAIL / 2 DIAG / 1 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot301_sunrise.csv
  Samples:    918
  Duration:   4.4h
  Elevation:  [-11.5, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=5.48e-16 W2=0.1342
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.837
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/253 (from elevation)
  C13 Voronoi Partition:    PASS   min_W2=0.0363 (DAWN↔DAY_CLEAR) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=99.6 κ_mean=13.6

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[573,1071,2290] profile=accelerating
  C6  OT Shadow:            N/A    No ot_error column (pre-OT-shadow firmware)
  C14 Dual Observability:   PASS   dual=49/49 spec=49 κ_ok=49
  C19 Stationarity:         PASS   cloud_std=3.2 mean=2% range=11%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=23.0%
  C10 Displ. Convexity:     PASS   MIXED excess=-0.015 [+0.060..-0.037]
  C12 Geodesic Additive:    FAIL   ratio=1.230 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1230 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1034 W2(N,M)=0.0941 W2(M,D)=0.0361 min=0.0361 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=10/10 (100%)
  RES Resilience:           PASS   sub=9/9 full=10/10 mono=True
  DET Deterministic:        PASS   det=10/10 mean_dom=0.903

═══════════════════════════════════════════════════════
  Summary: 18 PASS / 2 FAIL / 1 BORDER / 1 DIAG / 1 INFO / 1 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot303_dusk.csv
  Samples:    1296
  Duration:   6.2h
  Elevation:  [-18.6, 45.0]
  Transition: dusk

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=2.67e-16 W2=0.1365
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.841
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9909
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   decreasing violations=0/253 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0167 (DAY_CLEAR↔DUSK) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    PASS   ρ=0.9909 (identity)
  C5  Fisher Boundary:      PASS   κ_max=3.3 κ_mean=1.1

  DYNAMICS
  --------
  C3  Velocity (dusk):      PASS   v=[16787,4993,1065] ratio=15.8x
  C6  OT Shadow:            PASS   err=0.0720 cv=0.09 t=dec
  C14 Dual Observability:   PASS   dual=50/50 spec=50 κ_ok=50
  C19 Stationarity:         PASS   cloud_std=3.0 mean=6% range=10%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      DIAG   excess=18.8% (expected for decelerating dusk)
  C10 Displ. Convexity:     PASS   MIXED excess=+0.021 [-0.036..+0.063]
  C12 Geodesic Additive:    PASS   ratio=1.188 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=3 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.2726 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1032 W2(N,M)=0.0921 W2(M,D)=0.0361 min=0.0361 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=10/10 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.891

═══════════════════════════════════════════════════════
  Summary: 22 PASS / 0 FAIL / 2 DIAG
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot305_dawn.csv
  Samples:    1457
  Duration:   7.0h
  Elevation:  [-21.6, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=4.27e-16 W2=0.1464
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.832
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9909
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/253 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0265 (DAWN↔DAY_CLOUDY) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=1.4 κ_mean=1.3

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:constant v=[1152,1185,1305] profile=constant
  C6  OT Shadow:            PASS   err=0.0767 cv=0.12 t=inc
  C14 Dual Observability:   PASS   dual=50/50 spec=50 κ_ok=50
  C19 Stationarity:         PASS   cloud_std=1.7 mean=95% range=6%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=18.1%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.023 [+0.030..+0.015]
  C12 Geodesic Additive:    PASS   ratio=1.181 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1539 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1129 W2(N,M)=0.1013 W2(M,D)=0.0375 min=0.0375 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=10/10 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.923

═══════════════════════════════════════════════════════
  Summary: 19 PASS / 2 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot308_dawn.csv
  Samples:    240
  Duration:   1.5h
  Elevation:  [-17.9, -9.1]
  Transition: none

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  N/A    Insufficient transition samples
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9273
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      N/A    Insufficient transition samples
  C13 Voronoi Partition:    N/A    Fewer than 2 regimes observed

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      N/A    Insufficient transition samples

  DYNAMICS
  --------
  C3  Velocity:             N/A    No transition detected
  C6  OT Shadow:            N/A    Insufficient transition samples
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         N/A    Insufficient transition samples

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=2/2 (100%)
  RES Resilience:           N/A    Insufficient bins in subset
  DET Deterministic:        PASS   det=2/2 mean_dom=0.865

═══════════════════════════════════════════════════════
  Summary: 3 PASS / 0 FAIL / 21 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot312_dawn.csv
  Samples:    904
  Duration:   5.1h
  Elevation:  [-20.5, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     PASS   gap=2.57e-16 W2=0.1351
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.854
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9909
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/253 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0389 (DAWN↔DAY_CLOUDY) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=50.8 κ_mean=12.5

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[172,206,1774] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0658 cv=0.13 t=inc
  C14 Dual Observability:   FAIL   dual=47/50 spec=47 κ_ok=50
  C19 Stationarity:         PASS   cloud_std=17.5 mean=85% range=60%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=19.6%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.040 [+0.081..-0.038]
  C12 Geodesic Additive:    PASS   ratio=1.196 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=3 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.3040 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1007 W2(N,M)=0.0822 W2(M,D)=0.0514 min=0.0514 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=10/10 (100%)
  RES Resilience:           PASS   sub=8/8 full=10/10 mono=True
  DET Deterministic:        PASS   det=10/10 mean_dom=0.891

═══════════════════════════════════════════════════════
  Summary: 18 PASS / 3 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot314_dawn.csv
  Samples:    920
  Duration:   4.4h
  Elevation:  [-11.3, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=2.46e-16 W2=0.1336
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.853
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/251 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0235 (DAY_MIXED↔DAY_CLOUDY) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=86.8 κ_mean=2.2

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:mixed v=[588,2381,1001] profile=mixed
  C6  OT Shadow:            PASS   err=0.0707 cv=0.12 t=inc
  C14 Dual Observability:   FAIL   dual=45/50 spec=50 κ_ok=45
  C19 Stationarity:         PASS   cloud_std=9.6 mean=55% range=33%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=22.5%
  C10 Displ. Convexity:     PASS   MIXED excess=+0.034 [+0.105..-0.005]
  C12 Geodesic Additive:    FAIL   ratio=1.225 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1157 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.0995 W2(N,M)=0.0971 W2(M,D)=0.0192 min=0.0192 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=10/10 (100%)
  RES Resilience:           PASS   sub=10/10 full=10/10 mono=True
  DET Deterministic:        PASS   det=10/10 mean_dom=0.909

═══════════════════════════════════════════════════════
  Summary: 18 PASS / 3 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot319_dawn.csv
  Samples:    900
  Duration:   4.3h
  Elevation:  [-22.2, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      PASS   increasing violations=0/60 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0493 (NIGHT↔DAWN) k=2

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      PASS   κ_max=1.8 κ_mean=1.3

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:constant v=[151,108,79] profile=constant
  C6  OT Shadow:            PASS   err=0.0551 cv=0.09 t=inc
  C14 Dual Observability:   PASS   dual=49/49 spec=49 κ_ok=49
  C19 Stationarity:         PASS   cloud_std=0.0 mean=99% range=0%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=5/5 (100%)
  RES Resilience:           PASS   sub=2/2 full=5/5 mono=True
  DET Deterministic:        PASS   det=5/5 mean_dom=0.935

═══════════════════════════════════════════════════════
  Summary: 11 PASS / 0 FAIL / 1 INFO / 12 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot320_dawn.csv
  Samples:    624
  Duration:   3.0h
  Elevation:  [-0.2, 29.4]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      PASS   increasing violations=0/186 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0195 (DAY_CLOUDY↔DAY_MIXED) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      PASS   κ_max=18.4 κ_mean=4.2

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[244,381,627] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0622 cv=0.03 t=inc
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         PASS   cloud_std=0.4 mean=100% range=3%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=6/6 (100%)
  RES Resilience:           PASS   sub=6/6 full=6/6 mono=True
  DET Deterministic:        PASS   det=6/6 mean_dom=0.901

═══════════════════════════════════════════════════════
  Summary: 10 PASS / 0 FAIL / 1 INFO / 13 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot320_merged_dawn.csv
  Samples:    1466
  Duration:   7.3h
  Elevation:  [-22.2, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     PASS   gap=2.46e-16 W2=0.1438
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.866
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/189 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0195 (DAY_CLOUDY↔DAY_MIXED) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=18.4 κ_mean=4.1

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[202,380,586] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0620 cv=0.04 t=inc
  C14 Dual Observability:   PASS   dual=27/27 spec=27 κ_ok=27
  C19 Stationarity:         PASS   cloud_std=0.4 mean=99% range=3%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=17.3%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.054 [+0.077..+0.007]
  C12 Geodesic Additive:    PASS   ratio=1.173 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.0968 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1088 W2(N,M)=0.0820 W2(M,D)=0.0591 min=0.0591 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=10/10 (100%)
  RES Resilience:           PASS   sub=9/9 full=10/10 mono=True
  DET Deterministic:        PASS   det=10/10 mean_dom=0.912

═══════════════════════════════════════════════════════
  Summary: 19 PASS / 2 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot322_dusk.csv
  Samples:    1361
  Duration:   6.5h
  Elevation:  [-21.4, 45.0]
  Transition: dusk

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     PASS   gap=3.85e-16 W2=0.1432
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.824
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9785
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   decreasing violations=0/251 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0252 (DAY_CLOUDY↔DUSK) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    PASS   ρ=0.9909 (identity)
  C5  Fisher Boundary:      PASS   κ_max=13.1 κ_mean=8.6

  DYNAMICS
  --------
  C3  Velocity (dusk):      PASS   v=[6742,1843,882] ratio=7.6x
  C6  OT Shadow:            PASS   err=0.0703 cv=0.09 t=dec
  C14 Dual Observability:   PASS   dual=49/49 spec=49 κ_ok=49
  C19 Stationarity:         PASS   cloud_std=4.6 mean=76% range=19%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      DIAG   excess=14.9% (expected for decelerating dusk)
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.027 [-0.027..+0.093]
  C12 Geodesic Additive:    PASS   ratio=1.149 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.0897 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1060 W2(N,M)=0.0949 W2(M,D)=0.0347 min=0.0347 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=11/11 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.905

═══════════════════════════════════════════════════════
  Summary: 21 PASS / 1 FAIL / 2 DIAG
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot324_partial.csv
  Samples:    54
  Duration:   0.3h
  Elevation:  [-22.1, 45.0]
  Transition: none

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  N/A    Insufficient transition samples
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      N/A    Insufficient samples
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      N/A    Insufficient transition samples
  C13 Voronoi Partition:    N/A    Fewer than 2 regimes observed

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      N/A    Insufficient transition samples

  DYNAMICS
  --------
  C3  Velocity:             N/A    No transition detected
  C6  OT Shadow:            N/A    Insufficient transition samples
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         N/A    Insufficient transition samples

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       N/A    Insufficient bins (<3)
  RES Resilience:           N/A    Insufficient bins in subset
  DET Deterministic:        N/A    Insufficient bins (<3)

═══════════════════════════════════════════════════════
  Summary: 0 PASS / 0 FAIL / 24 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot325_dawn.csv
  Samples:    21
  Duration:   0.1h
  Elevation:  [25.1, 45.0]
  Transition: none

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  N/A    Insufficient transition samples
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      N/A    Insufficient samples
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      N/A    Insufficient transition samples
  C13 Voronoi Partition:    N/A    Fewer than 2 regimes observed

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      N/A    Insufficient transition samples

  DYNAMICS
  --------
  C3  Velocity:             N/A    No transition detected
  C6  OT Shadow:            N/A    Insufficient transition samples
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         N/A    Insufficient transition samples

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       N/A    Insufficient bins (<3)
  RES Resilience:           N/A    Insufficient data (<50 samples)
  DET Deterministic:        N/A    Insufficient bins (<3)

═══════════════════════════════════════════════════════
  Summary: 0 PASS / 0 FAIL / 24 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot326_dawn.csv
  Samples:    1
  Duration:   0.0h
  Elevation:  [45.0, 45.0]
  Transition: none

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  N/A    Insufficient transition samples
  C4  Dual Consistency:     N/A    Insufficient NIGHT/DAY samples
  Cv  Vertex Sparsity:      N/A    Insufficient NIGHT/DAY samples
  Cm  Monge Structure:      N/A    Insufficient NIGHT/DAY samples
  C7  Map Persistence:      N/A    Insufficient samples
  C9  Cyclical Monotone:    N/A    Insufficient NIGHT/DAY samples
  C11 OT Monotonicity:      N/A    Insufficient transition samples
  C13 Voronoi Partition:    N/A    Fewer than 2 regimes observed

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    N/A    Insufficient NIGHT/DAY samples
  C5  Fisher Boundary:      N/A    Insufficient transition samples

  DYNAMICS
  --------
  C3  Velocity:             N/A    No transition detected
  C6  OT Shadow:            N/A    Insufficient transition samples
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         N/A    Insufficient transition samples

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         N/A    Insufficient data
  C16 Local Monotonicity:   N/A    Insufficient data
  C17 Tangent Bundle:       N/A    Insufficient data
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       N/A    Insufficient bins (<3)
  RES Resilience:           N/A    Insufficient data (<50 samples)
  DET Deterministic:        N/A    Insufficient bins (<3)

═══════════════════════════════════════════════════════
  Summary: 0 PASS / 0 FAIL / 24 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot330_dawn.csv
  Samples:    1806
  Duration:   8.6h
  Elevation:  [-22.4, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     PASS   gap=6.25e-16 W2=0.1564
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.817
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9970
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/250 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0459 (DAWN↔DAY_MIXED) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=97.8 κ_mean=2.5

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[530,627,5731] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0671 cv=0.10 t=inc
  C14 Dual Observability:   PASS   dual=49/49 spec=49 κ_ok=49
  C19 Stationarity:         PASS   cloud_std=8.8 mean=79% range=27%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=17.9%
  C10 Displ. Convexity:     PASS   MIXED excess=+0.049 [+0.106..-0.033]
  C12 Geodesic Additive:    PASS   ratio=1.179 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1506 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1199 W2(N,M)=0.0936 W2(M,D)=0.0557 min=0.0557 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=11/11 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.898

═══════════════════════════════════════════════════════
  Summary: 20 PASS / 1 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot332_dawn.csv
  Samples:    825
  Duration:   3.9h
  Elevation:  [-6.1, 32.3]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=7.62e-16 W2=0.1187
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.795
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/250 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0290 (DAY_CLEAR↔DAY_MIXED) k=4

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    PASS   ρ=0.9909 (identity)
  C5  Fisher Boundary:      PASS   κ_max=5.9 κ_mean=1.6

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[675,1779,2529] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0706 cv=0.07 t=inc
  C14 Dual Observability:   PASS   dual=49/49 spec=49 κ_ok=49
  C19 Stationarity:         PASS   cloud_std=5.4 mean=10% range=18%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=22.3%
  C10 Displ. Convexity:     PASS   MIXED excess=+0.018 [+0.063..-0.007]
  C12 Geodesic Additive:    FAIL   ratio=1.223 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1659 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.0919 W2(N,M)=0.0808 W2(M,D)=0.0432 min=0.0432 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=9/9 (100%)
  RES Resilience:           PASS   sub=9/9 full=9/9 mono=True
  DET Deterministic:        PASS   det=9/9 mean_dom=0.915

═══════════════════════════════════════════════════════
  Summary: 20 PASS / 2 FAIL / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot334_dawn.csv
  Samples:    1328
  Duration:   6.3h
  Elevation:  [-22.6, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=5.45e-16 W2=0.1430
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.861
  C7  Map Persistence:      PASS   ρ(T1,T2)=1.0000
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/249 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0315 (DAWN↔DAY_CLOUDY) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=5.5 κ_mean=1.2

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:accelerating v=[630,1612,2529] profile=accelerating
  C6  OT Shadow:            PASS   err=0.0712 cv=0.07 t=inc
  C14 Dual Observability:   PASS   dual=48/48 spec=48 κ_ok=48
  C19 Stationarity:         PASS   cloud_std=2.1 mean=94% range=9%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=20.9%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.076 [+0.117..+0.033]
  C12 Geodesic Additive:    FAIL   ratio=1.209 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.0991 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1089 W2(N,M)=0.0986 W2(M,D)=0.0320 min=0.0320 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=9/9 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.902

═══════════════════════════════════════════════════════
  Summary: 18 PASS / 3 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot336_dawn.csv
  Samples:    55
  Duration:   5.9h
  Elevation:  [-15.0, 40.3]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  N/A    Insufficient transition samples
  C4  Dual Consistency:     PASS   gap=1.21e-16 W2=0.1529
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.830
  C7  Map Persistence:      N/A    Insufficient samples
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      N/A    Insufficient transition samples
  C13 Voronoi Partition:    PASS   min_W2=0.0647 (DAWN↔DAY_MIXED) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      N/A    Insufficient transition samples

  DYNAMICS
  --------
  C3  Velocity (dawn):      N/A    Insufficient transition samples
  C6  OT Shadow:            N/A    Insufficient transition samples
  C14 Dual Observability:   N/A    Insufficient overlap samples
  C19 Stationarity:         PASS   cloud_std=4.3 mean=53% range=20%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      N/A    Insufficient regime samples
  C10 Displ. Convexity:     N/A    Insufficient regime samples
  C12 Geodesic Additive:    N/A    Insufficient regime samples

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1641 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       N/A    Insufficient data

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=3/3 (100%)
  RES Resilience:           PASS   sub=2/2 full=3/3 mono=True
  DET Deterministic:        PASS   det=3/3 mean_dom=0.889

═══════════════════════════════════════════════════════
  Summary: 11 PASS / 0 FAIL / 1 BORDER / 1 DIAG / 11 N/A
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot347_dawn.csv
  Samples:    1157
  Duration:   5.5h
  Elevation:  [-18.6, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=0.9970
  C4  Dual Consistency:     PASS   gap=1.35e-16 W2=0.1316
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.847
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9939
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/248 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0435 (DAWN↔DAY_CLOUDY) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=5.8 κ_mean=1.8

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:mixed v=[263,211,923] profile=mixed
  C6  OT Shadow:            PASS   err=0.0624 cv=0.05 t=inc
  C14 Dual Observability:   PASS   dual=48/48 spec=48 κ_ok=48
  C19 Stationarity:         PASS   cloud_std=0.0 mean=100% range=0%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=20.6%
  C10 Displ. Convexity:     PASS   MIXED excess=+0.035 [+0.083..-0.045]
  C12 Geodesic Additive:    FAIL   ratio=1.206 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=3 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.2903 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.0985 W2(N,M)=0.0791 W2(M,D)=0.0543 min=0.0543 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=10/10 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.915

═══════════════════════════════════════════════════════
  Summary: 19 PASS / 2 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```

```
═══════════════════════════════════════════════════════
  LUCES CERTIFICATE RUNNER
═══════════════════════════════════════════════════════
  File:       boot349_dawn.csv
  Samples:    1295
  Duration:   6.2h
  Elevation:  [-22.2, 45.0]
  Transition: dawn

  STRUCTURAL INVARIANTS
  ---------------------
  C2  Transport Stability:  PASS   coupling_ρ=1.0000
  C4  Dual Consistency:     PASS   gap=2.12e-16 W2=0.1547
  Cv  Vertex Sparsity:      PASS   nnz=19 ≤ 19
  Cm  Monge Structure:      PASS   monge=0.817
  C7  Map Persistence:      PASS   ρ(T1,T2)=0.9970
  C9  Cyclical Monotone:    PASS   violations=0/171 support=19
  C11 OT Monotonicity:      PASS   increasing violations=0/246 (recorded)
  C13 Voronoi Partition:    PASS   min_W2=0.0421 (DAWN↔DAY_CLEAR) k=3

  RANK + BOUNDARY
  ---------------
  C1  Rank Preservation:    BORDER ρ=0.9847 (identity)
  C5  Fisher Boundary:      PASS   κ_max=2.9 κ_mean=1.4

  DYNAMICS
  --------
  C3  Velocity (dawn):      INFO:constant v=[726,1052,983] profile=constant
  C6  OT Shadow:            PASS   err=0.0706 cv=0.04 t=inc
  C14 Dual Observability:   PASS   dual=47/47 spec=47 κ_ok=47
  C19 Stationarity:         PASS   cloud_std=0.1 mean=0% range=0%

  GEODESIC STRUCTURE
  ------------------
  C8  Near-Optimality:      FAIL   excess=17.4%
  C10 Displ. Convexity:     FAIL   CONCAVE excess=+0.046 [+0.087..+0.014]
  C12 Geodesic Additive:    PASS   ratio=1.174 (1.0=perfect geodesic)

  PANARETOS (Wasserstein Statistics)
  -----------------------------------
  C15 Brenier Diff:         PASS   max_jump=2 mean_jump=1.00 (≤3=differentiable)
  C16 Local Monotonicity:   PASS   inversions=0/9 (0=locally monotone)
  C17 Tangent Bundle:       DIAG   gap=0.1606 (Monge vs Kantorovich midpoint)
  C18 Barycenter Sep:       PASS   W2(N,D)=0.1185 W2(N,M)=0.0981 W2(M,D)=0.0488 min=0.0488 (>0.01=separated)

  PROOF-PRESERVING GRAPH
  ----------------------
  PPG Graph Validity:       PASS   valid=11/11 (100%)
  RES Resilience:           PASS   sub=10/10 full=11/11 mono=True
  DET Deterministic:        PASS   det=11/11 mean_dom=0.913

═══════════════════════════════════════════════════════
  Summary: 19 PASS / 2 FAIL / 1 BORDER / 1 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```
