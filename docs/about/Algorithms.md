# Algorithms

This page details the pseudocode and mathematical formulation of the algorithms used in this software


# Heuristic

```python
def Heuristic(dispatch):
  ''' dispatch: partially built or newly initiated solution'''
  while c in C:
    vehicles = available_vehicles(dispatch)
    customers = feasible_next_customers(vehicles)
    
    lowest_cost = None
    for vehicle, customer in vehicles, customers:
      cost = GNNH(vehicle, customer)
      if cost < lowest_cost:
        best = vehicle, customer
        lowest_cost = cost
     
     serve(vehicle, customer)

  return dispatch
```


A solution is a set of vehicles and associated constraints (\(\{V\}, \omega \)), possibly empty.
A vehicle is an ordered set of customers.

\(V\) is the set of all vehicles
\(C\) is the set of all customers

\( GNNH: V \times C \rightarrow \mathbb{R}\) is a generalized metric between a vehicle 
and a customer.

\( available\_vehicles: V \rightarrow V \) returns the set of available vehicles.

\( feasible\_next\_customers: \{V\} \rightarrow \{V \times C\} \) maps a set of 
vehicles onto a set of vehicle customer pairs where each customer is a feasible
next customer and each vehicle was in the input set.

## How to you denote that a function goes to a set 
of elements in R? not a tuple or lenght \(n\), but an arbitrarily sized set.



# Rollout 






# Improvement






