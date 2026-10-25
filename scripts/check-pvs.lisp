;;; Batch checks for the PVS 8.1 proof API. The caller supplies a private copy.
(in-package :pvs)

(declaim (special *noninteractive* *noninteractive-timeout*
                 *auto-fix-on-rerun* *proof-for-unexpected-branches*
                 *dependings* *proved-dependings* *unproved-dependings*
                 *defn-dependings* *axiom-dependings* *assumption-dependings*
                 *depending-chain* *depending-cycles* *current-context*
                 *possible-judgements* *dont-write-object-files*
                 *in-checker* *justifications-changed?*))

(defvar *ppg-check-root* nil)
(defvar *ppg-check-forced* nil)
(defvar *ppg-check-prepared* nil)
(defvar *ppg-check-last-run* nil)
(defvar *ppg-check-project-files* nil)

(defvar *ppg-check-scope-cache* nil)

(defun ppg-check-project-path-p (path)
  (and (<= (length *ppg-check-root*) (length path))
       (string= *ppg-check-root* path :end2 (length *ppg-check-root*))))

(defun ppg-check-raw-path-equal-p (raw entry)
  ;; Retain a string copy as well: a mutable string designator must not make
  ;; an in-place path change invisible through an EQ cache key.
  (and (equal raw (first entry))
       (string= (namestring raw) (second entry))))

(defun ppg-check-project-module-p (th)
  (and (module? th)
       (let ((raw (context-path th)))
         ;; Relative pathnames depend on the current working directory. Keep
         ;; their original TRUENAME behavior rather than caching that context.
         (if (or (null *ppg-check-scope-cache*)
                 (not (eq (first (pathname-directory (pathname raw))) :absolute)))
             (ppg-check-project-path-p (namestring (truename raw)))
             (let ((entry (gethash th *ppg-check-scope-cache*)))
               (if entry
                   (progn
                     (unless (ppg-check-raw-path-equal-p raw entry)
                       (error "Module context path changed: ~a" (id th)))
                     (fourth entry))
                   (let* ((path (namestring (truename raw)))
                          (project (ppg-check-project-path-p path)))
                     (setf (gethash th *ppg-check-scope-cache*)
                           (list (if (stringp raw) (copy-seq raw) raw)
                                 (copy-seq (namestring raw))
                                 (copy-seq path) project))
                     project)))))))

(defun ppg-check-revalidate-scope-cache ()
  (when *ppg-check-scope-cache*
    (maphash
     (lambda (th entry)
       (unless (module? th) (error "Cached module is no longer a module"))
       (let ((raw (context-path th)))
         (unless (ppg-check-raw-path-equal-p raw entry)
           (error "Module context path changed: ~a" (id th)))
         (let ((path (namestring (truename raw))))
           (unless (and (string= path (third entry))
                        (eq (ppg-check-project-path-p path) (fourth entry)))
             (error "Canonical module context path changed: ~a" (id th))))))
     *ppg-check-scope-cache*))
  t)

