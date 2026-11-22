# Powertrain, quattro drivetrain, suspension and cooling of the S1 E2.
# The 2,110 cc (79.3 x 85.4 mm) twenty-valve inline-five sits longitudinally ahead of the front
# axle with the turbocharger on the right; the gearbox follows it with the front differential in
# its nose, a centre differential at its tail, a propshaft and a rear differential. Internal
# dimensions are reconstructions from public descriptions.
mat('Spring enamel','C3262B',.25,.30)
mat('Damper','2B3034',.55,.36)
mat('Cast alloy','B7B9B4',.55,.42)
mat('Polished','D8DCDD',.92,.16)
mat('Kevlar','D4A72E',.30,.45)
mat('Wrap','C9A040',.75,.38)
mat('Bronze','6E5A36',.65,.40)
mat('Anodised blue','2D63C8',.6,.3)
mat('Anodised red','C42A2A',.6,.3)

def motion(**k):component_meta[cur]['run']=k
BORE,STROKE,ROD=.0793,.0854,.144
CY=.395                                   # crank axis height
CZ=[1.330+.090*i for i in range(5)]       # cylinder stations, cylinder 1 at the rear
THROW={0:0,1:144,2:216,3:288,4:72}        # firing order 1-2-4-5-3
def crankpin(i):
    a=THROW[i]*pi/180;return (STROKE/2*sin(a),CY+STROKE/2*cos(a),CZ[i])
def pin_height(i):
    x,y,z=crankpin(i);return y+sqrt(ROD*ROD-x*x)

# ── Engine ───────────────────────────────────────────────────────────────────────────────
group('engine','Inline-five turbo engine','涡轮增压直列五缸发动机',(0,.62,.55),'2.1 升 20 气门全铝直列五缸，纵置于前轴之前；右侧 KKK 涡轮与排气歧管，左侧进气稳压腔与喷油器。可进入内部拆解。')
DECK=CY+.252
component('Alloy cylinder block','铝合金缸体','缸体与润滑',(0,0,0));motion(role='shell')
box((0,(CY+DECK)/2+.02,(CZ[0]+CZ[4])/2),(.20,DECK-CY-.04,.50),'Cast alloy')
for s in (-1,1):
    box((s*.105,CY-.01,(CZ[0]+CZ[4])/2),(.03,.10,.50),'Cast alloy')
    for i in range(6):box((s*.108,CY+.12,CZ[0]-.045+.09*i),(.012,.20,.012),'Cast alloy')
for z in CZ:tor((0,DECK+.001,z),(0,1,0),BORE/2+.004,.003,'Steel',28,6)
component('Oil sump','油底壳','缸体与润滑',(0,-.30,0));motion(role='shell')
shell((0,CY-.045,(CZ[0]+CZ[4])/2),(0,0,1),[(-.26,.0),(-.26,.115),(.26,.115),(.26,.0)],'Cast alloy',4)
box((0,CY-.105,(CZ[0]+CZ[4])/2),(.21,.12,.52),'Cast alloy')
for k in range(9):box((0,CY-.168,CZ[0]-.02+.06*k),(.20,.008,.010),'Cast alloy')
component('Crankshaft','曲轴','曲柄连杆机构',(0,-.17,0));motion(role='crank')
for k in range(6):cyl((0,CY,CZ[0]-.045+.09*k-.012),(0,CY,CZ[0]-.045+.09*k+.012),.030,'Steel',20)
for i in range(5):
    p=crankpin(i)
    for side in (-1,1):
        z=CZ[i]+side*.024;a=THROW[i]*pi/180
        d=(sin(a),cos(a),0);n=(cos(a),-sin(a),0)
        q=[add((0,CY,z),add(mul(d,-.040),mul(n,-.042))),add((0,CY,z),add(mul(d,-.040),mul(n,.042))),
           add((0,CY,z),add(mul(d,.052),mul(n,.030))),add((0,CY,z),add(mul(d,.052),mul(n,-.030)))]
        plate(q,'Steel',(0,0,-side*.014))
    cyl((p[0],p[1],CZ[i]-.017),(p[0],p[1],CZ[i]+.017),.024,'Silver',18)
