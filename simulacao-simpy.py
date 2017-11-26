#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gerador de números aleatórios
import simpy # biblioteca de simulação

class Estatisticas(object):
	def __init__(self, tempo_simulacao):
		self.tempo_simulacao = tempo_simulacao
		self.servidor_livre = -1
		self.tempos_fila = []
		self.tempos_sistema = []
		self.ocupacao_servidores = {"Servidor 1": [0, 0], "Servidor 2": [0, 0]}
		self.numero_clientes_atendidos = 0
		self.usuarios_no_sistema = [None, None]
		self.temposFila = {}

	def VerificaServidorLivre(self):
		if self.usuarios_no_sistema[0] != None and self.usuarios_no_sistema[1] != None:
			pass
		else:
			if self.usuarios_no_sistema[0] == None and self.usuarios_no_sistema[1] == None:
				self.servidor_livre = random.randint(1,2)
			elif self.usuarios_no_sistema[0] == None and self.usuarios_no_sistema[1] != None:
				self.servidor_livre = 1
			elif self.usuarios_no_sistema[0] != None and self.usuarios_no_sistema[1] == None:
				self.servidor_livre = 2
			return self.servidor_livre
		return None

	def TemposVariavelClientesFila(self, tamanho_fila, t):
		self.tamanho_fila = tamanho_fila
		self.t = t
		
		if self.tamanho_fila not in self.temposFila.keys():
			self.temposFila[self.tamanho_fila] = self.t
		else:
			self.temposFila[self.tamanho_fila] += self.t
		#~ for i in range(len(self.temposFila)):
			#~ print "Tempo em que a variável 'número de clientes na fila' permaneceu em %d: %.2f (%.2f %%)" %(self.temposFila.keys()[i], self.temposFila.values()[i], (self.temposFila.values()[i] / self.tempo_simulacao) * 100)

	def NumeroMedioClientesFila(self):
		pass

	def TempoTotalOcupacaoServidor(self, numero_servidor, tempoOcupado):
		self.tempoOcupado = tempoOcupado

		if self.numero_servidor == 1:
			self.ocupacao_servidores["Servidor 1"][0] += self.tempoOcupado
			self.ocupacao_servidores["Servidor 1"][1] += 1
		elif self.numero_servidor == 2:
			self.ocupacao_servidores["Servidor 2"][0] += self.tempoOcupado
			self.ocupacao_servidores["Servidor 2"][1] += 1

	def TaxaMediaOcupacaoServidor(self):
		taxa_media_servidor1 = self.ocupacao_servidores["Servidor 1"][0] / self.ocupacao_servidores["Servidor 1"][1]
		taxa_media_servidor2 = self.ocupacao_servidores["Servidor 2"][0] / self.ocupacao_servidores["Servidor 2"][1]
		return (taxa_media_servidor1, taxa_media_servidor2)

	def TempoTotalFila(self, tempoFila):
		self.tempoFila = tempoFila
		self.tempos_fila.append(self.tempoFila)

	def TempoMedioFila(self):
		return sum(self.tempos_fila) / len(self.tempos_fila)

	def TempoTotalSistema(self, tempoAtendimento):
		self.tempoAtendimento = tempoAtendimento
		self.tempos_sistema.append(self.tempoAtendimento)

	def TempoMedioSistema(self):
		return sum(self.tempos_sistema) / len(self.tempos_sistema)

	def ContaClientes(self):
		self.numero_clientes_atendidos += 1
	
	def TotalClientes(self):
		return self.numero_clientes_atendidos

class Simulacao(Estatisticas):
	def __init__(self, env, servidor, tempo_simulacao):
		Estatisticas.__init__(self, tempo_simulacao)
		self.env = env
		self.servidor = servidor
		self.tempo_simulacao = tempo_simulacao

		self.tempos_chegada = {"0-5": [random.uniform(0,5), 35],"5-10": [random.uniform(5,10), 19],"10-15": [random.uniform(10,15), 19],"15-20": [random.uniform(15,20), 13],"20-25": [random.uniform(20,25), 3], "25-30": [random.uniform(25,30), 7], "30-35": [random.uniform(30, 35), 1], "35-40": [random.uniform(35,40), 2], "40-45": [random.uniform(40,45), 1]}

		self.tempos_servico = {"9,5-10": [random.uniform(9.5,10), 6,5],"10-10,5": [random.uniform(10,10.5), 5,4],"10,5-11": [random.uniform(10.5,11), 23,15],"11-11,5": [random.uniform(11,11.5), 20,16],"11,5-12": [random.uniform(11.5,12), 21,23], "12-12,5": [random.uniform(12,12.5), 12,20], "12,5-13": [random.uniform(12.5, 13), 9,10], "13-13,5": [random.uniform(13,13.5), 2,5], "13,5-14": [random.uniform(13.5,14), 1,2]}

	def TempoChegada(self):
		self.lista = []
		for i in range(len(self.tempos_chegada)):
			self.lista += [self.tempos_chegada.keys()[i]] * self.tempos_chegada.values()[i][1]
		random.shuffle(self.lista)
		return self.tempos_chegada[random.choice(self.lista)][0]

	def TempoServico(self, numero_servidor):
		self.numero_servidor = numero_servidor
		self.lista = []
		for i in range(len(self.tempos_servico)):
			self.lista += [self.tempos_servico.keys()[i]] * self.tempos_servico.values()[i][self.numero_servidor]
		random.shuffle(self.lista)
		return self.tempos_servico[random.choice(self.lista)][0]

	def Chegadas(self):
		contador = 0
		while True:
			contador += 1
			yield self.env.timeout(self.TempoChegada())
			print "\n%.2f\tCliente %d chegou ao sistema" % (self.env.now, contador)
			self.env.process(self.Atendimento(contador))

	def Atendimento(self, n):

		numero_elementos_fila = len(self.servidor.queue)
		livre = self.VerificaServidorLivre()

		if livre == 1 or livre == 2:
			t = self.TempoServico(livre)

			requisicao = self.servidor.request()
			chegada_fila = self.env.now
			self.usuarios_no_sistema[livre - 1] = requisicao
			
			yield requisicao

			tempo_fila = self.env.now - chegada_fila

			inicio = self.env.now
			print "%.2f\tCliente %d iniciou atendimento no Servidor %d" %(self.env.now, n, livre)
			yield self.env.timeout(t)
			print "%.2f\tCliente %d finalizou atendimento no Servidor %d" %(self.env.now, n, livre)
			total = self.env.now - inicio
			
			self.usuarios_no_sistema[livre - 1] = None
			yield self.servidor.release(requisicao)
			
			self.TemposVariavelClientesFila(numero_elementos_fila, total)
			self.TempoTotalOcupacaoServidor(livre, t)
			self.TempoTotalFila(tempo_fila)
			self.TempoTotalSistema(t)
			self.ContaClientes()
		
	def Resultados(self):
		print """\n\n------------------------------ RESULTADOS ------------------------------\n
Número médio de clientes na fila: 

Taxa média de ocupação dos servidores:
	Servidor 1: %.2f
	Servidor 2: %.2f

Tempo médio do cliente na fila: %.2f

Tempo médio no sistema: %.2f

Clientes atendidos: %d""" % (self.TaxaMediaOcupacaoServidor()[0], self.TaxaMediaOcupacaoServidor()[1], self.TempoMedioFila(), self.TempoMedioSistema(), self.TotalClientes())

env = simpy.Environment()
servidor = simpy.Resource(env, capacity=2)

S = Simulacao(env, servidor, 500)

env.process(S.Chegadas())
env.run(until=S.tempo_simulacao)

S.Resultados()

