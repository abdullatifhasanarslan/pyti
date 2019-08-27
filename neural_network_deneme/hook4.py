from pyprocessing import *
from random import randint,uniform
from math import radians,sin,cos,atan,degrees
#CONSTANTS-----------------------------
WIDTH,HEIGHT = screen.width, screen.height #1920,1080
DISTANCE=200
SIZE_X, SIZE_Y = screen.width/2-DISTANCE/2,screen.height #1920/2-DISTANCE/2,1080
ORIJIN_X,ORIJIN_Y=0,0
HERO_SIZE=50
GOLD_AREA=500
SURVIVER=4

MAP_COLOR=50
GOLD_AREA_COLOR=(50,50,0)
GOLD_GAIN=0.05
GOLD_LOOSE=0.05
WIN=100
LOOSE=-10

HERO_COUNT=20
#FLOW CONTROLLERS----------------------
FLOW=True

L=0
R=0

#CLASSSES------------------------------
#--------------------------------------
#INTERFACE-----------------------------
class object:
	objects=[]
	object_count=0
	def __init__(self,x,y,size_x,size_y):
		self.x,self.y,self.size_x,self.size_y=x,y,size_x,size_y
	#DON'T WANT TO USE THIS
	def add(self):
		object.objects.append(self)
		object.object_count+=1
	def display(self):
		rect(self.x,self.y,self.size_x,self.size_y)