cyl((0,CY,CZ[0]-.07),(0,CY,CZ[0]-.045),.030,'Steel',20)
cyl((0,CY,CZ[4]+.045),(0,CY,CZ[4]+.11),.022,'Steel',16)
for no in range(5):
    p=crankpin(no);top=(0,pin_height(no),CZ[no])
    component('Connecting rod '+str(no+1),str(no+1)+' 号连杆','曲柄连杆机构',(.24,-.05,0));motion(role='rod',i=no)
    cyl(p,top,.010,'Steel',10);sleeve(p,(0,0,1),.031,.024,.020,'Steel',20);sleeve(top,(0,0,1),.016,.011,.018,'Steel',16)
    component('Piston '+str(no+1),str(no+1)+' 号活塞','曲柄连杆机构',(0,.22,0));motion(role='piston',i=no)
    shell((0,top[1]-.030,CZ[no]),(0,1,0),[(0,BORE/2-.001),(.060,BORE/2-.001),(.064,BORE/2-.004),(.064,0)],'Alloy',28)
    for k in range(3):tor((0,top[1]+.018+k*.0075,CZ[no]),(0,1,0),BORE/2-.0005,.0012,'Steel',28,4)
component('Head gasket','气缸垫','缸盖与配气',(0,.30,0));motion(role='shell')
box((0,DECK+.0015,(CZ[0]+CZ[4])/2),(.205,.003,.50),'Copper')
HEAD=DECK+.003
component('20-valve cylinder head','二十气门铝合金缸盖','缸盖与配气',(0,.40,0));motion(role='shell')
box((0,HEAD+.055,(CZ[0]+CZ[4])/2),(.22,.11,.50),'Cast alloy')
for s in (-1,1):
    for z in CZ:box((s*.115,HEAD+.040,z),(.02,.05,.050),'Cast alloy')
FIRE=[0,144,576,288,432]      # firing angle of cylinders 1-5 in degrees (order 1-2-4-5-3)
for s_,side_en,side_zh in ((-1,'Exhaust','排气'),(1,'Intake','进气')):
    component(side_en+' camshaft',side_zh+'凸轮轴','缸盖与配气',(s_*.10,.62,0));motion(role='cam',side=s_,intake=side_en=='Intake',x=s_*.045,y=HEAD+.130)
    cyl((s_*.045,HEAD+.130,CZ[0]-.07),(s_*.045,HEAD+.130,CZ[4]+.08),.013,'Steel',14)
    for i,z in enumerate(CZ):
        for dz in (-.018,.018):
            # Each lobe points straight down (valve fully open) at its peak-lift crank angle.
            peak=FIRE[i]*pi/180+(pi*2.5 if side_en=='Intake' else pi*1.5)
            a=-pi/2-peak/2
            c=(s_*.045,HEAD+.130,z+dz)
            plate([add(c,((.016+.006*max(0,cos(t)))*cos(a+t),(.016+.006*max(0,cos(t)))*sin(a+t),-.006)) for t in seq(0,2*pi,14)[:-1]],'Steel',(0,0,.012))
    pul=(s_*.045,HEAD+.130,CZ[4]+.090)
    cyl(add(pul,(0,0,-.012)),add(pul,(0,0,.012)),.058,'Gunmetal',36);cyl(add(pul,(0,0,.012)),add(pul,(0,0,.016)),.020,'Steel',16)
for s_,side_en,side_zh in ((-1,'Exhaust','排气'),(1,'Intake','进气')):
    for i,z in enumerate(CZ):
        component('%s valves %d'%(side_en,i+1),'%d 号缸%s气门'%(i+1,side_zh),'缸盖与配气',(s_*.10,.50,0));motion(role='valve',i=i,side=s_,intake=side_en=='Intake')
        for dz in (-.017,.017):
            b=(s_*.026,HEAD+.008,z+dz);t=(s_*.045,HEAD+.110,z+dz)
            cyl(b,t,.0032,'Steel',6);cyl(b,add(b,(0,.003,0)),.014,'Steel',14)
            spring(add(t,(0,-.040,0)),add(t,(0,-.008,0)),.010,.0016,'Steel')
component('Cam cover','铸铝凸轮轴罩盖','缸盖与配气',(0,.74,0));motion(role='shell')
CM=(CZ[0]+CZ[4])/2
box((0,HEAD+.137,CM),(.230,.054,.530),'Cast alloy')
for x in (-.095,-.070,-.045,.045,.070,.095):box((x,HEAD+.168,CM),(.009,.010,.500),'Cast alloy')
for z in (CZ[0]-.07,CZ[4]+.07):box((0,HEAD+.162,z),(.20,.012,.012),'Cast alloy')
box((0,HEAD+.165,CM),(.050,.004,.520),'Gunmetal')                  # plug-well channel
for i,z in enumerate(CZ):
    for k in (-1,1):bolt((k*.108,HEAD+.165,z+.045),(0,1,0),.006,'Steel')
