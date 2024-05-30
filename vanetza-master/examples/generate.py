import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import geopy.distance
import math
import os

roads = [[(40.64196130815548, -8.651599817893402), (40.64197241724041, -8.651542535774675), (40.641983525585786, -8.65148525339929), (40.64199463317894, -8.651427970763033), (40.642005740006745, -8.65137068786153), (40.642016846055554, -8.651313404690244), (40.64202795131126, -8.651256121244474), (40.64203905575917, -8.651198837519342), (40.64205015938403, -8.651141553509765), (40.64206126216996, -8.651084269210465), (40.64207236410047, -8.651026984615955), (40.642083465158336, -8.650969699720509), (40.642094565325635, -8.650912414518167), (40.64210566458366, -8.650855129002707), (40.642116762912856, -8.65079784316762), (40.642127860292774, -8.650740557006126), (40.64213895670204, -8.650683270511104), (40.642150052118254, -8.650625983675107), (40.642161146517914, -8.650568696490327), (40.64217223987634, -8.650511408948567), (40.642183332167605, -8.650454121041209), (40.642194423364394, -8.65039683275917), (40.64220551343792, -8.650339544092892), (40.642216602357806, -8.650282255032286), (40.64222769009194, -8.65022496556667), (40.642238776606305, -8.650167675684756), (40.64224986186481, -8.65011038537456), (40.64226094582916, -8.650053094623352), (40.6422720284585, -8.649995803417585), (40.64228310970933, -8.6499385117428), (40.642294189535114, -8.64988121958355), (40.64230526788599, -8.649823926923288), (40.64231634470837, -8.649766633744235), (40.642327419944586, -8.649709340027247), (40.64233849353231, -8.64965204575165), (40.64234956540402, -8.649594750895035), (40.64236063548632, -8.649537455433062), (40.642371703699126, -8.649480159339177), (40.6423827699547, -8.649422862584286), (40.64239383415652, -8.649365565136392), (40.64240489619785, -8.649308266960112), (40.642415955960104, -8.649250968016153), (40.64242701331063, -8.649193668260574), (40.642438068100184, -8.649136367643939), (40.642449120159554, -8.649079066110204), (40.64246016929523, -8.6490217635953), (40.642471215283756, -8.648964460025276), (40.64248225786429, -8.648907155313813), (40.64249329672825, -8.648849849358843), (40.64250433150492, -8.64879254203779), (40.642515361740536, -8.648735233200677), (40.642526386866955, -8.648677922659775), (40.64253740615196, -8.648620610173307), (40.64254841861622, -8.648563295418047), (40.64255942288272, -8.648505977939834), (40.64257041687237, -8.648448657053507), (40.64258139708278, -8.648391331606092), (40.64259235636288, -8.64833399924699), (40.64260232822538, -8.648281407423386)], [(40.6425641904421, -8.648104086128557), (40.64252051755419, -8.648089704103327), (40.64247684513885, -8.648075319612827), (40.64243317321991, -8.648060932532838), (40.64238950182369, -8.648046542726078), (40.64234583097949, -8.648032150040043), (40.642302160720014, -8.64801775430432), (40.64225849108207, -8.648003355327234), (40.64221482210736, -8.64798895289162), (40.64217115384355, -8.647974546749367), (40.64212748634562, -8.647960136614314), (40.64208381967774, -8.647945722152757), (40.642040153915666, -8.647931302970557), (40.64199648915031, -8.647916878595083), (40.64195282549274, -8.647902448449203), (40.641909163081664, -8.647888011812341), (40.64186550209525, -8.647873567759449), (40.64182184277069, -8.647859115059681), (40.6417781854393, -8.647844651994875), (40.64173453059629, -8.647830175999044), (40.641690879061905, -8.647815682826193), (40.6416472324565, -8.64780116410059), (40.64160359547523, -8.647786595611782), (40.641601012057706, -8.647785673242867)], [(40.64158087763361, -8.647778626816859), (40.64162463080166, -8.647792581822888), (40.6416683835128, -8.64780653930483), (40.641712135743816, -8.647820499387658), (40.641755887468996, -8.647834462209712), (40.64179963865971, -8.647848427924965), (40.6418433892839, -8.647862396705817), (40.64188713930543, -8.647876368746639), (40.641930888683206, -8.647890344268223), (40.64197463737017, -8.647904323523582), (40.64201838531181, -8.647918306805542), (40.64206213244429, -8.64793229445694), (40.64210587869186, -8.64794628688462), (40.6421496239631, -8.647960284579193), (40.64219336814556, -8.64797428814385), (40.64223711109765, -8.647988298338106), (40.64228085263546, -8.64800231614757), (40.64232459251069, -8.648016342902443), (40.64236833036961, -8.648030380496339), (40.64241206566799, -8.648044431839981), (40.6424557974612, -8.648058501980291), (40.6424995237071, -8.648072601809812), (40.642531400552464, -8.648082975328139)], [(40.642716577699275, -8.64798879195188), (40.64272609019846, -8.647931016023373), (40.642735601013335, -8.64787323960878), (40.642745110062634, -8.647815462685138), (40.64275461725668, -8.647757685227116), (40.64276412249599, -8.64769990720662), (40.64277362566962, -8.647642128592318), (40.64278312665306, -8.647584349349055), (40.64279262530549, -8.64752656943709), (40.642802121466474, -8.647468788811148), (40.64281161495147, -8.647411007419171), (40.64282110554599, -8.64735322520067), (40.64283059299762, -8.647295442084475), (40.64284007700503, -8.647237657985663), (40.6428495572022, -8.647179872801114), (40.642859033135004, -8.647122086402941), (40.64286850422515, -8.647064298628356), (40.64287796971098, -8.64700650926308), (40.642887428543894, -8.64694871801229), (40.64289687918821, -8.646890924444541), (40.64290631917881, -8.64683312786792), (40.64291574390956, -8.646775326991234), (40.64292514169372, -8.646717518545271), (40.6429279060416, -8.646700223922215)], [(40.642882822718036, -8.6465925337987), (40.64283909177863, -8.646578459013359), (40.64279536190374, -8.646564378536356), (40.64275163322784, -8.646550291650712), (40.642707905924006, -8.646536197433944), (40.64266418022338, -8.646522094655046), (40.64262045645009, -8.64650798158877), (40.6425767350914, -8.646493855643582), (40.642533016961984, -8.646479712491354), (40.64248930369913, -8.6464655434459), (40.64244607644473, -8.646451422602368)], [(40.64244607644473, -8.646451422602368), (40.642489807402605, -8.64646549722225), (40.64253353729188, -8.646479577570549), (40.642577265978076, -8.646493664364264), (40.642620993288084, -8.646507758525892), (40.642664718990765, -8.646521861286459), (40.642708442762, -8.646535974371231), (40.64275216411452, -8.646550100371782), (40.64279588223365, -8.646564243616263), (40.642839595482066, -8.646578412790925), (40.642882822718036, -8.6465925337987)], [(40.642953566928895, -8.646489987939923), (40.64296485959666, -8.646432766874005), (40.642976151780715, -8.646375545633932), (40.642987443475974, -8.646318324217974), (40.64299873467722, -8.646261102624381), (40.643010025379134, -8.64620388085134), (40.64302131557627, -8.64614665889701), (40.64303260526306, -8.646089436759508), (40.64304389443378, -8.646032214436898), (40.643055183082595, -8.64597499192721), (40.64306647120352, -8.645917769228406), (40.643077758790405, -8.645860546338415), (40.64308904583697, -8.64580332325511), (40.643100332336786, -8.645746099976307), (40.643111618283214, -8.645688876499763), (40.6431229036695, -8.645631652823194), (40.64313418848867, -8.64557442894424), (40.64314547273359, -8.645517204860488), (40.643156756396905, -8.645459980569454), (40.64316803947111, -8.645402756068586), (40.64317932194842, -8.645345531355266), (40.64319060382089, -8.645288306426798), (40.64320188508034, -8.645231081280405), (40.64321316571833, -8.645173855913251), (40.64322444572619, -8.6451166303224), (40.643235725094996, -8.645059404504826), (40.643247003815546, -8.645002178457421), (40.64325828187835, -8.644944952176974), (40.64326955927365, -8.644887725660181), (40.64328083599133, -8.644830498903628), (40.64329211202101, -8.6447732719038), (40.64330338735192, -8.644716044657063), (40.64331466197296, -8.644658817159652), (40.64332593587264, -8.644601589407698), (40.643337209039096, -8.644544361397179), (40.64334848146003, -8.644487133123947), (40.643359753122716, -8.644429904583696), (40.64337102401397, -8.644372675771962), (40.64338229412011, -8.644315446684132), (40.64339356342695, -8.644258217315405), (40.64340483191974, -8.644200987660808), (40.643416099583206, -8.644143757715165), (40.64342736640141, -8.644086527473103), (40.64343863235779, -8.644029296929018), (40.643449897435104, -8.643972066077097), (40.643461161615384, -8.643914834911252), (40.64347242487983, -8.643857603425147), (40.6434836872089, -8.643800371612175), (40.64349494858209, -8.643743139465418), (40.64350620897799, -8.64368590697764), (40.64351746837417, -8.643628674141269), (40.6435287267471, -8.64357144094836), (40.6435399840721, -8.64351420739058), (40.6435512403232, -8.64345697345917), (40.6435624954731, -8.64339973914491), (40.64357374949302, -8.643342504438081), (40.64358500235259, -8.64328526932844), (40.64359625401973, -8.643228033805164), (40.64360750446044, -8.64317079785678), (40.643618753638755, -8.643113561471152), (40.64363000151638, -8.643056324635367), (40.64364124805264, -8.642999087335701), (40.64365249320414, -8.642941849557511), (40.643663736924495, -8.642884611285169), (40.64367497916407, -8.64282737250193), (40.64368621986955, -8.642770133189826), (40.64369745898355, -8.642712893329515), (40.64370869644416, -8.642655652900128), (40.64371993218432, -8.642598411879069), (40.64373116613119, -8.642541170241804), (40.6437423982054, -8.642483927961583), (40.64375362832004, -8.642426685009143), (40.64376485637964, -8.64236944135233), (40.64377608227874, -8.642312196955645), (40.64378730590031, -8.642254951779677), (40.64379852711369, -8.642197705780463), (40.64380974577205, -8.642140458908601), (40.643820961709274, -8.642083211108208), (40.643832174735785, -8.642025962315513), (40.64384338463322, -8.641968712457114), (40.64385459114739, -8.641911461447563), (40.643865793978584, -8.641854209186157), (40.64387699276819, -8.64179695555244), (40.643888187079426, -8.64173970039975), (40.64389937636859, -8.6416824435456), (40.64391055994031, -8.641625184756718), (40.64392173687379, -8.641567923724367), (40.64393290589178, -8.64151066002058), (40.64394406510371, -8.641453393012377), (40.64395521142384, -8.641396121667631), (40.643966338911966, -8.64133884400215), (40.6439774313901, -8.64128155462438), (40.64397914538013, -8.641272445716009)], [(40.644105963126066, -8.6414250479259), (40.64409457063122, -8.64148223585077), (40.64408317858397, -8.641539423919594), (40.644071786989834, -8.641596612134274), (40.64406039585448, -8.64165380049674), (40.64404900518369, -8.641710989008978), (40.64403761498338, -8.641768177673008), (40.64402622525964, -8.641825366490913), (40.64401483601869, -8.641882555464816), (40.6440034472669, -8.641939744596904), (40.64399205901081, -8.641996933889414), (40.64398067125713, -8.642054123344632), (40.643969284012734, -8.642111312964921), (40.64395789728469, -8.64216850275269), (40.643946511080244, -8.642225692710422), (40.64393512540684, -8.642282882840663), (40.643923740272136, -8.642340073146025), (40.64391235568398, -8.642397263629196), (40.64390097165047, -8.642454454292945), (40.64388958817991, -8.642511645140111), (40.64387820528087, -8.642568836173629), (40.64386682296213, -8.642626027396501), (40.64385544123279, -8.642683218811822), (40.64384406010217, -8.64274041042279), (40.64383267957991, -8.642797602232706), (40.64382129967594, -8.64285479424495), (40.643809920400514, -8.642911986463034), (40.6437985417642, -8.642969178890574), (40.64378716377792, -8.643026371531299), (40.643775786452984, -8.643083564389068), (40.64376440980105, -8.643140757467872), (40.643753033834194, -8.643197950771832), (40.64374165856493, -8.64325514430522), (40.64373028400617, -8.643312338072457), (40.64371891017135, -8.643369532078129), (40.64370753707439, -8.643426726326979), (40.643696164729725, -8.64348392082394), (40.64368479315233, -8.643541115574134), (40.64367342235781, -8.643598310582883), (40.643662052362345, -8.64365550585572), (40.64365068318281, -8.643712701398403), (40.643639314836776, -8.64376989721692), (40.64362794734256, -8.643827093317539), (40.64361658071927, -8.643884289706776), (40.64360521498688, -8.643941486391444), (40.64359385016623, -8.643998683378664), (40.64358248627921, -8.644055880675888), (40.64357112334867, -8.644113078290925), (40.643559761398606, -8.644170276231964), (40.64354840045423, -8.644227474507604), (40.643537040542036, -8.644284673126876), (40.64352568168991, -8.644341872099298), (40.643514323927256, -8.644399071434897), (40.64350296728509, -8.64445627114425), (40.643491611796236, -8.64451347123854), (40.64348025749543, -8.64457067172961), (40.64346890441952, -8.644627872630023), (40.643457552607664, -8.644685073953124), (40.643446202101536, -8.644742275713119), (40.6434348529456, -8.644799477925156), (40.64342350518741, -8.64485668060543), (40.64341215887788, -8.644913883771286), (40.64340081407174, -8.644971087441371), (40.64338947082792, -8.645028291635754), (40.64337812921008, -8.645085496376108), (40.64336678928719, -8.645142701685911), (40.643355451134255, -8.645199907590683), (40.64334411483307, -8.64525711411828), (40.64333278047329, -8.645314321299198), (40.64332144815352, -8.645371529166976), (40.643310117982814, -8.64542873775871), (40.64329879008236, -8.645485947115615), (40.64328746458766, -8.64554315728375), (40.64327614165123, -8.645600368314955), (40.64326482144598, -8.645657580268004), (40.64325350416969, -8.64571479321008), (40.64324219005072, -8.645772007218726), (40.64323087935569, -8.645829222384473), (40.64321957240001, -8.64588643881438), (40.64320826956268, -8.645943656637028), (40.643196971307596, -8.646000876009742), (40.64318567821577, -8.64605809712949), (40.643174391036105, -8.64611532025001), (40.64316311077049, -8.646172545710579), (40.64315183882819, -8.646229773988097), (40.64314057733811, -8.64628700580237), (40.6431293298896, -8.646344242365736), (40.64311810382305, -8.646401486153719), (40.643107956090425, -8.646453654080425)], [(40.64314103943572, -8.646678924009313), (40.643184613694096, -8.646693812812797), (40.64322818733871, -8.646708704719916), (40.64327176033215, -8.646723599918417), (40.64331533263219, -8.646738498620344), (40.64335890419078, -8.646753401067075), (40.64340247495267, -8.646768307535861), (40.64344604485376, -8.646783218348448), (40.6434896138187, -8.646798133882728), (40.64353318175775, -8.646813054588831), (40.64357674856216, -8.646827981012004), (40.64362031409739, -8.64684291382629), (40.64366387819284, -8.646857853886265), (40.64370744062502, -8.64687280231068), (40.643751001088575, -8.646887760627276), (40.643794559141256, -8.64690273104697), (40.64383811408561, -8.646917717053503), (40.64388166465914, -8.646932724945092), (40.64392520788451, -8.64694776954757), (40.64394606245026, -8.6469550613415)], [(40.64394606245026, -8.6469550613415), (40.643902488231326, -8.64694017219892), (40.64385891462166, -8.646925279991446), (40.643815341658666, -8.646910384531337), (40.64377176938457, -8.646895485606562), (40.64372819784742, -8.646880582975745), (40.64368462710246, -8.646865676361651), (40.64364105721379, -8.646850765442538), (40.643597488256745, -8.646835849840523), (40.64355392032108, -8.646820929105493), (40.643510353515566, -8.646806002692214), (40.643466787974695, -8.646791069926657), (40.64342322386907, -8.646776129954263), (40.64337966142219, -8.646761181656291), (40.643336100939415, -8.646746223505028), (40.643292542862966, -8.646731253289573), (40.6432489878903, -8.646716267526223), (40.6432054372839, -8.646701259916792), (40.6431618940211, -8.646686215635512), (40.64314103943572, -8.646678924009313)], [(40.643014219856376, -8.646715257868811), (40.643003359191596, -8.64677262292154), (40.642992500396026, -8.646829988574838), (40.64298164356469, -8.646887354859587), (40.64297078880263, -8.646944721809922), (40.6429599362266, -8.647002089463777), (40.64294908596717, -8.647059457863557), (40.64293823817124, -8.647116827056967), (40.64292739300546, -8.647174197098105), (40.64291655066032, -8.647231568048808), (40.64290571135582, -8.647288939980458), (40.64289487534887, -8.64734631297638), (40.64288404294332, -8.647403687135117), (40.642873214504334, -8.647461062575022), (40.64286239047886, -8.647518439440923), (40.64285157142667, -8.647575817914122), (40.642840758069326, -8.647633198228185), (40.64282995137214, -8.647690580695414), (40.64281915269305, -8.647747965754833), (40.642808364083436, -8.64780535406911), (40.64279758900232, -8.647862746754429), (40.642786834524905, -8.647920146090437), (40.642777121735605, -8.647972409407442)], [(40.642854316565064, -8.64820494610823), (40.64289745230482, -8.648221893303417), (40.642940587211704, -8.648238844161344), (40.64298372123182, -8.648255798917319), (40.643026854303876, -8.648272757839118), (40.643069986357446, -8.648289721234198), (40.64311311731085, -8.648306689459199), (40.64315624706812, -8.648323662932787), (40.64319937551504, -8.64834064215335), (40.64324250251325, -8.648357627724153), (40.64328562789184, -8.648374620390305), (40.64332875143424, -8.648391621095431), (40.643371872857145, -8.648408631073117), (40.64341499177426, -8.648425652004711), (40.64345810762756, -8.648442686316928), (40.643501219540575, -8.648459737818083), (40.64354432593779, -8.648476813345773), (40.643587423158166, -8.64849392875943), (40.64360971839902, -8.648502883756114)], [(40.64360971839902, -8.648502883756114), (40.64356658270583, -8.648485936199883), (40.64352344783991, -8.648468985024572), (40.643480313855136, -8.648452029994873), (40.64343718081279, -8.648435070843021), (40.64339404878328, -8.64841810726157), (40.64335091784831, -8.648401138893885), (40.643307788103826, -8.648384165321316), (40.64326465966406, -8.64836718604549), (40.64322153266735, -8.648350200463153), (40.64317840728462, -8.648333207829207), (40.64313528373246, -8.648316207200052), (40.64309216229412, -8.648299197342114), (40.64304904335591, -8.648282176574067), (40.64300592747585, -8.648265142469228), (40.64296281553039, -8.648248091219301), (40.64291970909504, -8.64823101598673), (40.64287661183083, -8.648213900912134), (40.642854316565064, -8.64820494610823)], [(40.64274403820994, -8.648321214458623), (40.642731952881874, -8.648378155585398), (40.64271986830569, -8.648435096976943), (40.642707784495606, -8.64849203863842), (40.64269570146634, -8.648548980575201), (40.642683619233175, -8.648605922792857), (40.64267153781198, -8.648662865297172), (40.642659457219246, -8.648719808094151), (40.642647377472144, -8.648776751190061), (40.64263529858852, -8.648833694591396), (40.642623220587, -8.648890638304936), (40.64261114348697, -8.648947582337748), (40.64259906730868, -8.64900452669721), (40.64258699207328, -8.649061471391024), (40.64257491780289, -8.649118416427234), (40.642562844520654, -8.649175361814276), (40.642550772250836, -8.649232307560979), (40.64253870101888, -8.649289253676613), (40.64252663085149, -8.649346200170903), (40.642514561776785, -8.649403147054072), (40.64250249382433, -8.649460094336883), (40.642490427025315, -8.649517042030684), (40.64247836141267, -8.64957399014746), (40.64246629702123, -8.649630938699875), (40.64245423388786, -8.64968788770135), (40.64244217205168, -8.649744837166113), (40.642430111554276, -8.649801787109288), (40.64241805243994, -8.64985873754698), (40.642405994755926, -8.649915688496366), (40.642393938552765, -8.649972639975822), (40.64238188388461, -8.650029592005033), (40.642369830809685, -8.650086544605154), (40.64235777939069, -8.65014349779897), (40.64234572969541, -8.65020045161111), (40.6423336817973, -8.650257406068254), (40.64232163577626, -8.65031436119943), (40.64230959171952, -8.650371317036308), (40.6422975497227, -8.650428273613606), (40.64228550989106, -8.650485230969545), (40.64227347234109, -8.650542189146394), (40.642261437202315, -8.650599148191155), (40.64224940461975, -8.650656108156419), (40.64223737475669, -8.65071306910144), (40.64222534779856, -8.65077003109343), (40.64221332395762, -8.650826994209343), (40.642201303479354, -8.650883958538131), (40.64218928665083, -8.650940924183807), (40.642177273812365, -8.650997891269611), (40.64216526537376, -8.65105485994391), (40.6421532618381, -8.651111830388768), (40.642141263837665, -8.651168802832876), (40.64212927219111, -8.651225777572211), (40.642117288000165, -8.65128275500485), (40.64210531282728, -8.651339735694942), (40.642093349061426, -8.65139672050432), (40.642081400810575, -8.651453710913337), (40.64206947680396, -8.651510710062585), (40.642060308335076, -8.65155492832519)]]

