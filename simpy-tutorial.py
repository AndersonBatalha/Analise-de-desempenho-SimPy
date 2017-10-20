#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simpy-tutorial.py

import random # módulo gerador de números aleatórios
import simpy # biblioteca de simulação

random.seed(1000) #semente para o gerador de números aleatórios, garante a sequência de números geradoa será sempre a mesma
env = simpy.Environment() # variável que representa o ambiente de simulação do SimPy
