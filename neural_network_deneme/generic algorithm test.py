from pyprocessing import *
from random import randint
#CONSTANTS-----------------------------
ORIJIN_X,ORIJIN_Y = 0,0
SIZE_X, SIZE_Y = 100,200
SPEED = 10
DISTANCE = 600
START = 700
BOX_LIMIT=25
#EVERY 70 ACTION WILL CONSIDERED AS 1 IN CROSSOVER
#1580
#FLOW CONTROLLERS----------------------
FLOW=True

#CLASSSES------------------------------
#--------------------------------------
#INTERFACE-----------------------------
class object:
	"""EVERY OBJECT"""
	objects=[]
	object_count=0
	def __init__(self,x,y,size_x,size_y):
		self.x,self.y,self.size_x,self.size_y=x,y,size_x,size_y
		object.objects.append(self)
		object.object_count+=1
	def display(self):
		rect(self.x,self.y,self.size_x,self.size_y)

class BOX(object):
	"""Just a box nothing more"""
	boxes=[]
	backup=[]
	def __init__(self,x,y,size_x=SIZE_X,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
		BOX.boxes.append(self)
		BOX.backup.append(self)

class BIRD(object):
	"""PHONEIX"""
	birds=[]
	alives=[]
	def __init__(self,x=0,y=0,size_x=50,size_y=50):
		object.__init__(self,x,y,size_x,size_y)
		self.image=loadImage("images/phoneix.png")
		self.vector = [SPEED,0]
		self.score=0
		self.desicion=DESICION()
		BIRD.birds.append(self)
		BIRD.alives.append(self)
	def flap(self):
		self.vector[1]=-10
	def update(self):
		self.vector[1]+=1
		self.x+=self.vector[0]
		self.y+=self.vector[1]
		if len(BOX.boxes)==0:
			VICTORY()
			return
		#IF REACHED TO NEXT TUNNEL
		if self.x+50>BOX.boxes[0].x:
			#IF IT IS NOT IN ALTITUTE TO ENTER THE TUNNEL
			if self.y<BOX.boxes[0].y or self.y+50>BOX.boxes[0].y+SIZE_Y:
				#IF IT IS IN TUNNEL
				if self.x<BOX.boxes[0].x+SIZE_X:
					FAIL()
				#IF IT PASSED THE TUNNEL
		if self.x>BOX.boxes[0].x+SIZE_X:
			BOX.boxes.pop(0)
			self.score+=1
	def display(self):
		image(self.image,self.x,self.y)

class DESICION:
	def __init__(self):
		self.action=[]
		for index in range(1080):
			if randint(0,1)==1:
				self.action+=[True]
			else:
				self.action+=[False]
		self.fitness=0

#VARIABLES
phoneix = BIRD(y=randint(0,screen.height-100))

#FUNCTIONS
def RESTART():
	global SPEED
	global phoneix
	BOX.boxes.clear()
	BOX.boxes=BOX.backup.copy()
	phoneix.x=0
	phoneix.y=randint(0,screen.height-100)
	phoneix.vector=[SPEED,0]
	phoneix.score=0


def FITNESS():
	def SELECTRION():
		def GENERIC():
			pass
		pass
def MUTATION():
	pass
def VICTORY():
	RESTART()
def FAIL():
	FITNESS()
	RESTART()
#GENERIC
def CROSSOVER():
	pass
def MUTATION():
	pass
def setup():
	global game_map,SIZE_Y,DISTANCE
	size(fullscreen=True)
	background(0,0,0)
	fill(50)
	stroke(150,150,0)
	strokeWeight(3)
	textFont(createFont("Times",30))
	current=START
	for i in range(BOX_LIMIT):
		BOX(current,randint(100,screen.height-200))
		current+=DISTANCE


def draw():
	global ORIJIN_X,ORIJIN_Y,FLOW
	global phoneix

	#FOR DISPLAY----------------------
	background(0,0,0)
	ORIJIN_X=phoneix.x
	translate(-ORIJIN_X,ORIJIN_Y)

	if key.char == "f":		
		FLOW = not FLOW
		key.char = " "
	elif key.char == "a":		
		phoneix.flap()
		key.char = " "

	if FLOW:
		phoneix.update()
		fill(255,255,0)
		text(str(phoneix.score), ORIJIN_X + screen.width/2, 30);
		fill(50)
	
	for rectangle in object.objects:
		rectangle.display()







if __name__ == "__main__":
	run()
