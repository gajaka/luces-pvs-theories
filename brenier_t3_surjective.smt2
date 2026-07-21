; brenier_t3_surjective.smt2
; Verify: strictly monotone map on {0,...,N-1} -> {0,...,N-1} is surjective
; i.e., injective function on finite set of same cardinality is surjective
;
; We check for N=20 (concrete instance matching the theory)

(set-logic QF_LIA)

; T is strictly monotone: T(0) < T(1) < ... < T(19)
; and T(i) in {0,...,19}
; Claim: for every j in {0,...,19}, exists i such that T(i) = j

(declare-const t0 Int) (declare-const t1 Int) (declare-const t2 Int)
(declare-const t3 Int) (declare-const t4 Int) (declare-const t5 Int)
(declare-const t6 Int) (declare-const t7 Int) (declare-const t8 Int)
(declare-const t9 Int) (declare-const t10 Int) (declare-const t11 Int)
(declare-const t12 Int) (declare-const t13 Int) (declare-const t14 Int)
(declare-const t15 Int) (declare-const t16 Int) (declare-const t17 Int)
(declare-const t18 Int) (declare-const t19 Int)

; Range: all in {0,...,19}
(assert (and (>= t0 0) (< t0 20)))
(assert (and (>= t1 0) (< t1 20)))
(assert (and (>= t2 0) (< t2 20)))
(assert (and (>= t3 0) (< t3 20)))
(assert (and (>= t4 0) (< t4 20)))
(assert (and (>= t5 0) (< t5 20)))
(assert (and (>= t6 0) (< t6 20)))
(assert (and (>= t7 0) (< t7 20)))
(assert (and (>= t8 0) (< t8 20)))
(assert (and (>= t9 0) (< t9 20)))
(assert (and (>= t10 0) (< t10 20)))
(assert (and (>= t11 0) (< t11 20)))
(assert (and (>= t12 0) (< t12 20)))
(assert (and (>= t13 0) (< t13 20)))
(assert (and (>= t14 0) (< t14 20)))
(assert (and (>= t15 0) (< t15 20)))
(assert (and (>= t16 0) (< t16 20)))
(assert (and (>= t17 0) (< t17 20)))
(assert (and (>= t18 0) (< t18 20)))
(assert (and (>= t19 0) (< t19 20)))

; Strictly monotone
(assert (< t0 t1)) (assert (< t1 t2)) (assert (< t2 t3))
(assert (< t3 t4)) (assert (< t4 t5)) (assert (< t5 t6))
(assert (< t6 t7)) (assert (< t7 t8)) (assert (< t8 t9))
(assert (< t9 t10)) (assert (< t10 t11)) (assert (< t11 t12))
(assert (< t12 t13)) (assert (< t13 t14)) (assert (< t14 t15))
(assert (< t15 t16)) (assert (< t16 t17)) (assert (< t17 t18))
(assert (< t18 t19))

; Negation of surjectivity: exists j not in image
; If strictly monotone on {0..19} with values in {0..19}, then
; t0=0, t1=1, ..., t19=19 is the ONLY possibility.
; So negation: NOT (t0=0 AND t1=1 AND ... AND t19=19) should be unsat
; Actually let's just check: exists j with no preimage
(declare-const j Int)
(assert (>= j 0))
(assert (< j 20))
(assert (not (= j t0))) (assert (not (= j t1))) (assert (not (= j t2)))
(assert (not (= j t3))) (assert (not (= j t4))) (assert (not (= j t5)))
(assert (not (= j t6))) (assert (not (= j t7))) (assert (not (= j t8)))
(assert (not (= j t9))) (assert (not (= j t10))) (assert (not (= j t11)))
(assert (not (= j t12))) (assert (not (= j t13))) (assert (not (= j t14)))
(assert (not (= j t15))) (assert (not (= j t16))) (assert (not (= j t17)))
(assert (not (= j t18))) (assert (not (= j t19)))

(check-sat)
; Expected: unsat (no j exists outside the image)
