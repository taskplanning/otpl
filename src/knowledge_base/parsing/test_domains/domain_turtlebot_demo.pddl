(define (domain turtlebot_demo)

(:requirements :strips :typing :fluents :disjunctive-preconditions :durative-actions)

(:types
	waypoint locatable - object
	robot - locatable
)

(:predicates
	(robot_at ?v - robot ?wp - waypoint)
	(visited ?wp - waypoint)
)

(:constants
    kenny - robot
	generic_object
)

(:functions
    (distance ?a ?b - waypoint)
)

;; Move between any two waypoints, avoiding terrain
(:durative-action goto_waypoint
	:parameters (?v - robot ?from ?to - waypoint)
	:duration ( = ?duration (distance ?from ?to))
	:condition (and
		(at start (robot_at ?v ?from)))
	:effect (and
		(at start (not (robot_at ?v ?from)))
		(at end (robot_at ?v ?to)))
)

(:action snap
	:parameters (?v - robot ?w - waypoint)
	:precondition (and (robot_at ?v ?w))
	:effect (and (visited ?w))
)

)
