;;; Avoid recursive binary cache serialization between project libraries.
(in-package :pvs)
(setf *dont-write-object-files* t)
