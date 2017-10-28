#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gerador de números aleatórios
import simpy # biblioteca de simulação

def tempoChegada(probabilidades = {}, lista = []):
	#Esta função gera um tempo de chegadas de acordo com a tabela 1 (ver descrição da atividade)

	# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo a probabilidade(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

	probabilidades = {"0-5":[35, random.uniform(0,5)], "5-10":[19, random.uniform(5,10)], "10-15":[19, random.uniform(10,15)], "15-20":[13, random.uniform(15,20)], "20-25":[3, random.uniform(20,25)], "25-30":[7, random.uniform(25,30)], "30-35":[1, random.uniform(30,35)], "35-40":[2, random.uniform(0,5)], "40-45":[1, random.uniform(0,5)]}
	lista = []

	# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
	# Exemplo: chave "20-25", probabilidade 3% = 3 / 100
	# ["20-25" * 3]
	# Resultado: ["20-25","20-25","20-25"]

	for i in range(len(probabilidades)):
		lista += [probabilidades.keys()[i]] * probabilidades.values()[i][0]

	random.shuffle(lista) # embaralha a lista para obter um valor mais aleatório possível

	# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
	return probabilidades[random.choice(lista)][1]

def tempoServico(Servidor, probabilidades = {}, lista = []):
	#Esta função gera um tempo de servico de acordo com a tabela 2 (ver descrição da atividade)

	# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo as probabilidades dos servidores 1 e 2(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

	probabilidades = {"9,5-10":[6,5, random.uniform(9.5,10)], "10-10,5":[5,4, random.uniform(10,10.5)], "10,5-11":[23,15, random.uniform(10.5,11)], "11-11,5":[20,16, random.uniform(11,11.5)], "11,5-12":[21,23, random.uniform(11.5,12)], "12-12,5":[12,20, random.uniform(12,12.5)], "12,5-13":[9,10, random.uniform(12.5,13)], "13-13,5":[2,5, random.uniform(13,13.5)], "13,5-14":[1,2, random.uniform(13.5, 14)]}

	# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
	# Exemplo: chave "20-25", probabilidade 6% = 6 / 100
	# ["9,5-10"] * 3
	# Resultado: ["9,5-10","9,5-10","9,5-10","9,5-10","9,5-10","9,5-10"]

	for i in range(len(probabilidades)):
		lista += [probabilidades.keys()[i]] * probabilidades.values()[i][Servidor]

	random.shuffle(lista) # embaralha a lista para obter um valor mais aleatório possível

	# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
	return probabilidades[random.choice(lista)][2]

def chegadas(env, servidor):
	contador = 0 # contador de chegadas
	while True: # executa a função enquanto a simulação estiver ocorrendo
		contador += 1 # incrementa o contador com uma chegada
		yield env.timeout(tempoChegada()) # causa um atraso de tempo definido pela funcao tempoChegada()
		print "\n%.2f\tUsuário %d chegou na fila" %(env.now, contador) # imprime o tempo de chegada
		env.process(atendimento(env, "Usuario %d" %(contador), servidor)) # executa o processo para atendimento dos clientes

def atendimento(env, nome, servidor):
	request = servidor.request() #requisita o uso do servidor
	yield request #aguarda até o servidor estar livre
	print "%.2f\t%s iniciou atendimento" %(env.now, nome) #imprime o início do atendimento
	yield env.timeout(tempoServico(0))
	print "%.2f\t%s terminou atendimento" %(env.now, nome) #imprime o fim do atendimento
	yield servidor.release(request) #libera o recurso


env = simpy.Environment() #variável que representa o ambiente de simulação criado pelo SimPy
servidor = simpy.Resource(env, capacity=2) #variavel que representa o recurso a ser ocupado pelos clientes (servidor)
#~ servidor.users = [None, None]
env.process(chegadas(env, servidor)) #cria o processo de chegadas de entidade
env.run(until=100) # executa a simulação por 100 unidades de tempo