# Raised cast "AUDI" lettering near the front of the cover, reading along the engine.
STROKES={'A':[((0,0),(2,6)),((2,6),(4,0)),((1,2.5),(3,2.5))],
         'U':[((0,6),(0,1)),((0,1),(1,0)),((1,0),(3,0)),((3,0),(4,1)),((4,1),(4,6))],
         'D':[((0,0),(0,6)),((0,6),(2.5,6)),((2.5,6),(4,4.5)),((4,4.5),(4,1.5)),((4,1.5),(2.5,0)),((2.5,0),(0,0))],
         'I':[((2,0),(2,6))]}
for k,ch in enumerate('AUDI'):
    for (u0,v0),(u1,v1) in STROKES[ch]:
        P=lambda u,v:(-.048+(v-3)*.0042,HEAD+.1745,1.645+k*.026+u*.0042)
        cyl(P(u0,v0),P(u1,v1),.0016,'Gunmetal',6)
component('Plug boots and HT loom','火花塞帽与高压线束','点火与正时',(.06,.86,0))
LX=.078
for z in CZ:
    cyl((0,HEAD+.150,z),(0,HEAD+.186,z),.012,'Black',14)
    pipe([(0,HEAD+.186,z),(.03,HEAD+.196,z),(LX-.012,HEAD+.190,z+.010)],.0045,'Black',8)
box((LX,HEAD+.186,CM-.02),(.030,.026,.460),'Black')
pipe([(LX,HEAD+.186,CZ[0]-.21),(LX+.03,HEAD+.18,CZ[0]-.13),(.10,HEAD+.15,CZ[0]-.09)],.010,'Black',10)
component('Distributor','分电器','点火与正时',(.12,.80,-.12))
cyl((.10,HEAD+.10,CZ[0]-.10),(.10,HEAD+.15,CZ[0]-.10),.034,'Black',20)
cyl((.10,HEAD+.15,CZ[0]-.10),(.10,HEAD+.16,CZ[0]-.10),.028,'Red',20)
component('Toothed timing belt drive','正时皮带与皮带轮','点火与正时',(0,.02,.24))
FZB=CZ[4]+.090
motion(role='shell')
pul=[((0,CY,FZB),.072),((.07,CY+.18,FZB),.030)]
for (c,r) in pul:cyl(add(c,(0,0,-.012)),add(c,(0,0,.012)),r,'Gunmetal',36);cyl(add(c,(0,0,.012)),add(c,(0,0,.016)),r*.35,'Steel',16)
belt=[(0,CY-.075,FZB),(.075,CY,FZB),(.10,CY+.18,FZB),(.10,HEAD+.13,FZB),(.045,HEAD+.19,FZB),(-.045,HEAD+.19,FZB),(-.104,HEAD+.13,FZB),(-.075,CY,FZB),(0,CY-.075,FZB)]
path(belt,.006,'Black',6)
component('Kevlar timing belt cover','凯夫拉正时皮带罩','点火与正时',(0,.04,.40));motion(role='shell')
box((0,(CY-.09+HEAD+.165)/2,FZB+.030),(.26,HEAD+.165-CY+.09,.010),'Kevlar')
for k in (-1,1):box((k*.128,(CY-.09+HEAD+.165)/2,FZB+.006),(.010,HEAD+.165-CY+.09,.050),'Kevlar')
box((0,HEAD+.160,FZB+.006),(.26,.010,.050),'Kevlar')
for k in range(14):box((0,CY-.07+k*.030,FZB+.036),(.24,.002,.002),'Wrap')
component('Vibration damper and crank pulley','曲轴减振皮带轮','点火与正时',(0,-.04,.34));motion(role='crank')
cyl((0,CY,FZB+.035),(0,CY,FZB+.060),.085,'Black',36);cyl((0,CY,FZB+.060),(0,CY,FZB+.064),.030,'Steel',16)
component('Intake plenum and runners','进气稳压腔与进气歧管','进气与燃油',(.36,.22,0))
IX=.30
cyl((IX,HEAD+.10,CZ[0]-.07),(IX,HEAD+.10,CZ[4]+.08),.058,'Polished',28)
for z in (CZ[0]-.07,CZ[4]+.08):tor((IX,HEAD+.10,z),(0,0,1),.058,.006,'Polished',28,6)
for z in CZ:pipe([(.11,HEAD+.05,z),(.19,HEAD+.06,z),(.25,HEAD+.085,z),(IX,HEAD+.10,z)],.019,'Polished',12)
cyl((IX,HEAD+.10,CZ[4]+.08),(IX,HEAD+.10,CZ[4]+.14),.040,'Steel',20)
component('Fuel rail and injectors','燃油导轨与喷油器','进气与燃油',(.24,.46,0))
cyl((.17,HEAD+.12,CZ[0]-.03),(.17,HEAD+.12,CZ[4]+.04),.009,'Steel',10)
for z in CZ:cyl((.17,HEAD+.12,z),(.15,HEAD+.07,z),.007,'Black',8)
component('Exhaust manifold','排气歧管','涡轮增压与排气',(-.30,.06,0))
for i,z in enumerate(CZ):
    pipe([(-.11,HEAD+.03,z),(-.18,HEAD+.00,z),(-.23,CY+.14,mix((0,0,z),(0,0,1.48),.5)[2]),(-.26,CY+.12,1.48)],.020,'Heat',12)
