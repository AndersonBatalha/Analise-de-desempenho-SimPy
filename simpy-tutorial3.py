#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import simpy

def car(env, name, bcs, driving_time, charge_duration): #nome, estação de carregamento da bateria, tempo dirigindo e tempo de carga
	yield env.timeout(driving_time)
	
	print ("%s chegando a %d" %(name, env.now))
	with bcs.request() as req:
		yield req
		
		print ("%s começou a carregar as baterias em %d" %(name, env.now))
		yield env.timeout(charge_duration)
		print ("%s saiu da estação de carregamento da bateria (BCS) em %d" %(name, env.now))

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(1,5):
	env.process(car(env, "Carro %d" %i, bcs, i * 2, 5))

env.run()
