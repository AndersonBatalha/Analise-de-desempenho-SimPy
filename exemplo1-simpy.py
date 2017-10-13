#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação

# função geradora
def geraChegadas(env,nome,taxa):
	#função que gera chegada de entidades ao sistema
	contaChegada = 0
	while True:
		# random.expovariate --> gera intervalos de tempo aleatórios. lambd é a taxa de ocorrência dos eventos (inverso do tempo médio entre eventos sucessivos)
		yield env.timeout(random.expovariate(1.0/taxa)) # função do simpy que causa um atraso de tempo
		contaChegada += 1
		print "%s %i chega em %.1f" % (nome,contaChegada, env.now)

random.seed(1000) #semente do gerador de números aleatórios
env = simpy.Environment() # ambiente de simulação
env.process(geraChegadas(env, "Cliente", 2)) #cria o processo de chegadas de entidades
env.run(until=10) # roda a simulação por 10 unidades de tempo
