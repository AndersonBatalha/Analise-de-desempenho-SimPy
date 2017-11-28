#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random # gerador de números aleatórios
import simpy # biblioteca de simulação

class Estatisticas(object):
	def __init__(self, tempo_simulacao):
		self.tempo_simulacao = tempo_simulacao 
		self.servidor_livre = -1 # indica qual servidor está livre
		self.numero_clientes_atendidos = 0 # conta o número de atendimentos
		self.numero_chegadas = 0 # conta o número de chegadas de clientes
		self.tempo_total_fila = 0 # tempo total dos clientes na fila
		self.tempo_total_sistema = 0 # tempo total dos clientes no sistema
		self.taxa_media_servidor1 = 0 # calcula a taxa de ocupação do servidor 1
		self.taxa_media_servidor2 = 0 # calcula a taxa de ocupação do servidor 2
		self.tempos_variavel_fila = {} # calcula o tempo em que a variável da fila esteve em um determinado valor
		self.ocupacao_servidores = {"Servidor 1": [0, 0], "Servidor 2": [0, 0]} # cria um dicionário para registrar o tempo total de ocupação do servidor, e quantos clientes foram atendidos

	# para cada atendimento, incrementa uma variável que mede o tempo em que a variável da fila esteve em um determinado valor
	def TempoTotalVariavelClientesFila(self, tamanho_fila, tempo_da_variavel):
		self.tamanho_fila = tamanho_fila
		self.tempo_da_variavel = tempo_da_variavel
		
		if self.tamanho_fila not in self.tempos_variavel_fila.keys():
			self.tempos_variavel_fila[self.tamanho_fila] = self.tempo_da_variavel
		else:
			self.tempos_variavel_fila[self.tamanho_fila] += self.tempo_da_variavel

	# retorna o número médio de clientes na fila
	def NumeroMedioClientesFila(self):
		soma_tempos = 0
		# para cada par chave-valor no dicionário, multiplica o número de clientes na fila por seu percentual em relação ao tempo total
		for i in range(len(self.tempos_variavel_fila)):
			soma_tempos += self.tempos_variavel_fila.keys()[i] * ((self.tempos_variavel_fila.values()[i] / self.tempo_simulacao) * 100)
		# retorna o valor médio
		return soma_tempos / self.TotalChegadas()

	# para cada atendimento, incrementa uma variável que mede o tempo total de ocupação de cada um dos servidores
	def TempoTotalOcupacaoServidor(self, tempoOcupado):
		self.tempoOcupado = tempoOcupado

		if self.servidor_livre == 1:
			self.ocupacao_servidores["Servidor 1"][0] += self.tempoOcupado
			self.ocupacao_servidores["Servidor 1"][1] += 1
		elif self.servidor_livre == 2:
			self.ocupacao_servidores["Servidor 2"][0] += self.tempoOcupado
			self.ocupacao_servidores["Servidor 2"][1] += 1

	# retorna o tempo médio de ocupação dos servidores
	def TaxaMediaOcupacaoServidor(self):
		try:
			self.taxa_media_servidor1 = self.ocupacao_servidores["Servidor 1"][0] / self.ocupacao_servidores["Servidor 1"][1]
			self.taxa_media_servidor2 = self.ocupacao_servidores["Servidor 2"][0] / self.ocupacao_servidores["Servidor 2"][1]
			return (self.taxa_media_servidor1, self.taxa_media_servidor2)
		except ZeroDivisionError: # verifica se o servidor atendeu pelo menos um cliente, caso contrário ocorre erro na divisão, pois não é possível dividir um número por 0
			if self.ocupacao_servidores["Servidor 1"][1] == 0 and self.ocupacao_servidores["Servidor 2"][1] == 0:
				return (0, 0)
			else:
				if self.ocupacao_servidores["Servidor 1"][1] == 0:
					self.taxa_media_servidor2 = self.ocupacao_servidores["Servidor 2"][0] / self.ocupacao_servidores["Servidor 2"][1]
					return (0, self.taxa_media_servidor2)
				elif self.ocupacao_servidores["Servidor 2"][1] == 0:
					self.taxa_media_servidor1 = self.ocupacao_servidores["Servidor 1"][0] / self.ocupacao_servidores["Servidor 1"][1]
					return (self.taxa_media_servidor1, 0)

	# para cada atendimento, incrementa uma variável que mede o tempo total na fila
	def TempoTotalFila(self, tempoFila):
		self.tempoFila = tempoFila
		self.tempo_total_fila += self.tempoFila

	# retorna o tempo médio na fila
	def TempoMedioFila(self):
		if self.TotalClientes() > 0:
			return self.tempo_total_fila / self.TotalClientes()
		else:
			return self.tempo_total_fila

	# para cada atendimento, incrementa uma variável que mede o tempo total no sistema
	def TempoTotalSistema(self, tempoAtendimento):
		self.tempoAtendimento = tempoAtendimento
		self.tempo_total_sistema += self.tempoAtendimento

	# retorna o tempo médio no sistema
	def TempoMedioSistema(self):
		if self.TotalClientes() > 0:
			return self.tempo_total_sistema / self.TotalClientes()
		else:
			return self.tempo_total_sistema

	# para cada atendimento, incrementa uma variável que mede o número de clientes atendidos
	def ContaAtendimentos(self):
		self.numero_clientes_atendidos += 1
	
	# retorna o total de clientes atendidos
	def TotalClientes(self):
		return self.numero_clientes_atendidos

	# para cada atendimento, incrementa uma variável que mede o número de chegadas de clientes
	def ContaChegadas(self):
		self.numero_chegadas += 1
	
	# retorna o total de chegadas de clientes
	def TotalChegadas(self):
		return self.numero_chegadas

