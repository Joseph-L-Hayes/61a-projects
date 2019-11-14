(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  'replace-this-line)

(define (zip pairs)
    (list (map car pairs) (map cadr pairs))
  )

;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (define enum-list '())
  (define (helper s count)
      (if (null? s) enum-list
        (begin
          (set! enum-list (append enum-list (cons (list count (car s)) nil) ))

          (helper (cdr s) (+ 1 count))
        )
      )
    )
  (helper s 0))
  ; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
  (cond ((= total 0) (list nil) )

        ((or (null? denoms) (< total 0) ) cons nil )

        (else (append (cons-all (car denoms) ;list 1
                  (list-change (- total (car denoms)) denoms )) ;list 2
                    ;list-change with total not including already tested denoms
                    ;and full denom list
                (list-change total (cdr denoms)) ;list 3
              ) ;return list-change with the total and rest of denoms
          ) ;getting denom too big in front and () between lists instead of around
  )
)
  ; (define change ()) ;list to store combos
  (define (cons-all first rests)
          (if (null? rests)
            nil
          (map (lambda (x) (cons first x))  rests) ;had list instead of cons!
          ); cons is okay because we are getting a malformed list as a result
  )
  ;; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))
  ;
(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr)) ;lambda
               (params (cadr expr)) ;(a 1) (b 2)
               (body   (cddr expr))) ;((+ a b))
           ; BEGIN PROBLEM 19
           ;(print (cdr expr))
           (cons form (cons (map let-to-lambda params) (map let-to-lambda body)))
           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr)) ; ((a 1) (b 2))
               (body   (cddr expr))) ;((a b) (1 2)) values
           ; BEGIN PROBLEM 19
           (define zip-val (zip values)) ;created zipped pairs of args and values
           (define args (car zip-val)) ;just the args
           (cons (list 'lambda args (let-to-lambda (car body))) (let-to-lambda (cadr zip-val)))
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
         (map let-to-lambda expr)
         ; END PROBLEM 19
         )))






(define-macro (zero-cond clauses)
  (cons 'cond ;arg 1 of cons
         (map
             (lambda (clause)
               (cons
                 (not (= 0 (eval (car clause))))
                   (cdr clause))) ;first arg to map is proc

                  clauses) ;second arg to map is list
          ;puts clauses into clause
          ;
  )
)

(define (some-cond clauses)
        (cond
            ((map
                (lambda (clause)
                  (cons
                    (not (= 0 (eval (car clause))))
                      (cdr clause))))) clauses
          )
)
