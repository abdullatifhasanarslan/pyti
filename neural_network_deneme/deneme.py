from random import randint,uniform
from math import radians,sin,cos,atan,degrees
#CONSTANTS-----------------------------
WIDTH,HEIGHT = 1920,1080
DISTANCE=0
SIZE_X, SIZE_Y = 1920/2-DISTANCE/2,1080
ORIJIN_X,ORIJIN_Y=0,0
HERO_SIZE=50
GOLD_AREA=175
SURVIVER=4

LAST_GAME=0

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
		left_champ_weight1= [[-3.66181198630804, -0.47470394046651565, 7.394824471324606, 2.430644542784127, -3.8314063643735436, 1.2605450480831781, -0.571400587443188, 1.6689805104779112, 2.2863650004664686], [-1.0009500647101934, -2.584475101171856, -0.5697185060655549, -4.624508054949618, -1.3487751430092083, -3.8713347400178826, -1.939580704596455, 3.599195727952729, 1.5597287830025004], [1.12690831493475, -2.3014716663166723, 2.508173177253819, 5.848585067941553, 1.3771075790003096, -1.4112759554735077, -1.6119126372690111, 2.1807976400201072, -1.2694141499219913], [-0.23632203001007357, -5.547277094379341, 5.779752841751678, -3.3035229172242278, 2.4887629242866547, 3.0196724924178473, 0.14033948020408815, -4.001287969667718, -0.45205435079527645], [-5.255871296438838, -5.827949522646352, -4.454255176432558, -3.787842068619666, -1.918842036403992, -4.2924440767616945, -2.4708376758320894, -4.204721325872178, -1.3242588777811126], [4.818689235669695, 5.0097791494307105, 4.11203009884654, 1.4967000862586783, -3.551673575106144, 2.769807877815526, -1.9915029546409242, 0.05286953403130146, 0.998955308127299], [0.6299544540089047, -4.2326137910289745, -2.272975894946649, -4.9778362717270745, 0.9560173654970996, 1.43204919160305, -3.8815112656153663, -1.7735432508896465, 2.340387782974536], [1.8845534239700954, 2.5575306690407418, 3.0959403579411497, 4.262452966208431, -0.49915230072727335, -6.308762060291548, -1.8656079998246584, -5.91485221678129, -0.6091487690401174], [5.145215828101163, 1.2265166033103072, -3.1474052833823896, 3.26132809213449, -0.8551403873912365, 1.4199199016800508, -0.21161027490267548, -5.890653501299871, 0.7923930398640522], [3.6313000478207513, 1.3615563981651904, -6.686786540446892, 0.20606120327621813, 3.947721130516507, -3.0532662141317077, 7.505043607438945, 4.432578576516853, 3.7215801961315598], [0.36846116197174206, -1.1424629747714552, -2.566791813365037, 3.4960658854118347, 0.03665880535582988, -3.5790916260722185, -0.006116969396869898, -0.8141910053448695, -6.567875204933999], [5.090539626602131, -3.721259679500237, -1.3605564128502388, 0.8455015129149744, 1.7080519031533004, 8.376864189202461, -0.14312047489777158, -0.8181240753443084, 1.4592691743398807], [-3.5044564049074856, 0.4341236533826036, -1.2822069901338042, 3.581425594493748, 3.5179594868697417, -4.7917806896920805, -3.4120955857682485, -7.70610831783192, -0.6995210345630241], [-4.1493776054156015, -5.043201011881125, -6.467720084226011, -2.6083534208620796, -1.666153909613287, 4.31891410450859, -2.7200713141438184, -2.3956022207385472, -0.7525562589614345], [5.166654526591315, -3.4075624789881864, -3.172423671689244, 4.36291534287983, -3.8134541251193794, -2.431035642421109, 5.00074105084776, 1.9463631218968898, -3.025036585601305], [-6.254584252384034, 3.7400155518317626, 1.5162179629760555, 2.002107193925429, -1.9415037064883565, 0.8738305175636956, 3.0368692453974497, 3.1774536278284384, 1.9651505878397528], [-4.120430429698787, 1.4832695977712196, 6.4850575614093025, 1.2731729471244502, -2.8285167023212274, 2.197462445274379, 4.232586175729985, -6.077963738160152, 2.703354505500752], [-5.408519786167797, -4.6074707709088045, 1.425184989880209, 0.2645553719821532, -0.42642466285514635, 3.9105706235560462, 2.2445154190074756, -2.122246196313903, 0.8800767767352417], [4.9105688262918665, 3.353718911163008, 1.264281656779747, 3.5702532554958517, -0.9421201010667939, 3.9537732693188716, 4.958822333324693, 2.6461923892315515, 6.838009973556827], [-1.8398954017984983, 1.5260870247965483, 4.570273062239385, -3.142712927397231, 3.293142915951, 0.778644988205367, 4.796719213031209, -5.575737913532345, 3.3129992395105763]]
		left_champ_weight2= [[-2.512316596201293, 7.26339141266028, 2.801778044509643, 1.0925926499807332, -4.525930589605282, -4.179258009686638, 1.4388320775134462, 1.8611304446838925, 5.7258414821973735, 1.4840900594633095, -4.0819323482215, -1.8394923617112058, 0.751677151862112, 1.8977490076492747, -2.8289661957385235, -3.7456663335317795, -0.22271522381438769, -3.1933127574743763, -6.603071592248859, -2.858284479576904], [3.9608940390778846, -2.099016924579655, -0.4618143296256223, -1.128588871216833, -0.16210010102473182, -4.643735674176659, -3.7376559834713197, 2.9687975480253175, -2.4406701430768547, 0.024719238176643343, 4.40733688925224, 2.3671052679699214, 5.306740105299515, -6.29776659603818, 0.9240346699157092, 5.281570436997752, 0.6982107203852109, 1.1953720994181958, 1.0630179322316438, -1.8569433798185289], [-2.4902031340642408, -3.0214536070618183, 0.43508508717730454, -7.805083208381655, -2.696298530639563, 3.9099920478991206, -2.8543008719752683, -1.594773019992409, -5.549084066925875, -2.0851458622711134, 2.7403456516296765, 1.4685107294684778, -4.928413567916889, 1.9871560821666159, -0.09489485220726246, -4.865228776302481, -2.9426222609320747, 0.9053499164033654, -2.1023937625335556, -5.172140870151738], [5.945063796795463, -1.0082191753537568, 0.04789341673913794, -4.725605768132825, -4.349009176255956, -3.086530585949084, 0.5042179522006571, -0.9757318156733584, 1.4145844605120348, -3.9401249802177283, -4.197825983138058, 0.00018267048486075854, -1.6340099435434943, -1.6970816623086449, -1.939539531004349, 4.49352099409262, 0.2802157074914233, 0.6930815908796609, 0.5965305593003581, 0.7120937794539204], [5.270331500736105, 0.23705174731963552, -1.307058616877455, 6.242944219398138, 5.618462520440643, -1.612257384975432, -1.4409038648424153, -1.7825284794907674, -3.0214112398159862, -3.9236366942872807, -3.5258883700370793, 0.08051457145311358, -1.1730157376802897, 0.4957413152902034, 1.4997496092610059, 4.760711192915757, 1.534064254025352, 2.4587989401879944, -3.7936054106903394, -1.8395876916917735], [3.8991433337822445, 1.9187808506828168, -5.343373102205571, 2.042175256003084, -1.8387956599999704, 2.726291350952237, 2.6108382609369696, 6.533246419820715, 1.6420057600746474, 4.975838318644036, 0.13292375450854432, -4.60312345039884, 0.05474751095692809, 3.5354117642495226, 3.3660829145878632, -4.948265296304484, -3.4186621923100065, -4.231668034841845, 6.410630280273026, -0.5908930231872899], [-6.324038595237891, -4.6192137150343395, 1.0414712536598776, 0.09073152210284219, -3.4502207950776853, 1.2361830348697955, -2.2526625337167236, 2.5096967432223214, 3.3256427696643165, -5.6717487170529655, 2.3044135986367786, 4.8835136228352845, -1.7465501636817762, -6.412335572424346, -2.7731189127609532, -3.1716086049291032, -5.8035350203134835, 4.782912550077854, -0.7857098102288824, 0.8328883696823386], [-0.008781067346498195, 3.1189120994629156, -3.4254646762432173, 1.5502763606651158, 4.4891046690661325, 1.0988804672764942, -3.4304674426539425, -2.213470343003437, 6.676756805449144, -1.6761197351374102, 3.5726544420584676, 4.293751782848175, -4.334807057906481, -0.6215987260198708, -3.660237135600779, 2.408066321618957, -1.5713521225843636, 3.8521037672536655, -3.501030529374739, -2.9668522970155764], [0.588331064922673, 1.97795691043739, 4.554892186082298, -0.09993779622766785, -1.8470985325502471, -1.0907596327190197, -2.374134157107533, -2.3758612265794223, 6.8806138379912865, -5.85761563402337, 0.8364172634841742, -3.150688304632075, 4.083328378809498, 6.305961629152499, -3.2450399345683016, 0.5001486775777602, 4.927860621113329, 2.957769463683788, -6.185416868429287, -0.5466948182280618], [-1.7816302894216531, -2.259194814651102, 4.947994487159381, -4.184116523534283, -4.068829181703238, -6.145793512372656, 0.7260676369550931, 3.8829504950334623, -2.5498217533346947, -2.389314456109939, -5.495311393022059, 5.20617803741831, 1.6074520135856258, -1.1349804766069382, 0.781249392128877, 1.0198851460684248, -2.9917295393435115, -2.6735512976802482, 5.331009116940222, 3.40547218922854]]
		left_champ_weight3= [[-1.88468294635104, -0.6123197656062795, -0.08471188722278611, -2.262035802451876, -2.720842079901879, -5.860090483027537, -1.7818671884107413, 2.035123039606703, 1.4361670709378918, -5.402968333797312], [0.931041311527685, -5.885671619183761, -1.3880364112548977, -0.057860357437279464, 2.7849362955977783, -4.727538057553112, -1.4951461392631014, -4.628812955994656, 0.20723854643874073, 2.6436231927908085], [-5.6243885282384305, 1.7204736384686274, 2.4929525555623675, 0.5370114610372343, -1.4147966316240752, -1.6341671842128465, -0.18048564721266047, 3.848443486361673, 5.219680464304864, 10.647282781874848], [-3.7181362700265304, 4.519754342858803, -4.324537743064726, -1.1354922289551435, 6.021707911048973, 6.386948951131155, 0.7599458378383452, 2.4354027149291277, -2.526159274261653, 0.31399920547704374], [-0.44919837588047384, -3.0717057861912047, -0.54090549864537, 3.688726378487705, 3.6599248134405795, -1.4273631377309681, 0.0745141354245662, 6.590001008921086, -0.17580412995016148, 5.404872711959018], [1.9493375723364657, -0.7539377141324393, 2.1344775028951353, 1.085425202725054, 1.4014453088576713, 7.66096549450513, -5.6172871715532615, -1.0700613003790829, -5.1104560823309075, -0.8299846563781711], [-4.908212993850206, -4.2911187470530585, -3.0584437229578, -4.8562165371157215, 2.2874679359153434, 2.081501493319498, -6.015301333845356, -0.4420004405696729, 7.214477186587558, -3.1519873813478423], [1.2025105380390824, -3.51153902958738, -2.430606349229037, -0.5276768612618163, 2.314273600423811, -2.249459849006014, 3.294727080707698, 3.8647563455488934, 3.6727646993061587, -0.5084431918264392]]
		right_champ_weight1= [[-2.088712203039227, -2.064264326759745, -1.7193757698149876, -2.434793060584991, 3.601577344877202, -4.111303538580734, 2.2980470860181788, -5.480746973783159, -5.436308752727414], [-0.033653610950488466, 2.594411047622823, -1.5394759165886416, 1.398712892057224, 2.4647462361981898, 2.2118080426686126, 7.472970555220382, -1.335851631082765, -2.6093381329206737], [0.7505952639173613, 1.0223283724886199, 3.034721953427097, 1.4220960918504404, 5.421979022899113, 4.40442726208074, 1.4641910620974907, -2.256159664606236, -3.125018444846308], [0.7981722771970365, -2.1359306734743733, -0.6761695550067479, 0.4049799365823116, -0.16228515366084972, 5.074428010635162, -2.355039138470958, -0.6131250673055864, -3.7317480009074964], [5.844694391897663, -0.6840613812564221, -2.8095644979652494, 2.2525117595749045, -0.8889100368263092, 4.466709844614005, 1.0190368337819673, -2.0353001773844523, 2.2775632585096646], [1.0922432443666774, -2.857551550922966, -0.061769599474234105, 3.4743759133460013, 0.056516809086576525, -1.9292815678470845, -4.305995049382412, 1.3709555849135366, 3.603307869848198], [-4.324913683017682, -5.230882192952402, 0.3561076961050875, 4.829326990244679, 3.7367129755135897, -4.924648242106069, 0.80080344889034, 5.6180504635367585, 3.353560853233706], [0.6205788563210298, -2.317217156408448, -1.0016460608748017, 3.9222508856355143, 0.4258221906480337, 3.095758665557521, -4.7496838672966355, -5.602992271673596, -1.3783323748840681], [-5.2958937794648, 7.132826681454277, 3.8572587526762425, -0.9244697858685871, 3.197754471326093, 1.4913081768342078, -2.363405294352251, -5.567789642579896, 6.583641993098382], [1.4767500598799526, -6.7403464124303, 1.2780435332782987, -3.905959182784976, -2.1034075638316265, 1.7063790386878774, -5.077905095630629, -5.140728178945584, 0.536424310358836], [-1.1240643171431421, 2.1451056659062666, -2.4739001464019794, 3.1588900173848304, -2.977212257426955, -0.4734471625395188, 2.748700614286051, -1.8865891633910015, 0.3644615600057669], [-0.075068495625505, 0.4395261312882087, 1.8003741515185279, 3.3222787903073705, -2.5882534744909513, 5.121185582871953, 0.4049477893445651, 6.390016629537842, -0.1186436551637069], [4.936810957455442, 2.4493122623957264, 0.4335478996989286, 1.6951540274576784, 3.199055080019273, 0.030089939851340675, 0.488523314191047, -7.350661100345619, 5.2506141735494545], [-0.4948749896577843, -2.4743320750618203, -2.763110964192551, 8.696805181553447, 4.470450266383175, -0.584548924547766, -0.1895620781622831, 4.07456187935295, -4.505739767153042], [-4.819260772681618, 0.4833666988940287, 5.839811216162476, -1.0952879940225446, -0.8977666144561147, 1.6714885522000684, -1.775383708623206, 2.7325408043237984, -0.6602865836267384], [-2.9753333079748128, -4.272652200038598, -1.069716813975901, 2.436919207779709, 5.68030305227371, -5.484920426092348, -4.435038915612584, 1.7831568068606196, -0.38455494294190107], [-7.158116863752963, 7.693592040576217, 0.5859417798487337, -1.2996347359590859, 7.3660511377143205, -2.880075511082787, -2.3740679750749925, -0.9150523325956799, 6.1921042848879875], [2.8256098180768134, 3.2831932990005437, 4.315423252450965, 6.981073557269753, -1.4348111377820802, 1.5711097995209817, -3.4951143433432748, 0.33864107955685374, 0.06398372439416511], [-1.9187575907736538, 5.587331951966861, 3.0542805840971496, -2.401500673092103, -0.8996350220476715, -1.4068170221279832, -1.2866845841195393, 0.8991896782966448, -7.380884425778223], [-0.31305270323550216, 2.0833415929236034, -8.54480271980539, -3.7078614266268177, -2.6893721751398876, -3.962952017656971, -3.8438915098883006, 5.805150176328555, 0.4619691709287371]]
		right_champ_weight2= [[6.60146933508233, -2.2461641530554393, -4.597986473899747, -1.327189333275082, 0.6096566838427392, 0.5987253948470023, 2.6256257457917256, 2.828843171152851, -6.946457704855549, 0.3248314356179649, 1.0118480087649102, -1.263196835771414, 2.5494031244422297, 0.08288173984097014, 3.276203455470974, -4.643732230600097, -0.268165229044944, 0.48441899673000455, 2.9825770513236325, 2.0148906557565422], [-1.4520749647574738, -2.828260543426143, -0.9263747718395001, -1.9877642457303453, -3.1381972358049524, 0.7950122402333238, 2.3437260634832837, -5.990525083177837, -2.5212842475648363, 3.487206718377135, -1.9126311133653269, -2.673966763354972, 5.013206574751093, 3.5949573938815087, -3.623735629926531, 0.6811230055589674, -3.807551414528435, -1.4068284346433708, -2.8177477000054045, -3.868908779445044], [3.9689661457602767, 2.946320868126739, 1.3721740140045497, -2.289436171194172, -1.8109101694482481, 0.796920301677221, -3.4992996134697365, -0.007484990525191693, 3.453633909410105, -5.783036112205776, 0.14889761921623734, 2.0734405032318586, -8.62139976134807, 2.277125345672112, -4.427925619245036, -4.577094474120971, -3.512552166524456, 1.0858158241882987, 3.7166219531904754, 3.85658667567486], [1.1597351213429672, 6.972491778667829, -0.8351177842667222, -4.33728136519101, -2.103432233208328, -2.9820119834381966, -0.21956567556144224, 5.737714946394869, 3.5465548065133383, 3.9470744656772028, 5.702506342681523, 1.3221837032406856, 1.2393385983050016, 2.236014013425946, -3.271441272482905, 2.960836881572478, -2.1546350098446356, 4.779084261718388, -0.508180862275827, 0.7003691249839769], [-0.5696636215182045, 0.8182959207847662, -5.613649900046067, -0.6456289519329731, 2.841754157425491, -3.7343308401603226, 3.49812687552557, -1.7568734316790322, 0.7438584330363586, 1.0878523491354986, -2.945459451365057, -1.850363928723477, -1.2463009816218595, -2.3671438967009437, 4.274595883338665, -8.142628190484272, 0.857083065301321, -2.569131329208873, 0.4923975260342397, -0.9767477290128909], [-5.442489515484508, -3.3889813173330934, -3.3461566357948573, 0.6255145885131228, -1.7354249008902152, 3.4271458976969615, -2.661643305225703, 7.300527259627919, -3.9789432723198037, -1.8129828413012756, 3.5190354928253234, -3.019839086896236, 4.174841692390069, 6.309412953404721, -4.29021070386403, -2.637089656902294, 1.1503972704872432, 1.0353104827933768, 2.511380697241978, -7.01919307105276], [2.5913052096523597, 1.6993346965097582, -0.9085461100428934, 3.2137726916297447, -2.163993353248865, 1.9617964129273413, 4.154983199493528, 5.089301714467414, -3.726669286089974, -1.804257276911943, 3.1508022384041183, -7.832474453677606, 2.0490853627036354, -1.66220375770782, -4.405681481756639, 1.9134287129135354, -4.805155736470014, -0.7518394713272899, -4.3861253336273585, 1.2664603226741553], [1.3847478358439704, -1.2626093311577051, -5.498867294193614, -4.193820855668639, 1.0350702313147042, 1.0004125945893532, 2.912789626138103, -1.6963029637445057, 3.229033706033436, 1.7764163982946686, 2.112418602820318, 5.36893854193732, -0.9790594988540574, 1.7808812240753018, 1.5502598785044137, -0.9894867845786228, -1.0181057133413434, -0.47684396359821746, -7.4452257536869135, 3.1317935908574426], [4.695366178961084, 2.8569709972640833, -0.3020386536840891, 0.528101844992767, 0.9522519991334155, -0.35601221791713356, 0.21640593467270752, -3.018965948234431, -0.41265160961677094, 3.3778383138562464, 1.6417519981960338, -4.691629317392791, 1.4087998737585348, -3.974452543035151, 2.243254924571472, 0.9903342548313191, -3.7412160673279877, -2.468909506932358, 7.092195719985198, -7.003945126086081], [-1.3712273214424733, 0.596912066287819, -2.90532801769789, 1.997420186660092, -0.0797728955036584, -1.8012949357204655, -2.8523206578114344, -2.4554875102437093, -2.7100641530014657, 0.4549895142202097, -4.707022398412694, -9.187842424928512, -4.152914141363345, 2.5844000243460545, 3.9166918070038705, -3.215472271716811, 0.8498601331658955, -3.76293865010195, -0.2992329339480493, -0.9695251976998802]]
		right_champ_weight3= [[0.1340269282576687, 1.2966453917831644, -0.3440181743052704, 1.0579775562484541, -0.09941262771869053, 5.57865146790478, -2.809404234512538, -3.737764910415478, 0.1642922668321929, 1.8617696243250965], [-2.0390612734397484, 2.9955917577356104, 6.699966932830071, 0.807895481800626, 1.2262516747916155, -0.5038416891583328, -4.483652276515164, 4.50936269471313, 4.164439515402216, 0.6485791485809558], [-1.408710799745318, 0.3521250114533766, 1.7033334889549678, -4.056336450662195, -2.6907943798538922, -2.776766708289843, -0.013617081466293368, 2.688308391953431, -0.167403101276978, -1.1219279482788531], [1.9158625660157502, 1.447075296224301, 7.270788988270178, -0.10100224955087456, 1.3047395605118917, -6.409880879400876, 6.644319908985153, 3.0457850715082304, -5.014331238074151, -1.8508620646318312], [-5.374670481707821, 3.9034598121394684, 0.7392866018969932, -1.6564975967599114, -2.8579369302532354, -1.4151522584716312, -4.902326985040826, 0.27654253636762716, -2.0584239044699357, 7.590133127144956], [0.7970003803110187, -6.952805044762304, -1.2249114171179984, 1.0885396174214184, -0.09098132786823632, 1.2549566699234758, 4.107873214731091, 1.3001141522608841, 3.9963076858609186, 0.731427507671781], [1.2336260442077829, 7.485126424592279, 3.5395237703407765, -2.8542693147454923, 7.681902830404643, -1.1374002911749188, -2.669934292606072, 1.6164037982334332, -3.8279289915788004, -1.9044451091765853], [0.06909927797895221, -1.8936708955287627, 1.5723639588096632, 3.930171612737498, 8.479985431017603, -0.030262038752266407, -2.668926183056904, -2.5961052177955386, 4.307216767482151, -5.262709719323575]]
		left_champ_bias1= [118.6403008356866, -37.79721766903939, -8.179094807816512, 4.305427751030839, -49.117375683513316, 32.675856489481134, -66.52080672186557, -59.57637574332165, -90.52933072683214, -133.66612299734564, 94.24037148835346, -39.139272050918514, 20.519813329486922, 68.2966529481479, -93.4103540202828, -125.05413015319004, -10.488226436722947, 58.38034190731041, -108.82976714252256, -70.45634456522222]
		left_champ_bias2= [39.19625300428389, -5.189821343366246, 29.889034309857337, 25.029984908936576, -29.616286886560438, 131.09092648037944, -98.65346332720465, -19.451411427824755, 72.52874268929682, -52.04067866247029]
		left_champ_bias3= [-79.37265442540453, -42.364005312342364, 24.637584110729378, 45.186182478632944, 5.162626494991674, -97.72658047628654, -40.65633805416249, -52.761906109621364]
		right_champ_bias1= [52.54859525842843, -122.58892551546802, 16.42591675113504, -46.81118631495377, 133.7519076565984, -13.372782865112644, 72.9735967051748, -5.063580763085264, -76.45538238129166, 70.48574479605216, -85.04178527885546, 75.80537897238685, -72.58024376921527, -70.64500199635772, -52.93744160354757, -40.31859910357845, 96.06883784980866, 56.11896052620096, 98.76042035113483, -4.2197026569943406]
		right_champ_bias2= [-36.8605309528399, 48.26198089621917, 97.17171185190114, -63.821592105588174, -16.839105892451848, 96.92642545628156, -29.72617442416118, -97.82201683512706, 30.194450883078943, 70.25067111014764]
		right_champ_bias3= [-51.043075243193, 21.570958371869008, 69.50447213253746, 96.49627363092229, -12.428560511191332, 25.27265929791849, -12.216479166152695, 64.15671723304871]
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

			self.weight1=hero.left_champ_weight1
			self.weight2=hero.left_champ_weight2
			self.weight3=hero.left_champ_weight3
			self.bias1=hero.left_champ_bias1
			self.bias2=hero.left_champ_bias2
			self.bias3=hero.left_champ_bias3
		elif side=="right":	
			self.angle=180
			object.__init__(self,WIDTH-HERO_SIZE-500,HEIGHT-100-len(hero.right_heroes)*(HERO_SIZE+10)-HERO_SIZE,HERO_SIZE,HERO_SIZE)
			hero.heroes.append(self)
			hero.right_alives.append(self)
			hero.right_heroes.append(self)


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
				eleman.y=randint(0,HEIGHT-HERO_SIZE)
			else:
				eleman.x=right_side.x+SIZE_X-HERO_SIZE-500
				eleman.angle=180
				eleman.y=randint(0,HEIGHT-HERO_SIZE)
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

			self.layer1[2:]=[self.x,left_side.size_x-self.x,self.y,HEIGHT-self.y,left_side.x+left_side.size_x-GOLD_AREA-self.x,self.angle,self.cooldown]
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
			self.layer1[2:]=[self.x-right_side.x,right_side.x+right_side.size_x-self.x,self.y,HEIGHT-self.y,right_side.x+GOLD_AREA-self.x,self.angle,self.cooldown]
			if self.x<=right_side.x+GOLD_AREA:
				if self.x == right_side.x:
					self.score-=GOLD_LOOSE
				else:
					self.score+=GOLD_GAIN
			else:
				self.score-=GOLD_LOOSE
		self.layer2=[100 if sum([self.weight1[i][j]*(self.layer1[j]+self.bias1[i]) for j in range(9)])>=5 else -100 for i in range(20)]
		self.layer3=[100 if sum([self.weight2[i][j]*(self.layer2[j]+self.bias2[i]) for j in range(20)])>=5 else -100 for i in range(10)]

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
#VARIABLES-----------------------------
#MAP-----
for i in range(HERO_COUNT-1):
	hero("left")
	hero("right")
hero("right",player=False)
hero("left")

	#hero("left",player=True)


while True:
	try:
		#print(str(hero.left_alives[0].score),"l")
		#print(str(hero.right_alives[0].score),"r")
		pass
	except:
		pass


	#FOR DISPLAY----------------------
	#translate(ORIJIN_X,ORIJIN_Y)

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
		
		print()
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
		try:
			print(str(hero.left_alives[0].score))
			print(str(L),"L")
			print(str(R),"R")
			print(str(hero.right_alives[0].score))
			print(MATCH)
			print()
		except:
			pass
		hero.restart()
	if len(hero.left_alives)>HERO_COUNT or len(hero.right_alives)>HERO_COUNT:
		print(hero.left_alives)
		print()
		print(hero.right_alives)
		print("l",len(hero.left_alives),"\nr",len(hero.right_alives))
		input("PROBLEM CONTINUES")
		if len(hero.left_alives)>=HERO_COUNT:
			hero.left_alives=hero.left_alives[1:]
		if len(hero.right_alives)>=HERO_COUNT:
			hero.right_alives=hero.right_alives[1:]

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
	
