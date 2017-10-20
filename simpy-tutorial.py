#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

def geraChegadas(env, nome, taxa):
	#função que gera chegadas de entidades no sistema, a uma taxa definida pela variável "taxa"
	contaChegada = 0
	while True:
		#random.expovariate gera intervalos de tempo exponencialmente distribuídos --> 1.0/taxa
		yield env.timeout(random.expovariate(lambd=1.0/taxa)) # yield retorna um gerador que causa um atraso de tempo definido por env.timeout
		contaChegada += 1 # contador
		print "%.2f %s %i chegou ao sistema" %(env.now, nome, contaChegada) 

random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números gerados será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
env.process(geraChegadas(env, "Cliente", 2)) # cria o processo de chegadas definido pela função "geraChegadas"
env.run(until=25) # executa a simulação por 10 unidades de tempo
