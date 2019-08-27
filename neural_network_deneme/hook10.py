from pyprocessing import *
from random import randint,uniform
from math import radians,sin,cos,atan,degrees
import numpy as np
#CONSTANTS-----------------------------
WIDTH,HEIGHT = screen.width, screen.height #1920,1080
DISTANCE=0
SIZE_X, SIZE_Y = screen.width/2-DISTANCE/2,screen.height #1920/2-DISTANCE/2,1080
ORIJIN_X,ORIJIN_Y=0,0
HERO_SIZE=50
GOLD_AREA=175
SURVIVER=4

LAST_GAME=0

MAP_COLOR=50
GOLD_AREA_COLOR=(50,50,0)
GOLD_GAIN=0.2
GOLD_LOOSE=0.1
WIN=150
LOOSE=-10
RESTART=False
COOLDOWN=5

MATCH=1

HERO_COUNT=30
#FLOW CONTROLLERS----------------------
FLOW=True

L=0
R=0

large_font = createFont("Times New Roman", 30); 
small_font = createFont("Times New Roman", 12); 



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
	left_alives=[]
	right_alives=[]
	left_heroes=[]
	right_heroes=[]
	player=0

	if LAST_GAME==0:
		left_champ_weight1= np.matrix(np.zeros(((20,9))))
		left_champ_weight2= np.matrix(np.zeros((10,20)))
		left_champ_weight3= np.matrix(np.zeros((8,10)))
		right_champ_weight1= np.matrix(np.zeros((20,9)))
		right_champ_weight2= np.matrix(np.zeros((10,20)))
		right_champ_weight3= np.matrix(np.zeros((8,10)))
		left_champ_bias1= np.matrix(np.zeros(20))
		left_champ_bias2= np.matrix(np.zeros(10))
		left_champ_bias3= np.matrix(np.zeros(8))
		right_champ_bias1= np.matrix(np.zeros(20))
		right_champ_bias2= np.matrix(np.zeros(10))
		right_champ_bias3= np.matrix(np.zeros(8))

	elif LAST_GAME==1:
		pass
	def __init__(self,side,
				 mana=300,mana_regen=5,mana_gain=20,
				 cooldown=10,hook_range=300,hook_speed=50,hook_speed_gain=2,hook_size=5,
				 movement_speed=5,movement_gain=1,
				 level=1,player=False):
				 #turn_rate+vision_range is not considered for this game
		self.player=player
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
		self.hook_animation_time=0
		self.hook_duration=self.hook_range/self.hook_speed
		self.hook_vector=[0,0]

		#8 INPUT, 20x10 INNER, 8 OUTPUT
		self.layer1=np.zeros(9)
		self.layer2=np.zeros(20)
		self.layer3=np.zeros(10)

		#turn left, turn right, hook, move
		self.action=[]

		#these conditions is just for placing and counting in the beginning purposes
		if side=="left":
			self.angle=0
			object.__init__(self,500,100+len(hero.left_heroes)*(HERO_SIZE+10),HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.left_alives.append(self)
			hero.left_heroes.append(self)
			self.image=loadImage("images/viper_left.png")

			self.weight1=hero.left_champ_weight1
			self.weight2=hero.left_champ_weight2
			self.weight3=hero.left_champ_weight3
			self.bias1=hero.left_champ_bias1
			self.bias2=hero.left_champ_bias2
			self.bias3=hero.left_champ_bias3
		elif side=="right":	
			self.angle=180
			object.__init__(self,screen.width-HERO_SIZE-500,screen.height-100-len(hero.right_heroes)*(HERO_SIZE+10)-HERO_SIZE,HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.right_alives.append(self)
			hero.right_heroes.append(self)
			self.image=loadImage("images/sniper_left.png")


			self.weight1=hero.right_champ_weight1
			self.weight2=hero.right_champ_weight2
			self.weight3=hero.right_champ_weight3
			self.bias1=hero.right_champ_bias1
			self.bias2=hero.right_champ_bias2
			self.bias3=hero.right_champ_bias3

		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		if self.player:
			hero.player=self
	"""
	def __repr__(self):
		print(self.score)
		return str(self.score)
	"""
	def turn_left(self):
		self.angle+=5
		if self.angle>=180:
			self.angle=-179
		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.status="IDLE"
	def turn_right(self):
		self.angle-=5
		if self.angle<=-180:
			self.angle=179
		self.arrow_vector=[cos(radians(self.angle))*self.movement_speed,-sin(radians(self.angle))*self.movement_speed]
		self.status="IDLE"
	def move(self):
		if self.side=="left":
			self.movement_vector=[self.movement_speed,0]
		else:
			self.movement_vector=[-self.movement_speed,0]
		self.status="MOVING"
	def go_back(self):
		if self.side=="left":
			self.movement_vector=[-self.movement_speed,0]
		else:
			self.movement_vector=[self.movement_speed,0]
		self.status="MOVING"
	def go_left(self):
		if self.side=="left":
			self.movement_vector=[0,-self.movement_speed]
		else:
			self.movement_vector=[0,self.movement_speed]
		self.status="MOVING"
	def go_right(self):
		if self.side=="left":
			self.movement_vector=[0,self.movement_speed]
		else:
			self.movement_vector=[0,-self.movement_speed]
		self.status="MOVING"
	def hook(self):
		if self.cooldown>0:
			self.score-=10
			self.status="IDLE"
		else:
			self.hook_vector=[cos(radians(self.angle))*self.hook_speed,-sin(radians(self.angle))*self.hook_speed]
			self.status="HOOKING"
			self.cooldown=COOLDOWN

	#-------------
	def __distance(self,enemy):
		return ((self.x-enemy.x)**2+(self.y-enemy.y)**2)**0.5

	def desicion(self):
		if not self.player:
			self.action=np.argmax(np.array(sum([self.weight3*self.layer3 for j in range(10)]))+self.bias3 for i in range(8))
			result=self.action
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
		del self.weight1,self.weight2,self.weight3,self.bias1,self.bias2,self.bias3
		if randint(0,10)>=3:
			if self.side == "left":
				self.weight1=hero.left_champ_weight1+np.random.rand(20,9)
				self.weight2=hero.left_champ_weight2+np.random.rand(10,20)
				self.weight3=hero.left_champ_weight3+np.random.rand(8,10)
				self.bias1=hero.left_champ_bias1+np.random.rand(20)
				self.bias2=hero.left_champ_bias2+np.random.rand(10)
				self.bias3=hero.left_champ_bias3+np.random.rand(8)
			else:
				self.weight1=hero.right_champ_weight1+np.random.rand(3,2)
				self.weight2=hero.right_champ_weight2+np.random.rand(10,20)
				self.weight3=hero.right_champ_weight3+np.random.rand(8,10)
				self.bias1=hero.right_champ_bias1+np.random.rand(20)
				self.bias2=hero.right_champ_bias2+np.random.rand(10)
				self.bias3=hero.right_champ_bias3+np.random.rand(8)
		else:
			self.weight1=np.random.rand(20,9)
			self.weight2=np.random.rand(10,20)
			self.weight3=np.random.rand(8,10)

			self.bias1=np.random.rand(20)
			self.bias2=np.random.rand(10)
			self.bias3=np.random.rand(8)
	#-------------
	def restart():
		global MATCH,WIN,RESTART
		hero.left_champ_weight1=hero.left_heroes[0].weight1.copy()
		hero.left_champ_weight2=hero.left_heroes[0].weight2.copy()
		hero.left_champ_weight3=hero.left_heroes[0].weight3.copy()
		hero.right_champ_weight1=hero.right_heroes[0].weight1.copy()
		hero.right_champ_weight2=hero.right_heroes[0].weight2.copy()
		hero.right_champ_weight3=hero.right_heroes[0].weight3.copy()

		hero.left_champ_bias1=hero.left_heroes[0].bias1.copy()
		hero.left_champ_bias2=hero.left_heroes[0].bias2.copy()
		hero.left_champ_bias3=hero.left_heroes[0].bias3.copy()
		hero.right_champ_bias1=hero.right_heroes[0].bias1.copy()
		hero.right_champ_bias2=hero.right_heroes[0].bias2.copy()
		hero.right_champ_bias3=hero.right_heroes[0].bias3.copy()
		MATCH+=1;WIN+=0.5
		i=0
		for eleman in hero.left_alives:
			if i>=SURVIVER:
				eleman.new_desicion()
			else:
				i+=1
		i=0
		for eleman in hero.right_alives:
			if i>=SURVIVER:
				eleman.new_desicion()
			else:
				i+=1
		for eleman in hero.heroes:
			eleman.score=0
			eleman.cooldown=COOLDOWN
			if eleman.alive==False:
				eleman.new_desicion()
				eleman.alive=True
				if eleman.side == "left":
					eleman.angle=0
					hero.left_alives.append(eleman)
				else:
					eleman.angle=180
					hero.right_alives.append(eleman)
			if eleman.side == "left":
				eleman.x=left_side.x+500
				eleman.angle=0
				eleman.y=randint(0,screen.height-HERO_SIZE)
			else:
				eleman.x=right_side.x+SIZE_X-HERO_SIZE-500
				eleman.angle=180
				eleman.y=randint(0,screen.height-HERO_SIZE)
			eleman.turn_left()
			eleman.turn_right()
			eleman.move()
		#print("l",len(hero.left_alives))
		#print("r",len(hero.right_alives))
		#print()
		RESTART=False
		"""
		print(len(hero.heroes))
		print(len(hero.left_heroes),len(hero.left_alives))
		print(len(hero.right_heroes),len(hero.right_alives))
		print(len(hero.left_heroes[0].layer1),len(hero.left_heroes[0].weight1))
		print()
		"""
	"""
	def die(self):
		global RESTART
		if self.side=="left":
			hero.left_alives.remove(self)
			if len(hero.left_alives)==0:
				RESTART=True
		else:
			hero.right_alives.remove(self)
			if len(hero.right_alives)==0:
				RESTART=True
	"""
	def update(self):
		global HERO_COUNT,L,R,GOLD_GAIN,GOLD_LOOSE,WIN,LOOSE,RESTART
		#enemydistance xy,walldistance xy,angle M[]6x1
		if self.side=="left":
			if 90>self.angle and self.angle>-90:
				found =False
				for i in range(len(hero.right_alives)):
					if hero.right_alives[i].alive:
						if degrees(atan(-((hero.right_alives[i].y)-(self.y+HERO_SIZE/2))/((hero.right_alives[i].x+HERO_SIZE)-(self.x+HERO_SIZE))))>=self.angle and self.angle>=degrees(atan(-((hero.right_alives[i].y+HERO_SIZE)-(self.y+HERO_SIZE/2))/((hero.right_alives[i].x+HERO_SIZE)-(self.x+HERO_SIZE)) )) and self.__distance(hero.right_alives[i])<=self.hook_range:
							self.layer1[0]=1
							hero.right_alives[i].layer1[1]=1
							found=True
							break
				if not found:
					self.layer1[0]=0

			self.layer1[2]=self.x
			self.layer1[3]=left_side.size_x-self.x
			self.layer1[4]=self.y
			self.layer1[5]=screen.height-self.y
			self.layer1[6]=left_side.x+left_side.size_x-GOLD_AREA-self.x
			self.layer1[7]=self.angle
			self.layer1[8]=self.cooldown
			if self.score<=100:
				if self.x+self.size_x>=left_side.x+SIZE_X-GOLD_AREA:
					if self.x==left_side.x+SIZE_X-self.size_x:
						self.score-=GOLD_LOOSE	
					else:
						self.score+=GOLD_GAIN
				else:
					self.score-=GOLD_LOOSE

		elif self.side=="right":	
			if not(90>self.angle and self.angle>-90):
				found =False
				for i in range(len(hero.left_alives)):
					if hero.left_alives[i].alive:
						if degrees(atan(-((self.y+HERO_SIZE/2)-(hero.left_alives[i].y+HERO_SIZE))/((self.x)-(hero.left_alives[i].x))))>=self.angle-180 and self.angle-180>=degrees(atan(-((self.y+HERO_SIZE/2)-(hero.left_alives[i].y))/((self.x)-(hero.left_alives[i].x)) )) and self.__distance(hero.left_alives[i])<=self.hook_range:
							self.layer1[0]=1
							hero.left_alives[i].layer1[1]=1
							found=True
							break
				if not found:
					self.layer1[0]=0			
			self.layer1[2:]=[self.x-right_side.x,right_side.x+right_side.size_x-self.x,self.y,screen.height-self.y,right_side.x+GOLD_AREA-self.x,self.angle,self.cooldown]
			if self.score<=100:
				if self.x<=right_side.x+GOLD_AREA:
					if self.x == right_side.x:
						self.score-=GOLD_LOOSE
					else:
						self.score+=GOLD_GAIN
				else:
					self.score-=GOLD_LOOSE
		self.layer1=np.matrix(np.array(self.layer1))
		self.layer2=np.matrix(np.array(1 if sum([self.weight1*self.layer1 for j in range(9)])+self.bias1>=1 else -1 for i in range(20)))
		self.layer3=np.matrix(np.array(1 if sum([self.weight2*self.layer2 for j in range(20)])+self.bias2>=5 else -1 for i in range(10)))

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
			RESTART=True
		if self.y < 0:
			self.y=0
		elif self.y>SIZE_Y-HERO_SIZE:
			self.y=SIZE_Y-HERO_SIZE	
		if self.player:
			self.score=LOOSE+GOLD_LOOSE*2
		if self.cooldown>0:
			self.cooldown-=0.1
	def display(self):
		if self.player:
			fill(255,0,255)
			rect(self.x-5,self.y-5,HERO_SIZE+10,HERO_SIZE+10)
			fill(50)
		image(self.image,self.x,self.y)
		if self.status=="MOVING" or self.status=="IDLE":
			if self.layer1[0]==1:
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
	for i in range(HERO_COUNT-1):
		hero("left")
		hero("right")
	hero("right",player=False)
	hero("left")

	#hero("left",player=True)


def draw():
	global ORIJIN_X,ORIJIN_Y,FLOW,L,R,MATCH,RESTART
	global large_font,small_font
	global WIN


	#FOR DISPLAY----------------------
	background(0,0,0)
	#translate(ORIJIN_X,ORIJIN_Y)

	if FLOW:	
		for rectangle in object.objects:
			rectangle.display()
		try:
			fill(255,255,0)
			textFont(small_font)
			text(str(hero.left_alives[0].score), screen.width/2-30, 30)
			text(str(L),screen.width/2-50, 80)
			text(str(R),screen.width/2-50, 250)
			text(str(hero.right_alives[0].score), screen.width/2-30, 200)
			text("'Z'YE BASINIZ", screen.width/2-50, 500)
			text("tyughjn tuşlarıyla oynayabilirsiniz", screen.width/2-50, 800)
			fill(50)

			fill(255,255,0)
			rect(hero.left_alives[0].x-5,hero.left_alives[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
			rect(hero.right_alives[0].x-5,hero.right_alives[0].y-5,HERO_SIZE+5,HERO_SIZE+5)
			fill(50)
		except:
			pass
		"""
		for at in hero.left_alives:
			at.display()
		for at in hero.right_alives:
			at.display()
		"""
	else:
		fill(255,255,0)
		textFont(large_font)
		text(str(MATCH)+". DENEME", screen.width/2-400, 30)
		text("ANTREMANDAYIZ, LÜTFEN EKRANI KAPATMAYINIZ.",screen.width/2-400, 80)
		text("NELER OLDUĞUNU GÖRMEK İÇİN 'A'YA BASINIZ",screen.width/2-400, 300)
		text("ANCAK BAKMANIZ BİTTİĞİNDE 'Z'YE BASINIZ", screen.width/2-400, 400)
		text("BAŞLAT+TAB YAPARAK BİLGİSAYARI KULLANABİLİRSİNİZ", screen.width/2-400, 600)
		fill(50)

	
	for at in hero.left_alives:
		at.update()
		if at.status != "HOOKING" and not at.player:
			at.desicion()
	for at in hero.right_alives:
		at.update()
		if at.status != "HOOKING" and not at.player:
			at.desicion()

	for i in range(HERO_COUNT):
		hero.left_heroes[i].layer1[0,1] = 0
		hero.right_heroes[i].layer1[0,1]= 0
	
	hero.left_alives.sort(key=lambda x: x.score,reverse=True)
	hero.right_alives.sort(key=lambda x: x.score,reverse=True)
	hero.left_heroes.sort(key=lambda x: x.score,reverse=True)
	hero.right_heroes.sort(key=lambda x: x.score,reverse=True)
	while len(hero.left_alives)!=0:
		if not hero.left_alives[-1].alive:
			hero.left_alives.pop()
		else: 
			break
		if len(hero.left_alives)==0:
			RESTART=True
			break
	while len(hero.right_alives)!=0:
		if not hero.right_alives[-1].alive:
			hero.right_alives.pop()
		else:
			break
		if len(hero.right_alives)==0:
			RESTART=True
			break
	if RESTART:
		hero.restart()

	#ALL FLOW GOES FROM HERE----------
	

	
	#MOUSE BINDINGS------------------
	"""
	PRESS AND DRAG TO MOVE WORKSPACE
	"""
	"""
	if mouse.pressed:
		ORIJIN_X += mouse.x-pmouse.x
		ORIJIN_Y += mouse.y-pmouse.y
	"""
	#KEY BINDINGS--------------------
	"""
	F:FLOW
	R:RESET ORIJIN
	A:ZOOM IN
	S:ZOOM OUT
	"""
	if hero.player!=0:	
		if key.char=="t":
			hero.player.turn_left()
			key.char = " "
		elif key.char=="y":
			hero.player.move()
			key.char = " "
		elif key.char=="u":
			hero.player.turn_right()
			key.char = " "
		elif key.char=="g":
			hero.player.go_left()
			key.char = " "
		elif key.char=="h":
			hero.player.hook()
			key.char = " "
		elif key.char=="j":
			hero.player.go_right()
			key.char = " "
		elif key.char=="n":
			hero.player.go_back()
			key.char = " "
	
	if key.char == "a":		
		FLOW = True
		key.char = " "
	elif key.char == "z":		
		FLOW = False
		key.char = " "
	elif key.char == "p":		
		print("left_champ_weight1=",hero.left_champ_weight1)
		print("left_champ_weight2=",hero.left_champ_weight2)
		print("left_champ_weight3=",hero.left_champ_weight3)
		print("right_champ_weight1=",hero.right_champ_weight1)
		print("right_champ_weight2=",hero.right_champ_weight2)
		print("right_champ_weight3=",hero.right_champ_weight3)

		print("left_champ_bias1=",hero.left_champ_bias1)
		print("left_champ_bias2=",hero.left_champ_bias2)
		print("left_champ_bias3=",hero.left_champ_bias3)
		print("right_champ_bias1=",hero.right_champ_bias1)
		print("right_champ_bias2=",hero.right_champ_bias2)
		print("right_champ_bias3=",hero.right_champ_bias3)
		print()
		key.char = " "
	elif key.char == "r":		
		hero.restart()
		key.char = " "
	if len(hero.left_alives)>HERO_COUNT or len(hero.right_alives)>HERO_COUNT:
		print(hero.left_alives)
		print()
		print(hero.right_alives)
		print("l",len(hero.left_alives),"\nr",len(hero.right_alives))
		print("PROBLEM CONTINUES")
		if len(hero.left_alives)>=HERO_COUNT:
			hero.left_alives=hero.left_alives[1:]
		if len(hero.right_alives)>=HERO_COUNT:
			hero.right_alives=hero.right_alives[1:]









if __name__ == "__main__":
	run()