class MAP(object):
	"""Just a box nothing more"""
	def __init__(self,x=0,y=0,size_x=SIZE_X,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
		self.add()

class GOLD(object):
	"""Just a box nothing more"""
	def __init__(self,x=0,y=0,size_x=GOLD_AREA,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
		self.add()
		
	def display(self):
		fill(GOLD_AREA_COLOR[0],GOLD_AREA_COLOR[1],GOLD_AREA_COLOR[2])
		rect(self.x,self.y,self.size_x,self.size_y)
		fill(MAP_COLOR)

left_side = MAP()
left_gold = GOLD(SIZE_X-GOLD_AREA)
right_side = MAP(SIZE_X+DISTANCE)
right_gold = GOLD(SIZE_X+DISTANCE)
#class StatusBar:
"""HP+MANA+regen+armors+stats+items+skills"""


#HEROOOOOOOOOOOOOOOOOOOOOOOOOOES

class hero(object):
	"""every single hero is also a 'hero' object"""
	heroes=[]
	left_champ=0
	right_champ=0
	left_alives=[]
	right_alives=[]
	left_heroes=[]
	right_heroes=[]

	left_champ_weight1=[[uniform(-1,1) for j in range(HERO_COUNT+5)] for i in range(20+HERO_COUNT)]
	left_champ_weight2=[[uniform(-1,1) for j in range(20+HERO_COUNT)] for i in range(10)]
	left_champ_weight3=[[uniform(-1,1) for j in range(10)] for i in range(7)]
	right_champ_weight1=[[uniform(-1,1) for j in range(HERO_COUNT+5)] for i in range(20+HERO_COUNT)]
	right_champ_weight2=[[uniform(-1,1) for j in range(20+HERO_COUNT)] for i in range(10)]
	right_champ_weight3=[[uniform(-1,1) for j in range(10)] for i in range(7)]
	def __init__(self,side,
				 mana=300,mana_regen=5,mana_gain=20,
				 cooldown=10,hook_range=1000,hook_speed=50,hook_speed_gain=2,hook_size=10,
				 movement_speed=5,movement_gain=1,
				 level=1):
				 #turn_rate+vision_range is not considered for this game
		self.side=side#
		self.mana=mana;	self.mana_regen=mana_regen; self.mana_gain=mana_gain#
		self.cooldown=cooldown; self.hook_range=hook_range
		self.hook_speed=hook_speed; self.hook_size=hook_size#
		self.movement_speed=movement_speed; self.movement_gain=movement_gain#
		self.level=1
		
		self.status="MOVING"#MOVING,HOOKING,TURNING
		self.alive=True
		self.score=0
		self.movement_vector=[0,0]
		self.arrow_vector=[0,0]
		self.hook_animation_time=0
		self.hook_duration=self.hook_range/self.hook_speed
		self.hook_vector=[0,0]

		#M[]20xHERO_COUNT+5 X M[]HERO_COUNT+5x1 + M[]20x1
		self.layer1=[0 for i in range(HERO_COUNT+5)]
		self.weight1=[[uniform(-1,1) for i in range(HERO_COUNT+5)] for j in range(20+HERO_COUNT)]
		
		#M[]10x20 X M[]20x1 + M[]10x1
		self.layer2=[]
		self.weight2=[[uniform(-1,1) for i in range(20+HERO_COUNT)] for j in range(10)]

		#M[]4x10 X M[]10x1 + M[]4x1
		self.layer3=[0 for i in range(10)]
		self.weight3=[[uniform(-1,1) for i in range(10)] for j in range(7)]

		#turn left, turn right, hook, move
		self.action=[]

		#these conditions is just for placing and counting in the beginning purposes
		if side=="left":
			self.angle=0
			object.__init__(self,0,100+len(hero.left_heroes)*(HERO_SIZE+10),HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.left_alives.append(self)
			hero.left_heroes.append(self)
			self.image=loadImage("images/viper_left.png")
		elif side=="right":	
			self.angle=180
			object.__init__(self,screen.width-HERO_SIZE,screen.height-100-len(hero.right_heroes)*(HERO_SIZE+10)-HERO_SIZE,HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.right_alives.append(self)
			hero.right_heroes.append(self)
			self.image=loadImage("images/sniper_left.png")

	def turn_left(self):
		self.angle+=5
		if self.angle==360:
			self.angle=0
		self.status="IDLE"
	def turn_right(self):
		self.angle-=5
		if self.angle==-360:
			self.angle=0
		self.status="IDLE"
	def move(self):
		self.movement_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.arrow_vector=self.movement_vector[:]
		self.status="MOVING"
	def go_back(self):
		self.movement_vector=[-cos(radians(self.angle))*self.movement_speed,sin(radians(self.angle))*self.movement_speed]
		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.status="MOVING"
	def go_left(self):
		self.movement_vector=[-sin(radians(self.angle))*self.movement_speed,cos(radians(self.angle))*self.movement_speed]
		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.status="MOVING"
	def go_right(self):
		self.movement_vector=[sin(radians(self.angle))*self.movement_speed,-cos(radians(self.angle))*self.movement_speed]
		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.status="MOVING"
	def hook(self):
		self.hook_vector=[cos(radians(self.angle))*self.hook_speed,-sin(radians(self.angle))*self.hook_speed]
		self.status="HOOKING"

	#-------------
	def __distance(self,enemy):
		return ((self.x-enemy.x)**2+(self.y-enemy.y)**2)**0.5

	def desicion(self):
		self.action=[sum([self.weight3[i][j]*self.layer3[j] for j in range(10)]) for i in range(7)]
		result=self.action.index(max(self.action))
		if result == 0:
			self.turn_left()
		elif result == 1:
			self.turn_right()
		elif result == 2:
			self.move()
		elif result == 3:
			self.go_back()
		elif result == 4:
			self.go_left()
		elif result == 5:
			self.go_right()
		else:
			self.hook()			
	def new_desicion(self):
		if randint(0,10)>=7:
			if self.side == "left":
				self.weight1=[[hero.left_champ_weight1[i][j]+uniform(-0.1,0.1) for j in range(HERO_COUNT+5)] for i in range(20+HERO_COUNT)]
				self.weight2=[[hero.left_champ_weight2[i][j]+uniform(-0.1,0.1) for j in range(20+HERO_COUNT)] for i in range(10)]
				self.weight3=[[hero.left_champ_weight3[i][j]+uniform(-0.1,0.1) for j in range(10)] for i in range(7)]
			else:
				self.weight1=[[hero.right_champ_weight1[i][j]+uniform(-0.1,0.1) for j in range(HERO_COUNT+5)] for i in range(20+HERO_COUNT)]
				self.weight2=[[hero.right_champ_weight2[i][j]+uniform(-0.1,0.1) for j in range(20+HERO_COUNT)] for i in range(10)]
				self.weight3=[[hero.right_champ_weight3[i][j]+uniform(-0.1,0.1) for j in range(10)] for i in range(7)]
		else:
			self.weight1=[[uniform(-1,1) for j in range(HERO_COUNT+5)] for i in range(20+HERO_COUNT)]
			self.weight2=[[uniform(-1,1) for j in range(20+HERO_COUNT)] for i in range(10)]
			self.weight3=[[uniform(-1,1) for j in range(10)] for i in range(7)]
	#-------------
	def restart():
		hero.left_champ_weight1=hero.left_heroes[0].weight1
		hero.left_champ_weight2=hero.left_heroes[0].weight2
		hero.left_champ_weight3=hero.left_heroes[0].weight3
		hero.right_champ_weight1=hero.right_heroes[0].weight1
		hero.right_champ_weight2=hero.right_heroes[0].weight2
		hero.right_champ_weight3=hero.right_heroes[0].weight3
		for eleman in hero.heroes:
			eleman.score=0
			if not eleman.alive:
				eleman.new_desicion()
				eleman.alive=True
				if eleman.side == "left":
					hero.left_alives.append(eleman)
				else:
					hero.right_alives.append(eleman)
			if eleman.side == "left":
				eleman.x=left_side.x
				eleman.y=randint(0,screen.height-HERO_SIZE)
			else:
				eleman.x=right_side.x+SIZE_X-HERO_SIZE
				eleman.y=randint(0,screen.height-HERO_SIZE)
	def die(self):
		self.score=0
		if self.side=="left":
			hero.left_alives.remove(self)
			if len(hero.left_alives)==0:
				hero.restart()
		else:
			hero.right_alives.remove(self)
			if len(hero.right_alives)==0:
				hero.restart()
	def update(self):
		global HERO_COUNT,L,R,GOLD_GAIN,GOLD_LOOSE,WIN,LOOSE
		#enemydistance xy,walldistance xy,angle M[]HERO_COUNT+5x1
		if self.side=="left":

			
			self.layer1=[self.__distance(hero.right_heroes[i]) if hero.right_heroes[i].alive and (degrees(atan(-((hero.right_heroes[i].y+HERO_SIZE)-(self.y+HERO_SIZE/2))/((hero.right_heroes[i].x)-(self.x+HERO_SIZE))))<=self.angle and self.angle<=degrees(atan(-((hero.right_heroes[i].y)-(self.y+HERO_SIZE/2))/((hero.right_heroes[i].x+HERO_SIZE)-(self.x+HERO_SIZE)) ))) else 5000 for i in range(HERO_COUNT)]
			self.layer1+=[self.x,self.y,left_side.size_x-self.x,screen.height-self.y,left_side.x+GOLD_AREA-self.x]
			if self.x>=left_side.x+SIZE_X-GOLD_AREA:
				if self.x==left_side.x+SIZE_X-self.size_x:
					self.score-=GOLD_LOOSE	
				else:
					self.score+=GOLD_GAIN
			else:
				self.score-=GOLD_LOOSE

		elif self.side=="right":
			
			self.layer1=[self.__distance(hero.left_heroes[i]) if hero.left_heroes[i].alive and (degrees(atan(-((self.y+HERO_SIZE/2)-(hero.left_heroes[i].y+HERO_SIZE))/((self.x)-(hero.left_heroes[i].x+HERO_SIZE))))>=self.angle-180 and self.angle-180>=degrees(atan(-((self.y+HERO_SIZE/2)-(hero.left_heroes[i].y))/((self.x)-(hero.left_heroes[i].x)) ))) else 5000 for i in range(HERO_COUNT)]
			self.layer1+=[self.x-left_side.size_x,self.y,left_side.x+left_side.size_x-self.x,screen.height-self.y,left_side.size_x-GOLD_AREA-self.x]
			if self.x<=right_side.x+GOLD_AREA:
				if self.x == right_side.x:
					self.score-=GOLD_LOOSE
				else:
					self.score+=GOLD_GAIN
			else:
				self.score-=GOLD_LOOSE
		self.layer2=[sum([self.weight1[i][j]*self.layer1[j] for j in range(HERO_COUNT+5)]) for i in range(20+HERO_COUNT)]
		self.layer3=[sum([self.weight2[i][j]*self.layer2[j] for j in range(20+HERO_COUNT)]) for i in range(10)]

		if self.status=="MOVING":
			if self.movement_vector[0] < 0:
				if self.side=="left":
					if self.x-left_side.x >= -self.movement_vector[0]:
						self.x+=self.movement_vector[0]
					else:
						self.x=left_side.x
				elif self.side=="right":
					if self.x-right_side.x >= -self.movement_vector[0]:
						self.x+=self.movement_vector[0]
					else:
						self.x=right_side.x
			elif self.movement_vector[0] > 0:
				if self.side=="left":
					if left_side.x+SIZE_X-HERO_SIZE-self.x >= self.movement_vector[0]:
						self.x+=self.movement_vector[0]
					else:
						self.x=left_side.x+SIZE_X-HERO_SIZE
				elif self.side=="right":
					if right_side.x+SIZE_X-HERO_SIZE-self.x >= self.movement_vector[0]:
						self.x+=self.movement_vector[0]
					else:
						self.x=right_side.x+SIZE_X-HERO_SIZE
			if self.movement_vector[1] < 0:
				if self.y >= -self.movement_vector[1]:
					self.y+=self.movement_vector[1]
				else:
					self.y=0
			elif self.movement_vector[1] > 0:
				if SIZE_Y-HERO_SIZE-self.y >= self.movement_vector[1]:
					self.y+=self.movement_vector[1]
				else:
					self.y=SIZE_Y-HERO_SIZE

		elif self.status=="HOOKING":

			self.hook_animation_time+=1
			
			if self.side=="left":
				for enemy in hero.right_heroes:
					if enemy.alive and enemy.x <= self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time+self.hook_size and enemy.x+HERO_SIZE >= self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time+self.hook_size and ((enemy.y <= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time) or (enemy.y <= self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)):
					   self.score+=20
					   enemy.score-=20
			
			elif self.side=="right":
				for enemy in hero.left_heroes:
					if enemy.alive and enemy.x <= self.x+self.hook_vector[0]*self.hook_animation_time-self.hook_size and enemy.x+HERO_SIZE >= self.x+self.hook_vector[0]*self.hook_animation_time-self.hook_size and ((enemy.y <= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time) or (enemy.y <= self.y+HERO_SIZE/2+self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2+self.hook_size/2+self.hook_vector[1]*self.hook_animation_time)):
					   self.score+=20
					   enemy.score-=20

			


			if self.hook_animation_time>=self.hook_duration:
				self.hook_animation_time=0
				self.status="IDLE"

		elif self.status=="IDLE":
			pass

		if self.score<=LOOSE:
			if self.side=="left":
				L+=1
			else:
				R+=1
			self.alive=False
			#self.new_desicion()
		if self.score>=WIN:
			self.score=0
			self.new_desicion()
			hero.restart()
		if self.y < 0:
			self.y=0
		elif self.y>SIZE_Y-HERO_SIZE:
			self.y=SIZE_Y-HERO_SIZE	
	def display(self):
		image(self.image,self.x,self.y)
		if self.status=="MOVING":
			for i in range(HERO_COUNT):
				if 0<self.layer1[i] and self.layer1[i]<=self.hook_range:
					stroke(255,0,0)
			if self.side=="left":
				line(self.x+HERO_SIZE,self.y+HERO_SIZE/2,self.x+HERO_SIZE+self.arrow_vector[0]*5,self.y+HERO_SIZE/2+self.arrow_vector[1]*5)
			else:
				line(self.x,self.y+HERO_SIZE/2,self.x+self.arrow_vector[0]*5,self.y+HERO_SIZE/2+self.arrow_vector[1]*5)
			stroke(150,150,0)
		elif self.status=="HOOKING":
			if self.side=="left":
				line(self.x+HERO_SIZE,self.y+HERO_SIZE/2,self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)
				rect(self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time,self.hook_size,self.hook_size)
			elif self.side=="right":
				line(self.x,self.y+HERO_SIZE/2,self.x+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)
				rect(self.x-self.hook_size+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time,self.hook_size,self.hook_size)

#VARIABLES-----------------------------
#MAP-----
def setup():
	global HERO_COUNT
	size(fullscreen=True)
	background(0,0,0)
	fill(50)
	stroke(150,150,0)
	strokeWeight(3)
	for i in range(HERO_COUNT):
		hero("left")
		hero("right")


def draw():
	global ORIJIN_X,ORIJIN_Y,FLOW,L,R


	#FOR DISPLAY----------------------
	background(0,0,0)
	#translate(ORIJIN_X,ORIJIN_Y)

	if FLOW:	
		for rectangle in object.objects:
			rectangle.display()
		try:
			fill(255,255,0)
			text(str(hero.left_alives[0].score), screen.width/2, 30)
			text(str(L),screen.width/2-20, 80)
			text(str(R),screen.width/2-20, 250)
			text(str(hero.right_alives[0].score), screen.width/2, 200)
			fill(50)

			fill(255,255,0)
			rect(hero.left_alives[0].x-5,hero.left_alives[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
			rect(hero.right_alives[0].x-5,hero.right_alives[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
			fill(50)
		except:
			pass

		for at in hero.left_alives:
			at.display()
		for at in hero.right_alives:
			at.display()
	if len(hero.left_alives) != 0:
		for at in range(len(hero.left_alives)):
			if at!=0 and len(hero.left_alives)!=1:
				if hero.left_alives[at].score > hero.left_alives[at-1].score:
					hero.left_alives[at-1],hero.left_alives[at]=hero.left_alives[at],hero.left_alives[at-1]
					if hero.left_alives[at-1].status != "HOOKING":
						hero.left_alives[at-1].desicion()
					hero.left_alives[at-1].update()
				else:
					if hero.left_alives[at].status != "HOOKING":
						hero.left_alives[at].desicion()
					hero.left_alives[at].update()

			else:
				if hero.left_alives[at].status != "HOOKING":
					hero.left_alives[at].desicion()
				hero.left_alives[at].update()
	if len(hero.right_alives) != 0:
		for at in range(len(hero.right_alives)):
			if at!=0 and len(hero.right_alives)!=1:
				if hero.right_alives[at].score > hero.right_alives[at-1].score:
					hero.right_alives[at-1],hero.right_alives[at]=hero.right_alives[at],hero.right_alives[at-1]
					if hero.right_alives[at-1].status != "HOOKING":
						hero.right_alives[at-1].desicion()
					hero.right_alives[at-1].update()
				else:
					if hero.right_alives[at].status != "HOOKING":
						hero.right_alives[at].desicion()
					hero.right_alives[at].update()
			else:
				if hero.right_alives[at].status != "HOOKING":
					hero.right_alives[at].desicion()
				hero.right_alives[at].update()
	if len(hero.left_heroes) != 0:
		for at in range(len(hero.left_heroes)):
			if at!=0 and len(hero.left_heroes)!=1:
				if hero.left_heroes[at].score > hero.left_heroes[at-1].score:
					hero.left_heroes[at-1],hero.left_heroes[at]=hero.left_heroes[at],hero.left_heroes[at-1]
	if len(hero.right_heroes) != 0:
		for at in range(len(hero.right_heroes)):
			if at!=0 and len(hero.right_heroes)!=1:
				if hero.right_heroes[at].score > hero.right_heroes[at-1].score:
					hero.right_heroes[at-1],hero.right_heroes[at]=hero.right_heroes[at],hero.right_heroes[at-1]
	for eleman in hero.left_alives:
		if not eleman.alive:
			eleman.die()
	for eleman in hero.right_alives:
		if not eleman.alive:
			eleman.die()
	#ALL FLOW GOES FROM HERE----------
	

	
	#MOUSE BINDINGS------------------
	"""
	PRESS AND DRAG TO MOVE WORKSPACE
	"""
	if mouse.pressed:
		ORIJIN_X += mouse.x-pmouse.x
		ORIJIN_Y += mouse.y-pmouse.y

	#KEY BINDINGS--------------------
	"""
	F:FLOW
	R:RESET ORIJIN
	A:ZOOM IN
	S:ZOOM OUT
	"""
	if key.char == "a":		
		FLOW = True
		key.char = " "
	elif key.char == "z":		
		FLOW = False
		key.char = " "
	elif key.char == "p":		
		print("lcw1",hero.left_champ_weight1)
		print("lcw2",hero.left_champ_weight2)
		print("lcw3",hero.left_champ_weight3)
		print("rcw1",hero.right_champ_weight1)
		print("rcw2",hero.right_champ_weight2)
		print("rcw3",hero.right_champ_weight3)
		key.char = " "
	elif key.char == "r":		
		hero.restart()
		key.char = " "








if __name__ == "__main__":
	run()