class Simulacao(Estatisticas):

	def __init__(self, env, servidor, tempo_simulacao):
		Estatisticas.__init__(self, tempo_simulacao)

		self.env = env # cria o ambiente de simulação
		self.servidor = servidor # cria uma variável para representar o recurso a ser ocupado (o servidor)
		self.tempo_simulacao = tempo_simulacao # tempo total de simulação

		# dicionário armazena os tempos de chegada, e suas probabilidades, além da função random.uniform, que gera números aleatórios de ponto flutuante (ver descrição da atividade --> tabela 1)
		self.tempos_chegada = {"0-5": [random.uniform(0,5), 35],"5-10": [random.uniform(5,10), 19],"10-15": [random.uniform(10,15), 19],"15-20": [random.uniform(15,20), 13],"20-25": [random.uniform(20,25), 3], "25-30": [random.uniform(25,30), 7], "30-35": [random.uniform(30, 35), 1], "35-40": [random.uniform(35,40), 2], "40-45": [random.uniform(40,45), 1]}

		# dicionário armazena os tempos de serviço, e suas probabilidades, além da função random.uniform, que gera números aleatórios de ponto flutuante (ver descrição da atividade --> tabela 2)
		self.tempos_servico = {"9,5-10": [random.uniform(9.5,10), 6,5],"10-10,5": [random.uniform(10,10.5), 5,4],"10,5-11": [random.uniform(10.5,11), 23,15],"11-11,5": [random.uniform(11,11.5), 20,16],"11,5-12": [random.uniform(11.5,12), 21,23], "12-12,5": [random.uniform(12,12.5), 12,20], "12,5-13": [random.uniform(12.5, 13), 9,10], "13-13,5": [random.uniform(13,13.5), 2,5], "13,5-14": [random.uniform(13.5,14), 1,2]}

		self.usuarios_no_sistema = [None, None] # lista que representa os servidores disponíveis

		self.tempo_total = 0
		print self.__str__()

	def __str__(self):
		return """
Simulação de Sistema com Dois Servidores
Análise e Desempenho de Sistemas – 2017/2
"""

	def VerificaServidorLivre(self): # método que verifica qual servidor está disponível
		if self.usuarios_no_sistema[0] == None and self.usuarios_no_sistema[1] == None:
			self.servidor_livre = random.randint(1,2)
		elif self.usuarios_no_sistema[0] == None and self.usuarios_no_sistema[1] != None:
			self.servidor_livre = 1
		elif self.usuarios_no_sistema[0] != None and self.usuarios_no_sistema[1] == None:
			self.servidor_livre = 2
		return self.servidor_livre

	def TempoChegada(self):
		self.lista = []
		# cria uma lista com 100 posições, com cada elemento representando a classe (em segundos)
		for i in range(len(self.tempos_chegada)):
			self.lista += [self.tempos_chegada.keys()[i]] * self.tempos_chegada.values()[i][1]
		random.shuffle(self.lista) # embaralha a lista para obter um valor aleatório
		return self.tempos_chegada[random.choice(self.lista)][0] # retorna o tempo de chegada

	def TempoServico(self, numero_servidor):
		self.numero_servidor = numero_servidor
		self.lista = []
		# cria uma lista com 100 posições, com cada elemento representando a classe (em segundos)
		for i in range(len(self.tempos_servico)):
			self.lista += [self.tempos_servico.keys()[i]] * self.tempos_servico.values()[i][self.numero_servidor]
		random.shuffle(self.lista) # embaralha a lista para obter um valor aleatório
		return self.tempos_servico[random.choice(self.lista)][0] # retorna o tempo de serviço

	def Chegadas(self):
		while True: # executa o processo de chegadas de clientes enquanto a simulação estiver ocorrendo
			inicio = self.env.now
			self.ContaChegadas() # incrementa um contador de chegadas
			yield self.env.timeout(self.TempoChegada()) # env.timeout causa um atraso de tempo definido pela função TempoChegada()
			print "%.2f\tCliente %d chegou ao sistema\n" % (self.env.now, self.TotalChegadas()) # imprime o tempo de chegada (env.now)
			fim = self.env.now
			tempo = fim - inicio
			self.TempoTotalVariavelClientesFila(len(self.servidor.queue), tempo)
			self.env.process(self.Atendimento(self.TotalChegadas())) # invoca a função que processa o atendimento

	def Atendimento(self, numeroCliente):
		servidorlivre = self.VerificaServidorLivre() #verifica qual servidor está livre

		if servidorlivre == 1 or servidorlivre == 2: # verifica se pelo menos um servidor está livre, caso contrário não realiza o atendimento, e aguarda na fila
			tempoAtendimento = self.TempoServico(servidorlivre) # gera um tempo de atendimento definido pela função TempoServico

			requisicao = self.servidor.request() # requisita o uso do servidor
			chegada_fila = self.env.now # registra o tempo de chegada na fila
			self.usuarios_no_sistema[servidorlivre - 1] = requisicao # ocupa o servidor
			
			yield requisicao # caso um dos servidores estiver livre, realiza o atendimento

			tempo_fila = self.env.now - chegada_fila # registra o tempo de saída da fila

			# exibe início e término do atendimento
			print "%.2f\tCliente %d iniciou atendimento no Servidor %d\n" %(self.env.now, numeroCliente, servidorlivre)
			yield self.env.timeout(tempoAtendimento)
			print "%.2f\tCliente %d finalizou atendimento no Servidor %d\n" %(self.env.now, numeroCliente, servidorlivre)
			
			# desocupa o servidor
			self.usuarios_no_sistema[servidorlivre - 1] = None
			yield self.servidor.release(requisicao)

			#executa as funções para calcular:
			# - tempo médio de ocupação dos servidores
			# - tempo médio na fila
			# - tempo médio no sistema

			# Para cada atendimento, o valor da variável é incrementado para obter o tempo total de ocupação dos servidores, tempo total na fila e o tempo total no sistema
 
			self.TempoTotalOcupacaoServidor(tempoAtendimento)
			self.TempoTotalFila(tempo_fila)
			self.TempoTotalSistema(tempoAtendimento)

		self.ContaAtendimentos() # conta quantos clientes chegaram no sistema e foram atendidos

	def Resultados(self): # exibe os resultados da simulação
		print """------------------------------ RESULTADOS ------------------------------\n
Número médio de clientes na fila: %f

Taxa média de ocupação dos servidores:
	Servidor 1: %f
	Servidor 2: %f

Tempo médio do cliente na fila: %f

Tempo médio no sistema: %f

Clientes que chegaram ao sistema: %d

Clientes atendidos: %d

------------------------------------------------------------------------

""" % (self.NumeroMedioClientesFila(), self.TaxaMediaOcupacaoServidor()[0], self.TaxaMediaOcupacaoServidor()[1], self.TempoMedioFila(), self.TempoMedioSistema(), self.TotalChegadas(), self.TotalClientes())

tempo_simulado = int(raw_input("Informe o tempo de simulação: "))

env = simpy.Environment() # cria o ambiente de simulação
servidor = simpy.Resource(env, capacity=2) # cria uma variável para representar o recurso a ser ocupado (o servidor)

S = Simulacao(env, servidor, tempo_simulado) # cria uma instância da classe

env.process(S.Chegadas()) # inclui o processo de chegadas como parte do processo de simulação
env.run(until=S.tempo_simulacao) # executa a simulação por um determinado período de tempo

S.Resultados() # exibe os resultados