component('KKK turbocharger','KKK 涡轮增压器','涡轮增压与排气',(-.46,.04,.10))
TC=(-.30,CY+.10,1.46)
shell(add(TC,(0,0,-.03)),(0,0,1),[(0,.0),(0,.088),(.07,.092),(.075,.0)],'Heat',32)
shell(add(TC,(0,0,.06)),(0,0,1),[(0,.0),(0,.075),(.07,.080),(.08,.0)],'Cast alloy',32)
cyl(add(TC,(0,0,.14)),add(TC,(0,0,.22)),.040,'Cast alloy',20)
cyl(add(TC,(0,.075,.02)),add(TC,(0,.15,.02)),.022,'Cast alloy',14)
component('Wastegate','废气泄压阀','涡轮增压与排气',(-.40,.32,.14))
WG=(-.24,HEAD-.02,1.74)
pipe([(-.26,CY+.12,1.50),(-.25,CY+.18,1.64),(WG[0],WG[1]-.05,WG[2])],.024,'Heat',12)
cyl(add(WG,(0,-.05,0)),add(WG,(0,-.01,0)),.030,'Heat',18)
shell(WG,(0,1,0),[(0,.0),(0,.058),(.012,.060),(.040,.052),(.062,.030),(.070,.0)],'Polished',36)
cyl(add(WG,(0,.070,0)),add(WG,(0,.082,0)),.010,'Anodised blue',12)
component('Blow-off valve','泄压阀','涡轮增压与排气',(-.42,.10,.18))
cyl(add(TC,(-.02,.15,.10)),add(TC,(-.02,.21,.10)),.026,'Gunmetal',16)
component('Front intercooler','前置中冷器','涡轮增压与排气',(0,-.12,.64))
box((0,.50,1.845),(.64,.17,.040),'Steel')
for k in range(16):box((-.30+k*.04,.50,1.866),(.004,.16,.004),'Black')
for x in (-.33,.33):box((x,.50,1.845),(.03,.19,.05),'Cast alloy')
def coupler(c,axis,r=.040,length=.05):cyl(add(c,mul(axis,-length/2)),add(c,mul(axis,length/2)),r,'Silicone',18)
component('Charge-air crossover','增压横跨管','涡轮增压与排气',(0,.30,-.48))
xover=[add(TC,(0,0,.22)),(-.32,.60,1.66),(-.26,.76,1.42),(-.16,.835,1.22),(.16,.835,1.20),(.30,.78,1.22)]
pipe(xover,.034,'Polished',16)
coupler(add(TC,(0,0,.24)),(0,0,1));coupler((.30,.78,1.22),unit((.5,-.2,.4)))
component('Heat-wrapped charge pipe','隔热包裹增压管','涡轮增压与排气',(.64,.08,.10))
wrapped_pts=[(.33,.765,1.25),(.40,.72,1.40),(.41,.70,1.60),(.38,.62,1.76),(.30,.52,1.83)]
pipe(wrapped_pts,.036,'Wrap',16)
for t in seq(0,1,40):
    i=min(3,int(t*4));u=t*4-i;c=mix(wrapped_pts[i],wrapped_pts[i+1],u);d=unit(sub(wrapped_pts[i+1],wrapped_pts[i]))
    tor(c,d,.037,.0018,'Kevlar',20,4)
