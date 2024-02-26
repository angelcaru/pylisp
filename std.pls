(module std
  (fun not (b) (if b false true))
  (fun and (a b) (if a b false))
  (fun or (a b) (if a true b))

  (fun minmax (a b) (
    if (< a b)
      (' a b)
      (' b a)
  ))
  (fun min (a b) (first  (minmax a b)))
  (fun max (a b) (second (minmax a b)))
  (fun pow (base power) 
    (if (= power 0)
      1
      (* base (pow base (- power 1)))
  ))

  (fun len (l) 
    (if (is-empty l)
      0
      (+ 1 (len (tail l)))
  ))

  (fun first (p) (head p))
  (fun second (p) (head (tail p)))

  (fun enumerate (l)
    (foreach (range 0 (len l)) i
      (' i (nth l i))
  ))

  (fun sum (l)
    (reduce l (x a)
      (+ x a) 0
  ))

  (fun unshift (x l)
    (foreach (range 0 (+ (len l) 1)) i
      (if (= i 0)
        x
        (nth l (- i 1))
  )))
  (fun push (x xs) (bind l (len xs)
    (foreach (range 0 (+ l 1)) i
      (if (= i l)
        x
        (nth xs i)
  ))))
)