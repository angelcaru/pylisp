(module block
  (println (block       // Commented out code: (println "Why?")
    (println "Hello")
    (println "Hi")
    (return "Foo")      // Return a value from the block
  ))
)