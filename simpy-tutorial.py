#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import simpy

def car(env):
	while True: 
		print ("Estacionado e carregando as baterias\tTempo: %d" % env.now)
		parking_duration = 5
		yield env.timeout(parking_duration)
		yield env.process(charge(env, 10))
		print ("Dirigindo\t\t\t\tTempo: %d" % env.now)
		trip_duration = 2
		yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until=200)
print "Tempo total de execução: %d" %env.now

