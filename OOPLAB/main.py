# -*- coding: utf-8 -*-
import pygame
import time
import random
pygame.init()
win = pygame.display.set_mode([1200,1150])
pygame.display.set_caption("COROnAVIRUS:ESCAPE FROM LAB")
sides = {'LEFT':(-1,0),'RIGHT':(1,0),'UP':(0,-1),'DOWN':(0,1)}
images = {0:pygame.image.load("wall.png"),1:pygame.image.load("floor.png"),2:pygame.image.load("door.png"),3:pygame.image.load("probirkas.png")}
field = []
scientists = []
timer = 0
finishes = {1:61,2:56,3:418,4:167,5:260}
file = open("field.txt",'r')
lines = file.readlines()
field = []
for line in lines:
	field.append(list(map(int, line.split(" "))))
graph = [[] for j in range(466)]
smth = 1
for i in range(21):
	for j in range(21):
		if field[i][j]==1:
			if i>= 1:
				if field[i-1][j]==1:
					graph[smth-21].append(smth)
			if i<= 21 :
				if field[i+1][j]==1:
					graph[smth+21].append(smth)

			if j>= 1:
				if field[i][j-1]==1:
					graph[smth-1].append(smth)
			if j<= 21 :
				if field[i][j+1]==1:
					graph[smth+1].append(smth)
		smth+=1

print(graph)
def to_coords(x):
	return (x//21+(x%21),x%21 if x%21!=0 else 21)


def astar(start,finish):
	fr = [-1 for i in range(453)]
	dist = [1000000 for i in range(453)]
	pq = [start]
	dist[start] = 0
	while len(pq)>0:
		current = pq.pop(0)
		for top in graph[current]:
			if dist[top]>dist[current]+1:
				dist[top] = dist[current]+1
				fr[top] = current
			pq.append(top)
		sorted(pq,key =  lambda a: abs(to_coords(a)[0] - to_coords(fin)[0]) + abs(to_coords(a)[1] - to_coords(fin)[1]))
		if fr[finish]!=-1:
			break
	path = []
	current = finish
	while fr[current]!=-1:
		path.append(current)
		current = fr[current]
	path.append(start)
	print("path",path)
	return path

def draw():
		global win
		win.fill((255,255,255))
		for i in range(21):
			for j in range(21):
				win.blit(images[field[i][j]],(50+j*50,i*50))
		for pers in scientists:
			win.blit(pers.textures[pers.side],(pers.x*50,pers.y*50))
		pygame.display.update()

def move_all():
	for man in scientists:
		man.move()

#Функція виводу тексту
def echo(word,x,y,fsize,color):
	font = pygame.font.SysFont('Comic Sans MS', fsize)#Підключення шрифту відповідного розміру
	text = font.render(word, True, color)#Cтворення об*єкта з текстом
	win.blit(text, [x, y] )#та вивід його на екран в заданих координатах

def winlose():
	win.fill((255,255,255))

class sciensist:
	textures = {"LEFT":pygame.image.load("sciencistLeft.png"),"RIGHT":pygame.image.load("sciencistRight.png"),"UP":pygame.image.load("sciencistUp.png"),"DOWN":pygame.image.load("sciencistDown.png")}
	x,y = None,None
	temperature = 36.6
	infected = False
	astar = []
	side = "LEFT"
	point = 1
	thing = 0
	def __init__(self,x,y,temp = 36.6):
		self.x = x
		self.y = y
		self.temperature = temp
		self.infected = False
		self.point = 1

	def move(self):
		if self.infected == True:
			pass
		elif self.astar!=[]:
			next_point = to_coords(astar.pop(0))
			self.x,self.y = next_point[1],next_point[0]
		elif self.astar == [] and self.thing == 50:
			self.thing = 0
			self.astar = astar(2,14)
		elif self.thing == 0:
			self.do_thing()

	def rize(self):
		self.temperature+=0.2
		
	def do_thing(self):
		side = random.choice(["LEFT,RIGHT,UP,DOWN"])
		self.thing += 0.1



scientists.append(sciensist(14,2))
scientists.append(sciensist(20,20))
scientists.append(sciensist(8,13))
scientists.append(sciensist(20,13))
scientists.append(sciensist(20,8))

class virus:
	vx = 0
	vy = 0
	victim = None
	indVictim = None
	def __init__(self,x = 0,y = 0):
		self.x = x
		self.y = y

	def infect(self):
		global scientists
		aviable = self.scan()
		if hero==None:
			self.victim = aviable[0]
			self.indVictim = scientists.index(self.victim)
			scientists[indVictim].infected = True
			scientists[indVictim].astar = []
			self.indVictim.astar = []
		else:
			scientists[indVictim].infected = False
	
	def move(self,side):
		if self.victim == None:
			pass
		else:
			self.victim.x = self.victim.x + sides[side][0]
			self.victim.y = self.victim.y + sides[side][1]
			self.vx,self.vy= self.victim.x,self.victim.y

	def scan(self):
		global scientists
		global field
		aviable = []
		wars = [-1,0,1]
		for i in wars:
			for j in wars:
				cx = self.vx + i
				cy = self.vy + j
				if 0<=cx<=21 and 0<=cy<=21:
					for man in scientists:
						if man!=self.victim and man.x == cx and man.y == cy:
							aviable.append(man)
		return aviable

	def winlose(self):
		global field
		if self.victim!=None:
			if field[self.victim.y][self.victim.x] == 2:
				return "win"
			if self.victim.temperature > 38.6:
				return "Lose"


mh = virus()

while True:
	pygame.time.delay(100)
	move_all()
	draw()
	print(scientists[1].astar)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			break
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		break
	elif keys[pygame.K_UP]:
		mh.move("UP")
	elif keys[pygame.K_DOWN]:
		mh.move("DOWN")
	elif keys[pygame.K_LEFT]:
		mh.move("LEFT")
	elif keys[pygame.K_RIGHT]:
		mh.move("RIGHT")
	elif keys[pygame.K_SPACE]:
		mh.infect()
	timer+=0.1
	if timer==3:
		timer==0
		
pygame.quit()