coupler(wrapped_pts[1],unit(sub(wrapped_pts[2],wrapped_pts[0])),.041);coupler(wrapped_pts[-2],unit(sub(wrapped_pts[-1],wrapped_pts[-3])),.041)
component('Plenum feed pipe','稳压腔进气管','进气与燃油',(.30,.30,.30))
pipe([(.18,.55,1.83),(.24,.66,1.84),(IX,HEAD+.10,CZ[4]+.14)],.032,'Polished',14)
coupler((.24,.66,1.84),unit((.5,.8,0)),.038)
component('Dry-sump oil tank','干式油底壳储油罐','缸体与润滑',(.34,.08,-.10))
OT=(.48,.48,1.30)
cyl(OT,add(OT,(0,.26,0)),.062,'Bronze',28)
for y in (.0,.26):tor(add(OT,(0,y,0)),(0,1,0),.062,.006,'Bronze',28,6)
cyl(add(OT,(0,.26,0)),add(OT,(0,.29,0)),.026,'Silver',16)
for dy,m in ((.05,'Anodised blue'),(.20,'Anodised red')):
    cyl(add(OT,(-.06,dy,0)),add(OT,(-.085,dy,0)),.010,m,12)
pipe([add(OT,(-.085,.05,0)),(.30,.44,1.32),(.12,CY-.06,1.36)],.008,'Braid',8)
pipe([add(OT,(-.085,.20,0)),(.30,.70,1.30),(.08,HEAD+.10,CZ[0]-.07)],.008,'Braid',8)
component('Coolant header tank','冷却液膨胀罐','附件',(-.30,.30,-.18))
HT=(-.34,.80,.80)
cyl(add(HT,(-.10,0,0)),add(HT,(.10,0,0)),.058,'Polished',28)
for x in (-.10,.10):tor(add(HT,(x,0,0)),(1,0,0),.058,.005,'Polished',28,6)
cyl(add(HT,(0,.05,0)),add(HT,(0,.075,0)),.028,'Gunmetal',16)
pipe([add(HT,(.08,-.05,0)),(-.20,.66,1.00),(0,HEAD+.05,FZB-.05)],.012,'Silicone',10)
component('Alternator and water pump','发电机与水泵','附件',(.36,-.10,.12))
cyl((.17,CY+.07,CZ[4]-.02),(.17,CY+.07,CZ[4]+.10),.060,'Cast alloy',24)
cyl((0,CY+.15,FZB-.05),(0,CY+.15,FZB-.005),.045,'Cast alloy',20)
component('Oil filter','机油滤清器','缸体与润滑',(.26,-.16,0))
cyl((.12,CY+.02,CZ[1]),(.20,CY+.02,CZ[1]),.040,'Black',20)
component('Turbo downpipe','涡轮下排气管','涡轮增压与排气',(-.30,-.22,.04))
pipe([add(TC,(0,-.09,-.03)),(-.30,.26,1.34),(-.31,.20,1.12)],.032,'Exhaust',14)

