# Experiments
Need to start collecting data and running many experiments with many different modifications.
Look into using AWS.  The problems would be well suited for map-reduce.

To facilitate these, and for my own edification, run these experiments on AWS.

1. Run on all 56 problems all of the following with and without parameter tuning:
    * Just the heuristic 
    * Just the rollout
    * Rollout w/ Improvement Algo 
2. Generate reports for each of the following:
    * How rollout and improvement effect the results w.r.t the heuristic.
    * How using parameters found from tuning based on just the heuristic effect the 
  results of the rollout and improvement phases.
        * Is it necessary? and how much improvement can you expect?
    * Comparison with multiple parameter tuning methods
    * Do these reports and results differ if we choose a different heuristic?

# Improvement bounds
From initial experiments it looks like the `improvement` algorithm will often not actually
improve anything.  Very often, the new partial solution is worse than the original input.
I want to explore why this happens. 

* Is there a bug in the code?
* Are there any theoretical results that could determine when the new solution
will be an improvement
* Can I prove any new theoretical results about this `improvement` algorithm?


# Hyperparameters
Approach hyperparameter optimization from two directions:

* Tradiational outer-loop optimization.  
  * Compare grid search, random search, and sequential methods.
  * Learn multi-armed bandit.
* Inside-the-loop optimization.
  * Try tuning mid optimization.
  * Integrate the multi-armed bandit into the `parallel heuristic` rollout step.

# Software
The unittests have fallen to ruin.  Need to update the unittests.  Also need to 
refactor much of the dispatch code.  Lots of it has become entirely too complicated
and can be greatly simplified. I believe I also prematurely optimized for readability 
and there is some very silly code.

At each stable point:

* Profile the code and address biggest weaknesses
* Repair unittests
* Refactor

