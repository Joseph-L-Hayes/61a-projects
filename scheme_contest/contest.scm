;;; Scheme Recursive Art Contest Entry
;;;
;;; Please do not include your name or personal info in this file.
;;;
;;; Title: <Your title here>
;;;
;;; Description:
;;;   <It's your masterpiece.
;;;    Use these three lines to describe
;;;    its inner meaning.>

(define (draw)
  ; YOUR CODE HERE
  (list (forward 100)
       (left 90)
       (forward 100)
       (left 90)
       (forward 100)
       (left 90)
       (forward 100)
       (right 120)
       )
    (list (draw) (right 45))
  (exitonclick))

; Please leave this last line alone.  You may add additional procedures above
; this line.
(draw)
