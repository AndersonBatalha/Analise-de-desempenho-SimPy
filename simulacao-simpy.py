#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação

class Simulacao(object):
	# o construtor da classe cria o ambiente de desenvolvimento e o recurso a ser utilizado, no caso o servidor
	# o usuário deve passar como parâmetro apenas o tempo de simulação desejado
	def __init__(self, tempoSimulacao, env=None, servidor=None):
		self.tempoSimulacao = tempoSimulacao #tempo em que a simulação é realizada
		self.env = simpy.Environment() #variavel que representa o ambiente de simulação criado pelo SimPy
		self.servidor = simpy.Resource(self.env, capacity=2) #variavel que representa o recurso a ser ocupado
		self.env.process(self.chegadaClientes()) #env.process informa ao SimPy que a função chegadaClientes faz parte do processo de simulação
		self.env.run(until=tempoSimulacao)

	def __str__(self):
		return "Simulação de um sistema com dois servidores"
	
	def tempoChegada(self, probabilidades = {}, lista = []):
		#Este método da classe gera um tempo de chegadas de acordo com a tabela 1 (ver descrição da atividade)
		
		# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo a probabilidade(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

		self.probabilidades = {"0-5":[35, random.uniform(0,5)], "5-10":[19, random.uniform(5,10)], "10-15":[19, random.uniform(10,15)], "15-20":[13, random.uniform(15,20)], "20-25":[3, random.uniform(20,25)], "25-30":[7, random.uniform(25,30)], "30-35":[1, random.uniform(30,35)], "35-40":[2, random.uniform(0,5)], "40-45":[1, random.uniform(0,5)]} 
		self.lista = []
		
		# Em uma lista, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
		# Exemplo: chave "20-25", probabilidade 3% = 3 / 100
		# ["20-25" * 3]
		# Resultado: ["20-25","20-25","20-25"]
		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][0]

		# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
		return self.probabilidades[random.choice(self.lista)][1] 

	def chegadaClientes(self, contador = 0):
		self.contador = contador #conta o número de chegadas de entidades
		
		while True:
			self.contador += 1 #incrementa o contador com uma nova chegada
			yield self.env.timeout(self.tempoChegada()) #env.timeout causa um atraso de tempo aleatório definido pelo método tempoChegada()
			print "\nCliente %d chegou em %.2f" %(self.contador, self.env.now) #imprime o valor do contador e o tempo atual de simulação 
			self.env.process(self.atendimento(1, "Cliente %d" %(self.contador))) # invoca o processo de atendimento dos clientes

	def atendimento(self, TEMPO_MEDIO_ATENDIMENTO, nomeCliente, request=None):
		self.TEMPO_MEDIO_ATENDIMENTO = TEMPO_MEDIO_ATENDIMENTO
		self.nomeCliente = nomeCliente
		self.request = request

		self.request = self.servidor.request() #requisita o uso do recurso
		yield self.request #aguarda até a liberação do recurso
		
		print "%.2f %s começou a ser atendido" %(self.env.now, self.nomeCliente) # imprime o tempo atual e o início do atendimento
		
		yield self.env.timeout(self.TEMPO_MEDIO_ATENDIMENTO)
		
		print "%.2f %s terminou de ser atendido" %(self.env.now, self.nomeCliente) # imprime o tempo atual e o fim do atendimento
		yield self.servidor.release(self.request) #libera o recurso


sim = Simulacao(500)
