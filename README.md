# LUCES — Formal PVS Theories for Optimal Transport on Embedded Spectral Data

**21 theories, 88 machine-checked theorems**

Formal verification of optimal transport structure observed on a 4-node ESP32 mesh network performing real-time spectral adaptive lighting control.

## Theories

| Theory | Theorems | Topic |
|--------|----------|-------|
| `kantorovich_duality.pvs` | 4 | Kantorovich dual formulation |
| `brenier_uniqueness.pvs` | 3 | Brenier map uniqueness |
| `cyclical_monotonicity.pvs` | 3 | Cyclical monotonicity characterization |
| `displacement_interpolation.pvs` | 5 | McCann displacement interpolation |
| `displacement_concavity.pvs` | 3 | Displacement concavity/convexity |
| `wasserstein_metric.pvs` | 5 | Wasserstein metric properties |
| `transport_structure.pvs` | 8 | Transport map structure |
| `transport_structure_v2.pvs` | 5 | Refined transport structure |
| `transport_stability.pvs` | 5 | Stability of transport maps |
| `stability_of_maps.pvs` | 3 | Map persistence under perturbation |
| `monge_kantorovich_equivalence.pvs` | 3 | Monge-Kantorovich equivalence |
| `lie_generator_structure.pvs` | 10 | Lie generator coherence (T10 key theorem) |
| `fisher_boundary.pvs` | 2 | Fisher information boundary |
| `fisher_voronoi.pvs` | 4 | Fisher-Voronoi partition |
| `dual_observability.pvs` | 4 | Dual observability certificates |
| `hybrid_observability.pvs` | 2 | Hybrid observability |
| `tangent_bundle.pvs` | 6 | Tangent bundle structure |
| `velocity_asymmetry.pvs` | 6 | Dawn/dusk velocity asymmetry |
| `entropy_along_geodesic.pvs` | 5 | Entropy production along geodesics |
| `rank_orientation.pvs` | 2 | Rank and orientation preservation |
| `global_optimality.pvs` | 0 | Global optimality (axioms only) |

## Key Theorem (T10)

```pvs
thm_coherence_iff: THEOREM
  continuously_observed?(p) AND NOT shape_direction_reversal?(p)
    IFF coherent?(p)
```

Validated on 13 independent experiments.

## Related Publications

1. "Empirical Information Geometry on an Embedded Adaptive Lighting System" — [DOI: 10.5281/zenodo.20094759](https://zenodo.org/records/20094759)
2. "Excitation-Dependent Observability Geometry on an Embedded Adaptive Lighting Manifold" — [DOI: 10.5281/zenodo.20389804](https://zenodo.org/records/20389804)
3. (In preparation) "Optimal Transport Geometry of Natural Spectral Regime Transitions"

## System

- Hardware: 4-node ESP32 mesh (ESP32-S3 + ESP32-C6), AS7341 spectral sensor, TSL2591 lux
- Runtime: <2W total, no cloud dependency, FreeRTOS, real-time 7s control loop
- Verification: PVS (Prototype Verification System), NASA Langley

## Author

Dragan Stosic, MSc — [NASA PVS Libraries contributor](https://shemesh.larc.nasa.gov/fm/pvs/PVS-library/library.html#ds)

## License

© 2026 Dragan Stosic. All rights reserved.
