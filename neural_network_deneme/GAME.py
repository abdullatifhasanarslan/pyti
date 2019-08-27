from pyprocessing import *
#CONSTANTS-----------------------------
WIDTH,HEIGHT = screen.width, screen.height
ORIJIN_X,ORIJIN_Y = 0,0
SIZE_X, SIZE_Y = screen.width-200,screen.height-200
HERO_SIZE=50
#FLOW CONTROLLERS----------------------
FLOW=True

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
		return
	#DON'T WANT TO USE THIS
	def display(self):
		rect(self.x,self.y,self.size_x,self.size_y)
class MAP(object):
	"""Just a box nothing more"""
	def __init__(self,x=100,y=100,size_x=SIZE_X,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
#class StatusBar:
	"""HP+MANA+regen+armors+stats+items+skills"""


#HEROOOOOOOOOOOOOOOOOOOOOOOOOOES

class hero(object):
	"""every single hero is also a 'hero' object"""
	hero_count_left=0
	hero_count_right=0
	left_heroes=[]
	right_heroes=[]
	def __init__(self,side,
				 hp,mana,
				 hp_regen,mana_regen,
				 str,agi,int,
				 str_gain,agi_gain,int_gain,
				 damage,attack_rate,attack_range,projectile_speed,
				 armor,magic_resistance,
				 movement_speed,
				 level=1):
				 #turn_rate+vision_range is not considered for this game
		global HERO_SIZE
		self.side = side
		self.hp,self.mana=hp,mana
		self.hp_regen,self.mana_regen=hp_regen,mana_regen
		self.str,self.agi,self.int=str,agi,int
		self.str_gain,self.agi_gain,self.int_gain=str_gain,agi_gain,int_gain
		self.damage,self.attack_rate,self.attack_range,self.projectile_speed=damage,attack_rate,attack_range,projectile_speed
		self.armor,self.magic_resistance=armor,magic_resistance
		self.movement_speed=movement_speed
		self.level=level

		#these conditions is just for placing and counting in the beginning purposes
		if side=="left":
			object.__init__(self,0,100+hero.hero_count_left*(HERO_SIZE+10),HERO_SIZE,HERO_SIZE)
			hero.hero_count_left+=1
			hero.left_heroes.append(self)
		elif side=="right":
			object.__init__(self,screen.width-HERO_SIZE,screen.height-100-hero.hero_count_right*(HERO_SIZE+10)-HERO_SIZE,HERO_SIZE,HERO_SIZE)
			hero.hero_count_right+=1
			hero.right_heroes.append(self)

	def display(self):
		image(self.image,self.x,self.y)

class NECROPHOS(hero):
	"""HEAL+SLOW+AURA+ULTI"""
	def __init__(self,side):
		hero.__init__(self,side,
					  524,375,
					  1.6,1.4,
					  18,15,20,
					  2.6,1.2,2.5,
					  46,1.7,550,900,
					  3.4,25,
					  285)
		if self.side=="left":
			self.image=loadImage("images/necrophos_left.png")
		elif self.side=="right":
			self.image=loadImage("images/necrophos_right.png")

class SNIPER(hero):
	"""SHARAPNEL+HEADSHOT+TAKE_AIM+ASSASINATE"""
	def __init__(self,side):
		hero.__init__(self,side,
					  506,255,
					  1.6,1.2,
					  17,21,15,
					  1.7,2.7,2.6,
					  36,1.7,550,3000,
					  3.2,25,
					  285)
		if self.side=="left":
			self.image=loadImage("images/sniper_left.png")
		elif self.side=="right":
			self.image=loadImage("images/sniper_right.png")


class VIPER(hero):
	"""POISON+TOXIN+SKIN+STRIKE"""
	def __init__(self,side):
		hero.__init__(self,side,
					  578,255,
					  1.6,1.2,
					  21,21,15,
					  2.4,2.9,1.8,
					  44,1.7,575,1200,
					  2.2,25,
					  275)
		if self.side=="left":
			self.image=loadImage("images/viper_left.png")
		elif self.side=="right":
			self.image=loadImage("images/viper_right.png")
	
class CRYSTAL_MAIDEN(hero):
	"""NOVA+FROSTBITE+AURA+FIELD"""
	def __init__(self,side):
		hero.__init__(self,side,
					  524,285,
					  1.6,1.2,
					  18,16,14,
					  2.0,1.6,2.9,
					  40,1.7,600,900,
					  2.6,25,
					  275)
		if self.side=="left":
			self.image=loadImage("images/crystal_maiden_left.png")
		elif self.side=="right":
			self.image=loadImage("images/crystal_maiden_right.png")
class LICH(hero):
	"""BLAST+ARMOR+SACRIFICE+CHAIN"""
	def __init__(self,side):
		hero.__init__(self,side,
					  560,315,
					  1.6,1.3,
					  20,15,16,
					  1.9,2.0,3.3,
					  42,1.7,550,900,
					  1.4,25,
					  315)
		if self.side=="left":
			self.image=loadImage("images/lich_left.png")
		elif self.side=="right":
			self.image=loadImage("images/lich_right.png")


#VARIABLES-----------------------------
game_map = MAP()
necrophos_left=NECROPHOS("left")
sniper_left=SNIPER("left")
viper_left=VIPER("left")
crystal_maiden_left=CRYSTAL_MAIDEN("left")
lich_left=LICH("left")

necrophos_right=NECROPHOS("right")
sniper_right=SNIPER("right")
viper_right=VIPER("right")
crystal_maiden_right=CRYSTAL_MAIDEN("right")
lich_right=LICH("right")

def setup():
	global game_map
	size(fullscreen=True)
	background(0,0,0)
	fill(50)
	stroke(150,150,0)
	strokeWeight(3)


def draw():
	global ORIJIN_X,ORIJIN_Y

	#FOR DISPLAY----------------------
	background(0,0,0)
	translate(ORIJIN_X,ORIJIN_Y)
	for rectangle in object.objects:
		rectangle.display()

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
	if key.char == "f":		
		FLOW = not FLOW
		key.char = " "
	elif key.char == " ":		
		ORIJIN_X,ORIJIN_Y=0,0
		key.char = " "








if __name__ == "__main__":
	run()
