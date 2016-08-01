# About

## Class structure

### Customer
Basic structure of a customer as defined by the Solomon Problem sets

#### Attributes
* custNo - unique ID for the customer. There are no guards enforcing the uniqueness
* xcoord - 2D location of the customer 
* ycoord - 2D location of the customer
* demand - units of capacity required to service this customer
* readyTime - earliest feasible service time
* dueDate - latest feasible service time
* serviceLen - duration of time that vehicle must service this customer.

### Vehicle
Basic concept of the vehicle.  Tracks visited customers, current time, current capacity.

Vehicle inherits a custom ListBase class.  This allows the main vehicle class to 
act just like a python list.  
Vehicle then adds functions that help us check whether we can add to the list, 
and to find feasible customers.

#### Attributes
* customers - list of Customer objects that have been serviced by this vehicle
* curCapacity - current capacity of the vehicle. Each new customer served adds to this. 
* distTravel - current distance that has been traveled by this vehicle
* totalSlack - sum of all slack time by this vehicle
* totalTime - total amount traveled by this vehicle

** TODO these variables should be cleaned up and the names should be uniform. they all 
represent the current sum or state

#### Methods
* `append(next)` - the only way a customer should ever be added to the vehicle
* `travelDistance()` - returns total distance traveled - make this so it is computed while
customers are being added
* `isNotFull(next)` - checks if `next` customer would make this vehicle overfull
* `isValidTime(next)` - checks duedate time of `next` customer is reachable
* `isFeasible(next)` - combines results from `isNotFull` and `isValidTime`
* `lastCustomer()` - returns the last custoemr that was served
* `update(next)` - updates all of the tracked totals given `next` customer being added
    assumes customer is actually being added - currently has no undo.


### SolomonProblem
Basic problem definition of the Solomon Problem set. 

TODO: This about making this a singleton also.  Since it is readonly, global would probably be fine

#### Attributes
* problemName
* numVehicles
* capacity
* customers


### Routes
Solution set.  Container of multiple vehicles.  Manages adding new vehicles or 
adding to existing vehicles (routes). Defines functions for finding top N next nodes 
used in heuristic

One confusing aspect of this class is that it always has a vehicle that is at the depot.
This represents a vehicle that is ready to leave at a moments notice.  It also makes it
much easier to find the best next nodes, because we can look at the cost of leaving
from the depot just the same as from a customer.

#### Attributes
* sp - reference to the solomon problem that this solution was designed for
* objList - 

#### Methods


### CostFunction
Defines multiple different cost functions for defining best next nodes and cost of routes.

Instantiate the class with a string input as heuristicType. Implemented ones are
the gnnh defined in the paper and a distance only.

#### Attributes
* heuristicType - 
* switch - dictionary of possible cost functions

#### Methods
* gnnh - 
* distanceOnly - 


### Parameters
This is parameters object takes the SolomonProblem (or potentially another
problem configuration) and builds the distance matrices.  It then provides the object
as a singleton that can be instantiated as a singleton.

The singleton must be initialzed with the problem definition  

```python
params = Parameters()
params.build(sp: SolomonProblem)
```

Then, it can at any time be cheaply summoned by an easy instantiation:
`params = Parameters()`


#### Methods
* `build` - 
* `buildDistMatrix` -
* `buildTimeMatrix` - 



#### Attributes
* `customers` - list of customers - *this should never be modified* - make a copy and 
modify that.
* `distMatrix` - travel distance matrix from a to b
* `timeMatrix` - expected time to travel from a to b
* `params` - solomon probelm definition




### Heuristic
Algorithm for building part 1 of the ICRI paper.  Use CostFunction to build solution
using a greedy algorithm

#### Attributes

#### Methods

### RollOut
Algorithm for building part 2 of the ICRI paper. 

#### Attributes

#### Methods



### Matrices
Constructors for distance and time matrices.  This should be redefined as a singleton class

This is a singleton class.  
To build the matrices, supply a list of customers to the build function

#### Attributes

#### Methods

### ListBase

#### Attributes

#### Methods
