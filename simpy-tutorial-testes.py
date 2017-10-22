#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

#1. Acrescente ao programa inicial, uma função distribution como a proposta na Dica do Dia e faça o tempo entre chegadas sucessivas de entidades chamar a função para obter o valor correto.
#2. Considere que 50% das entidades geradas durante a simulação são do sexo feminino e 50% do sexo masculino. Modifique o programa para que ele sorteie o gênero dos clientes. Faça esse sorteio dentro da função distribution já criada.

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

def distributions(tipo):
	return {"arrival": random.expovariate(lambd=1.0/3.0), "singing": random.triangular(0.1,1.1,1.0), "applause":random.gauss(10,1)}.get(tipo), random.choice(["Masculino","Feminino"])

def geraChegadas(env, nome, taxa, numeroMaxChegadas, tipoDistribuicao):
	#função que gera chegadas de entidades no sistema, a uma taxa definida pela variável "taxa"
	contaChegada = 0
	while contaChegada < numeroMaxChegadas: #desafio 2
		#random.triangular(min, max, moda) --> distribuição de números aleatórios (desafio 3)
		yield env.timeout(distributions(tipoDistribuicao)[0]) # yield retorna um gerador que causa um atraso de tempo definido por env.timeout
		contaChegada += 1 # contador
		print "%.2f %s %i chegou ao sistema\tSexo: %s" %(env.now, nome, contaChegada, distributions(tipoDistribuicao)[1]) 

random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números gerados será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
env.process(geraChegadas(env, "Cliente", 2, 10, "arrival")) # cria o processo de chegadas definido pela função "geraChegadas"
env.run(until=25) # executa a simulação por 10 unidades de tempo
