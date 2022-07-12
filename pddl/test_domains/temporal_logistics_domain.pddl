(define (domain temporal_logistics)
(:requirements :strips :typing :fluents :durative-actions :timed-initial-literals)
    
    (:types 
        location locatable - object
        package vehicle driver - locatable
        truck plane boat - vehicle
    )
    
    (:predicates
        (connected ?from ?to - location)
        (connected-sky ?from ?to - location)
        (connected-sea ?from ?to - location)
        
        (locatable_at ?o - locatable ?l - location)
        (in ?p - package ?v - vehicle)
        (driving ?d - driver ?v - vehicle)
        (deliverable ?p - object)
    )
    
    (:functions
        (distance ?from ?to - location)
        (walking-speed ?d - driver)
        (driving-speed ?v - vehicle)
    )
    
    ;;================;;
    ;; driver actions ;;
    ;;================;;
    
    (:durative-action walk
      :parameters (?d - driver ?from ?to - location)
      :duration (= ?duration (/ (distance ?from ?to) (walking-speed ?d)))
      :condition (and
        (at start (locatable_at ?d ?from))
        (over all (connected ?from ?to))
      )
      :effect (and
        (at start (not (locatable_at ?d ?from)))
        (at end (locatable_at ?d ?to))
      )
    )
    
    (:durative-action board_vehicle
      :parameters (?v - vehicle ?d - driver ?wp - location)
      :duration (= ?duration 10)
      :condition (and
        (at start (locatable_at ?d ?wp))
        (over all (locatable_at ?v ?wp))
      )
      :effect (and
        (at start (not (locatable_at ?d ?wp)))
        (at end (driving ?d ?v))
      )
    )
    
    (:durative-action disembark_vehicle
      :parameters (?v - vehicle ?d - driver ?wp - location)
      :duration (= ?duration 10)
      :condition (and
        (at start (driving ?d ?v))
        (over all (locatable_at ?v ?wp))
      )
      :effect (and
        (at start (not (driving ?d ?v)))
        (at end (locatable_at ?d ?wp))
      )
    )
    
    ;;=================;;
    ;; vehicle actions ;;
    ;;=================;;
    
    (:durative-action drive_truck
      :parameters (?t - truck ?d - driver ?from ?to - location)
      :duration (= ?duration (/ (distance ?from ?to) (driving-speed ?t)))
      :condition (and
        (at start (locatable_at ?t ?from))
        (over all (connected ?from ?to))
        (over all (driving ?d ?t))
      )
      :effect (and
        (at start (not (locatable_at ?t ?from)))
        (at end (locatable_at ?t ?to))
      )
    )
    
    (:durative-action move_plane
      :parameters (?p - plane ?from ?to - location)
      :duration (= ?duration (/ (distance ?from ?to) (driving-speed ?p)))
      :condition (and
        (at start (locatable_at ?p ?from))
        (over all (connected-sky ?from ?to))
      )
      :effect (and
        (at start (not (locatable_at ?p ?from)))
        (at end (locatable_at ?p ?to))
      )
    )
    
    (:durative-action move_boat
      :parameters (?b - boat ?from ?to - location)
      :duration (= ?duration (/ (distance ?from ?to) (driving-speed ?b)))
      :condition (and
        (at start (locatable_at ?b ?from))
        (over all (connected-sea ?from ?to))
      )
      :effect (and
        (at start (not (locatable_at ?b ?from)))
        (at end (locatable_at ?b ?to))
      )
    )

    ;;=================;;
    ;; package actions ;;
    ;;=================;;
    
    (:durative-action load_package
      :parameters (?v - vehicle ?p - package ?wp - location)
      :duration (= ?duration 10)
      :condition (and
        (at start (locatable_at ?p ?wp))
        (over all (locatable_at ?v ?wp))
      )
      :effect (and
        (at start (not (locatable_at ?p ?wp)))
        (at end (in ?p ?v))
      )
    )
    
    (:durative-action unload_package
      :parameters (?v - vehicle ?p - package ?wp - location)
      :duration (= ?duration 10)
      :condition (and
        (at start (in ?p ?v))
        (over all (locatable_at ?v ?wp))
        (at start (deliverable ?p))
      )
      :effect (and
        (at start (not (in ?p ?v)))
        (at end (locatable_at ?p ?wp))
      )
    )
    
)