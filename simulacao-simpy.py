#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gerador de números aleatórios
import simpy # biblioteca de simulação

class Estatisticas(object):
	def __init__(self):
		self.lista = []
		self.probabilidades = {}
		self.numero_servidor = -1
		self.tempos = []
		self.ocupacao_servidores = {"Servidor 1": 0, "Servidor 2": 0}

	def NumeroMedioFila(self, tamanho_fila, tempo):
		self.tamanho_fila = tamanho_fila
		self.tempo = tempo

		if self.tamanho_fila not in self.clientes_fila.keys():
			self.clientes_fila[self.tamanho_fila] = self.tempo
		else:
			self.clientes_fila[self.tamanho_fila] += self.tempo

	def TaxaMediaOcupacao(self, tempoOcupado):
		self.tempoOcupado = tempoOcupado
		if self.numero_servidor == 1:
			self.ocupacao_servidores["Servidor 1"] += self.tempoOcupado
		elif self.numero_servidor == 2:
			self.ocupacao_servidores["Servidor 2"] += self.tempoOcupado
		return self.ocupacao_servidores

	def TempoMedioFila(self, tempoFila):
		self.tempoFila = tempoFila
		self.tempos.append(self.tempoFila)
		return sum(self.tempos) / len(self.tempos)

	def TempoMedioFila(self, tempoAtendimento):
		self.tempoAtendimento = tempoAtendimento
		self.tempos.append(self.tempoFila)
		return sum(self.tempos) / len(self.tempos)


class Simulacao(Estatisticas):

	def __init__(self, env, servidor, tempo_simulacao):
		Estatisticas.__init__(self)
		self.env = env
		self.servidor = servidor
		self.tempo_simulacao = tempo_simulacao

	def TempoChegada(self):
		self.lista = []
		self.probabilidades = {"0-5": [random.uniform(0,5), 35],"5-10": [random.uniform(5,10), 19],"10-15": [random.uniform(10,15), 19],"15-20": [random.uniform(15,20), 13],"20-25": [random.uniform(20,25), 3], "25-30": [random.uniform(25,30), 7], "30-35": [random.uniform(30, 35), 1], "35-40": [random.uniform(35,40), 2], "40-45": [random.uniform(40,45), 1]}
		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][1]
		random.shuffle(self.lista)
		return self.probabilidades[random.choice(self.lista)][0]

	def TempoServico(self, numero_servidor):
		self.numero_servidor = numero_servidor
		
		self.lista = []
		self.probabilidades = {"9,5-10": [random.uniform(9.5,10), 6,5],"10-10,5": [random.uniform(10,10.5), 5,4],"10,5-11": [random.uniform(10.5,11), 23,15],"11-11,5": [random.uniform(11,11.5), 20,16],"11,5-12": [random.uniform(11.5,12), 21,23], "12-12,5": [random.uniform(12,12.5), 12,20], "12,5-13": [random.uniform(12.5, 13), 9,10], "13-13,5": [random.uniform(13,13.5), 2,5], "13,5-14": [random.uniform(13.5,14), 1,2]}
		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][self.numero_servidor]
		random.shuffle(self.lista)
		return self.probabilidades[random.choice(self.lista)][0]

	def Chegadas(self):
		contador = 0
		while True:
			contador += 1
			yield self.env.timeout(self.TempoChegada())
			print "\n%.2f\tCliente %d chegou ao sistema" % (self.env.now, contador)
			self.env.process(self.Atendimento(contador))

	def Atendimento(self, n):
		self.n = n
		requisicao = self.servidor.request()
		
		yield requisicao
		
		print "%.2f\tCliente %d iniciou atendimento" %(self.env.now, n)
		yield self.env.timeout(self.TempoServico(random.randint(1,2)))
		print "%.2f\tCliente %d finalizou atendimento" %(self.env.now, n)
		
		yield self.servidor.release(requisicao)

env = simpy.Environment()
servidor = simpy.Resource(env, capacity=2)

S = Simulacao(env, servidor, 100)

env.process(S.Chegadas())
env.run(until=S.tempo_simulacao)
