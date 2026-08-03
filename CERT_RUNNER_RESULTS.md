# Certificate Runner — Paper 3 Final Dataset

22 certificates evaluated on 8 independent experiments (5 dawn, 3 dusk).
PPG certificates (PPG, RES, DET, CCI, ATL) achieve 100% PASS on all logs.
DEV classifies each log into balanced/transitional/unbalanced regime.

---

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
  CCI Curv-Coh Inverse:     PASS   r=-0.718 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=1.01 κ=100.8 coh=0.737 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0289 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 23 PASS / 0 FAIL / 3 DIAG / 1 N/A
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
  CCI Curv-Coh Inverse:     PASS   r=-0.858 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=1.92 κ=92.3 coh=0.679 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0357 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 24 PASS / 0 FAIL / 3 DIAG
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
  CCI Curv-Coh Inverse:     PASS   r=-0.896 n=9
  DEV Deviation Regime:     DIAG   UNBALANCED Dev=3.91 κ=291.4 coh=0.679 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0532 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 21 PASS / 2 FAIL / 1 BORDER / 2 DIAG / 1 INFO
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
  CCI Curv-Coh Inverse:     PASS   r=-0.884 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=2.65 κ=164.5 coh=0.637 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0270 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 23 PASS / 1 FAIL / 3 DIAG
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
  CCI Curv-Coh Inverse:     PASS   r=-0.570 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=1.76 κ=176.2 coh=0.782 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0467 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 22 PASS / 1 FAIL / 1 BORDER / 2 DIAG / 1 INFO
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
  CCI Curv-Coh Inverse:     PASS   r=-0.571 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=2.60 κ=259.9 coh=0.727 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0321 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 20 PASS / 3 FAIL / 1 BORDER / 2 DIAG / 1 INFO
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
  CCI Curv-Coh Inverse:     PASS   r=-0.824 n=10
  DEV Deviation Regime:     DIAG   UNBALANCED Dev=4.22 κ=422.1 coh=0.722 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0460 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 21 PASS / 2 FAIL / 1 BORDER / 2 DIAG / 1 INFO
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
  CCI Curv-Coh Inverse:     PASS   r=-0.793 n=10
  DEV Deviation Regime:     DIAG   TRANSITIONAL Dev=1.43 κ=142.7 coh=0.851 rev=False exc=0.0000
  ATL Atlas Consistency:    PASS   min_d=0.0434 (TRANS↔DAY) k=3

═══════════════════════════════════════════════════════
  Summary: 21 PASS / 2 FAIL / 1 BORDER / 2 DIAG / 1 INFO
═══════════════════════════════════════════════════════
```
