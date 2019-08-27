from pyprocessing import *
from random import randint,uniform
from math import radians,sin,cos,atan,degrees
#CONSTANTS-----------------------------
WIDTH,HEIGHT = screen.width, screen.height #1920,1080
DISTANCE=0
SIZE_X, SIZE_Y = screen.width/2-DISTANCE/2,screen.height #1920/2-DISTANCE/2,1080
ORIJIN_X,ORIJIN_Y=0,0
HERO_SIZE=50
GOLD_AREA=175
SURVIVER=4

LAST_GAME=1

MAP_COLOR=50
GOLD_AREA_COLOR=(50,50,0)
GOLD_GAIN=0.2
GOLD_LOOSE=0.1
WIN=100
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
		left_champ_weight1= [[0 for j in range(9)] for i in range(20)]
		left_champ_weight2= [[0 for j in range(20)] for i in range(10)]
		left_champ_weight3= [[0 for j in range(10)] for i in range(8)]
		right_champ_weight1= [[0 for j in range(9)] for i in range(20)]
		right_champ_weight2= [[0 for j in range(20)] for i in range(10)]
		right_champ_weight3= [[0 for j in range(10)] for i in range(8)]
		left_champ_bias1= [0 for i in range(20)]
		left_champ_bias2= [0 for i in range(10)]
		left_champ_bias3= [0 for i in range(8)]
		right_champ_bias1= [0 for i in range(20)]
		right_champ_bias2= [0 for i in range(10)]
		right_champ_bias3= [0 for i in range(8)]

	elif LAST_GAME==1:
		left_champ_weight1= [[-3.690645076128273, -0.5059300310748666, 7.510971885528269, 3.167002358743437, -4.34018524661661, 1.0107883810381173, -0.3810119494158961, 2.417550469979013, 1.7913934062970216], [-1.156902489174557, -2.5786185622424727, -0.5593669723573255, -3.993474295876595, -1.4698271480000977, -3.750712024969825, -2.303249108515838, 4.244917493024875, 1.267245624090127], [1.5843714418809238, -1.8306584758675397, 1.6497087888671675, 5.639696393036269, 1.227516930587765, -1.5952914307445498, -2.1866555435331723, 2.2859226869718468, -1.3242464420687052], [-0.2538743114183729, -5.732133573065479, 5.655704546028583, -3.421283596318148, 2.2886860395655133, 3.0976429590473273, -0.09880983725846493, -3.499349201635302, 0.20247346023096824], [-4.588746300431423, -4.998864269389996, -5.148005933531685, -3.2179875839529006, -1.9318633803498844, -3.6927616773037473, -2.670627108822088, -3.6924033692926903, -1.6862459408416068], [4.6995190709225065, 5.051205088836948, 4.122287096374738, 1.2519766372165075, -3.615858112004393, 3.495429128491769, -1.5521260236316312, 0.8007660647005562, 1.2456482496524428], [0.7596385120960051, -3.4843966894377068, -2.141631498542226, -4.303744741875135, 0.8116558079148772, 1.4368971611371542, -4.01588893926089, -1.6696302455434497, 1.930041216464673], [2.3450191288305033, 2.94487607271995, 3.2188738181055836, 4.068454107377242, -0.8143288450892112, -6.918096049214254, -2.007989785207415, -5.279874995680835, -0.01900441921394669], [4.517505116106596, 1.774024956819523, -2.8657186475979586, 4.129006063978595, -1.329935366381163, 1.891205048910724, 0.15496699219274002, -5.545500911923301, 0.4846576893835356], [2.9319829105632738, 0.9183581591185197, -6.367471404216407, 0.07255854188905742, 3.4250071046283224, -2.376092030474206, 7.561875693677292, 4.36113612929268, 3.528702440288875], [0.7376236774042619, -1.2531884292748452, -2.810351741050732, 3.3428334555051027, 0.15041133191228517, -3.8861520866451755, 0.855833957594008, -1.124825734174545, -6.455222925646785], [4.8942325143441066, -3.511932842173327, -1.603789324325763, 0.8103665139587309, 2.4406304286142424, 8.258695949888583, 0.10189270212661994, -1.2559419737611353, 0.7847456129109543], [-3.329182667546351, 0.36116697881313475, -1.2580915027106894, 3.8694423649565963, 3.633271299943933, -4.270674777846602, -3.4976768044656676, -7.759038971662584, -0.15974324023494746], [-3.696650185255455, -4.607643359402258, -6.325055915659406, -2.4150636629617788, -1.5470790010386448, 3.9521101440755277, -2.4436243938042344, -1.9483733319681407, -1.095854827671023], [4.923727774920173, -3.932814547582244, -3.194199391748659, 4.097026682348729, -2.8288910206796185, -2.108500549557037, 5.010135047657034, 2.3715065400714197, -3.0594841124648924], [-5.919378163824423, 3.856062588947269, 1.9290244943125463, 2.268945439524952, -2.0559960173235385, 0.8082157368029356, 3.012689024529224, 3.083236036740737, 1.8003939035947822], [-3.9124476069575005, 0.6819745961786744, 6.748812350741302, 0.6326951103322195, -2.9832318845405803, 2.4671926292055844, 4.629076121745893, -6.334621799701655, 2.7703449165640013], [-5.9565993866785885, -4.383094101383664, 0.7374091385360112, 0.4137703493215684, -0.7451956588258755, 3.2421825825447774, 3.0524226178869194, -1.9832036001541158, 1.690287912784671], [4.72500651341021, 3.246312617526273, 0.8022148507674683, 2.8931958576792716, -1.3593570326955762, 4.381403083945031, 4.728934845873731, 2.217900286478037, 6.6249369127095274], [-1.6646236497024907, 1.9686903847993769, 4.884366334214307, -3.3639761751372683, 3.510086676685555, 1.7061068568088948, 4.611597329981262, -4.966906667237099, 3.367594857825441]]
		left_champ_weight2= [[-2.9882237712295536, 7.354831169242348, 2.377530358077634, 1.5217593230655089, -5.37963471546234, -3.9122692617423867, 1.2108836885430594, 1.12164006711139, 5.693153278401794, 1.5215207446650787, -4.636319400432654, -2.096890817046436, 0.5968288047560275, 1.1577776604006922, -3.0881896738784675, -3.6011842558048976, -0.2344029593584651, -3.461841994169163, -6.052214614239681, -3.0588325448582374], [3.6766990896862026, -1.3411550486570092, -0.6001727161832665, -1.2225475071142078, 0.04397520971988689, -5.519637302576436, -4.0648356536673615, 2.405914379971609, -2.038120395482687, 0.8566142215706194, 4.564676190077701, 1.7738335710389663, 6.0181770876908915, -6.715716541693677, 0.41019981092243907, 5.496358912741767, 0.14879525821543027, 1.2367179684305936, 1.4202772501864573, -1.2046274967475414], [-2.9392737574970837, -2.8769416127433285, 0.5293380000564321, -7.497600786568678, -2.455034114685839, 3.327923274974682, -3.6105657194045615, -2.1274549249082346, -5.038234973631972, -2.218037883341016, 2.747198751611959, 1.5358378896204143, -5.275453675152231, 1.654673236490162, -0.5452116179489378, -5.379081168719641, -3.092233232156972, 0.5852252502688948, -1.5895894105847233, -5.012552389479487], [6.57141644372753, -0.8792849617771021, 0.7491654450813321, -4.245972545567972, -4.167310649645793, -2.5089874468424758, 0.621812162693979, -1.0699332198084979, 1.2041406954010574, -4.054382215241465, -3.2998850594954945, -0.26584726440669204, -1.2748624901731866, -1.7948501638370233, -1.5905843382802543, 3.7948831139867125, 0.95847354601244, 0.6372999696243182, 0.01223621289363852, 0.7234077597156755], [5.302401310052673, -0.10095061677099482, -2.1243757856146415, 6.293329653344685, 5.963654293930567, -1.5994146722598062, -1.4110885190215376, -1.6905783404769088, -2.4259657127813523, -3.3534584373692633, -2.9237092110552823, 0.10231102988733132, -0.6981804196391118, 0.6553987095589564, 1.9258584746120633, 4.661568939824711, 1.6517166914845598, 2.510394567588847, -3.931271521817282, -1.7314152088544905], [4.076763614848876, 2.136661212156823, -5.015209221087103, 2.7382990358990282, -1.6456557583613565, 1.9689863407060413, 2.223676078233234, 6.37482116707417, 2.140661357819301, 4.22113327543872, 0.5589251375315372, -4.506815977001849, 0.24267538047225645, 3.2856485561020348, 3.4501600555160556, -4.5862483850229285, -3.143823207261175, -3.4481246917360773, 5.687686872627428, -0.4225163965589095], [-6.318238564834672, -5.101093744329391, 1.4724153103746696, -0.19785561365902682, -3.179535028682574, 1.1920255199121108, -2.7938576977421024, 2.412815833641173, 2.6512435335476976, -5.91761922524513, 2.48324009151363, 4.557834099028224, -2.054227723723684, -6.474223123710423, -3.0536348401405125, -3.399334940428967, -6.320725716156197, 4.997532741795125, -0.7280010774011437, 0.06904463215390677], [0.2227926284279157, 3.6498830431886504, -3.1322511721620168, 1.7230627166154946, 4.786883887474077, 0.3382711086531687, -2.6541378582278723, -1.753602893412484, 6.40680490493198, -2.150787852755009, 3.694517330111422, 4.529755068809554, -4.0439675231190995, 0.27824324073366424, -4.445864896111545, 1.8926033846491253, -1.9717504798867413, 4.213806893859376, -3.1809278501390525, -2.1545993650619906], [0.4220453242355555, 1.8277732655381742, 4.840337325259987, -0.13813104876743743, -2.581327459370196, -1.4178693924593917, -2.3035481355294287, -1.9391496989310677, 6.135430758475276, -5.895834666887555, 0.5520701196002665, -3.0879961547081143, 3.2196119644175796, 6.424074037349037, -3.9690457627291695, 1.165932042564522, 4.494645679493479, 3.254564714490474, -5.631857135902497, -0.13560942975297663], [-1.7723388138697223, -2.23540327142985, 5.325351596582673, -3.266572326580561, -4.401021996060888, -6.066919422639645, 0.7165158411616551, 3.8977723027583084, -2.4618882174004426, -2.3460405576347947, -5.587682568811905, 5.533194470814538, 2.2568289699370694, -1.3683789222327976, 0.8904121483244966, 1.6845892126830937, -2.5198091226969295, -2.333354551545183, 5.388565558527999, 3.0368057401245743]]
		left_champ_weight3= [[-1.6970986646852149, -0.18375266875488994, -0.10344802461419444, -1.3909956749483134, -2.2616805390720467, -6.355400622791725, -1.9558853906655846, 2.0131198090386127, 1.0377820554849184, -5.2814636523770595], [0.9780172991692138, -5.263694146986075, -0.7791619063641175, 0.41809915028271805, 3.232664036575265, -4.959013513438965, -1.6305564773446068, -5.446374603525443, 0.34331555157046867, 2.329386202456797], [-5.0613568711277575, 2.037189498653042, 2.9190727572562167, 0.8318362149487486, -1.5014122509921284, -1.620625446567641, -0.8752872233080969, 4.029416227844023, 5.874899485463282, 10.859918040600189], [-3.7365894303960783, 4.318965129931023, -4.712440227725897, -1.1810415032442516, 5.464292922167089, 6.715054452342965, -0.052131848445610696, 2.058887670466832, -2.8558323149262614, 0.7408116839880269], [0.38101038497162076, -2.946792682192313, -0.48965522581777754, 3.752434376133888, 3.167160428654617, -1.3011081381199814, 0.004076588391764724, 6.579175645018829, 0.4818002993850037, 5.3714131351997265], [1.5745120662776668, -0.8799427772812712, 1.6945334939747956, 0.7353944069403026, 1.7349064270632266, 7.419799882798877, -5.000371518159768, -1.4466310280890364, -5.5783146747296195, -1.131294685730289], [-5.195208386134017, -4.672270694500987, -2.7148313010760092, -5.029421920394523, 2.7913870940294094, 1.9817253366807472, -5.911093012307184, -0.008091763596929646, 7.069783412940636, -3.1854463286746904], [1.2448547108212302, -3.77066678642669, -2.7262613067239845, -0.18922644144093081, 2.350684504000499, -2.382977694190815, 2.8268651118486385, 4.051886956129298, 4.3189779179178736, -1.171493063517176]]
		right_champ_weight1= [[-1.5171138222818135, -0.8957329170479302, -1.8760742290759116, -3.021440608195782, 3.3463787413133215, -3.6604048030895435, 1.5819277463959776, -5.535569513637605, -4.544042678719198], [1.3532620115836647, 3.4125511401768467, -0.3809548017800778, 1.4339046627023855, 3.4803652430325394, 1.9267707531075176, 7.1673991020022605, -1.764999658379792, -1.7692295204329866], [-0.6455637381260475, 0.41407214033928885, 3.550374348040648, 2.035616706320953, 6.656155379842282, 3.5586691083966473, 1.5752317186183173, -2.1076390068661346, -3.220906410146889], [0.43088317647625385, -1.6318631101804686, -1.827879479114394, 0.4922593258024025, -0.15674194019776422, 3.3699092238636155, -2.543299531013894, -0.9758840119556564, -3.3486177536589494], [5.705046459055475, 0.05856769183332988, -3.222548776761951, 1.7674461071263927, -1.487903406445703, 3.75086590496458, 0.5053165068715759, -3.23710124533837, 2.297911624843409], [1.2346295978121888, -2.7955358574994547, 0.6492145211720634, 4.244321694649882, 1.1216570020490497, -0.6142454985120552, -3.801181117257686, 1.0259730340984343, 4.416741291298779], [-3.3555455829935887, -5.014901657883641, 1.7619731281382829, 4.944948974441699, 2.525930576625238, -4.598652001079717, 2.0188706641849747, 4.798297458191914, 2.8832939856452264], [1.3629858876422545, -1.921444898209569, -1.4133940352263026, 3.1931201450041993, 1.2968238344934298, 2.4565400034730915, -5.3366978269352305, -6.268624366408, -0.9872004923537702], [-5.819993963513409, 7.638783598889938, 3.0839637303287484, -1.7903691014637233, 3.1801697241932763, 1.4441771747423315, -3.5603402605128682, -5.224590413765821, 5.767935786439645], [1.1679017119526502, -8.022882049487327, 0.6747410394554602, -1.6691841443142688, -3.917595599147882, 0.12427344549835084, -4.862149425514211, -5.530482198676684, -0.022043554010693134], [-2.4749308503410887, 1.8757847328380381, -1.1952384256490114, 2.2215800165450696, -2.7538902415211917, -0.9223565209643358, 3.513463639481376, -2.076679592658772, 1.2978315847633008], [-0.11366558238453484, 0.7549510697103413, 3.3578575746918746, 3.41218492290857, -1.5898135487283942, 5.123294953414733, -0.25665643856061393, 4.818724383519113, 0.3867644054212177], [5.331893909358168, 2.5507665158463224, 0.09874171690662514, 1.6606694176881642, 3.2889819553507613, 0.5291413403883439, -0.008438554668374065, -6.127189095607514, 4.694556673050395], [-0.4143337119720715, -1.586605103536826, -2.9002632502465624, 8.499151511883777, 4.399459221216876, -1.0165028254220623, -0.3578265374669961, 5.259418318549942, -4.688883828225555], [-4.985518619416952, -0.5812910518220469, 5.675661549981739, -1.110618939719851, -1.0935807876809034, 0.8477166118362444, -1.617707829195703, 1.5631357268612165, -1.0650730084070208], [-2.3586332900205536, -5.503014894838558, -1.2844953979622942, 3.3610359386480715, 5.615341692239488, -5.216059532406697, -3.369296800580554, 1.9826450454574625, -0.17170230640350115], [-6.052377763351557, 7.608676022150117, 0.6940829584126214, -0.5002108036862704, 6.026502861771457, -4.105750730910177, -1.6891967192352513, -1.019586446004934, 5.405696840399802], [1.7087486823016085, 3.928899210657879, 4.351639894653775, 6.4162488765874475, -1.7050616279173574, 1.971630115235889, -3.1002966107692305, 0.15235739421000016, -0.2787881285674956], [-3.115012725102156, 4.907047240251631, 2.109871468853784, -1.282112700015116, -1.058851794552043, -1.3824944120739644, -1.7346052383342097, 0.45759425385316244, -6.668108910207879], [-0.6299540933412487, 0.3453646342911455, -8.550660661429612, -2.611577086418677, -3.1916616460400773, -4.2290332062653935, -4.359541636402707, 5.406587606705438, 0.6044050045038125]]
		right_champ_weight2= [[6.271505264284956, -2.675617107197527, -4.050987285349412, -1.3003646289745023, 0.5236355480258674, 0.8484375827705738, 2.0808155664540884, 3.160853066637058, -6.426675919127231, 1.4416333519553968, 1.4632786337618504, -2.168905544489849, 4.6640987110419605, -0.9944904820366436, 3.5070226666459687, -2.8845060426421636, -2.3665369513151675, 0.06246300299220764, 3.6526433585027562, 0.8441935641169932], [-2.0857373539283257, -3.0441693906352563, -2.105809711234713, -1.6923632905571413, -3.5018635404548872, 1.327977997312904, 1.5015271269936914, -6.41972358583865, -3.974443265240495, 3.5349197621161395, -1.6021476348806727, -3.335233599946941, 5.081902503470472, 2.8379754566693736, -2.9083018550746775, -0.12642332539503653, -3.7776441928626783, -1.598504396728705, -2.3546606230177516, -4.405942073555473], [5.03614383253632, 3.0836143962407805, 1.4413039797042915, -2.477181515648306, -3.286014518076316, 1.1337513913121147, -3.876815057155978, -0.33291804894899535, 4.801437630754584, -5.452323059607171, 0.41873325470714484, 2.1242645271037253, -7.5380315062234615, 2.9518986119575414, -3.6688384450259437, -4.575968877255563, -3.5906334720453277, 0.6769915205597986, 4.510250077508842, 5.004513209177053], [0.26101249638229906, 8.024317033011231, -0.4763185110559591, -2.9233171351142655, -1.8819254814596422, -3.7000744621401402, 0.6527851482457433, 4.862852626376624, 2.2057855670628146, 5.501172497880344, 4.166824226088543, 2.2860683426667094, 0.8906967545415659, 1.0330663490333543, -2.1909262520733406, 2.97921226486699, -2.879028940302318, 5.633402690862251, -0.9552125806496888, 0.5080117103255731], [-1.5750308545679235, 0.23486218506761136, -4.271102972662157, -0.359805306195905, 2.9744255724190576, -4.5130186414832, 3.9536719351940914, -1.8127313358528123, 0.5790768689145123, 0.41161911437405363, -2.55405656872239, -1.2049185661397426, -1.796587735600938, -3.160654014031512, 3.828686535885481, -8.181045474313716, 1.0589598222124987, -3.1249151193955527, -0.875414149180273, -1.2674277037160664], [-5.704554879332906, -5.020406916078275, -3.7333833273416253, -0.10466671053167498, -1.6450637148051726, 4.43291574217744, -2.265672153434515, 7.188742697727581, -2.6333026078830084, -1.6842590199051917, 5.009252631453377, -1.2291366509132844, 3.0460959407139057, 5.250498453238751, -3.392355831835065, -1.8418042603815354, 0.527776038017565, 1.517985840700815, 2.1692355777325254, -8.123398823932282], [3.8520902389773823, 2.6321003496236557, -0.3930010883281976, 4.700423117463685, -1.7613465784188778, 2.981413323193586, 4.090501034281851, 5.298131770637019, -4.1529357962353055, -1.9387717145160446, 3.050368766799348, -6.69524406319754, 1.6697562241041914, -1.6980809111896678, -3.766862630746883, 2.3905994594162907, -3.9237769057265672, -1.1163415533950167, -4.389462059218381, 2.0921458697487494], [1.3297267512437614, -1.1391789687456193, -5.909881398685641, -2.228538276258204, 1.3596137876346028, 0.4642352713943567, 2.2270349712756623, -1.183798035915288, 4.385841169872157, 2.36616058789959, 2.682422035501589, 5.4383325284354544, -0.5906386230009482, 0.38113505871281816, 0.5912044671434108, -1.6602646131633754, -1.6270799204493698, -0.4092959466564098, -6.907189827624604, 2.3758922631001775], [4.82475012786204, 2.8916769642328, -0.294984877014676, 0.0850060794739459, 0.6268019164611228, -0.28176828840388124, 0.10128566129284133, -2.713927921904367, 0.6299415857174544, 2.65941398084834, 0.2753080539267736, -3.575177157835401, 1.1178059064130974, -4.494014551085893, 1.8774042133944935, 0.9659082962629463, -2.729365951772395, -2.996947975273151, 6.302177752039376, -5.204450794089084], [-1.6112558644278283, -0.8491426341808953, -2.5210796221083713, 1.843616734962369, -0.07137732458110135, -2.716252564600214, -2.2898719207094715, -2.744179853382358, -0.9996245581808187, 1.6704621290701946, -5.4437908417826115, -9.580857905137306, -4.8906530702409245, 2.1514428587722985, 2.4446013893109826, -2.9555874398001576, -0.14246826070901542, -2.7607073853782493, -0.4991200223305292, 0.7091493198265757]]
		right_champ_weight3= [[0.1366453141917463, 1.9311607802117265, -0.11108815823462459, -0.1819655662508014, 0.11263429480698339, 3.6739286355316616, -2.3599349712003943, -4.162654299030932, 0.358354064128764, 2.087243743233196], [-3.1585707617547993, 2.1943981317018277, 5.000501562782273, 1.4587557115452416, 1.4911958343522558, 0.007657915022718842, -4.222241074596783, 5.297438489806216, 2.67375314551427, 0.3828659195345335], [-1.93570746914572, 1.7016370262796907, 3.0406636727399263, -4.388171185061847, -4.056428996969897, -2.9152253750452544, 0.124120550387256, 1.8899069298121272, -0.6048765214910806, -0.6603281432204641], [1.9535112475365244, 2.1196473980520625, 6.243170840398915, 0.046301776020889696, 2.1270770449192584, -5.447125157470363, 5.253147377151488, 2.7783319540407163, -5.0543159048722766, -1.870288375065884], [-4.1151071326960995, 3.3513675583941134, 0.6444217175862923, -1.3160838073609722, -2.992909330891386, -1.7491784832369093, -4.491766448964678, 0.03573173129866691, -0.2763185563788134, 6.833316051937671], [-0.19781013772483003, -6.6052391841036755, -2.9126878219050845, 0.37707848688346846, -0.9124589061817059, 2.068357200117819, 3.612693890517244, 0.35182545879204896, 3.813972204663977, 1.167207952025897], [0.7815920917926265, 6.606649080843759, 4.087435140676308, -3.143553817776251, 7.946051658297532, -0.837064802942765, -0.8608065187336403, 3.357257593260657, -3.5462574334821992, -0.4271700553908516], [-0.1865799523643541, -1.0471453277558718, 0.7318717169467585, 4.364314656356553, 7.708226472440989, 0.17047728892795588, -2.177640324313693, -2.7120656412114172, 3.9110757065001227, -5.771162352256394]]
		left_champ_bias1= [110.19662166478469, -33.68588952021641, -4.897234020480411, -11.355223118318454, -50.33246371570078, 23.854719331177122, -63.58848451365685, -63.718137005790894, -81.58775122036606, -128.98023424590798, 94.08268635287311, -24.797282310356387, 9.574763460195001, 73.22086321794703, -98.96831816124508, -127.48944460870142, -14.878370766670685, 67.73981235334142, -100.74049287091883, -56.867827628900855]
		left_champ_bias2= [32.01858746739177, -7.954463229466377, 30.39565041318887, 28.47454877091872, -26.917630816422925, 127.41573269620662, -102.93341906298755, -14.95391489968565, 63.90979948704421, -47.05343036881625]
		left_champ_bias3= [-80.64485051567692, -35.637017451592946, 34.183420788549086, 53.242269945607944, -5.724422253664875, -102.17847985571285, -38.5570686578103, -63.786905764255515]
		right_champ_bias1= [23.192158704582333, -123.21170186578527, 2.2173900422481267, -63.21958496393515, 140.12573737250904, -10.901557283174808, 52.13707131212743, -11.630983806252527, -89.99316431290904, 60.0416899369291, -56.35531784707032, 69.78301259172905, -63.76885275068406, -74.22853923531433, -66.19193411594337, -29.33588766135138, 65.60536306644802, 55.62489726948706, 97.12036571451631, 12.089090874673388]
		right_champ_bias2= [-52.733958159033165, 76.93159001968701, 104.00678510654791, -59.793798654495866, -29.841412627215337, 94.0028501016848, -53.78656618688183, -99.3499377757057, 31.271436108002067, 60.6615106358488]
		right_champ_bias3= [-50.29350681616572, 43.86088768142129, 53.92197232619056, 88.54864310516737, -33.31466664025949, 3.6536748688618683, 33.52568867925001, 43.55714370721824]
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
		self.layer1=[0 for i in range(9)]
		self.layer2=[0 for i in range(20)]
		self.layer3=[0 for i in range(10)]

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
			self.action=[sum([self.weight3[i][j]*self.layer3[j] for j in range(10)])+self.bias3[i] for i in range(8)]
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
		del self.weight1,self.weight2,self.weight3,self.bias1,self.bias2,self.bias3
		if randint(0,10)>=3:
			if self.side == "left":
				self.weight1=[[hero.left_champ_weight1[i][j]+uniform(-0.5,0.5) for j in range(9)] for i in range(20)]
				self.weight2=[[hero.left_champ_weight2[i][j]+uniform(-0.5,0.5) for j in range(20)] for i in range(10)]
				self.weight3=[[hero.left_champ_weight3[i][j]+uniform(-0.5,0.5) for j in range(10)] for i in range(8)]
				self.bias1=[hero.left_champ_bias1[i]+uniform(-10,10) for i in range(20)]
				self.bias2=[hero.left_champ_bias2[i]+uniform(-10,10) for i in range(10)]
				self.bias3=[hero.left_champ_bias3[i]+uniform(-10,10) for i in range(8)]
			else:
				self.weight1=[[hero.right_champ_weight1[i][j]+uniform(-0.5,0.5) for j in range(9)] for i in range(20)]
				self.weight2=[[hero.right_champ_weight2[i][j]+uniform(-0.5,0.5) for j in range(20)] for i in range(10)]
				self.weight3=[[hero.right_champ_weight3[i][j]+uniform(-0.5,0.5) for j in range(10)] for i in range(8)]
				self.bias1=[hero.right_champ_bias1[i]+uniform(-10,10) for i in range(20)]
				self.bias2=[hero.right_champ_bias2[i]+uniform(-10,10) for i in range(10)]
				self.bias3=[hero.right_champ_bias3[i]+uniform(-10,10) for i in range(8)]
		else:
			self.weight1=[[uniform(-5,5) for j in range(9)] for i in range(20)]
			self.weight2=[[uniform(-5,5) for j in range(20)] for i in range(10)]
			self.weight3=[[uniform(-5,5) for j in range(10)] for i in range(8)]

			self.bias1=[uniform(-100,100) for i in range(20)]
			self.bias2=[uniform(-100,100) for i in range(10)]
			self.bias3=[uniform(-100,100) for i in range(8)]
	#-------------
	def restart():
		global MATCH,WIN,RESTART
		hero.left_champ_weight1=hero.left_heroes[0].weight1[:]
		hero.left_champ_weight2=hero.left_heroes[0].weight2[:]
		hero.left_champ_weight3=hero.left_heroes[0].weight3[:]
		hero.right_champ_weight1=hero.right_heroes[0].weight1[:]
		hero.right_champ_weight2=hero.right_heroes[0].weight2[:]
		hero.right_champ_weight3=hero.right_heroes[0].weight3[:]

		hero.left_champ_bias1=hero.left_heroes[0].bias1[:]
		hero.left_champ_bias2=hero.left_heroes[0].bias2[:]
		hero.left_champ_bias3=hero.left_heroes[0].bias3[:]
		hero.right_champ_bias1=hero.right_heroes[0].bias1[:]
		hero.right_champ_bias2=hero.right_heroes[0].bias2[:]
		hero.right_champ_bias3=hero.right_heroes[0].bias3[:]
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
							self.layer1[0]=100
							hero.right_alives[i].layer1[1]=100
							found=True
							break
				if not found:
					self.layer1[0]=-100

			self.layer1[2:]=[self.x,left_side.size_x-self.x,self.y,screen.height-self.y,left_side.x+left_side.size_x-GOLD_AREA-self.x,self.angle,self.cooldown]
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
							self.layer1[0]=100
							hero.left_alives[i].layer1[1]=100
							found=True
							break
				if not found:
					self.layer1[0]=-100			
			self.layer1[2:]=[self.x-right_side.x,right_side.x+right_side.size_x-self.x,self.y,screen.height-self.y,right_side.x+GOLD_AREA-self.x,self.angle,self.cooldown]
			if self.x<=right_side.x+GOLD_AREA:
				if self.x == right_side.x:
					self.score-=GOLD_LOOSE
				else:
					self.score+=GOLD_GAIN
			else:
				self.score-=GOLD_LOOSE
		self.layer2=[100 if sum([self.weight1[i][j]*self.layer1[j] for j in range(9)])+self.bias1[i]>=5 else -100 for i in range(20)]
		self.layer3=[100 if sum([self.weight2[i][j]*self.layer2[j] for j in range(20)])+self.bias2[i]>=5 else -100 for i in range(10)]

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
			if self.layer1[0]==100:
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

		for at in hero.left_alives:
			at.display()
		for at in hero.right_alives:
			at.display()
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
		hero.left_heroes[i].layer1[1]=-100
		hero.right_heroes[i].layer1[1]=-100
	
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
