#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Desafio 7: retome o problema da lavanderia (Desafio 6). Estime o tempo médio que os clientes atendidos aguardaram pela lavadora. Dica: você precisará de uma variável global para o cálculo do tempo de espera e um atributo para marcar a hora de chegada no sistema.

#Desafio 8: no desafio anterior, caso você simule por 10 ou mais horas, deve notar como o tempo de espera pela lavadora fica muito alto. Para identificar o gargalo do sistema, acrescente a impressão do número de clientes que ficaram em fila ao final da simulação. Você consegue otimizar o sistema a partir do modelo construído?

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

def distributions(tipo):
	return {"chegadas": random.expovariate(1.0/5.0), "lavagem": 20, "carregar": random.uniform(1,4), "descarregar": random.uniform(1,2), "secagem": random.uniform(9,12)}.get(tipo)

def geraChegadas(env, nome, Lavadora, Secadora, Cesto):
	#função que gera chegadas de entidades no sistema, a uma taxa definida pela variável TEMPO_MEDIO_CHEGADAS
	contaChegada = 0
	while True:
		#random.expovariate gera intervalos de tempo exponencialmente distribuídos --> 1.0/taxa
		yield env.timeout(distributions("chegadas")) # yield retorna um gerador que causa um atraso de tempo definido por env.timeout
		contaChegada += 1 # contador
		print "\n%.2f - %s %i chegou na lavanderia" %(env.now, nome, contaChegada) 
		env.process(Atendimento(env, nome + " " + str(contaChegada), Lavadora, Secadora, Cesto))

def Atendimento(env, nome, lavadora, secadora, cesto):
	reqLavadora = lavadora.request() #cliente requisita o uso da máquina de lavar roupas
	yield reqLavadora # aguarda até o recurso estar disponível
	print "%.2f - %s iniciou a lavagem das roupas" % (env.now, nome) # imprime o tempo em que iniciou a utilizar o recurso
	yield env.timeout(distributions("lavagem")) 
	print "%.2f - %s terminou a lavagem das roupas" % (env.now, nome) # imprime o tempo em que acabou de utilizar o recurso
	reqCesto = cesto.request() # pega o cesto de roupas antes de liberar a máquina de lavar
	yield lavadora.release(reqLavadora) #libera o recurso lavadora
	print "%.2f - %s está levando o cesto de roupas para a secadora" % (env.now, nome) # imprime o tempo em que iniciou a utilizar o recurso
	yield env.timeout(distributions("carregar")) 
	print "%.2f - %s chegou na secadora" % (env.now, nome) # imprime o tempo em que acabou de utilizar o recurso
	yield env.timeout(distributions("descarregar")) 
	reqSecadora = secadora.request() #requisita a secadora antes de liberar o cesto
	yield cesto.release(reqCesto)
	print "%.2f - %s colocou as roupas na secadora" % (env.now, nome) # imprime o tempo em que iniciou a utilizar o recurso
	yield env.timeout(distributions("secagem")) 
	print "%.2f - %s retirou as roupas da secadora" % (env.now, nome) # imprime o tempo em que acabou de utilizar o recurso
	yield secadora.release(reqSecadora)

random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números gerados será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
maquina = simpy.Resource(env, capacity=4)
secadora = simpy.Resource(env, capacity=3)
cesto = simpy.Resource(env, capacity=5)
env.process(geraChegadas(env, "Cliente", maquina, secadora, cesto)) # cria o processo de chegadas definido pela função "geraChegadas"
env.run(until=40) # executa a simulação por 50 unidades de tempo
