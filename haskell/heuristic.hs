module Main where

data Customer = Customer Float Float deriving (Show)

a = Customer 0 0
b = Customer 1 1
c = Customer 1 2
d = Customer 2 2
e = Customer 0 1.5
f = Customer 1 0.5
g = Customer 0.5 0.4
h = Customer 3 3

cs = [b,c,d,e,f,g,h]

-- Euclidean distance between two customers
dist :: Customer -> Customer -> Float
dist (Customer xa ya) (Customer xb yb) = sqrt ((xa - xb)^2 + (ya - yb)^2)

-- a function, 2 items, return an item
minarg :: (Ord b) => (a -> b) -> a -> a -> a
minarg f a b 
    | f a <= f b = a
    | otherwise  = b

closest xs x = foldr1 (minarg $ dist x) xs
bz = closest cs a


main = do putStrLn "Distance between two customers"
          print bz