# ── Quattro drivetrain ───────────────────────────────────────────────────────────────────
group('gearbox','quattro drivetrain','quattro 四驱传动系统',(-.90,.10,.10),'双片离合器、带前差速器的六速变速箱、中央差速器、两段式传动轴、后差速器与四根半轴。可进入内部拆解。')
GY=.33
component('Flywheel and twin-plate clutch','飞轮与双片离合器','离合器',(0,0,.30));motion(role='input',y=CY)
cyl((0,CY,CZ[0]-.115),(0,CY,CZ[0]-.090),.130,'Steel',40)
for k in range(2):cyl((0,CY,CZ[0]-.140-k*.022),(0,CY,CZ[0]-.124-k*.022),.112,'Black',36)
cyl((0,CY,CZ[0]-.190),(0,CY,CZ[0]-.165),.120,'Gunmetal',36)
component('Bell housing and front differential case','离合器壳与前差速器壳','前差速器',(0,-.05,.18));motion(role='shell')
shell((0,CY-.02,CZ[0]-.22),(0,0,1),[(-.10,.11),(0,.16),(.16,.16),(.16,0)],'Cast alloy',36)
box((0,GY,FZ),(.30,.20,.22),'Cast alloy')
component('Front differential','前差速器','前差速器',(.0,-.30,0));motion(role='diff',zone='front',y=GY,z=FZ)
cyl((-.07,GY,FZ),(.07,GY,FZ),.080,'Steel',32)
gear((-.08,GY,FZ),(1,0,0),.105,.05,.022,37,'Steel')
for s in (-1,1):cyl((s*.07,GY,FZ),(s*.15,GY,FZ),.030,'Steel',16)
component('Six-speed gearbox case','六速变速箱壳体','变速箱',(0,-.20,0));motion(role='shell')
box((0,GY+.02,.80),(.26,.22,.42),'Cast alloy')
for k in range(7):box((0,GY+.135,.62+.06*k),(.20,.008,.012),'Cast alloy')
IY,OY=GY+.07,GY-.04          # input and output shaft axes
GZ=[.62+.065*k for k in range(6)]
DRIVE=[12,15,17,19,21,23];DRIVEN=[43-n for n in DRIVE]   # tooth counts on a fixed centre distance
M=.220/43                                              # module so the pitch circles meet at the 0.11 m spacing
component('Input shaft','输入轴','变速箱',(.26,.06,0));motion(role='input',y=IY)
cyl((0,IY,.56),(0,IY,1.06),.016,'Steel',14)
component('Output shaft','输出轴','变速箱',(.26,-.10,0));motion(role='output',y=OY)
cyl((0,OY,.50),(0,OY,1.06),.018,'Steel',14)
for k in range(6):
    z=GZ[k];rd=DRIVE[k]*M/2;rn=DRIVEN[k]*M/2
    component('Gear %d driver'%(k+1),'%d 挡主动齿轮'%(k+1),'变速箱',(.30,.12,0));motion(role='driver',gear=k+1,y=IY)
    gear((0,IY,z),(0,0,1),rd,.016,.016,DRIVE[k],'Steel',helix=.3)
    component('Gear %d driven'%(k+1),'%d 挡从动齿轮'%(k+1),'变速箱',(.30,-.16,0));motion(role='driven',gear=k+1,y=OY)
    gear((0,OY,z),(0,0,1),rn,.018,.016,DRIVEN[k],'Gunmetal',helix=-.3)
ZR=1.020
component('Reverse driver','倒挡主动齿轮','变速箱',(.30,.12,.06));motion(role='reverseIn',y=IY)
gear((0,IY,ZR),(0,0,1),.034,.016,.016,13,'Steel')
component('Reverse driven','倒挡从动齿轮','变速箱',(.30,-.16,.06));motion(role='reverseOut',y=OY)
gear((0,OY,ZR),(0,0,1),.064,.018,.016,25,'Gunmetal')
component('Reverse idler','倒挡惰轮','变速箱',(.38,0,.06));motion(role='idler',x=.078,y=(IY+OY)/2)
gear((.078,(IY+OY)/2,ZR),(0,0,1),.030,.010,.016,12,'Steel');cyl((.078,(IY+OY)/2,ZR-.03),(.078,(IY+OY)/2,ZR+.03),.008,'Steel',10)
SLOTS=[(1,2),(3,4),(5,6),(-1,0)]
for j,(lo,hi) in enumerate(SLOTS):
    zc=(GZ[lo-1]+GZ[hi-1])/2 if hi else (GZ[5]+ZR)/2+.006
    component('Sliding collar %d'%(j+1),'%d 号接合套'%(j+1),'变速箱',(.22,-.10,0));motion(role='collar',slot=j+1,low=lo,high=hi,y=OY)
    sleeve((0,OY,zc),(0,0,1),.040,.020,.012,'Silver',28)
    component('Selector fork %d'%(j+1),'%d 号拨叉'%(j+1),'变速箱',(-.24,.18,0));motion(role='fork',slot=j+1,low=lo,high=hi)
    box((0,OY+.055,zc),(.012,.050,.010),'Gunmetal');cyl((-.05+.035*j,GY+.12,.58),(-.05+.035*j,GY+.12,1.04),.005,'Steel',8)
    path([(0,OY+.080,zc),(-.05+.035*j,GY+.12,zc)],.005,'Gunmetal',6)
component('Centre differential','中央差速器','中央与后差速器',(0,-.20,-.25));motion(role='centre',y=GY-.04)
cyl((0,GY-.04,.50),(0,GY-.04,.58),.072,'Steel',28)
for k in range(4):
    a=k*pi/2;cyl((.04*cos(a),GY-.04+.04*sin(a),.54),(.055*cos(a),GY-.04+.055*sin(a),.54),.016,'Gunmetal',10)
