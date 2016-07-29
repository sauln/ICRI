# About

## Class structure

### Customer
Basic structure of a customer as defined by the Solomon Problem sets

### Vehicle
Basic concept of the vehicle.  Tracks visited customers, current time, current capacity.

### SolomonProblem
Basic problem definition of the Solomon Problem set. 

### Routes
Solution set.  Container of multiple vehicles.  Manages adding new vehicles or 
adding to existing vehicles (routes). Defines functions for finding top N next nodes 
used in heuristic

### CostFunction
Defines multiple different cost functions for defining best next nodes and cost of routes.

### Heuristic
Algorithm for building part 1 of the ICRI paper.  Use CostFunction to build solution
using a greedy algorithm

### Matrices
Constructors for distance and time matrices.  This should be redefined as a singleton class

### 





## Algorithm Components
