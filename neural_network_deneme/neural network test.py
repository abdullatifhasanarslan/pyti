from pyprocessing import *
from random import randint,uniform
#CONSTANTS-----------------------------
ORIJIN_X,ORIJIN_Y = 0,0
SIZE_X, SIZE_Y = 100,200
SPEED = 10
DISTANCE = 600
START = 600
BOX_LIMIT=25
SURVIVER=4
BIRD_NUMBER=5
CURRENT_BOX=START
#EVERY 70 ACTION WILL CONSIDERED AS 1 IN CROSSOVER
#1580
#FLOW CONTROLLERS----------------------
FLOW=True
TICK=0
FULLSCREEN=False
DISPLAY=True
POPULATION=1
SCORE=0
RECORD=0
#NEURAL NETWORK------------------------
"""
LAST_GAME_CHAMPION_WEIGHTS_1=[
[0.5883298321858019, -0.5159120443660252, 0.1164100479788821],
[-0.09869537917202642, -0.8596656520626649, -0.4044059591806364],
[-0.42574447259983006, 0.6433386154932823, 0.5328167107134938],
[0.2933144046422411, -0.37004850398948963, -0.4014714093915901],
[0.7168903597874541, 0.4120107818669956, -0.9037262980141352],
[0.2689908865274231, 0.12690224473927159, 0.8607984100449653],
] 
LAST_GAME_CHAMPION_WEIGHTS_2=[-0.14886536296537267, -0.7710529259150629, 0.9348941685388157, -0.6319703004370059, 0.5932656503593643, 0.6283618989099253]
"""
LAST_GAME_CHAMPION_WEIGHTS_1=[
[0, 0,0],
[0,0,0],
[0,0,0],
[0,0,0],
[0,0,0],
[0,0,0],
] 
LAST_GAME_CHAMPION_WEIGHTS_2=[0,0,0,0,0,0]
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
	#backup=[]
	def __init__(self,x,y,size_x=SIZE_X,size_y=SIZE_Y):
		object.__init__(self,x,y,size_x,size_y)
		BOX.boxes.append(self)
		#BOX.backup.append(self)

class BIRD(object):
	"""PHONEIX"""
	birds=[]
	alives=[]
	def __init__(self,x=0,y=0,size_x=50,size_y=50):
		object.__init__(self,x,y,size_x,size_y)
		self.image=loadImage("images/phoneix.png")
		self.vector = [SPEED,0]
		self.fitness=0
		self.alive=True
		self.score=0
		
		#travelled distance,vertical distance to next tunneş M[]2x1
		self.layer1=[self.x,self.y-(BOX.boxes[0].y+SIZE_Y/2),self.vector[1]]
		#2 weights for 6 times M[]6x2
		self.weight1=[[uniform(-1,1) for i in range(3)] for j in range(6)]
		#self.bias1=[uniform()]
		#6 layers M[]6x1
		self.layer2=[self.weight1[i][0]*self.layer1[0]+self.weight1[i][1]*self.layer1[1]+self.weight1[i][2]*self.layer1[2] for i in range(6)]
		#1 weights for 6 time M[]1x6
		self.weight2=[uniform(-1,1) for i in range(6)]

		self.action=sum([self.layer2[i]*self.weight2[i] for i in range(6)])

		BIRD.birds.append(self)
		BIRD.alives.append(self)
	def flap(self):
		self.vector[1]=-10
	def desicion(self):
		self.action=sum([self.layer2[i]*self.weight2[i] for i in range(6)])
		if self.action>=0.1:
			return True
		else:
			return False
	def random_desicion(self):
		self.weight1=[[uniform(-1,1) for i in range(3)] for j in range(6)]
		self.weight2=[uniform(-1,1) for i in range(6)]
	def die(self):
		BIRD.alives.remove(self)
		self.vector=[0,0]
		self.score=0
		self.alive=False
	def reborn(self):
		global SPEED
		self.x=0
		self.y=screen.height/2 #randint(0,screen.height-100)
		self.vector=[SPEED,0]
		self.alive=True
		BIRD.alives.append(self)
	def update(self):
		global SCORE
		self.vector[1]+=1
		self.x+=self.vector[0]
		self.y+=self.vector[1]
		
		self.layer1=[BOX.boxes[0].x-self.x,self.y-(BOX.boxes[0].y+SIZE_Y/2),self.vector[1]]
		self.layer2=[self.weight1[i][0]*self.layer1[0]+self.weight1[i][1]*self.layer1[1]+self.weight1[i][2]*self.layer1[2] for i in range(6)]
		#IF REACHED TO NEXT TUNNEL
		if self.x+50>BOX.boxes[0].x:
			#IF IT IS NOT IN ALTITUTE TO ENTER THE TUNNEL
			if self.y<BOX.boxes[0].y or self.y+50>BOX.boxes[0].y+SIZE_Y:
				#IF IT IS IN TUNNEL
				if self.x<BOX.boxes[0].x+SIZE_X:
					FAIL(self)
	def display(self):
		image(self.image,self.x,self.y)


