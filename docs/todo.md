# TODO

## Big
- [ ] right now, the routes always has a depot vehicle stub.  This is so the getBestNNodes
step can check what it would be to start from the depot instead of continue another customer
We need to remove this stub and refactor the getBestNNodes so that it goes:
```python
for each cust:
    for each vehicle:
        if feasible add to tmp list
    if tmplist empty
        mainlist add vehicle(depot, cust)
    else
        mainlist add tmplist
```

This will make it so we only consider starting a new vehicle if the cust cannot be reached
by any customers and should considerable cut down on vehicles used. and should cut
down on the amount of iterations in this loop

- [ ] incorporate *robustness* of solution into the cost function
- [ ] integrate changing hyperparameters (delta) into loop
- [ ] incorporate stopping conditions into algo 2
- [ ] build soft timewindows into algo


## Smaller
- [x] numpyify code - lots of very naive implementations - put more operations into 
numpy language to speed up.
- [x] get this task list to render (extensions/tasklist.md?)
- [ ] make Parameters::customers return a shallow copy on `get`


