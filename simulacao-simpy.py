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
		#variaveis que representa o recurso a ser ocupado (servidor)
		self.servidor = simpy.Resource(self.env, capacity=2)
		self.env.process(self.chegadaClientes()) #env.process informa ao SimPy que a função chegadaClientes faz parte do processo de simulação
		self.env.run(until=self.tempoSimulacao)

	def __str__(self):
		return "Simulação de um sistema com dois servidores"

	def chegadaClientes(self):
		self.contador = 0 #conta o número de chegadas de entidades
		while self.contador < 10:
			self.contador += 1 #incrementa o contador com uma nova chegada
			yield self.env.timeout(self.tempoChegada()) #env.timeout causa um atraso de tempo aleatório definido pelo método tempoChegada()
			print ("\n%.2f\tUsuário %d chegou no sistema" % (self.env.now,self.contador)) #imprime o valor do contador e o tempo atual de simulação
			self.env.process(self.atendimento("Usuário " + str(self.contador))) # invoca o processo de atendimento dos clientes

	def atendimento(self, nome, request=None):
		self.nome = nome
		self.request = request

		with self.servidor.request() as self.request:
			yield self.request #aguarda até a liberação do recurso
			print "%.2f\t%s iniciou atendimento" %(self.env.now, self.nome)
			
			yield self.env.timeout(self.tempoServico(random.randint(0,1)))
			
			print "%.2f\t%s terminou atendimento" %(self.env.now, self.nome)

	def tempoChegada(self, probabilidades = {}, lista = []):
		#Este método da classe gera um tempo de chegadas de acordo com a tabela 1 (ver descrição da atividade)

		# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo a probabilidade(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

		self.probabilidades = {"0-5":[35, random.uniform(0,5)], "5-10":[19, random.uniform(5,10)], "10-15":[19, random.uniform(10,15)], "15-20":[13, random.uniform(15,20)], "20-25":[3, random.uniform(20,25)], "25-30":[7, random.uniform(25,30)], "30-35":[1, random.uniform(30,35)], "35-40":[2, random.uniform(0,5)], "40-45":[1, random.uniform(0,5)]}
		self.lista = []

		# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
		# Exemplo: chave "20-25", probabilidade 3% = 3 / 100
		# ["20-25" * 3]
		# Resultado: ["20-25","20-25","20-25"]

		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][0]

		# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
		return self.probabilidades[random.choice(self.lista)][1]

	def tempoServico(self, Servidor, probabilidades = {}, lista = []):
		self.Servidor = Servidor
		self.lista = lista
		#Este método da classe gera um tempo de servico de acordo com a tabela 2 (ver descrição da atividade)

		# Um dicionário representa com pares no formato chave-valor, onde a chave representa a classe, e o valor é uma lista contendo as probabilidades dos servidores 1 e 2(inteiro), e o método random.uniform, para gerar valores aleatórios de ponto flutuante

		self.probabilidades = {"9,5-10":[6,5, random.uniform(9.5,10)], "10-10,5":[5,4, random.uniform(10,10.5)], "10,5-11":[23,15, random.uniform(10.5,11)], "11-11,5":[20,16, random.uniform(11,11.5)], "11,5-12":[21,23, random.uniform(11.5,12)], "12-12,5":[12,20, random.uniform(12,12.5)], "12,5-13":[9,10, random.uniform(12.5,13)], "13-13,5":[2,5, random.uniform(13,13.5)], "13,5-14":[1,2, random.uniform(13.5, 14)]}

		# Cria uma lista com 100 posições, para cada par chave-valor do dicionário, o valor da chave é multiplicado por sua probabilidade
		# Exemplo: chave "20-25", probabilidade 3% = 3 / 100
		# ["20-25" * 3]
		# Resultado: ["20-25","20-25","20-25"]

		for i in range(len(self.probabilidades)):
			self.lista += [self.probabilidades.keys()[i]] * self.probabilidades.values()[i][self.Servidor]

		# retorna random.uniform(x, y) # onde x e y é o intervalo. O método random.choice escolhe um valor qualquer na lista
		return self.probabilidades[random.choice(self.lista)][2]

sim = Simulacao(100)

def chegadas(env, nome, servidor):
	contador = 0
	while True:
		contador += 1
		yield env.timeout(1.5)
		print "%.2f\tUsuário %d chegou ao sistema" %(env.now, contador)
		env.process(Atendimento(env, "Usuário %d" %(contador), servidor))
		
def Atendimento(env, nome, servidor):
	request = servidor.request()
	yield request
	print "%.2f\t%s iniciou atendimento" %(env.now, nome)
	yield env.timeout(2)
	print "%.2f\t%s terminou atendimento" %(env.now, nome)
	yield servidor.release(request)
	
#~ env = simpy.Environment()
#~ servidor = simpy.Resource(env, capacity=2)
#~ env.process(chegadas(env, "Usuário", servidor))
#~ env.run(until=25)
