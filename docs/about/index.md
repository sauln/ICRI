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

### Vehicle
Basic concept of the vehicle.  Tracks visited customers, current time, current capacity.

Vehicle supplies functions that help check whether we can add to the list, 
and to find feasible customers.

isFeasible, travelTime, travelDist, geographicCenter, serveCustomer, last.

### Dispatch
Coordinates customers and vehicles. Decides which customers the vehicles serve and when
to add new vehicles.  Supplies a solution

### Parameters
Singleton object that captures the input parameters of the problem and some metaparameters
that are used for calculating the problem.

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

### Cost
Defines multiple different cost functions for defining best next nodes and cost of routes.

