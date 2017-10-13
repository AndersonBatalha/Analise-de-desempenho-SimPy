#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação
import time

TEMPO_MEDIO_CHEGADAS = 1.0 #tempo médio entre chegadas sucessivas de clientes
TEMPO_MEDIO_ATENDIMENTO = 0.5 #tempo médio de atendimento ao servidor

def geraChegadas(env, servidorRes):
	#função que gera chegada de entidades ao sistema
	contaChegada = 0
	while True:
		# random.expovariate --> gera intervalos de tempo aleatórios. lambd é a taxa de ocorrência dos eventos (inverso do tempo médio entre eventos sucessivos)
		yield env.timeout(random.expovariate(1/TEMPO_MEDIO_CHEGADAS)) # função do simpy que causa um atraso de tempo
		contaChegada += 1
		print "Tempo: %.1f\tChegada do cliente %d" % (env.now, contaChegada)
		env.process(atendimentoServidor(env, "Cliente %d" %(contaChegada), servidorRes))

def atendimentoServidor(env, nome, servidorRes):
	#função que ocupa o servidor e realiza o atendimento
	#solicita o recurso servidorRes
	with servidorRes.request() as request:
		#aguarda na fila até a liberação do recurso e o ocupa
		yield request
		print ("Tempo: %.1f\tServidor inicia o atendimento do %s" % (env.now, nome))
		chegada = env.now
		
		yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
		print ("Tempo: %.1f\tServidor termina o atendimento do %s" % (env.now, nome))
		partida = env.now

		tempoTotal = partida - chegada
		print("Tempo de permanência do cliente %s no sistema: %.2f\n" %(nome, tempoTotal))

random.seed(25) #semente do gerador de números aleatórios
env = simpy.Environment() # cria o ambiente (environment) de simulação
servidorRes = simpy.Resource(env, capacity=1) # cria o recurso de nome servidorRess
env.process(geraChegadas(env, servidorRes)) #inicia o processo de chegadas de entidades
env.run(until=5) # roda a simulação por 10 min
