from pyprocessing import *
from random import randint
#CONSTANTS-----------------------------
ORIJIN_X,ORIJIN_Y = 0,0
SIZE_X, SIZE_Y = 100,200
SPEED = 10
DISTANCE = 600
START = 700
BOX_LIMIT=25
SURVIVER=4
#EVERY 70 ACTION WILL CONSIDERED AS 1 IN CROSSOVER
#1580
#FLOW CONTROLLERS----------------------
FLOW=True
TICK=0

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
		self.fitness=0
		self.desicion=DESICION()
		self.alive=True
		BIRD.birds.append(self)
		BIRD.alives.append(self)
	def flap(self):
		self.vector[1]=-10
	def die(self):
		BIRD.alives.remove(self)
		self.vector=[0,0]
		self.alive=False
	def reborn(self):
		global SPEED
		self.x=0
		self.y=screen.height/2 #randint(0,screen.height-100)
		self.vector=[SPEED,0]
		self.alive=True
		BIRD.alives.append(self)
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
					FAIL(self)
		#IF IT PASSED THE TUNNEL
		if self.x>BOX.boxes[0].x+SIZE_X:
			BOX.boxes.pop(0)
			#self.score+=1
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
	def update(self):
		self.action.clear()
		for index in range(1080):
			if randint(0,1)==1:
				self.action+=[True]
			else:
				self.action+=[False]
		#self.fitness=0

#VARIABLES

#FUNCTIONS
def RESTART():
	global TICK
	BOX.boxes.clear()
	BOX.boxes=BOX.backup.copy()
	for phoneix in BIRD.birds:
		if phoneix.alive:
			phoneix.die()
			phoneix.reborn()
		else:
			phoneix.reborn()
	TICK=0
		#phoneix.score=0
def VICTORY():
	global FLOW
	FLOW=False
	"""
	for phoneix in BIRD.birds:
		if phoneix.alive:
			phoneix.die()
			phoneix.reborn()
		else:
			phoneix.reborn()
	RESTART()
	"""
def FAIL(phoneix):
	global SURVIVER
	phoneix.die()
	if len(BIRD.alives)==0:
		survivers=[]
		diers=[]
		for bird in BIRD.birds:
			FITNESS(bird)

			if len(survivers)==0:
				survivers.append(bird)
			for i in range(len(survivers)):
				if survivers[i].fitness<=bird.fitness:
					survivers.insert(i,bird)
					break
				elif i==len(survivers)-1 and i!=SURVIVER:
					survivers.append(bird)
					break
			else:
				diers.append(bird)
			if len(survivers)>SURVIVER:
				diers.append(survivers.pop(SURVIVER))
		print(survivers[0].fitness,survivers[1].fitness,survivers[2].fitness,survivers[3].fitness)
		for bird in diers:
			#print(bird.fitness)
			bird.desicion.update()
		#print(len(diers),len(survivers))
		survivers.clear()
		diers.clear()
		RESTART()
					
					#print(fitness)
	#RESTART()
def FITNESS(bird):
	bird.fitness=bird.x-abs((bird.y-(BOX.boxes[0].y+SIZE_Y/2)))*0.0001
	return bird.fitness
	
	"""
	def SELECTION():
		def GENERIC():
			pass
		pass
	"""
"""

def MUTATION():
	pass
#GENERIC
def CROSSOVER():
	pass
def MUTATION():
	pass
"""
def setup():
	global game_map,SIZE_Y,DISTANCE
	size(fullscreen=True)
	background(0,0,0)
	fill(50)
	stroke(150,150,0)
	strokeWeight(3)
	textFont(createFont("Times",30))
	current=START
	for i in range(10):
		phoneix = BIRD(y=screen.height/2) #BIRD(y=randint(0,screen.height-100))
	BOX(current,0)
	current+=DISTANCE	
	for i in range(BOX_LIMIT):
		BOX(current,randint(100,screen.height-200))
		current+=DISTANCE


def draw():
	global ORIJIN_X,ORIJIN_Y,FLOW,TICK,SPEED

	#FOR DISPLAY----------------------
	background(0,0,0)

	if key.char == " ":		
		FLOW = not FLOW
		key.char = " "
	elif key.char == "f":		
		#phoneix.flap()
		RESTART()
		key.char = " "

	if FLOW:
		TICK+=1
		ORIJIN_X=TICK*SPEED
		translate(-ORIJIN_X,ORIJIN_Y)
		for phoneix in BIRD.alives:
			if phoneix.desicion.action[TICK]:
				phoneix.flap()			
			phoneix.update()
		"""
		fill(255,255,0)
		text(str(phoneix.score), ORIJIN_X + screen.width/2, 30);
		fill(50)
		"""
	for rectangle in object.objects:
		rectangle.display()







if __name__ == "__main__":
	run()
