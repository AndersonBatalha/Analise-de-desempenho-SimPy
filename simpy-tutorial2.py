#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import simpy

class Car(object):
	def __init__(self, env):
		self.env = env
		self.action = env.process(self.run()) # a execução começa quando a instância for criada
		
	def run(self):
		 while True:
			print ("Veículo estacionado e baterias sendo carregadas em %d" %self.env.now)
			charge_duration=5
			yield self.env.process(self.charge(charge_duration))
			
			print ("Dirigindo em %d" %self.env.now)
			trip_duration=2
			yield self.env.timeout(trip_duration)
			
	def charge(self, duration):
		yield self.env.timeout(duration)

env=simpy.Environment()
carro = Car(env)
env.run(until=15)

print("\n\n\n\n\n\n")

#Interrupção de eventos

def driver(env, car):
	yield env.timeout(3)
	car.action.interrupt()

class Car(object):
	def __init__(self, env):
		self.env = env
		self.action = env.process(self.run()) # a execução começa quando a instância for criada
		
	def run(self):
		 while True:
			print ("Veículo estacionado e baterias sendo carregadas em %d" %self.env.now)
			charge_duration=5
			try:
				yield self.env.process(self.charge(charge_duration))
			except simpy.Interrupt:
				print "Foi interrompido. A bateria está cheia o suficiente"
			
			print ("Dirigindo em %d" %self.env.now)
			trip_duration=2
			yield self.env.timeout(trip_duration)
			
	def charge(self, duration):
		yield self.env.timeout(duration)


env=simpy.Environment()
carro = Car(env)
env.process(driver(env,carro))
env.run(until=15)
