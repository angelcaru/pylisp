(module std
  (fun not (b) (if b false true))
  (fun and (a b) (if a b false))
  (fun or (a b) (if a true b))

  (fun len (l) 
    (if (is-empty l)
      0
      (+ 1 (len (tail l)))
  ))
  (fun nth (l n)
    (if (= n 0)
      (head l)
      (nth (tail l) (- n 1))
  ))
)