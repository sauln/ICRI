# About

This is written in an amalgamation of procedural and object oriented code.

There are a set of base objects that are very obviously objects and a set of algorithms
and grouped functions.


## Base objects


### Customer
Basic structure of a customer as defined by the Solomon Problem sets

### SolomonProblem
Basic problem definition of the Solomon Problem set. 

### ListBase
Supplies list base so we can use Routes and Vehicle as a list

### Vehicle
Basic concept of the vehicle.  Tracks visited customers, current time, current capacity.

Vehicle inherits a custom ListBase class.  This allows the main vehicle class to 
act just like a python list.  
Vehicle then adds functions that help us check whether we can add to the list, 
and to find feasible customers.

This houses functions that determine whether adding a customer to it is feasible,
and micromanages

### Routes
Solution set.  Container of multiple vehicles.  Manages adding new vehicles or 
adding to existing vehicles (routes). Defines functions for finding top N next nodes 
used in heuristic

One confusing aspect of this class is that it always has a vehicle that is at the depot.
This represents a vehicle that is ready to leave at a moments notice.  It also makes it
much easier to find the best next nodes, because we can look at the cost of leaving
from the depot just the same as from a customer.

### Parameters
Singleton object that captures the input parameters of the problem and some metaparameters
that are used for calculating the problem.


## Algorithms



### CostFunction
Defines multiple different cost functions for defining best next nodes and cost of routes.

Instantiate the class with a string input as heuristicType. Implemented ones are
the gnnh defined in the paper and a distance only.

### RollOut
Algorithm for building part 2 of the ICRI paper. 


### Heuristic
Algorithm for building part 1 of the ICRI paper.  Use CostFunction to build solution
using a greedy algorithm

