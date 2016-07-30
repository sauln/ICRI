# About

## Class structure

### Customer
Basic structure of a customer as defined by the Solomon Problem sets

#### Attributes
* custNo - unique ID for the customer. There are no guards enforcing the uniqueness
* xcoord - 
* ycoord - 2D location of the customer
* demand - units of capacity required to service this customer
* readyTime - earliest feasible service time
* dueDate - latest feasible service time
* serviceLen - duration of time that vehicle must service this customer.

### Vehicle
Basic concept of the vehicle.  Tracks visited customers, current time, current capacity.

Vehicle has been broken out into two classes.  The base class handles the adding of 
customers to the list.  This allows the main vehicle class to act just like a 
python list.  The main class sits on top of this list/container construct and adds
functions that help us check whether we can add to the list, and to find feasible customers.

The ListBase class should be reworked in a more idiomatic python way. Look at how the
Matrices singleton object was built.  could we do something like that?



#### Attributes
* customers - list of Customer objects that have been serviced by this vehicle
* curCapacity - current capacity of the vehicle. Each new customer served adds to this. 
* distTravel - current distance that has been traveled by this vehicle
* totalSlack - sum of all slack time by this vehicle
* totalTime - total amount traveled by this vehicle

** these variables should be cleaned up and the names should be uniform. they all 
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

This about making this a singleton also.  Since it is readonly, global would probably be find

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

Please cut out the list aspects of this class into a generic class that is used by both
Routes and Vehicle



#### Attributes
* sp - reference to the solomon problem that this solution was designed for
* vList - list of vehicles

#### Methods


### CostFunction
Defines multiple different cost functions for defining best next nodes and cost of routes.
#### Attributes

#### Methods


### Heuristic
Algorithm for building part 1 of the ICRI paper.  Use CostFunction to build solution
using a greedy algorithm
#### Attributes

#### Methods


### Matrices
Constructors for distance and time matrices.  This should be redefined as a singleton class

This is a singleton class.  Summon by an instantiation:  

`m = Matrices()`

To build the matrices, supply a list of customers to the build function

`m.build(customers)`

#### Attributes

#### Methods


