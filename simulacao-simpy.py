#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gerador de números aleatórios
import simpy # biblioteca de simulação

class Simulacao(object):
	def __init__(self, tempoSimulacao, tempoTotalAtendimento = 0, env=None, servidor=None):
		self.tempoSimulacao = tempoSimulacao
		self.env = simpy.Environment() #variável que representa o ambiente de simulação criado pelo SimPy
		self.servidor = simpy.Resource(self.env, capacity=2) #variavel que representa o recurso a ser ocupado pelos clientes (servidor)
		self.env.process(self.chegadas()) #cria o processo de chegadas de entidade
		self.env.run(until=self.tempoSimulacao) # executa a simulação por 100 unidades de tempo
		
	def tempoChegada(self, probabilidades = {}, lista = []):
		#Esta função gera um tempo de chegadas de acordo com a tabela 1 (ver descrição da atividade)

		# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo a probabilidade(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

		self.probabilidades = {"0-5":[35, random.uniform(0,5)], "5-10":[19, random.uniform(5,10)], "10-15":[19, random.uniform(10,15)], "15-20":[13, random.uniform(15,20)], "20-25":[3, random.uniform(20,25)], "25-30":[7, random.uniform(25,30)], "30-35":[1, random.uniform(30,35)], "35-40":[2, random.uniform(0,5)], "40-45":[1, random.uniform(0,5)]}
		self.lista = []

		# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
		# Exemplo: chave "20-25", probabilidade 3% = 3 / 100
		# ["20-25" * 3]
		# Resultado: ["20-25","20-25","20-25"]

		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][0]

		random.shuffle(self.lista) # embaralha a lista para obter um valor mais aleatório possível

		# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
		return self.probabilidades[random.choice(self.lista)][1]

	def tempoServico(self, NServidor, probabilidades = {}, lista = []):
		self.NServidor = NServidor
		#Esta função gera um tempo de servico de acordo com a tabela 2 (ver descrição da atividade)

		# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo as probabilidades dos servidores 1 e 2(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

		self.probabilidades = {"9,5-10":[6,5, random.uniform(9.5,10)], "10-10,5":[5,4, random.uniform(10,10.5)], "10,5-11":[23,15, random.uniform(10.5,11)], "11-11,5":[20,16, random.uniform(11,11.5)], "11,5-12":[21,23, random.uniform(11.5,12)], "12-12,5":[12,20, random.uniform(12,12.5)], "12,5-13":[9,10, random.uniform(12.5,13)], "13-13,5":[2,5, random.uniform(13,13.5)], "13,5-14":[1,2, random.uniform(13.5, 14)]}
		self.lista = []

		# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
		# Exemplo: chave "20-25", probabilidade 6% = 6 / 100
		# ["9,5-10"] * 3
		# Resultado: ["9,5-10","9,5-10","9,5-10","9,5-10","9,5-10","9,5-10"]

		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][self.NServidor]
		
		random.shuffle(self.lista) # embaralha a lista para obter um valor mais aleatório possível

		# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
		return self.probabilidades[random.choice(self.lista)][2]

	def chegadas(self, contador = 0):
		self.contador = contador
		while True: # gera chegadas de entidades enquanto a simulação for executada
			self.contador += 1
			yield self.env.timeout(self.tempoChegada()) # gera um atraso de tempo referente a chegada
			print "\n%.2f\tUsuário %d chegou no sistema" % (self.env.now, self.contador)
			self.env.process(self.atendimento("Usuário %d" %(self.contador))) # invoca o processo de atendimento

	def atendimento(self, nomeCliente):
		self.nomeCliente = nomeCliente
		request = self.servidor.request()
		yield request
		print "%.2f\t%s iniciou atendimento" %(self.env.now, self.nomeCliente)
		yield self.env.timeout(self.tempoServico(random.randint(0,1)))
		print "%.2f\t%s finalizou atendimento" %(self.env.now, self.nomeCliente)
		yield self.servidor.release(request) #libera o recurso associado ao servidor

S = Simulacao(150)

class Estatisticas(object):
	def __init__(self):
		self.processos_ativos = [None, None]
		self.numero_servidor = -1
		self.tempoFila = 0
		self.n_elementos_fila = 0
		self.tempos = {}
		self.tempoOcupacao = 0

	def verificaServidorLivre(self): #método que verifica qual dos servidores está livre, e retorna para a função atendimento
		# verifica se ambos os servidores estão livres
		if self.processos_ativos[0] == None and self.processos_ativos[1] == None:
			self.numero_servidor = random.randint(0,1) #se os servidores estão livres, escolhe um aleatoriamente
		#verifica qual dos servidores está ocupado
		elif self.processos_ativos[0] == None and self.processos_ativos[1] != None:
			self.numero_servidor = 0
		elif self.processos_ativos[0] != None and self.processos_ativos[1] == None:
			self.numero_servidor = 1
		return self.numero_servidor

	def numeroMedioUsuariosFila(self):
		if self.n_elementos_fila not in self.tempos.keys():
			self.tempos[self.n_elementos_fila] = self.t
		else:
			self.tempos[self.n_elementos_fila] += self.t
		print "\nTempo em que o numero de elementos na fila permaneceu em determinado estado:\n", self.tempos

	def taxaMediaOcupacao(self):
		if self.numero_servidor == 0:
			if "Servidor 1" not in self.tempos.keys():
				self.tempos["Servidor 1"] = self.tempoOcupado
			else:
				self.tempos["Servidor 1"] += self.tempoOcupado
		elif self.numero_servidor == 1:
			if "Servidor 2" not in self.tempos.keys():
				self.tempos["Servidor 2"] = self.tempoOcupado
			else:
				self.tempos["Servidor 2"] += self.tempoOcupado
		print "Taxa de ocupação dos servidores", self.tempos


print Estatisticas().verificaServidorLivre()
