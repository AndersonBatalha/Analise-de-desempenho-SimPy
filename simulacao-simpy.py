#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gera números aleatórios
import simpy # biblioteca de simulação

"""
Probabilidades

tempos_servico = {"0-5":35, "5-10":19, "10-15":19, "15-20":13, "20-25":3, "25-30":7, "30-35":1, "35-40":2, "40-45":1}

tempo = {'0-5':random.uniform(0,5), '30-35':random.uniform(30,35), '5-10':random.uniform(5,10), '15-20':random.uniform(15,20), '35-40':random.uniform(35,40), '10-15':random.uniform(10,15), '20-25':random.uniform(20,25), '25-30':random.uniform(25,30), '40-45':random.uniform(40,45)}

"""

class Simulacao(object):
	# o construtor da classe cria o ambiente de desenvolvimento e o recurso a ser utilizado, no caso o servidor
	# o usuário deve passar como parâmetro apenas o tempo de simulação desejado
	def __init__(self, tempoSimulacao, env=None, servidor=None):
		self.tempoSimulacao = tempoSimulacao #tempo em que a simulação é realizada
		self.env = simpy.Environment() #variavel que representa o ambiente de simulação criado pelo SimPy
		self.servidor = simpy.Resource(self.env, capacity=2) #variavel que representa o recurso a ser ocupado
		self.env.process(self.chegadaEntidades(2))
		self.env.run(until=tempoSimulacao)

	def __str__(self):
		return "Simulação de um sistema com dois servidores"
	
	def tempoChegada(self, probabilidades = {}, lista = []):
		"""Este método da classe gera um tempo de chegadas de acordo com a tabela 1 (ver descrição da atividade)
		
		Dicionário: pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo a probabilidade(inteiro), e o método random.uniform, para gerar o tempo de chegada
		
		Como estamos trabalhando com porcentagem, se, por exemplo a probabilidade de ocorrência é de 39%, então são 39 valores iguais dentro de um vetor de 100 posições
		
		Criei uma lista vazia, para cada par chave-valor do dicionário, inseri o valor da chave em outro array, multiplicado por sua probabilidade
		"""
		self.probabilidades = {"0-5":[35, random.uniform(0,5)], "5-10":[19, random.uniform(5,10)], "10-15":[19, random.uniform(10,15)], "15-20":[13, random.uniform(15,20)], "20-25":[3, random.uniform(20,25)], "25-30":[7, random.uniform(25,30)], "30-35":[1, random.uniform(30,35)], "35-40":[2, random.uniform(0,5)], "40-45":[1, random.uniform(0,5)]}
		self.lista = []
		
		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][0] # concatenação
		
		return self.probabilidades[random.choice(self.lista)][1]

	def chegadaEntidades(self, TEMPO_MEDIO_CHEGADA, i = 0):
		self.TEMPO_MEDIO_CHEGADA = TEMPO_MEDIO_CHEGADA
		self.i = i
		
		while True:
			self.i += 1
			yield self.env.timeout(self.tempoChegada())
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

sim = Simulacao(None)
