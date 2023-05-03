import math
#Standard lib
import os
import random
import sys
import time

import camera
import display
import pylunky.player as player
import pygame
#Own Files
import readmap

pygame.init()
height = 320
width = 320
window = pygame.display.set_mode((height,width),pygame.RESIZABLE)
pygame.display.set_caption('PyLunky!')
screen = pygame.display.get_surface()
screen.convert_alpha()
clock = pygame.time.Clock()

def main():
	
	global gameinfo
	gameinfo = readmap.ReadMap('resources/maps/1.map')
	player = player.Player(x=gameinfo.gamemap.start[0]*32,y=gameinfo.gamemap.start[1]*32, direction=0, speed=0)
	
	cam = camera.cam(player.x, player.y, width, height, gameinfo.gamemap.width()*32, gameinfo.gamemap.height()*32)
	
	ui = display.display()

	while True:

		pygame.event.pump()

		player.loop(gameinfo, screen)

		event = pygame.event.poll()
		
		#Gamemap display
		for k in gameinfo.gamemap.map():
			for i in k:						
				screen.blit(i.mat, (i.posx*32-cam.x,i.posy*32-cam.y))

		#Entity display
		for ent in gameinfo.entlist.entlist:
			offcount = (32-ent.height,32-ent.width)
			screen.blit(ent.mat, 
			(ent.position()[0]+offcount[0]/2-cam.x,
			ent.position()[1]+offcount[1]-cam.y))
		
		#Player display
		screen.blit(player.image, (player.x-cam.x,player.y-cam.y))

		#UI elements
		ui.ui(screen, cam, player, gameinfo)

		#Camera update
		cam.move(player.x, player.y)

		pygame.display.flip()
		clock.tick(90)

main()
