#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

#Desafio 2: é comum que os comandos de criação de entidades nos softwares proprietários tenham a opção de limitar o número máximo de entidades geradas durante a simulação. Modifique a função geraChegadas de modo que ela receba como parâmetro numeroMaxChegadas e limite a criação de entidades a este número.
#Desafio 3: modifique a função geraChegadas de modo que as chegadas entre entidades sejam distribuídas segundo uma distribuição triangular de moda 1, menor valor 0,1 e maior valor 1,1.+

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

def geraChegadas(env, nome, taxa, numeroMaxChegadas):
	#função que gera chegadas de entidades no sistema, a uma taxa definida pela variável "taxa"
	contaChegada = 0
	while contaChegada < numeroMaxChegadas: #desafio 2
		#random.triangular(min, max, moda) --> distribuição de números aleatórios (desafio 3)
		yield env.timeout(random.triangular(0.1, 1.1, 1)) # yield retorna um gerador que causa um atraso de tempo definido por env.timeout
		contaChegada += 1 # contador
		print "%.2f %s %i chegou ao sistema" %(env.now, nome, contaChegada) 

random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números gerados será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
env.process(geraChegadas(env, "Cliente", 2, 10)) # cria o processo de chegadas definido pela função "geraChegadas"
env.run(until=25) # executa a simulação por 10 unidades de tempo
