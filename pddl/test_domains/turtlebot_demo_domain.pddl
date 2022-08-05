(define (domain turtlebot_demo)

(:requirements :strips :typing :fluents :disjunctive-preconditions :durative-actions)

(:types
	waypoint locatable - object
	robot - locatable
)

(:predicates
	(robot_at ?v - robot ?wp - waypoint)
	(thing_at ?v - object ?wp - waypoint)
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
	:duration (= ?duration (* (distance ?from ?to) 10))
	:condition (and
		(at start (robot_at ?v ?from)))
	:effect (and
		(at start (not (robot_at ?v ?from)))
		(at end (robot_at ?v ?to))
		(increase (distance ?to ?from) (* #t 1))
		)
)

(:derived (visited ?wp) (exists (?r - robot) (at_robot ?r ?wp)))

(:action complicated_action
	:parameters (?v - robot ?w - waypoint ?ugo)
	:precondition (and
		(robot_at ?v ?w)
		(or (robot_at ?v ?w) (thing_at ?ugo ?w))
		(imply (robot_at ?v ?w) (thing_at ?ugo ?w))
		(not (visited ?wp))
		(exists (?wp - waypoint) (thing_at ?ugo ?wp))
		(forall (?wp - waypoint) (thing_at ?ugo ?wp))
		)
	:effect (and
		(visited ?w)
		(when (robot_at ?v ?w) (visited ?w))
		(forall (?wp - waypoint) (visited ?wp))
		(forall (?a ?b - waypoint) (assign (distance ?a ?b) (distance ?from ?to)))
		)
)

)
