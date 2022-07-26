Number of literals: 7
Constructing lookup tables:
Post filtering unreachable actions: 
[01;34mNo analytic limits found, not considering limit effects of goal-only operators[00m
50% of the ground temporal actions in this problem are compression-safe
Initial heuristic = 3.000, admissible cost estimate 0.000
b (2.000 | 8.000)b (1.000 | 8.000)(G)
; No metric specified - using makespan

; Plan found with metric 8.000
; States evaluated so far: 7
; States pruned based on pre-heuristic cost lower bound: 0
; Time 0.01
0.000: (light_match match1)  [8.000]
0.000: (light_match match2)  [8.000]
3.000: (mend_fuse fuse1 match1)  [5.000]

 * All goal deadlines now no later than 8.000

Resorting to best-first search
Running WA* with W = 5.000, not restarting with goal states

Problem Unsolvable
;;;; Solution Found
; States evaluated: 9
; Cost: 8.000
; Time 0.01
0.000: (light_match match1)  [8.000]
0.000: (light_match match2)  [8.000]
3.000: (mend_fuse fuse1 match1)  [5.000]
