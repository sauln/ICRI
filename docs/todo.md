# TODO

## Bigger
- [x] Build feasibility graph
- [x] push dispatch object through
- [ ] incorporate *robustness* of solution into the cost function
- [ ] integrate changing hyperparameters (delta) into loop
- [ ] more sophisticated method for choosing between possible solutions w/ delta
- [x] incorporate stopping conditions into algo 2
- [ ] build soft timewindows into algo
- [ ] make it faster - there are tons of opportunity for caching and short circuiting

## Smaller
- [x] make Parameters::customers return a shallow copy on `get`
- [ ] Cost functions in rollout only account for two parts of the route 
(base and potential new) but does not incorporate the cost of bridging the two


