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

	def verificaServidorLivre(self, processos_ativos, numeroServidor = 0): #método que verifica qual dos servidores está livre, e retorna para a função atendimento
		self.processos_ativos = processos_ativos
		self.numeroServidor = numeroServidor
		# verifica se ambos os servidores estão livres
		if self.processos_ativos[0] == None and self.processos_ativos[1] == None:
				self.numeroServidor = random.randint(0,1) #se os servidores estão livres, escolhe um aleatoriamente
		#verifica qual dos servidores está ocupado
		elif self.processos_ativos[0] == None and self.processos_ativos[1] != None:
				self.numeroServidor = 0
		elif self.processos_ativos[0] != None and self.processos_ativos[1] == None:
				self.numeroServidor = 1
		return self.numeroServidor

	def numeroMedioUsuariosFila(self, t, n_elementos_fila, tempoNumeroUsuariosFila = {}):
		self.t = t
		self.n_elementos_fila = n_elementos_fila
		self.tempoNumeroUsuariosFila = tempoNumeroUsuariosFila
		if self.n_elementos_fila not in self.tempoNumeroUsuariosFila.keys():
				self.tempoNumeroUsuariosFila[self.n_elementos_fila] = self.t
		else:
				self.tempoNumeroUsuariosFila[self.n_elementos_fila] += self.t
		print "\nTempo em que o numero de elementos na fila permaneceu em determinado estado:\n", self.tempoNumeroUsuariosFila

	def taxaMediaOcupacao(self, tempoOcupado, s, tempos = {}):
		self.tempoOcupado = tempoOcupado
		self.s = s
		self.tempos = tempos
		if self.s == 0:
			if "Servidor 1" not in self.tempos.keys():
				self.tempos["Servidor 1"] = self.tempoOcupado
			else:
				self.tempos["Servidor 1"] += self.tempoOcupado
		elif self.s == 1:
			if "Servidor 2" not in self.tempos.keys():
				self.tempos["Servidor 2"] = self.tempoOcupado
			else:
				self.tempos["Servidor 2"] += self.tempoOcupado
		print self.tempos

	def chegadas(self, contador = 0):
		self.contador = contador
		while True: # gera chegadas de entidades enquanto a simulação for executada
				self.contador += 1
				yield self.env.timeout(self.tempoChegada()) # gera um atraso de tempo referente a chegada
				print "\n%.2f\tUsuário %d chegou no sistema" % (self.env.now, self.contador)
				self.env.process(self.atendimento("Usuário %d" %(self.contador))) # invoca o processo de atendimento

	def atendimento(self, nomeCliente, usuarios = [None,None]):
		self.nomeCliente = nomeCliente
		self.usuarios = usuarios #cria uma lista com duas posições, que corresponde aos servidores
		request = self.servidor.request()
		chegadaFila = self.env.now
		servidor_livre = self.verificaServidorLivre(self.usuarios)
		self.usuarios[servidor_livre] = request
		yield request
		tempoFila = self.env.now - chegadaFila
		print "%.2f\t%s iniciou atendimento no Servidor %d" %(self.env.now, self.nomeCliente, servidor_livre + 1)
		yield self.env.timeout(self.tempoServico(servidor_livre))
		print "%.2f\t%s finalizou atendimento no Servidor %d" %(self.env.now, self.nomeCliente, servidor_livre + 1)
		self.usuarios[servidor_livre] = None
		yield self.servidor.release(request) #libera o recurso associado ao servidor
		print "Tempo na fila", tempoFila
		self.numeroMedioUsuariosFila(tempoFila, len(self.servidor.queue))


S = Simulacao(150)
