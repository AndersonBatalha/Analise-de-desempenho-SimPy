#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação

class Simulacao(object):
	
	def __init__(self, env, tempoSimulacao, servidor):
		self.env = env #variavel que representa o ambiente de simulação criado pelo SimPy
		self.tempoSimulacao = tempoSimulacao #tempo em que a simulação é realizada
		self.servidor = servidor #variavel que representa o recurso a ser ocupado

	def __str__(self):
		return "Simulação de um sistema com dois servidores"
	
	def chegadaEntidades(self, TEMPO_MEDIO_CHEGADA, i = 0):
		self.TEMPO_MEDIO_CHEGADA = TEMPO_MEDIO_CHEGADA
		self.i = i
		
		while True:
			yield self.env.timeout(self.TEMPO_MEDIO_CHEGADA)
			self.i += 1
			print "\nCliente %d chegou em %.2f" %(self.i, self.env.now)
			self.env.process(self.atendimento(1, "Cliente %d" %(self.i)))
			
	def atendimento(self, TEMPO_MEDIO_ATENDIMENTO, nomeCliente, request=None):
		self.TEMPO_MEDIO_ATENDIMENTO = TEMPO_MEDIO_ATENDIMENTO
		self.nomeCliente = nomeCliente
		self.request = request
		
		self.request = self.servidor.request()
		yield self.request
		
		print "%.2f %s --> Início do atendimento" %(self.env.now, self.nomeCliente)
		
		yield self.env.timeout(self.TEMPO_MEDIO_ATENDIMENTO)
		
		print "%.2f %s --> Término do atendimento" %(self.env.now, self.nomeCliente)
		self.servidor.release(self.request)



env = simpy.Environment()
s = simpy.Resource(env, capacity=2)
sim = Simulacao(env, 20, s)
env.process(sim.chegadaEntidades(0.5))
sim.env.run(sim.tempoSimulacao)

