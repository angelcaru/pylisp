(module fun
  (fun foo (a b) (block
    (println a)
    (return b)
  ))
  (fun bar () (block
    (return 69)
  )))