# Propshaft: one straight axis from the centre differential output to the rear pinion, so it
# spins true about its own centreline.
PA=(0,GY-.04,.50);PB=(0,.31,RZ+.10)
PAX=unit(sub(PB,PA))
component('Two-piece propeller shaft','两段式传动轴','传动轴与半轴',(0,-.28,0));motion(role='prop',pivot=list(PA),axis=list(PAX))
PM=mix(PA,PB,.50)
cyl(PA,PM,.026,'Steel',14);cyl(PM,add(PB,mul(PAX,-.03)),.026,'Steel',14)
for q in (add(PA,mul(PAX,.02)),PM,add(PB,mul(PAX,-.05))):cyl(add(q,mul(PAX,-.02)),add(q,mul(PAX,.02)),.040,'Gunmetal',16)
# Drive pinion at the rear of the shaft, meshing with the crownwheel.
shell(add(PB,mul(PAX,-.03)),PAX,[(0,.020),(.045,.034),(.060,.020)],'Steel',20)
component('Rear differential case','后差速器壳','中央与后差速器',(0,-.24,-.20));motion(role='shell')
shell((0,.31,RZ+.10),(0,0,1),[(-.02,.0),(-.02,.07),(.09,.07),(.13,.04),(.13,0)],'Cast alloy',28)
shell((0,.31,RZ),(1,0,0),[(-.12,.03),(-.12,.105),(.12,.105),(.12,.03)],'Cast alloy',32)
for k in (-1,1):cyl((k*.12,.31,RZ),(k*.135,.31,RZ),.045,'Cast alloy',20)
component('Rear crownwheel and carrier','后差速器冠齿与差速器壳体','中央与后差速器',(0,-.20,-.38));motion(role='diff',zone='rear',y=.31,z=RZ)
gear((.05,.31,RZ),(1,0,0),.090,.04,.020,41,'Steel')
cyl((-.06,.31,RZ),(.06,.31,RZ),.055,'Gunmetal',24)
for k in (-1,1):cyl((k*.06,.31,RZ),(k*.15,.31,RZ),.026,'Steel',16)
for s,zc,xc,yc in [(s,zc,xc,yc) for s in (-1,1) for zc,xc,yc in ((FZ,FX,GY),(RZ,RX,.31))]:
    tag=('Front' if zc>0 else 'Rear')+(' left' if s>0 else ' right')
    zh=('前' if zc>0 else '后')+('左' if s>0 else '右')
    component(tag+' driveshaft',zh+'半轴','传动轴与半轴',(s*.30,-.05,0))
    a=(s*.15,yc,zc);b=(s*(xc-.09),TR,zc)
    motion(role='axle',zone='front' if zc>0 else 'rear',side=s,pivot=list(a),axis=list(unit(sub(b,a))))
    cyl(a,b,.016,'Steel',12)
    for p in (a,b):shell(p,unit(sub(b,a)),[(-.04,.020),(-.02,.042),(.02,.042),(.04,.020)],'Black',18)