current_pos = None
final_pos = None
speed = 60/3.6  #km /3.6 = m/s
TIME = 0.4 #seconds
current_bearing = 0
index = 0
intention = list(os.getenv("INTENT"))

#intention = [0,1,2,11,12,13]
dataset = 0
first = True
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")
    #client.subscribe("vanetza/out/spatem")
    # client.subscribe("vanetza/out/denm")
    # ...


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    #print('Topic: ' + msg.topic)
    #print('Message' + message)

    obj = json.loads(message)

    # lat = obj["latitude"]
    # ...


def next_position(current_p, final_p, tempo):
    """
      Calcula a próxima posição com base em coordenadas GPS e velocidade.

      Args:
        coordenadas_gps: Tupla com latitude e longitude (em graus).
        velocidade_x: Velocidade na direção x (em metros por segundo).
        velocidade_y: Velocidade na direção y (em metros por segundo).
        tempo: Tempo em segundos.

      Returns:
        Tupla com as coordenadas da próxima posição (latitude e longitude em graus).
      """
    global current_bearing, index, TIME, simple_positions, first, final_pos
    distance = speed * TIME / 1000
    bearing = calculate_initial_compass_bearing(current_p, final_p)

    if math.fabs(int(current_bearing)- int(bearing))>5 and not first:
        index+=1
        if index == len(simple_positions):
            index = -1
        print("index = " + str(index))
        bearing = calculate_initial_compass_bearing(current_p, simple_positions[index][1])
        final_pos = simple_positions[index][1]
        first = True
        current_bearing = bearing
        end_point = simple_positions[index][0]
    else:
        end_point = geopy.distance.distance(kilometers=distance).destination(current_pos, bearing)


    current_bearing = bearing



    if first:
        first= False
    # Retorna a próxima posição
    return end_point[0], end_point[1]

