(define (domain basic_logistics)
(:requirements :strips :typing)
    
    (:types 
        location locatable - object
        package truck driver - locatable
    )
    
    (:predicates
        (connected ?from ?to - location)

        (locatable_at ?o - locatable ?l - location)
        (in ?p - package ?t - truck)
        (driving ?d - driver ?t - truck)
    )
    
    ;;================;;
    ;; driver actions ;;
    ;;================;;
    
    (:action walk
      :parameters (?d - driver ?from ?to - location)
      :precondition (and
        (locatable_at ?d ?from)
        (connected ?from ?to)
      )
      :effect (and
        (not (locatable_at ?d ?from))
        (locatable_at ?d ?to)
      )
    )
    
    (:action board_vehicle
      :parameters (?t - truck ?d - driver ?wp - location)
      :precondition (and
        (locatable_at ?d ?wp)
        (locatable_at ?t ?wp)
      )
      :effect (and
        (not (locatable_at ?d ?wp))
        (driving ?d ?t)
      )
    )
    
    (:action disembark_vehicle
      :parameters (?t - truck ?d - driver ?wp - location)
      :precondition (and
        (driving ?d ?t)
        (locatable_at ?t ?wp)
      )
      :effect (and
        (not (driving ?d ?t))
        (locatable_at ?d ?wp)
      )
    )
    
    ;;=================;;
    ;; vehicle actions ;;
    ;;=================;;
    
    (:action drive_truck
      :parameters (?t - truck ?d - driver ?from ?to - location)
      :precondition (and
        (locatable_at ?t ?from)
        (connected ?from ?to)
        (driving ?d ?t)
      )
      :effect (and
        (not (locatable_at ?t ?from))
        (locatable_at ?t ?to)
      )
    )
    
    ;;=================;;
    ;; package actions ;;
    ;;=================;;
    
    (:action load_package
      :parameters (?t - truck ?p - package ?wp - location)
      :precondition (and
        (locatable_at ?p ?wp)
        (locatable_at ?t ?wp)
      )
      :effect (and
        (not (locatable_at ?p ?wp))
        (in ?p ?t)
      )
    )
    
    (:action unload_package
      :parameters (?t - truck ?p - package ?wp - location)
      :precondition (and
        (in ?p ?t)
        (locatable_at ?t ?wp)
      )
      :effect (and
        (not (in ?p ?t))
        (locatable_at ?p ?wp)
      )
    )
    
)