(define (problem task)
(:domain turtlebot_demo)
(:requirements :strips :typing :fluents :disjunctive-preconditions :durative-actions)
(:objects
    kenny - robot
    wp1 wp2 wp3 
    wp4 wp5 wp6 - waypoint
    ugo
)
(:init
    (robot_at kenny wp1)
    (thing_at ugo wp4)
    (thing_at wp1 wp4)
    (= (distance wp1 wp2) 100)
    (= (distance wp1 wp2) 150)
    (at 200 (thing_at ugo wp8))
)
(:goal (and
    (robot_at kenny wp6)
))
(:metric minimize (distance wp1 wp2))
)
