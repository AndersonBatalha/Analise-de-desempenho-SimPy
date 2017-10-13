#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

names = ["Chewbacca", "R2D2"]
faces = ["Cara", "Coroa"]
bankroll = [5,5]

def transfer(winner, looser, bankroll, tossCount):
	if winner == 0: 
		bankroll[0] += 1
		bankroll[1] -= 1
	elif winner == 1:
		bankroll[0] -= 1
		bankroll[1] += 1
	print ("\nRodada %d\nO vencedor é %s\nPlacar: %s (%d) x (%d) %s" %(tossCount, names[winner], names[0], bankroll[0], bankroll[1], names[1])) 

def coinToss(bankroll, tossCount):
	vencedor = random.randint(0,1)
	face_moeda = faces[vencedor]
	if vencedor == 0:
		transfer(0, 1, bankroll, tossCount)
	else:
		transfer(1, 0, bankroll, tossCount)

def run2Ruin(bankroll):
	print ("\nInício da partida\nPlacar: %s (%d) x (%d) %s" %(names[0], bankroll[0], bankroll[1], names[1])) 
	n_partidas = 0
	while bankroll[0] > 0 and bankroll[1] > 0:
		n_partidas += 1
		coinToss(bankroll, n_partidas)
	winner = bankroll[1] > bankroll[0]
	print ("\n\nJOGO ENCERRADO !!\n")
	print "Após %d rodadas, o vencedor é %s\n" %(n_partidas, names[winner])
	print "Dinheiro dos jogadores: ", bankroll

run2Ruin(bankroll)