#VARIABLES

#FUNCTIONS
def RESTART():
	global TICK,SCORE,POPULATION,CURRENT_BOX,START
	BOX.boxes.clear()
	CURRENT_BOX=START
	create_boxes(BOX_LIMIT)
	for phoneix in BIRD.birds:
		if phoneix.alive:
			phoneix.die()
			phoneix.reborn()
		else:
			phoneix.reborn()
	POPULATION+=1
	TICK=0
	SCORE=0
	ORIJIN_X=0
def VICTORY():
	global BOX_LIMIT#,FLOW
	create_boxes(BOX_LIMIT)
	#FLOW=False
def FAIL(phoneix):
	global SURVIVER,LAST_GAME_CHAMPION_WEIGHTS_1,LAST_GAME_CHAMPION_WEIGHTS_2
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
		#print(survivers[0].fitness,survivers[1].fitness,survivers[2].fitness,survivers[3].fitness)
		print("[")
		for item in survivers[0].weight1:
			print(item)
		print("]","\n",survivers[0].weight2)
		print(survivers[0].fitness,"\n\n")
		#TAKE CHAMPION-----------------

		############################

		#TRIES TO HANG AROUND SURVIVER----
		"""
		a=-7
		#Increase
		for i in range(len(diers[-1].weight1)):
			for j in range(len(diers[-1].weight1[0])):
				diers[a].weight1[i][j]=survivers[0].weight1[i][j]+0.0001
				a-=1
		for i in range(len(diers[-1].weight2)):
			diers[a].weight2[i]=survivers[0].weight2[i]+0.0001
			a-=1
		#Decrease
		for i in range(len(diers[-1].weight1)):
			for j in range(len(diers[-1].weight1[0])):
				diers[a].weight1[i][j]=survivers[0].weight1[i][j]-0.0001
				a-=1
		for i in range(len(diers[-1].weight2)):
			diers[a].weight2[i]=survivers[0].weight2[i]-0.0001
			a-=1
		"""
		a=-7
		#---------------------------------
		diers[a].weight1=LAST_GAME_CHAMPION_WEIGHTS_1
		diers[a].weight2=LAST_GAME_CHAMPION_WEIGHTS_2
		a-=1
		#TRIES TO ESTIMATE BEST
		for i in range(len(diers[-1].weight1)):
			for j in range(len(diers[-1].weight1[0])):
				diers[-6].weight1[i][j]=survivers[0].weight1[i][j]+(survivers[0].weight1[i][j]-survivers[1].weight1[i][j])
				diers[-5].weight1[i][j]=survivers[0].weight1[i][j]+(survivers[0].weight1[i][j]-survivers[1].weight1[i][j])
		for i in range(len(diers[-1].weight2)):
			diers[-5].weight2[i]=survivers[0].weight2[i]+(survivers[0].weight2[i]-survivers[1].weight2[i])
			diers[-4].weight2[i]=survivers[0].weight2[i]+(survivers[0].weight2[i]-survivers[1].weight2[i])
		#TRIES AVERAGE OF SURVIVERS
		for i in range(len(diers[-1].weight1)):
			for j in range(len(diers[-1].weight1[0])):
				diers[-3].weight1[i][j]=0
				diers[-2].weight1[i][j]=0
				for surviver in survivers:
					diers[-3].weight1[i][j]+=surviver.weight1[i][j]
					diers[-2].weight1[i][j]+=surviver.weight1[i][j]
				diers[-3].weight1[i][j]/=len(survivers)
				diers[-2].weight1[i][j]/=len(survivers)
		for i in range(len(diers[-1].weight2)):
			diers[-1].weight2[i]=0
			diers[-2].weight2[i]=0
			for surviver in survivers:
				diers[-1].weight2[i]+=surviver.weight2[i]
				diers[-2].weight2[i]+=surviver.weight2[i]
			diers[-1].weight2[i]/=len(survivers)
			diers[-2].weight2[i]/=len(survivers)
		#RANDOM
		for bird in diers[:a]:
			bird.random_desicion()
		survivers.clear()
		diers.clear()
		RESTART()
					

