(define (problem problem_temporal_logistics)
(:domain temporal_logistics)
(:requirements :strips :typing :fluents :durative-actions :timed-initial-literals)
    
    (:objects 
        wp_sky wp_sea wp1 wp2 wp3 wp4 wp5 wp6 wp7 wp8 wp9 wp10 wp11 - location
        t1 t2 - truck
        dr1 dr2 - driver
        b1 - boat
        p1 - plane
        pack1 pack2 pack3 pack4 - package
    )
    
    (:init
        ;; drivers
        (locatable_at dr1 wp4)
        (locatable_at dr2 wp1)
        (= (walking-speed dr1) 0.5)
        (= (walking-speed dr2) 0.5)
        
        ;; trucks
        (locatable_at t1 wp6)
        (locatable_at t2 wp9)
        (= (driving-speed t1) 1.0)
        (= (driving-speed t2) 1.0)
        
        ;; other vehicles
        (locatable_at b1 wp_sea)
        (locatable_at p1 wp_sky)
        (= (driving-speed b1) 1.5)
        (= (driving-speed p1) 2.0)
        
        ;; packages
        (locatable_at pack1 wp2)
        (locatable_at pack2 wp3)
        (locatable_at pack3 wp5)
        (locatable_at pack4 wp11)
        
        (deliverable pack1)
        (deliverable pack2)
        (deliverable pack3)
        (deliverable pack4)
        
        ;; shortest possible deadline on pack1
        (at 321 (not (deliverable pack1)))
        
        ;; short deadline on package deliveries
        (at 1931 (not (deliverable pack2)))
        (at 1931 (not (deliverable pack3)))
        (at 1931 (not (deliverable pack4)))
        
        ;; Ground Connections
        (connected wp1 wp2) (= (distance wp1 wp2) 100)
        (connected wp2 wp1) (= (distance wp2 wp1) 100)
        (connected wp2 wp3) (= (distance wp2 wp3) 100)
        (connected wp3 wp2) (= (distance wp3 wp2) 100)
        (connected wp1 wp5) (= (distance wp1 wp5) 100)
        (connected wp5 wp1) (= (distance wp5 wp1) 100)
        (connected wp5 wp6) (= (distance wp5 wp6) 50)
        (connected wp6 wp5) (= (distance wp6 wp5) 50)
        (connected wp6 wp7) (= (distance wp6 wp7) 50)
        (connected wp7 wp6) (= (distance wp7 wp6) 50)
        (connected wp2 wp6) (= (distance wp2 wp6) 75)
        (connected wp6 wp2) (= (distance wp6 wp2) 75)
        (connected wp3 wp8) (= (distance wp3 wp8) 75)
        (connected wp8 wp3) (= (distance wp8 wp3) 75)
        (connected wp8 wp11) (= (distance wp8 wp11) 75)
        (connected wp11 wp8) (= (distance wp11 wp8) 75)
        (connected wp10 wp11) (= (distance wp10 wp11) 100)
        (connected wp11 wp10) (= (distance wp11 wp10) 100)
        (connected wp10 wp9) (= (distance wp10 wp9) 100)
        (connected wp9 wp10) (= (distance wp9 wp10) 100)
        (connected wp9 wp4) (= (distance wp9 wp4) 75)
        (connected wp4 wp9) (= (distance wp4 wp9) 75)
        (connected wp1 wp4) (= (distance wp1 wp4) 75)
        (connected wp4 wp1) (= (distance wp4 wp1) 75)
        
        ;; Sea Connections
        (connected-sea wp_sea wp7) (= (distance wp_sea wp7) 75)
        (connected-sea wp7 wp_sea) (= (distance wp7 wp_sea) 75)
        
        ;; Sky Connections
        (connected-sky wp_sky wp2) (= (distance wp_sky wp2) 20)
        (connected-sky wp2 wp_sky) (= (distance wp2 wp_sky) 20)
        (connected-sky wp_sky wp4) (= (distance wp_sky wp4) 20)
        (connected-sky wp4 wp_sky) (= (distance wp4 wp_sky) 20)
    )
    
    (:goal (and 
        
        ;; drivers home
        (locatable_at dr1 wp1)
        (locatable_at dr2 wp1)
        
        ;; packages delivered
        (locatable_at pack1 wp9)
        (locatable_at pack2 wp_sea)
        (locatable_at pack3 wp9)
        (locatable_at pack4 wp2)
    ))
)