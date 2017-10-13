#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação


def distribution(tipo):
	return {"arrival": random.expovariate(1/10.0), "singing": random.triangular(10,20,30), "applause": random.gauss(10,1)}.get(tipo,0.0)

# função geradora
def geraChegadas(env,nome,taxa, numeroMaxChegadas,tipo):
	#função que gera chegada de entidades ao sistema
	contaChegada = 0
	while contaChegada < numeroMaxChegadas:
		# random.expovariate --> gera intervalos de tempo aleatórios. lambd é a taxa de ocorrência dos eventos (inverso do tempo médio entre eventos sucessivos)
		yield env.timeout(distribution(tipo)) # função do simpy que causa um atraso de tempo
		contaChegada += 1
		print "%s %i chega em %.1f" % (nome,contaChegada, env.now)

random.seed(25) #semente do gerador de números aleatórios
env = simpy.Environment() # ambiente de simulação
env.process(geraChegadas(env, "Cliente", 2, 5, "arrival")) #cria o processo de chegadas de entidades
env.run(until=10) # roda a simulação por 10 unidades de tempo