def create_boxes(number):
	global CURRENT_BOX
	for i in range(number):
		BOX(CURRENT_BOX,randint(screen.height/2-200,screen.height/2+200))#randint(200,screen.height-400))
		CURRENT_BOX+=DISTANCE

#GENETIC----------------------
def FITNESS(bird):
	bird.fitness=bird.x-abs((bird.y-(BOX.boxes[0].y+SIZE_Y/2)))*0.01
	return bird.fitness


"""
#THEY ALL ACTUALLY HANDELED IN FAIL()
#1
def SELECTION():
	pass
#2
def CROSSOVER():
	pass
#3
def MUTATION():
	pass
"""
def setup():
	global game_map,SIZE_Y,DISTANCE,FULLSCREEN
	size(960,1080,fullscreen=FULLSCREEN)
	background(0,0,0)
	fill(50)
	stroke(150,150,0)
	strokeWeight(3)
	textFont(createFont("Times",30))
	create_boxes(BOX_LIMIT)
	for i in range(BIRD_NUMBER):
		BIRD(y=screen.height/2) #BIRD(y=randint(0,screen.height-100))


def draw():
	global ORIJIN_X,ORIJIN_Y,FLOW,TICK,SPEED,DISPLAY,SCORE,RECORD


	if key.char == "a":		
		FLOW = True
		key.char = " "
	if key.char == "z":		
		FLOW = False
		key.char = " "
	elif key.char == "s":		
		DISPLAY = False
		key.char = " "
	elif key.char == "d":		
		DISPLAY = True
		key.char = " "
	elif key.char == "f":		
		#phoneix.flap()
		RESTART()
		key.char = " "

	if FLOW:
		TICK+=1
		ORIJIN_X=BIRD.alives[0].x
		translate(-ORIJIN_X,ORIJIN_Y)
		for phoneix in BIRD.alives:
			if phoneix.desicion():
				phoneix.flap()
			phoneix.update()
		#IF IT PASSED THE TUNNEL
		if ORIJIN_X>BOX.boxes[0].x+SIZE_X:
			BOX.boxes.pop(0)
			SCORE+=1
			if SCORE > RECORD:
				RECORD=SCORE
			if len(BOX.boxes)==0:
				VICTORY()
		#FOR DISPLAY----------------------
		if DISPLAY:
			background(0,0,0)
			
			fill(255,255,0)
			text(str(POPULATION),ORIJIN_X+50,30)
			text(str(len(BIRD.alives)),ORIJIN_X+50,70)
			text(str(SCORE), ORIJIN_X + 480, 30)
			text(str(RECORD), ORIJIN_X + 480, 70)
			fill(50)
			
			"""
			for rectangle in object.objects:
				rectangle.display()
			"""
			for box in BOX.boxes:
				box.display()
			for bird in BIRD.alives:
				bird.display()






if __name__ == "__main__":
	run()
"""
[-0.15701169184622743, -2.104591396061745, 0.4857641190779316]
[-1.5531303547693487, 0.8834036898310376, 0.22149678510968296]
[0.6288984867954699, -1.256913532305276, -1.040739978207333]
[1.9377119928569835, 2.2194492296600377, -0.2480118048777249]
[2.2411956199826193, 0.988006496783912, -2.1086491551873063]
[-0.21708891072403413, -0.6728559250586115, 2.0475874505282388]
] 
 [-1.7420402774289885, 1.439541685519939, -0.830691650911167, 2.205741887109508, -0.9135673997946427, -1.139001319114434]
37158.75 


[
[0.5883298321858019, -0.5159120443660252, 0.1164100479788821]
[-0.09869537917202642, -0.8596656520626649, -0.4044059591806364]
[-0.42574447259983006, 0.6433386154932823, 0.5328167107134938]
[0.2933144046422411, -0.37004850398948963, -0.4014714093915901]
[0.7168903597874541, 0.4120107818669956, -0.9037262980141352]
[0.2689908865274231, 0.12690224473927159, 0.8607984100449653]
] 
 [-0.14886536296537267, -0.7710529259150629, 0.9348941685388157, -0.6319703004370059, 0.5932656503593643, 0.6283618989099253]
97159.44 
"""