# ── Suspension, steering and brakes ──────────────────────────────────────────────────────
group('susp','Suspension, steering and brakes','悬挂、转向与制动',(0,-.30,0),'前后均为麦弗逊滑柱与下摆臂，Boge 减振器、齿轮齿条转向、通风盘与四活塞卡钳。可进入内部拆解。')
for zc,xc,front in ((FZ,FX,True),(RZ,RX,False)):
    for s in (-1,1):
        where=('前' if front else '后')+('左' if s>0 else '右');en=('Front' if front else 'Rear')+(' left' if s>0 else ' right')
        hub=(s*(xc-.085),TR,zc)
        component(en+' MacPherson strut',where+'麦弗逊滑柱','滑柱与弹簧',(s*.20,.35,0))
        if front:motion(role='upright',side=s)
        bot=(s*(xc-.11),TR+.10,zc-.01);top=(s*(xc-.17),.86,zc-.04)
        cyl(bot,mix(bot,top,.62),.030,'Damper',18);cyl(mix(bot,top,.55),top,.012,'Silver',10)
        spring(mix(bot,top,.42),mix(bot,top,.94),.058,.008,'Spring enamel')
        cyl(mix(bot,top,.40),mix(bot,top,.42),.072,'Gunmetal',24);cyl(add(top,(0,-.01,0)),add(top,(0,.02,0)),.065,'Black',24)
        component(en+' hub carrier','%s转向节与轮毂'%where,'转向节与轮毂',(s*.30,0,0))
        if front:motion(role='upright',side=s)
        box(add(hub,(-s*.03,0,0)),(.05,.20,.10),'Cast alloy');cyl(hub,add(hub,(s*.05,0,0)),.055,'Steel',20)
        component(en+' lower wishbone',where+'下摆臂','摆臂与连杆',(s*.12,-.18,0))
        ball=(s*(xc-.10),.20,zc)
        for dz in (.16,-.13):
            inner=(s*.33,.23,zc+dz);cyl(inner,ball,.014,'Steel',10);sleeve(inner,(0,0,1),.022,.010,.04,'Black',14)
        component(en+' ventilated brake disc',where+'通风刹车盘','制动',(s*.40,0,0))
        motion(role='frontWheel' if front else 'wheel',side=s,zone='front' if front else 'rear',pivot=[s*xc,TR,zc],axis=[1,0,0])
        dx=s*(xc-.040)
        for k in (-1,1):cyl((dx+k*.008,TR,zc),(dx+k*.014,TR,zc),.150,'Steel',48)
        cyl((dx-.006,TR,zc),(dx+.006,TR,zc),.148,'Gunmetal',48);cyl((dx,TR,zc),(dx+s*.03,TR,zc),.07,'Steel',24)
        component(en+' four-piston caliper',where+'四活塞卡钳','制动',(s*.45,.10,0))
        if front:motion(role='caliper',side=s)
        ca=(-.9 if front else .9)
        box((dx,TR+.13*cos(ca),zc+.13*sin(ca)),(.07,.06,.12),'Red')
    component(('Front' if front else 'Rear')+' anti-roll bar',('前' if front else '后')+'防倾杆','摆臂与连杆',(0,-.12,(.15 if front else -.15)))
    zb=zc+(-.20 if front else .20)
    path([(-.62,.26,zc),(-.45,.26,zb),(.45,.26,zb),(.62,.26,zc)],.011,'Black',10)
component('Rack-and-pinion steering','齿轮齿条转向机','转向',(0,-.10,-.25));motion(role='rack')
cyl((-.34,.30,FZ-.12),(.34,.30,FZ-.12),.022,'Cast alloy',16)
for s in (-1,1):cyl((s*.34,.30,FZ-.12),(s*(FX-.13),.27,FZ-.12),.010,'Steel',10)
pipe([(.10,.30,FZ-.12),(.20,.45,.85),(.30,.62,.50),(.37,.70,.30)],.012,'Steel',10)

# ── E2 cooling: radiators moved into the boot ────────────────────────────────────────────
group('cooling','Rear-mounted cooling','后置冷却系统',(0,.55,-.45),'E2 把水箱、机油与变速箱冷却器移到后备厢：侧面进气口引风，经电子风扇从车尾黑色格栅排出。')
part('Water radiator and fans')
box((.30,.62,-1.70),(.52,.24,.05),'Steel')
for k in range(12):box((.30,.52+k*.018,-1.672),(.50,.004,.004),'Black')
for x in (.18,.42):cyl((x,.62,-1.73),(x,.62,-1.79),.10,'Black',24)
part('Oil and gearbox coolers')
box((-.30,.62,-1.70),(.52,.24,.05),'Steel')
for x in (-.18,-.42):cyl((x,.62,-1.73),(x,.62,-1.79),.10,'Black',24)
part('Cooling air ducts')
for s in (-1,1):
    pipe([(s*.86,.50,-.62),(s*.80,.55,-1.0),(s*.62,.60,-1.45),(s*.32,.62,-1.64)],.075,'Black',14)
part('Coolant lines to the engine')
for s in (-1,1):pipe([(s*.10,.62,-1.68),(s*.18,.24,-1.20),(s*.20,.22,.40),(s*.18,.50,1.20)],.016,'Silicone',10)

# ── Fuel cell under the rear seat ────────────────────────────────────────────────────────
current='chassis';part('Underfloor exhaust and silencer')
pipe([(-.31,.20,1.12),(-.32,.18,.95),(-.32,.17,.30),(-.32,.17,-.60),(-.36,.20,-1.40),(-.40,.22,-1.92)],.032,'Exhaust',14)
cyl((-.32,.17,-.10),(-.32,.17,-.55),.065,'Exhaust',20)
part('Safety fuel cell')
box((0,.33,-.72),(1.10,.22,.40),'Black')
cyl((.40,.45,-.72),(.40,.49,-.72),.04,'Silver',16)
