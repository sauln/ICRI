# TODO

## Hyperparameters
Want to approach hyperparameter optimization from two directions:
  
### Traditional Outer loop
* Compare grid search, random search, and sequential grid search
* Learn about sequential parameter tunings, 
* Setup naive in-the-loop adaptive parameter tuning.  Apply ideas from sequential parameter tunings.

### New Heuristics
* Implement new heuristic

### Optimizations
* Profile the roll out and improve slow points

## Bigger
- [ ] incorporate *robustness* of solution into the cost function
- [ ] build soft timewindows into algo
- [ ] make it faster - there are tons of opportunity for caching and short circuiting
- [ ] use O(n) min/max rather than sort+pop.
- [ ] profile time results
- [ ] document profiled results

## Smaller
- [x] make Parameters::customers return a shallow copy on `get`
- [ ] Cost functions in rollout only account for two parts of the route 
(base and potential new) but does not incorporate the cost of bridging the two

