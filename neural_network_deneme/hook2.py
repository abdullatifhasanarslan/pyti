from pyprocessing import *
from random import randint,uniform
#CONSTANTS-----------------------------
WIDTH,HEIGHT = screen.width, screen.height #1920,1080
DISTANCE=200
SIZE_X, SIZE_Y = screen.width/2-DISTANCE/2,screen.height #1920/2-DISTANCE/2,1080
ORIJIN_X,ORIJIN_Y=0,0
HERO_SIZE=50
GOLD_AREA=200
SURVIVER=4
CHAMP_W_1,CHAMP_W_2,CHAMP_W_3=0,0,0
CHAMP_B_1,CHAMP_B_2,CHAMP_B_3=0,0,0

MAP_COLOR=50
GOLD_AREA_COLOR=(50,50,0)
GOLD_GAIN=1

HERO_COUNT=30
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
		object.objects.append(self)
		object.object_count+=1
	#DON'T WANT TO USE THIS
	def display(self):
		rect(self.x,self.y,self.size_x,self.size_y)
class MAP(object):
	"""Just a box nothing more"""
	def __init__(self,x=0,y=0,size_x=SIZE_X,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)

class GOLD(object):
	"""Just a box nothing more"""
	def __init__(self,x=0,y=0,size_x=GOLD_AREA,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
		
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
	left_alives=[]
	right_alives=[]
	left_heroes=[]
	right_heroes=[]
	def __init__(self,side,
				 mana=300,mana_regen=5,mana_gain=20,
				 cooldown=10,hook_range=700,hook_speed=50,hook_speed_gain=2,hook_size=10,
				 movement_speed=5,movement_gain=1,
				 level=1):
				 #turn_rate+vision_range is not considered for this game
		self.side=side#
		self.mana=mana;	self.mana_regen=mana_regen; self.mana_gain=mana_gain#
		self.cooldown=cooldown; self.hook_range=hook_range
		self.hook_speed=hook_speed; self.hook_size=hook_size#
		self.movement_speed=movement_speed; self.movement_gain=movement_gain#
		self.level=1
		
		self.status="MOVING"#MOVING,HOOKING,HOOKED,IDLE
		self.alive=True
		self.score=0
		self.movement_vector=[0,0]
		self.hook_animation_time=0
		self.hook_duration=self.hook_range/self.hook_speed
		self.hook_vector=[0,0]

		#enemydistance xy,walldistance xy,enemyhook xy M[]HERO_COUNT*2+2x1
		self.layer1=[]
		#M[]20xHERO_COUNT*2+4
		self.weight1=[[uniform(-10,10) for i in range(HERO_COUNT*2+2)] for j in range(20)]
		#M[]20x1
		self.bias1=[uniform(-1000,1000) for i in range(20)]
		
		#M[]20x1
		self.layer2=[]
		# M[]10x20
		self.weight2=[[uniform(-10,10) for i in range(20)] for j in range(10)]
		#M[]10x1
		self.bias2=[uniform(-1000,1000) for i in range(10)]

		#M[]10x1
		self.layer3=[0 for i in range(10)]
		# M[]16x10
		self.weight3=[[uniform(-10,10) for i in range(10)] for j in range(16)]
		#M[]16x1
		self.bias3=[uniform(-1000,1000) for i in range(16)]

		# #  #  #
		#  \ | /
		# #- X -#	X2 for both hook and move
		#  / | \
		# #  #  #
		self.action=[]

		#these conditions is just for placing and counting in the beginning purposes
		if side=="left":
			object.__init__(self,0,100+len(hero.left_heroes)*(HERO_SIZE+10),HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.left_alives.append(self)
			hero.left_heroes.append(self)
			self.image=loadImage("images/viper_left.png")
		elif side=="right":	
			object.__init__(self,screen.width-HERO_SIZE,screen.height-100-len(hero.right_heroes)*(HERO_SIZE+10)-HERO_SIZE,HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.right_alives.append(self)
			hero.right_heroes.append(self)
			self.image=loadImage("images/sniper_left.png")

	def move(self,angle):
		self.movement_vector=[cos(angle)*self.movement_speed,-sin(angle)*self.movement_speed]
		self.status="MOVING"
	def hook(self,angle):
		self.hook_vector=[cos(angle)*self.hook_speed,-sin(angle)*self.hook_speed]
		#self.hook_angle=angle
		self.status="HOOKING"
	#-------------
	def desicion(self):
		self.action=[sum([self.weight3[i][j]*self.layer3[j] for j in range(10)])+self.bias3[i] for i in range(16)]
		result=self.action.index(max(self.action))
		if result < 8:
			self.move((360/8)*result)
		else:
			self.hook((360/8)*(result-8))			
	def new_desicion(self):
		if randint(0,10)==3:
			if self.side == "left":
				self.weight1=[[hero.left_heroes[0].weight1[i][j]+uniform(-0.01,0.01) for j in range(HERO_COUNT*2+2)] for i in range(20)]
				self.bias1=[hero.left_heroes[0].bias1[i]+uniform(-1,1) for i in range(20)]
				self.weight2=[[hero.left_heroes[0].weight2[i][j]+uniform(-0.01,0.01) for j in range(20)] for i in range(10)]
				self.bias2=[hero.left_heroes[0].bias2[i]+uniform(-1,1) for i in range(10)]
				self.weight3=[[hero.left_heroes[0].weight3[i][j]+uniform(-0.01,0.01) for j in range(10)] for i in range(16)]
				self.bias3=[hero.left_heroes[0].bias3[i]+uniform(-1,1) for i in range(16)]
			else:
				self.weight1=[[hero.right_heroes[0].weight1[i][j]+uniform(-0.01,0.01) for j in range(HERO_COUNT*2+2)] for i in range(20)]
				self.bias1=[hero.right_heroes[0].bias1[i]+uniform(-1,1) for i in range(20)]
				self.weight2=[[hero.right_heroes[0].weight2[i][j]+uniform(-0.01,0.01) for j in range(20)] for i in range(10)]
				self.bias2=[hero.right_heroes[0].bias2[i]+uniform(-1,1) for i in range(10)]
				self.weight3=[[hero.right_heroes[0].weight3[i][j]+uniform(-0.01,0.01) for j in range(10)] for i in range(16)]
				self.bias3=[hero.right_heroes[0].bias3[i]+uniform(-1,1) for i in range(16)]
		else:
			self.weight1=[[uniform(-1,1) for j in range(HERO_COUNT*2+2)] for i in range(20)]
			self.bias1=[uniform(-1,1) for i in range(20)]
			self.weight2=[[uniform(-0.01,0.01) for j in range(20)] for i in range(10)]
			self.bias2=[uniform(-1,1) for i in range(10)]
			self.weight3=[[uniform(-0.01,0.01) for j in range(10)] for i in range(16)]
			self.bias3=[uniform(-1,1) for i in range(16)]
	#-------------
	def die(self):
		if self.side=="left":
			hero.left_alives.remove(self)
		else:
			hero.right_alives.remove(self)
	def update(self):
		global HERO_COUNT,L,R
		#enemydistance xy,walldistance xy,enemyhook xy M[]HERO_COUNT*2+2x1
		if self.side=="left":
			self.layer1=[hero.right_heroes[i].x-self.x for i in range(HERO_COUNT)]
			self.layer1+=[hero.right_heroes[i].y-self.y for i in range(HERO_COUNT)]
			self.layer1+=[self.x-left_side.x,self.y]
			if self.x>=left_side.x+SIZE_X-GOLD_AREA:
				self.score+=0.01
			else:
				self.score-=0.01
		elif self.side=="right":
			self.layer1=[hero.left_heroes[i].x-self.x for i in range(HERO_COUNT)]
			self.layer1+=[hero.left_heroes[i].y-self.y for i in range(HERO_COUNT)]
			self.layer1+=[self.x-right_side.x,self.y]
			if self.x<=right_side.x+GOLD_AREA:
				self.score+=0.01
			else:
				self.score-=0.01
		self.layer2=[sum([self.weight1[i][j]*self.layer1[j] for j in range(HERO_COUNT*2+2)])+self.bias1[i] for i in range(20)]
		self.layer3=[sum([self.weight2[i][j]*self.layer2[j] for j in range(20)])+self.bias2[i] for i in range(10)]

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
					if enemy.x <= self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time+self.hook_size and enemy.x+HERO_SIZE >= self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time+self.hook_size and ((enemy.y <= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time) or (enemy.y <= self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)):
					   self.score+=20
					   enemy.score-=20
			
			elif self.side=="right":
				for enemy in hero.left_heroes:
					if enemy.x <= self.x+self.hook_vector[0]*self.hook_animation_time-self.hook_size and enemy.x+HERO_SIZE >= self.x+self.hook_vector[0]*self.hook_animation_time-self.hook_size and ((enemy.y <= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time) or (enemy.y <= self.y+HERO_SIZE/2+self.hook_size/2+self.hook_vector[1]*self.hook_animation_time and enemy.y+HERO_SIZE >= self.y+HERO_SIZE/2+self.hook_size/2+self.hook_vector[1]*self.hook_animation_time)):
					   self.score+=20
					   enemy.score-=20

			


			if self.hook_animation_time>=self.hook_duration:
				self.hook_animation_time=0
				self.status="MOVING"

		if self.score<=-10:
			if self.side=="left":
				L+=1
			else:
				R+=1
			self.new_desicion()
			self.score=0
		if self.score>300:
			self.score=0
			self.new_desicion()
		if self.y < 0:
			self.y=0
		elif self.y>SIZE_Y-HERO_SIZE:
			self.y=SIZE_Y-HERO_SIZE	
	def display(self):
		image(self.image,self.x,self.y)
		if self.status=="HOOKING":
			if self.side=="left":
				line(self.x+HERO_SIZE,self.y+HERO_SIZE/2,self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)
				rect(self.x+HERO_SIZE+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time,self.hook_size,self.hook_size)
			elif self.side=="right":
				line(self.x,self.y+HERO_SIZE/2,self.x+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2+self.hook_vector[1]*self.hook_animation_time)
				rect(self.x-self.hook_size+self.hook_vector[0]*self.hook_animation_time,self.y+HERO_SIZE/2-self.hook_size/2+self.hook_vector[1]*self.hook_animation_time,self.hook_size,self.hook_size)
def die(eleman):
	pass
class score():
	def __init__(self):
		self.score=0
	def __repr__(self):
		return self.score
	def __add__(self,value):
		self.score+=value
		return self.score
	def __sub__(self,value):
		self.score-=value
		return self.score
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
	for at in range(len(hero.left_heroes)):
		if hero.left_heroes[at].status != "HOOKING":
			hero.left_heroes[at].desicion()
		hero.left_heroes[at].update()
		if at!=0:
			if hero.left_heroes[at].score > hero.left_heroes[at-1].score:
				hero.left_heroes[at-1],hero.left_heroes[at]=hero.left_heroes[at],hero.left_heroes[at-1]
	for at in range(len(hero.right_heroes)):
		if hero.right_heroes[at].status != "HOOKING":
			hero.right_heroes[at].desicion()
		hero.right_heroes[at].update()
		if at!=0:
			if hero.right_heroes[at].score > hero.right_heroes[at-1].score:
				hero.right_heroes[at-1],hero.right_heroes[at]=hero.right_heroes[at],hero.right_heroes[at-1]


	if FLOW:
		
		fill(255,255,0)
		text(str(hero.left_heroes[0].score), screen.width/2, 30)
		text(str(L),screen.width/2-20, 80)
		text(str(R),screen.width/2-20, 250)
		text(str(hero.right_heroes[0].score), screen.width/2, 200)
		fill(50)
		
		for rectangle in object.objects:
			rectangle.display()
		fill(255,255,0)
		rect(hero.left_heroes[0].x-5,hero.left_heroes[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
		rect(hero.right_heroes[1].x-5,hero.right_heroes[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
		fill(50)

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
	if key.char == "z":		
		FLOW = False
		key.char = " "
	elif key.char == " ":		
		ORIJIN_X,ORIJIN_Y=0,0
		key.char = " "








if __name__ == "__main__":
	run()