def calculate_initial_compass_bearing(pointA, pointB):
  """
  Calculates the bearing between two points.
  The formulae used is the following:
      θ = atan2(sin(Δlong).cos(lat2),
                cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
  :Parameters:
    - `pointA: The tuple representing the latitude/longitude for the
      first point. Latitude and longitude must be in decimal degrees
    - `pointB: The tuple representing the latitude/longitude for the
      second point. Latitude and longitude must be in decimal degrees
  :Returns:
    The bearing in degrees
  :Returns Type:
    float
  """
  if (type(pointA) != tuple) or (type(pointB) != tuple):
    raise TypeError("Only tuples are supported as arguments")

  lat1 = math.radians(pointA[0])
  lat2 = math.radians(pointB[0])

  diffLong = math.radians(pointB[1] - pointA[1])

  x = math.sin(diffLong) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                         * math.cos(lat2) * math.cos(diffLong))

  initial_bearing = math.atan2(x, y)

  # Now we have the initial bearing but math.atan2 return values
  # from -180° to + 180° which is not what we want for a compass bearing
  # The solution is to normalize the initial bearing as shown below
  initial_bearing = math.degrees(initial_bearing)
  compass_bearing = (initial_bearing + 360) % 360

  return compass_bearing

def get_message(data):
    f = open('my_in_cam.json')
    m = json.load(f)
    global current_pos, final_pos, index, dataset, roads
    m["latitude"] = data[index][0]
    m["longitude"] = data[index][1]
    index += 1
    if index >= len(data):
        index = 0
        dataset +=1
    print(index)
    if dataset > len(intention) -1:
        dataset = 0
    return m

def generate():
    #f = open('in_spatem.json')
    f = open('my_in_cam.json')
    m = json.load(f)
    global current_pos, final_pos, index, dataset, roads
    #next_latitude, next_longitude = next_position(current_pos, final_pos, TIME)
    #current_pos = (next_latitude, next_longitude)
    #m["latitude"] = next_latitude
    #m["longitude"] = next_longitude


    m = get_message(roads[intention[dataset]])




    m["speed"] = speed*3.6
    m = json.dumps(m)
    print(m)
    print("DATASET = "+str(dataset))
#    client.publish("vanetza/in/spatem",m)
    client.publish("vanetza/in/cam",m)
    f.close()
    sleep(TIME)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(os.getenv("OBU_MQTT_IP"), os.getenv("OBU_MQTT_PORT"), 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
