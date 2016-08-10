# About

This is written in an amalgamation of procedural and object oriented code.

There are a set of base objects that are very obviously objects and a set of algorithms
and grouped functions.

I have tried to isolate all of the points of interest into just a few places.

There are a few cost functions in in Algorithms.CostFunction.

These are 
* Cost.ofRoutes - Cost of a routes object
* Cost.vehicleToCustomer - Cost of appending customer to vehicle
* Cost.gnnh - Generalized cost for greedy algorithm.

Cost.ofRoutes and Cost.vehicleToCustomer are used in the roll out algorithm to decide 
which route completion is the best

Cost.gnnh is used to build the greedy route



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

### Parameters
Singleton object that captures the input parameters of the problem and some metaparameters
that are used for calculating the problem.

### PotentialNextCustomer
Temporary object that combines the next customer, the vehicle it is being added to, the 
projected route if this customer is added, and all the costs associated with these actions.


## Algorithms
The algorithms directory contains many objects that describe the main algorithms and 
functions used in the solution. For many of these functions, there were not clear
places to go within an object, so they have found their home here, usually exposed
as static methods.

### Heuristic
Algorithm for building part 1 of the ICRI paper.  Use CostFunction to build solution
using a greedy algorithm

### RollOut
Algorithm for building part 2 of the ICRI paper. 

### Improvement
Procedures for part 3 of the ICRI paper.

### Validator
Helper object that consumes a routes object and confirms that it abides by all our rules.

### NextFinder
Some special static functions to help us find the best next nodes for appending. Returns 
a list of PotentialNextCustomer

### Cost
Defines multiple different cost functions for defining best next nodes and cost of routes.




