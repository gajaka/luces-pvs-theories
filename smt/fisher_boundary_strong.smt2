; fisher_boundary_strong.smt2
; Verify: for any non-axis-aligned centers c1, c2 and non-conformal metric w1 /= w2,
; there exists a point x where Euclidean and Fisher nearest-center assignments differ.
;
; Strategy: assert the NEGATION (no such x exists) and check for UNSAT.
; UNSAT means the negation is impossible, hence the theorem holds.

(set-logic QF_NRA)

; Metric weights (positive, different)
(declare-const w1 Real)
(declare-const w2 Real)
(assert (> w1 0))
(assert (> w2 0))
(assert (not (= w1 w2)))

; Centers (differ in both coordinates)
(declare-const c1x Real)
(declare-const c1y Real)
(declare-const c2x Real)
(declare-const c2y Real)
(assert (not (= c1x c2x)))
(assert (not (= c1y c2y)))

; Negation of the theorem:
; For ALL x: (dist_e(x,c1) <= dist_e(x,c2)) = (dist_w(x,c1) <= dist_w(x,c2))
;
; dist_e(x,c1) = (x0-c1x)^2 + (x1-c1y)^2
; dist_e(x,c2) = (x0-c2x)^2 + (x1-c2y)^2
; dist_w(x,c1) = w1*(x0-c1x)^2 + w2*(x1-c1y)^2
; dist_w(x,c2) = w1*(x0-c2x)^2 + w2*(x1-c2y)^2
;
; Euclidean comparison simplifies to:
;   dist_e(x,c1) <= dist_e(x,c2)  IFF  2*(c2x-c1x)*x0 + 2*(c2y-c1y)*x1 >= c2x^2-c1x^2 + c2y^2-c1y^2
;
; Fisher comparison simplifies to:
;   dist_w(x,c1) <= dist_w(x,c2)  IFF  2*w1*(c2x-c1x)*x0 + 2*w2*(c2y-c1y)*x1 >= w1*(c2x^2-c1x^2) + w2*(c2y^2-c1y^2)
;
; Let dx = c2x - c1x, dy = c2y - c1y (both nonzero)
; Let sx = c2x + c1x, sy = c2y + c1y
;
; Euclidean bisector: dx*x0 + dy*x1 = (dx*sx + dy*sy)/2
; Fisher bisector:    w1*dx*x0 + w2*dy*x1 = (w1*dx*sx + w2*dy*sy)/2
;
; The negation says: for all x, the side of Euclidean bisector = side of Fisher bisector.
; Two different lines through the same point (midpoint) divide the plane into regions.
; If the lines are different, there exist points on one side of one but other side of the other.
; Lines are different when (dx, dy) and (w1*dx, w2*dy) are not proportional,
; which happens when w1 /= w2 (since dx /= 0 and dy /= 0).

; We encode: for ALL x0, x1, the two comparisons agree
(declare-const x0 Real)
(declare-const x1 Real)

; Euclidean: dist_e(x,c1) <= dist_e(x,c2)
; Expands to: (x0-c1x)^2 + (x1-c1y)^2 <= (x0-c2x)^2 + (x1-c2y)^2
; Simplifies to: 2*(c2x-c1x)*x0 + 2*(c2y-c1y)*x1 >= c2x^2 - c1x^2 + c2y^2 - c1y^2

(define-fun eucl_le () Bool
  (<= (+ (* (- x0 c1x) (- x0 c1x)) (* (- x1 c1y) (- x1 c1y)))
      (+ (* (- x0 c2x) (- x0 c2x)) (* (- x1 c2y) (- x1 c2y)))))

(define-fun fisher_le () Bool
  (<= (+ (* w1 (* (- x0 c1x) (- x0 c1x))) (* w2 (* (- x1 c1y) (- x1 c1y))))
      (+ (* w1 (* (- x0 c2x) (- x0 c2x))) (* w2 (* (- x1 c2y) (- x1 c2y))))))

; Negation: for this x, both agree (= means IFF for booleans)
(assert (= eucl_le fisher_le))

; If UNSAT: no x can make them agree for ALL x under the given constraints
; But wait - we need FORALL x. With QF_NRA we can't do forall.
; Instead: we show that the two bisector LINES are different.
; If lines are different, there exist points where they disagree.
;
; Alternative encoding: assert that the two half-planes are IDENTICAL,
; which means the normal vectors are proportional: (dx, dy) ~ (w1*dx, w2*dy)
; i.e., w1/1 = w2/1, i.e., w1 = w2. Contradiction.

; Actually, let's encode it directly with quantifiers using NRA (not QF_NRA):

(reset)
(set-logic NRA)

(declare-const w1 Real)
(declare-const w2 Real)
(assert (> w1 0))
(assert (> w2 0))
(assert (not (= w1 w2)))

(declare-const c1x Real)
(declare-const c1y Real)
(declare-const c2x Real)
(declare-const c2y Real)
(assert (not (= c1x c2x)))
(assert (not (= c1y c2y)))

; Negation of EXISTS x such that comparisons differ:
; FORALL x: comparisons agree
(assert
  (forall ((x0 Real) (x1 Real))
    (= (<= (+ (* (- x0 c1x) (- x0 c1x)) (* (- x1 c1y) (- x1 c1y)))
            (+ (* (- x0 c2x) (- x0 c2x)) (* (- x1 c2y) (- x1 c2y))))
       (<= (+ (* w1 (* (- x0 c1x) (- x0 c1x))) (* w2 (* (- x1 c1y) (- x1 c1y))))
            (+ (* w1 (* (- x0 c2x) (- x0 c2x))) (* w2 (* (- x1 c2y) (- x1 c2y))))))))

(check-sat)
; Expected: unsat (theorem holds)