(defun ppg-check-input-registry (files)
  (let ((registry (make-hash-table :test #'equal)))
    (dolist (file files)
      (let ((path (namestring (truename file))))
        (unless (ppg-check-project-path-p path)
          (error "Project input is outside the workspace: ~a" file))
        (setf (gethash path registry) t)))
    registry))

(defun ppg-check-explicit-input-module-p (th)
  (and *ppg-check-project-files* (filename th)
       (let ((file (make-pathname :name (filename th) :type "pvs"
                                  :defaults (context-path th))))
         (and (probe-file file)
              (gethash (namestring (truename file)) *ppg-check-project-files*)))))

(defun ppg-check-modules ()
  (remove-if-not
   (lambda (th)
     (and (ppg-check-project-module-p th)
          (or (not (generated-by th)) (ppg-check-explicit-input-module-p th))
          (with-context th (typechecked? th))))
   (collect-all-theories)))

(defun ppg-check-skipped-generated-modules ()
  (remove-if-not
   (lambda (th)
     (and (ppg-check-project-module-p th) (generated-by th)
          (not (ppg-check-explicit-input-module-p th))
          (with-context th (typechecked? th))))
   (collect-all-theories)))

(defun ppg-check-own-body-p (d th)
  (and (not (typep d 'mapped-formula-decl))
       (eq (module d) th)
       (member d (append (theory th) (assuming th)) :test #'eq)))

(defun ppg-check-name (d)
  (format nil "~a.~a" (id (module d)) (id d)))

(defun ppg-check-classify-formulas (modules kinds)
  ;; Remember the classification before execution: an automatic TCC may acquire
  ;; a justification during its proof, but that does not make it an input script.
  (dolist (th modules)
    (with-context th
      (dolist (d (provable-formulas th))
        (if (ppg-check-own-body-p d th)
            (unless (member (gethash d kinds) '(:saved :automatic-tcc :missing))
              (setf (gethash d kinds)
                    (cond ((justification d) :saved)
                          ((eq (kind d) 'tcc) :automatic-tcc)
                          (t :missing))))
            (unless (gethash d kinds)
              (setf (gethash d kinds)
                    (if (typep d 'mapped-formula-decl) :mapped :copied)))))))
  kinds)

(defun ppg-check-formula-counts (kinds forced)
  (let ((own 0) (saved 0) (automatic 0) (mapped 0) (copied 0) (missing 0))
    (maphash
     (lambda (d kind)
       (case kind
         ((:saved :automatic-tcc :missing) (incf own))
         (:mapped (incf mapped))
         (:copied (incf copied)))
       (when (eq kind :missing) (incf missing))
       (when (gethash d forced)
         (ecase kind (:saved (incf saved)) (:automatic-tcc (incf automatic)))))
     kinds)
    (list :own-source-formulas own :existing-justification-bodies saved
          :automatic-tcc-bodies automatic :mapped-copies mapped
          :copied-formulas copied :missing-normal-scripts missing)))

(defun ppg-check-mapped-source (d)
  ;; PVS mapped-formula-decl has its original formula in GENERATED-BY.
  ;; It is not a mapped-decl mixin, and it has no independent saved body.
  (let ((seen nil))
    (loop while (typep d 'mapped-formula-decl) do
      (when (member d seen :test #'eq) (error "Cyclic mapped formula"))
      (push d seen)
      (setf d (generated-by d))
      (unless (formula-decl? d) (error "Mapped formula has no original formula")))
    (let ((th (module d)))
      (when (and (ppg-check-project-module-p th) (ppg-check-own-body-p d th)
                 (not (gethash d *ppg-check-forced*)))
        (error "Mapped original was not replayed: ~a" (ppg-check-name d)))
      (unless (string= (proof-status-string d) "proved - complete")
        (error "Incomplete mapped original: ~a" (ppg-check-name d))))
    t))

;;; Use the same traversal as the standard proof-chain command. In particular,
;;; formal import TCCs and possible judgements must not disappear from a check.
(defun ppg-check-current-dependencies (d)
  (let* ((*dependings* nil) (*proved-dependings* nil) (*unproved-dependings* nil)
         (*defn-dependings* nil) (*axiom-dependings* nil)
         (*assumption-dependings* nil) (*depending-chain* nil)
         (*depending-cycles* nil) (*current-context* (context d))
         (*possible-judgements* (possible-judgements d))
         (initial (union (union (union (refers-to d) (proof-refers-to d))
                                (assuming-tccs d))
                         *possible-judgements*)))
    (when (member nil initial) (error "NIL proof reference in ~a" (ppg-check-name d)))
    (pc-analyze* initial)
    (when (or (member nil *dependings*) *depending-cycles*)
      (error "Unresolved or cyclic proof chain in ~a" (ppg-check-name d)))
    (dolist (dep *dependings*)
      (when (and (formula-decl? dep) (not (axiom? dep)) (not (assumption? dep)))
        (let ((th (module dep)))
          (when (and (ppg-check-project-module-p th) (ppg-check-own-body-p dep th)
                     (not (gethash dep *ppg-check-forced*)))
            (error "Project dependency was not replayed: ~a" (ppg-check-name dep)))
          (unless (or (string= (proof-status-string dep) "proved - complete")
                      (and (typep dep 'mapped-formula-decl)
                           (string= (proof-status-string dep) "proved - by mapping")
                           (ppg-check-mapped-source dep)))
            (error "Incomplete dependency ~a: ~a" (ppg-check-name dep)
                   (proof-status-string dep)))))))
  t)

;;; Required external proof bodies; loading this file only defines helpers.
(in-package :pvs)

(defvar *ppg-check-library-roots* nil)
(defvar *ppg-check-native-forced* nil)
(defvar *ppg-check-native-counts* nil)
(defvar *ppg-check-native-in-flight* nil)
(defvar *ppg-check-native-strategy-contexts* nil)

(defun ppg-check-path-under-p (root path)
  (and (<= (length root) (length path))
       (string= root path :end2 (length root))))

(defun ppg-check-canonical-library-roots (roots)
  (mapcar
   (lambda (root)
     (let* ((path (truename root)) (name (namestring path)))
       (unless (and (null (pathname-name path))
                    (not (ppg-check-path-under-p *ppg-check-root* name))
                    (not (ppg-check-path-under-p name *ppg-check-root*)))
         (error "External library root overlaps the project: ~a" root))
       name))
   (remove-duplicates roots :test #'equal)))

(defun ppg-check-native-original (d)
  (let ((seen nil))
    (loop while (typep d 'mapped-formula-decl) do
      (when (member d seen :test #'eq) (error "Cyclic mapped formula"))
      (push d seen)
      (setf d (generated-by d))
      (unless (formula-decl? d) (error "Mapped formula has no original")))
    d))

(defun ppg-check-native-owner (d)
  ;; A .pvslib mapping may lead outside the copied roots. Check actual source
  ;; and proof-file truenames, including for generated theory objects.
  (let* ((th (module d))
         (directory (and (module? th) (namestring (truename (context-path th)))))
         (source (and directory (filename th)
                      (make-pathname :name (filename th) :type "pvs" :defaults directory)))
         (proof (and source (make-pathname :type "prf" :defaults source)))
         (source-name (and source (probe-file source) (namestring (truename source))))
         (root (and source-name
                    (find-if (lambda (r) (ppg-check-path-under-p r source-name))
                             *ppg-check-library-roots*)))
         (proof-name (and proof (probe-file proof) (namestring (truename proof)))))
    (unless (and root (not (from-prelude? d))
                 (not (typep d 'mapped-formula-decl))
                 (ppg-check-own-body-p d th)
                 (with-context th (and (typechecked? th)
                                       (member d (provable-formulas th) :test #'eq)))
                 (eq th (gethash (id th)
                                (pvs-theories (get-workspace-session (context-path th)))))
                 (or (not proof-name) (ppg-check-path-under-p root proof-name)))
      (error "Required external original has no canonical copied owner: ~a" (ppg-check-name d)))
    (list :declaration d :module th :definition (definition d)
          :source-file source-name :proof-file proof-name :library-root root
          :generated-module (not (null (generated-by th)))
          :generated-declaration (not (null (generated-by d))))))

(defun ppg-check-native-local-proved-p (d)
  (let ((proof (default-proof d)))
    (when (and (null proof) (proofs d))
      (error "Required external proof has no selected default: ~a" (ppg-check-name d)))
    (and proof (member (status proof) '(proved proved-complete proved-incomplete)
                       :test #'string-equal))))

(defun ppg-check-stock-prepared-tcc-p (d input)
  (let* ((th (module d)) (origin (generated-by d))
         (strategy (list "" (list (class-name (class-of d))))))
    (and (eq (kind d) 'tcc) (typep d 'tcc-decl)
         (declaration? origin) (eq (module origin) th)
         (member origin (append (theory th) (assuming th) (formals th)) :test #'eq)
         (equal (tcc-strategy d) strategy)
         (equal input (append strategy (list nil nil))))))

(defun ppg-check-required-native-originals (modules &optional native-roots)
  ;; Recursive stock PC traversal does not add each dependency's ASSUMING TCCs.
  ;; Expand every required original as a root, retaining the Project workspace
  ;; where it was required, including that workspace's judgement fallback.
  (let ((originals (make-hash-table :test #'eq))
        (scopes (make-hash-table :test #'eq))
        (pending nil))
    (labels ((register (dep scope)
               (when (and (formula-decl? dep) (not (axiom? dep)) (not (assumption? dep)))
                 (let ((d (ppg-check-native-original dep)))
                   (unless (or (axiom? d) (assumption? d) (from-prelude? d)
                               (ppg-check-project-module-p (module d)))
                     (unless (gethash d originals)
                       (setf (gethash d originals) (ppg-check-native-owner d)))
                     (unless (assoc *workspace-session* (gethash d scopes) :test #'eq)
                       (push (cons *workspace-session* scope) (gethash d scopes))
                       (push (cons d scope) pending))))))
             (walk (d scope)
               (register d scope)
               (let* ((*dependings* nil) (*proved-dependings* nil) (*unproved-dependings* nil)
                        (*defn-dependings* nil) (*axiom-dependings* nil) (*assumption-dependings* nil)
                        (*depending-chain* nil) (*depending-cycles* nil)
                        (*current-context* (context d))
                        (*possible-judgements* (possible-judgements d))
                        (initial (union (union (union (refers-to d) (proof-refers-to d))
                                                       (assuming-tccs d))
                                        *possible-judgements*)))
                   (when (member nil initial) (error "NIL root proof reference"))
                   (pc-analyze* initial)
                   (when (or (member nil *dependings*) *depending-cycles*)
                     (error "Unresolved or cyclic stock-PC closure"))
                 (dolist (dep *dependings*) (register dep scope)))))
      (dolist (th modules)
        (with-context th
          (dolist (d (provable-formulas th)) (walk d th))))
      ;; Each seed is (actual original . Project module), retained from this
      ;; invocation's previous census, never an unverified path/name lookup.
      (dolist (seed native-roots)
        (assert (and (consp seed) (formula-decl? (car seed)) (module? (cdr seed))))
        (with-context (cdr seed) (register (car seed) (cdr seed))))
      (loop while pending do
        (let ((next (pop pending)))
          (with-context (cdr next) (walk (car next) (cdr next)))))
      (values originals scopes))))

(defun ppg-check-force-native-original (d owner)
  (let* ((th (getf owner :module)) (definition (definition d))
         (proof (default-proof d)) (input (and proof (script proof)))
         (kind (if input :existing-justification :automatic))
         (prepared (and input (null (getf owner :proof-file))
                        (ppg-check-stock-prepared-tcc-p d input)))
         (generator (and prepared (generated-by d)))
         (generator-definition-present
           (and generator (slot-exists-p generator 'definition)
                (slot-boundp generator 'definition)))
         (generator-definition
           (and generator-definition-present (slot-value generator 'definition)))
         (state nil) (open-count nil) (qed nil) (failure nil))
    (assert (not (gethash d *ppg-check-native-forced*)))
    (assert (not (ppg-check-native-local-proved-p d)))
    (assert (equal owner (ppg-check-native-owner d)))
    (unless (or (and input (or (getf owner :proof-file) prepared))
                (and (null input) (eq (kind d) 'tcc)))
      (incf (getf *ppg-check-native-counts* :missing 0))
      (error "Required external body has no permitted original input: ~a" (ppg-check-name d)))
    (let ((entry (append owner (list :input-kind kind :input-script (copy-tree input)
                                     :input-origin (if prepared :stock-prepared-tcc kind)
                                     :input-generator generator
                                     :input-generator-definition generator-definition
                                     :actual-kind (kind d) :input-default proof
                                     :attempted nil :qed nil :open-leaves nil
                                     :proofstate-returned nil :API-result nil :failure nil))))
      ;; Record the attempt before entering the checker. A failed body is never
      ;; retried by the fixed point, and cannot satisfy the final ordinary gates.
      (setf (gethash d *ppg-check-native-forced*) entry
            *ppg-check-native-in-flight* d)
      (with-context th
        (unless (gethash th *ppg-check-native-strategy-contexts*)
          (read-strategies-files)
          (setf (gethash th *ppg-check-native-strategy-contexts*) t))
        (format t "~&PPG-CHECK-NATIVE-INPUT ~s~%"
                (list :name (ppg-check-name d) :source (getf owner :source-file)
                      :proof (getf owner :proof-file) :input-kind kind
                      :input-origin (getf entry :input-origin) :script (getf entry :input-script)))
        (finish-output)
        (assert (and (eq definition (definition d)) (eq proof (default-proof d))
                     (equal (getf entry :input-script)
                            (and (default-proof d) (script (default-proof d))))
                     (eq (kind d) (getf entry :actual-kind))
                     (or (not prepared)
                         (and (eq generator (generated-by d))
                              (ppg-check-stock-prepared-tcc-p d (getf entry :input-script))
                              (or (not generator-definition-present)
                                  (eq generator-definition (slot-value generator 'definition)))))
                     (equal owner (ppg-check-native-owner d))))
        (handler-case
            (let ((*justifications-changed?* nil))
              (incf (getf *ppg-check-native-counts* :attempts 0))
              (incf (getf *ppg-check-native-counts* kind 0))
              (setf (getf entry :attempted) t
                    state (pvs-prove-decl d t))
              (when (typep state 'proofstate)
                (setf open-count (length (collect-all-remaining-subgoals state))))
              (setf qed
                    (and (eq (status (default-proof d)) 'proved)
                         (if input
                             (and (typep state 'top-proofstate)
                                  (eq (status-flag state) '!) (eql open-count 0))
                             ;; Stock PROVE-TCC returns T, not its proofstate.
                             (and (eq (kind d) 'tcc) (eq state t))))))
          (error (condition) (setf failure (princ-to-string condition))))
        ;; Guard failures stop the run, rather than becoming ordinary proof failures.
        (assert (and (eq definition (definition d))
                     (eq (kind d) (getf entry :actual-kind))
                     (or (not prepared)
                         (and (eq generator (generated-by d))
                              (or (not generator-definition-present)
                                  (eq generator-definition (slot-value generator 'definition)))))
                     (equal owner (ppg-check-native-owner d))
                     (not *in-checker*) (null (extra-list-oracles))))
        (setf (getf entry :qed) (not (null qed))
              (getf entry :open-leaves) open-count
              (getf entry :proofstate-returned) (typep state 'proofstate)
              (getf entry :API-result) (if (typep state 'proofstate) :proofstate state)
              (getf entry :failure) failure
              *ppg-check-native-in-flight* nil)
        (incf (getf *ppg-check-native-counts* (if qed :qed :failed) 0))
        (format t "~&PPG-CHECK-NATIVE-RESULT ~a qed=~s open=~s input=~s error=~s~%"
                (ppg-check-name d) (not (null qed)) open-count kind failure)
        (finish-output)))))

(defun ppg-check-required-native-closure (&optional library-roots)
  ;; Callable independently at idle with the retained project bindings. It never
  ;; clears project forces, retypes modules, or reruns locally proved bodies.
  (let ((*ppg-check-library-roots*
          (if library-roots (ppg-check-canonical-library-roots library-roots)
              *ppg-check-library-roots*)))
  (assert (and *ppg-check-native-forced* *ppg-check-native-strategy-contexts*
               *ppg-check-forced* *dont-write-object-files* (not *in-checker*)
               (null (extra-list-oracles))))
  (let ((*noninteractive* t) (*auto-fix-on-rerun* nil)
        (*proof-for-unexpected-branches* nil)
        (project-forces (hash-table-count *ppg-check-forced*))
        (before (getf *ppg-check-native-counts* :attempts 0)))
    ;; Scan Project roots once. Only freshly executed Native bodies acquire new
    ;; proof references; feed those roots and their retained Project scopes back
    ;; into the collector until the required originals settle.
    (multiple-value-bind (originals scopes)
        (ppg-check-required-native-originals (ppg-check-modules))
      (loop for round from 1 to 64 do
        (let ((fresh nil))
          (setf (getf *ppg-check-native-counts* :required) (hash-table-count originals))
          (maphash
           (lambda (d owner)
             (unless (or (gethash d *ppg-check-native-forced*) (ppg-check-native-local-proved-p d))
               (ppg-check-force-native-original d owner)
               (dolist (scope (gethash d scopes))
                 (push (cons d (cdr scope)) fresh)))) originals)
          (unless fresh (return))
          (when (= round 64) (error "Required external proof expansion did not settle"))
          (multiple-value-bind (added added-scopes)
              (ppg-check-required-native-originals nil fresh)
            (maphash
             (lambda (d owner)
               (let ((old (gethash d originals)))
                 (when (and old (not (equal old owner)))
                   (error "Required external owner changed: ~a" (ppg-check-name d)))
                 (setf (gethash d originals) owner))) added)
            (maphash
             (lambda (d contexts)
               (dolist (scope contexts)
                 (unless (assoc (car scope) (gethash d scopes) :test #'eq)
                   (push scope (gethash d scopes))))) added-scopes)))))
    (assert (and (= project-forces (hash-table-count *ppg-check-forced*))
                 (null *ppg-check-native-in-flight*) (null (extra-list-oracles))))
    (unless (and (zerop (getf *ppg-check-native-counts* :failed 0))
                 (loop for entry being the hash-values of *ppg-check-native-forced*
                       always (getf entry :qed)))
      (error "Required external original proof bodies failed"))
    (- (getf *ppg-check-native-counts* :attempts 0) before))))

(defun ppg-check-unforced-project-body-p ()
  (some (lambda (th)
          (with-context th
            (some (lambda (d) (and (ppg-check-own-body-p d th)
                                  (not (gethash d *ppg-check-forced*))))
                  (provable-formulas th))))
        (ppg-check-modules)))


(defun ppg-check-status-file (path complete mode files modules bodies aliases bad counts explicit-generated skipped-generated &optional native-counts)
  (with-open-file (out path :direction :output :if-exists :error
                           :if-does-not-exist :create)
    (format out "{~%  \"complete\": ~a,~%  \"mode\": \"~a\",~%  \"files\": ~d,~%  \"modules\": ~d,~%  \"replayed_bodies\": ~d,~%  \"derived_formulas\": ~d,~%  \"incomplete\": ~d"
            (if complete "true" "false") mode files modules bodies aliases bad)
    (dolist (field '((:own-source-formulas . "own_source_formulas")
                    (:existing-justification-bodies . "existing_justification_bodies")
                    (:automatic-tcc-bodies . "automatic_tcc_bodies")
                    (:mapped-copies . "mapped_copies")
                    (:copied-formulas . "copied_formulas")
                    (:missing-normal-scripts . "missing_normal_scripts")))
      (format out ",~%  \"~a\": ~d" (cdr field) (getf counts (car field) 0)))
    (dolist (field '((:qed . "native_replayed_bodies")
                    (:existing-justification . "native_existing_justification_bodies")
                    (:automatic . "native_automatic_tcc_bodies")
                    (:missing . "native_missing_normal_scripts")
                    (:attempts . "native_force_attempts")
                    (:failed . "native_failed_bodies")
                    (:required . "native_required_originals")))
      (format out ",~%  \"~a\": ~d" (cdr field) (getf native-counts (car field) 0)))
    (format out ",~%  \"explicit_generated_modules\": ~d,~%  \"skipped_implicit_generated_modules\": ~d~%}~%"
            explicit-generated (length skipped-generated))))

(defun ppg-check-run-internal (&optional phase)
  (let* ((manifest-path (environment-variable "PPG_CHECK_MANIFEST"))
         (manifest
           (let ((*read-eval* nil))
             (with-open-file (in manifest-path)
               (let ((form (read in nil :eof)))
                 (assert (not (eq form :eof)))
                 (assert (eq (read in nil :eof) :eof)) form))))
         (*ppg-check-root* (getf manifest :root))
         (*ppg-check-forced* (make-hash-table :test #'eq))
         (*ppg-check-library-roots* (ppg-check-canonical-library-roots (getf manifest :library-roots)))
         (*ppg-check-native-forced* (make-hash-table :test #'eq))
         (*ppg-check-native-counts* nil) (*ppg-check-native-in-flight* nil)
         (*ppg-check-native-strategy-contexts* (make-hash-table :test #'eq))
         (*ppg-check-scope-cache* (make-hash-table :test #'eq))
         (*ppg-check-project-files* nil)
         (mode (getf manifest :mode)) (files (getf manifest :files))
         (project-files (or (getf manifest :project-files) files))
         (timeout (getf manifest :timeout 60))
         (status-path (getf manifest :status-file))
         (typed-files 0) (modules nil) (bodies 0) (aliases 0) (bad 0) (code 1)
         (in-flight nil) (formula-kinds (make-hash-table :test #'eq))
         (counts nil) (skipped-generated nil) (explicit-generated 0))
    (handler-case
        (let ((*auto-fix-on-rerun* nil) (*proof-for-unexpected-branches* nil)
              (*noninteractive* t)
              (*noninteractive-timeout* (and (plusp timeout) timeout)))
          (assert (and (integerp timeout) (not (minusp timeout))))
          (assert (member mode '("proof" "typecheck") :test #'string=))
          (assert (member phase '(nil :prepare :prove)))
          (assert (and files (stringp *ppg-check-root*)))
          (extra-disable-oracles '("_") nil)
          (unless (null (extra-list-oracles)) (error "Oracles remain enabled"))
          (setf *ppg-check-project-files* (ppg-check-input-registry project-files))
          ;; Finish all requested typing before a saved proof is replayed.
          ;; NIL forced? retains already typed imports and their actual objects.
          (if (eq phase :prove)
              (progn
                (assert *ppg-check-prepared*)
                (assert (equal (getf *ppg-check-prepared* :root) *ppg-check-root*))
                (assert (equal (getf *ppg-check-prepared* :files) files))
                (let ((current-modules (ppg-check-modules)))
                  (assert (every (lambda (th) (member th current-modules :test #'eq))
                                 (getf *ppg-check-prepared* :modules))))
                (setf typed-files (getf *ppg-check-prepared* :typed-files)
                      mode "proof"))
              (progn
                (setf *ppg-check-prepared* nil)
                (dolist (file files)
                  (change-workspace (directory-namestring file) t)
                  (typecheck-file (pathname-name file) nil nil nil t)
                  (let ((theories (theories-in-file (pathname-name file))))
                    (unless theories (error "No theories were read from ~a" file))
                    (dolist (th theories)
                      (unless (with-context th (typechecked? th))
                        (error "Theory did not typecheck: ~a" (id th)))))
                  (incf typed-files)
                  (format t "~&PPG-CHECK-TYPED ~d/~d ~a~%" typed-files (length files) file)
                  (finish-output))))
          (setf modules (ppg-check-modules)
                skipped-generated (ppg-check-skipped-generated-modules)
                explicit-generated (count-if #'generated-by modules))
          (ppg-check-classify-formulas modules formula-kinds)
          (when (eq phase :prepare)
            (setf mode "typecheck"
                  status-path (concatenate 'string status-path ".prepared.json")
                  *ppg-check-prepared*
                    (list :root *ppg-check-root* :files (copy-list files)
                          :typed-files typed-files :modules (ppg-check-modules))))
          (when (string= mode "proof")
            ;; Other project libraries, including formal IMPORTING parents, are
            ;; present in the workspace cache. Stock --import-chain omits them.
            ;; A saved proof may load another helper; replay newly found bodies
            ;; once, then check completeness only after the whole batch finishes.
            (loop for round from 1 to 64
                  for fresh = nil do
              (setf modules (ppg-check-modules)
                    skipped-generated (ppg-check-skipped-generated-modules)
                    explicit-generated (count-if #'generated-by modules))
              (ppg-check-classify-formulas modules formula-kinds)
              (dolist (th modules)
                (with-context th
                  (let ((decls
                          (remove-if-not
                           (lambda (d) (and (ppg-check-own-body-p d th)
                                            (not (gethash d *ppg-check-forced*))))
                           (provable-formulas th))))
                    (when decls
                      (setf fresh t)
                      (dolist (d decls)
                        (unless (or (justification d) (eq (kind d) 'tcc))
                          (error "No saved proof for ~a" (ppg-check-name d))))
                      (setf in-flight decls)
                      (proveit-theories (list (cons th decls)) t nil nil nil nil)
                      (dolist (d decls)
                        (setf (gethash d *ppg-check-forced*) t)
                        (incf bodies))
                      (setf in-flight nil)))))
              (when (and (or (= round 1) fresh)
                         (plusp (ppg-check-required-native-closure)))
                (setf fresh t))
              (when (ppg-check-unforced-project-body-p) (setf fresh t))
              (finish-output)
              (unless fresh (return))
              (when (= round 64) (error "Project dependency expansion did not settle")))
            (setf modules (ppg-check-modules))
            (dolist (th modules)
              (with-context th
                (dolist (d (provable-formulas th))
                  (let* ((own (ppg-check-own-body-p d th))
                         (status (proof-status-string d))
                         (complete
                           (or (string= status "proved - complete")
                               (and (not own) (typep d 'mapped-formula-decl)
                                    (string= status "proved - by mapping")
                                    (ppg-check-mapped-source d)))))
                    (unless own (incf aliases))
                    (unless (and complete (or (not own) (gethash d *ppg-check-forced*)))
                      (incf bad)
                      (format t "~&PPG-CHECK-INCOMPLETE ~a ~a~%" (ppg-check-name d) status))
                    (ppg-check-current-dependencies d)))))
            (when (plusp bad) (error "~d formulas are incomplete" bad)))
          (unless modules (setf modules (ppg-check-modules)))
          (ppg-check-classify-formulas modules formula-kinds)
          (ppg-check-revalidate-scope-cache)
          (setf code 0))
      (error (condition)
        (format t "~&PPG-CHECK-ERROR ~a~%" condition)
        (setf code 1)))
    (setf counts (ppg-check-formula-counts formula-kinds *ppg-check-forced*))
    (setf *ppg-check-last-run*
          (list :forced *ppg-check-forced* :modules modules
                :root *ppg-check-root* :files files :typed-files typed-files
                :code code :in-flight-declarations in-flight
                :library-roots *ppg-check-library-roots*
                :native-forced *ppg-check-native-forced* :native-counts *ppg-check-native-counts*
                :native-in-flight *ppg-check-native-in-flight*
                :formula-kinds formula-kinds :formula-counts counts
                :project-files project-files :explicit-generated-modules explicit-generated
                :skipped-implicit-generated-modules skipped-generated))
    (ppg-check-status-file status-path (zerop code) mode typed-files
                           (length modules) bodies aliases bad counts
                           explicit-generated skipped-generated *ppg-check-native-counts*)
    (format t "~&PPG-CHECK-FINISHED code=~d files=~d bodies=~d incomplete=~d~%"
            code typed-files bodies bad)
    (finish-output)
    (if phase code (bye code))))


(defun ppg-check-run (&optional phase)
  ;; The standard switch suppresses only compiled object serialization. It must
  ;; remain in scope during BYE's final SAVE-CONTEXT as well as during checking.
  (let ((*dont-write-object-files* t))
    (ppg-check-run-internal phase)))
