# Porsche 959 powertrain, drivetrain, suspension and cooling.
# The 2,849 cm3 (95 x 67 mm) flat-six sits longitudinally behind the rear axle, air-cooled barrels under
# water-cooled four-valve heads, with two sequential KKK turbochargers and a pair of air-to-air
# intercoolers. The six-speed gearbox sits ahead of it, between the rear wheels, with its pinion
# driving the rear differential; a viscous/PSK coupling at the front of the gearbox sends drive
# forward through a propshaft to the front differential. Internal dimensions are reconstructions
# from public descriptions, cutaway drawings and photographs.
mat('Spring enamel','16181B',.35,.40)
mat('Damper','2A5CB8',.35,.32)
mat('Cast alloy','B7B9B4',.55,.42)
mat('Polished','D8DCDD',.92,.16)
mat('Anodised blue','2D63C8',.6,.3)
mat('Magnesium','9FA3A0',.55,.5)
def motion(**k):component_meta[cur]['run']=k
BORE,STROKE,ROD=.095,.067,.127
CY=.500                                    # crank axis height
SIDE=[-1,-1,-1,1,1,1]                      # cylinders 1-3 on the right bank, 4-6 on the left
PAIR=[0,1,2,0,1,2]
CZ0=[-1.500,-1.605,-1.710]                 # crank-throw stations, flywheel end first
CZS=[CZ0[PAIR[i]]+(.0225 if SIDE[i]<0 else -.0225) for i in range(6)]
FIRE=[0,240,480,360,600,120]               # firing angles of cylinders 1-6 (order 1-6-2-4-3-5)
TH0=[(SIDE[i]*90+FIRE[i])%360 for i in range(6)]
CM=(CZ0[0]+CZ0[2])/2
R_=STROKE/2
def crankpin(i):
    a=TH0[i]*pi/180;return (R_*sin(a),CY+R_*cos(a),CZS[i])
def wrist(i):
    p=crankpin(i);return (p[0]+SIDE[i]*sqrt(ROD*ROD-(p[1]-CY)**2),CY,CZS[i])
DECK=.205                                  # cylinder deck distance from the crank axis
LET={'A':[((0,0),(2,6)),((2,6),(4,0)),((1,2.5),(3,2.5))],
     'B':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((0,3),(3,3)),((3,3),(4,2)),((4,2),(4,1)),((4,1),(3,0)),((3,0),(0,0))],
     'C':[((4,6),(0,6)),((0,6),(0,0)),((0,0),(4,0))],'D':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,1)),((4,1),(3,0)),((3,0),(0,0))],
     'E':[((4,6),(0,6)),((0,6),(0,0)),((0,0),(4,0)),((0,3),(3,3))],'H':[((0,0),(0,6)),((4,0),(4,6)),((0,3),(4,3))],
     'O':[((0,1),(0,5)),((0,5),(1,6)),((1,6),(3,6)),((3,6),(4,5)),((4,5),(4,1)),((4,1),(3,0)),((3,0),(1,0)),((1,0),(0,1))],
     'P':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((3,3),(0,3))],
     'R':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((3,3),(0,3)),((2,3),(4,0))],
     'S':[((4,6),(0,6)),((0,6),(0,3)),((0,3),(4,3)),((4,3),(4,0)),((4,0),(0,0))],
     '9':[((0,0),(4,0)),((4,0),(4,6)),((4,6),(0,6)),((0,6),(0,3)),((0,3),(4,3))],'5':[((4,6),(0,6)),((0,6),(0,3)),((0,3),(4,3)),((4,3),(4,0)),((4,0),(0,0))],
     '1':[((2,0),(2,6))],'3':[((0,6),(4,6)),((4,6),(4,0)),((4,0),(0,0)),((0,3),(4,3))],'6':[((4,6),(0,6)),((0,6),(0,0)),((0,0),(4,0)),((4,0),(4,3)),((4,3),(0,3))],' ':[]}
def lettering(text,x0,y,z0,size,adv,m):
    """Raised letters lying on a horizontal surface; text runs towards -z, letter tops point to -x."""
    for k,ch in enumerate(text):
        for (u0,v0),(u1,v1) in LET[ch]:
            P=lambda u,v:(x0-(v-3)*size,y,z0-(k*adv+u*size))
            cyl(P(u0,v0),P(u1,v1),size*.40,m,6)

# ── Engine ───────────────────────────────────────────────────────────────────────────────
group('engine','Twin-turbo flat-six','双涡轮增压水平对置六缸发动机',(0,.70,-.45),'2.85 升水平对置六缸，置于后轴后方；气缸风冷、缸盖水冷，每缸四气门，双顺序涡轮增压与两个空-空中冷器。可进入内部拆解。')
component('Crankcase halves','曲轴箱','缸体与润滑',(0,-.30,0));motion(role='shell')
box((0,CY,CM),(.19,.19,.470),'Magnesium')
for s in (-1,1):
    box((s*.100,CY,CM),(.040,.15,.46),'Magnesium')
    for k in range(7):bolt((s*.121,CY+.045*(k%2*2-1),CZ0[0]+.065-k*.0525),(s,0,0),.007,'Steel')
box((0,CY-.105,CM),(.17,.040,.47),'Magnesium')
component('Dry-sump oil tank and pump','干式油底壳与机油箱','缸体与润滑',(0,-.34,.12));motion(role='shell')
cyl((0,CY-.13,CZ0[2]-.05),(0,CY-.13,CZ0[0]+.06),.060,'Cast alloy',24)
box((-.20,.44,-1.20),(.14,.30,.22),'Cast alloy')
for k in range(5):tor((-.20,.30+k*.06,-1.20),(0,1,0),.075,.003,'Cast alloy',16,4)
component('Crankshaft','曲轴','曲柄连杆机构',(0,-.20,0));motion(role='crank')
for k in range(7):
    zz=CZ0[0]+.060-k*.0575
    if k<7:cyl((0,CY,zz-.010),(0,CY,zz+.010),.028,'Steel',20)
for i in range(6):
    p=crankpin(i);a=TH0[i]*pi/180;d=(sin(a),cos(a),0);n=(cos(a),-sin(a),0)
    for sd in (-1,1):
        z=CZS[i]+sd*.019
        q=[add((0,CY,z),add(mul(d,-.040),mul(n,-.038))),add((0,CY,z),add(mul(d,-.040),mul(n,.038))),
           add((0,CY,z),add(mul(d,.046),mul(n,.026))),add((0,CY,z),add(mul(d,.046),mul(n,-.026)))]
        plate(q,'Steel',(0,0,-sd*.011))
    cyl((p[0],p[1],CZS[i]-.0135),(p[0],p[1],CZS[i]+.0135),.022,'Silver',18)
cyl((0,CY,CZ0[0]+.05),(0,CY,CZ0[0]+.10),.035,'Steel',20);cyl((0,CY,CZ0[2]-.06),(0,CY,CZ0[2]-.14),.026,'Steel',16)
for no in range(6):
    p=crankpin(no);w=wrist(no)
    component('Connecting rod '+str(no+1),str(no+1)+' 号连杆','曲柄连杆机构',(-SIDE[no]*.0,-.05,.0+SIDE[no]*.04));motion(role='rod',i=no)
    cyl(p,w,.009,'Steel',10);sleeve(p,(0,0,1),.028,.021,.017,'Steel',20);sleeve(w,(0,0,1),.015,.010,.016,'Steel',16)
    component('Piston '+str(no+1),str(no+1)+' 号活塞','曲柄连杆机构',(SIDE[no]*.20,0,0));motion(role='piston',i=no)
    sd=SIDE[no]
    shell((w[0]-sd*.026,CY,CZS[no]),(sd,0,0),[(0,BORE/2-.001),(.052,BORE/2-.001),(.056,BORE/2-.004),(.056,0)],'Alloy',28)
    for k in range(3):tor((w[0]+sd*(.026-k*.0065+.0),CY,CZS[no]),(sd,0,0),BORE/2-.0005,.0012,'Steel',28,4)
# Cylinders: finned air-cooled barrels.
for i in range(6):
    sd=SIDE[i];z=CZS[i]
    component('Cylinder barrel '+str(i+1),str(i+1)+' 号气缸筒','缸体与润滑',(sd*.28,-.02,0));motion(role='shell')
    shell((sd*.100,CY,z),(sd,0,0),[(0,BORE/2+.002),(0,.068),(DECK-.100,.068),(DECK-.100,BORE/2+.002)],'Cast alloy',32)
    for k in range(7):tor((sd*(.112+k*.0145),CY,z),(sd,0,0),.068,.0032,'Cast alloy',32,4)
# Water-cooled four-valve heads, one per bank.
for sd,tag,zh in ((-1,'Right','右'),(1,'Left','左')):
    component(tag+' cylinder head','%s侧水冷缸盖'%zh,'缸盖与配气',(sd*.38,.04,0));motion(role='shell')
    zs=[CZS[i] for i in range(6) if SIDE[i]==sd]
    z0,z1=min(zs)-.055,max(zs)+.055
    box((sd*(DECK+.050),CY,(z0+z1)/2),(.100,.140,z1-z0),'Cast alloy')
    for z in zs:
        box((sd*(DECK+.050),CY+.082,z),(.060,.035,.050),'Cast alloy');box((sd*(DECK+.050),CY-.082,z),(.060,.035,.050),'Cast alloy')
        for k in range(4):bolt((sd*(DECK+.100),CY+.05*(k%2*2-1),z+.030*(k//2*2-1)),(sd,0,0),.006,'Steel')
    component(tag+' head gasket','%s侧缸垫'%zh,'缸盖与配气',(sd*.20,0,0));motion(role='shell')
    box((sd*(DECK+.0015),CY,(z0+z1)/2),(.003,.125,z1-z0),'Copper')
# Camshafts (one intake and one exhaust per bank) and valves.
CAMX=DECK+.136
for sd,tag,zh in ((-1,'Right','右'),(1,'Left','左')):
    zs=[CZS[i] for i in range(6) if SIDE[i]==sd]
    for d,kind,zhk in ((1,'Intake','进气'),(-1,'Exhaust','排气')):
        cx,cy_=sd*CAMX,CY+d*.052
        component('%s %s camshaft'%(tag,kind.lower()),'%s侧%s凸轮轴'%(zh,zhk),'缸盖与配气',(sd*.12,d*.14,0));motion(role='cam',x=cx,y=cy_)
        cyl((cx,cy_,min(zs)-.06),(cx,cy_,max(zs)+.06),.012,'Steel',14)
        for i in range(6):
            if SIDE[i]!=sd:continue
            mid=(2.5 if d>0 else 1.5)*pi
            beta=pi if sd>0 else 0
            a0=beta-(FIRE[i]*pi/180+mid)/2
            for dz in (-.017,.017):
                plate([add((cx,cy_,CZS[i]+dz),((.015+.006*max(0,cos(t)))*cos(a0+t),(.015+.006*max(0,cos(t)))*sin(a0+t),-.005)) for t in seq(0,2*pi,14)[:-1]],'Steel',(0,0,.010))
        sp=(cx,cy_,max(zs)+.075);cyl(add(sp,(0,0,-.010)),add(sp,(0,0,.010)),.034,'Gunmetal',30)
for i in range(6):
    sd=SIDE[i];z=CZS[i]
    for d,kind,zhk in ((1,'Intake','进气'),(-1,'Exhaust','排气')):
        component('%s valves %d'%(kind,i+1),'%d 号缸%s气门'%(i+1,zhk),'缸盖与配气',(sd*.16,d*.10,0))
        ax_=None
        for dz in (-.018,.018):
            hd=(sd*(DECK+.012),CY+d*.026,z+dz);tp=(sd*(CAMX-.030),CY+d*.052,z+dz);ax_=unit(sub(tp,hd))
            cyl(hd,tp,.0032,'Steel',6);cyl(hd,add(hd,mul(ax_,.003)),.016,'Steel',14)
            spring(add(hd,mul(ax_,.030)),add(hd,mul(ax_,.082)),.0105,.0016,'Steel')
        motion(role='valve',i=i,side=sd,intake=(d>0),axis=list(ax_))
# Cam covers with plug leads and lettering.
for sd,tag,zh in ((-1,'Right','右'),(1,'Left','左')):
    zs=[CZS[i] for i in range(6) if SIDE[i]==sd];z0,z1=min(zs)-.062,max(zs)+.062
    component(tag+' cam cover','%s侧铸镁凸轮轴罩盖'%zh,'缸盖与配气',(sd*.46,.06,0));motion(role='shell')
    box((sd*(CAMX+.020),CY,(z0+z1)/2),(.076,.205,z1-z0),'Magnesium')
    for z in zs:
        cyl((sd*(CAMX+.052),CY,z),(sd*(CAMX+.100),CY,z),.020,'Black',14)
component('Spark plug leads and distributors','火花塞线与分电器','点火与正时',(0,.60,-.30))
for i in range(6):
    sd=SIDE[i];z=CZS[i]
    cyl((sd*(CAMX+.100),CY,z),(sd*(CAMX+.128),CY,z),.014,'Red',14)
    pipe([(sd*(CAMX+.128),CY,z),(sd*(CAMX+.14),CY+.07,z+.02),(sd*.23,CY+.18,CZ0[2]-.12),(sd*.10,CY+.19,CZ0[2]-.13)],.0042,'Black',8)
for sd in (-1,1):
    cyl((sd*.10,CY+.19,CZ0[2]-.13),(sd*.10,CY+.19,CZ0[2]-.20),.028,'Anodised blue',20)
component('Timing chains and sprockets','正时链与链轮','点火与正时',(0,.02,-.26));motion(role='shell')
for sd in (-1,1):
    path([(sd*.034,CY,CZ0[2]-.115),(sd*(CAMX-.0),CY+.052,CZ0[2]-.115)],.004,'Black',6)
    path([(sd*.034,CY,CZ0[2]-.135),(sd*(CAMX-.0),CY-.052,CZ0[2]-.135)],.004,'Black',6)
cyl((0,CY,CZ0[2]-.108),(0,CY,CZ0[2]-.140),.034,'Gunmetal',28)
component('Cooling fan and shroud','冷却风扇与风道','附件',(0,.10,-.30));motion(role='crank')
FZF=CZ0[2]-.215
cyl((0,CY,FZF+.020),(0,CY,FZF-.020),.050,'Black',24)
for k in range(11):
    a=2*pi*k/11;u=(cos(a),sin(a),0);v=(-sin(a),cos(a),0)
    pts=[add((0,CY,FZF),add(mul(u,.050),mul(v,-.010))),add((0,CY,FZF),add(mul(u,.050),mul(v,.014))),add((0,CY,FZF+.012),add(mul(u,.150),mul(v,.034))),add((0,CY,FZF+.012),add(mul(u,.150),mul(v,.002)))]
    face(pts,'Charcoal');face(pts[::-1],'Charcoal')
shell((0,CY,FZF-.030),(0,0,1),[(0,.172),(.060,.176),(.064,.150)],'Magnesium',40)
component('Alternator and drive belt','发电机与传动皮带','附件',(0,.40,-.18))
cyl((0,CY+.20,FZF+.040),(0,CY+.20,FZF-.060),.058,'Gunmetal',26);cyl((0,CY+.20,FZF-.060),(0,CY+.20,FZF-.075),.034,'Black',24)
path([(0,CY+.20,FZF-.068),(.036,CY+.07,FZF-.068),(0,CY,FZF-.068)],.006,'Black',6)
# Intake: plenum, runners and fuel rails.
component('Air filter and plenum','空气滤清器与进气稳压腔','进气与燃油',(0,.48,.10))
PY=CY+.215
box((0,PY,CM),(.17,.085,.50),'Polished');cyl((0,PY,CZ0[0]+.25),(0,PY,CZ0[0]+.36),.050,'Polished',24)
box((0,PY+.06,CM),(.10,.040,.46),'Black')
component('Intake runners','进气歧管','进气与燃油',(0,.30,.14))
for i in range(6):
    sd=SIDE[i];z=CZS[i]
    pipe([(0,PY,z),(sd*.09,PY+.020,z),(sd*.19,CY+.14,z),(sd*(DECK+.050),CY+.100,z)],.020,'Polished',12)
component('Fuel rails and injectors','燃油导轨与喷油器','进气与燃油',(0,.32,.20))
for sd in (-1,1):
    zs=[CZS[i] for i in range(6) if SIDE[i]==sd]
    cyl((sd*.20,CY+.130,max(zs)+.05),(sd*.20,CY+.130,min(zs)-.05),.008,'Gold',10)
    for z in zs:cyl((sd*.20,CY+.130,z),(sd*.21,CY+.100,z),.008,'Black',8);cyl((sd*.20,CY+.130,z),(sd*.20,CY+.142,z),.009,'Red',8)
# Exhaust: manifolds to twin sequential turbochargers; intercoolers on the rear flanks.
TC={-1:(-.255,CY-.115,-1.985),1:(.255,CY-.115,-1.985)}
component('Exhaust manifolds','排气歧管','涡轮增压与排气',(0,-.26,-.10))
for i in range(6):
    sd=SIDE[i];z=CZS[i];tc=TC[sd]
    pipe([(sd*(DECK+.050),CY-.080,z),(sd*.285,CY-.125,z-.03),(sd*.30,CY-.140,mix((0,0,z),(0,0,tc[2]),.55)[2]),(sd*.28,CY-.125,tc[2]+.10)],.0200,'Exhaust',12)
for sd,tag,zh,big in ((-1,'Right','右',True),(1,'Left','左',False)):
    component(tag+' KKK turbocharger','%s侧 KKK 涡轮增压器'%zh,'涡轮增压与排气',(sd*.42,-.14,-.18))
    tc=TC[sd];rt=.082 if big else .068
    shell(add(tc,(0,0,.075)),(0,0,-1),[(0,0),(0,rt+.010),(.075,rt+.014),(.080,0)],'Heat',32)
    shell(add(tc,(0,0,-.010)),(0,0,-1),[(0,0),(0,rt),(.070,rt+.006),(.076,0)],'Cast alloy',32)
    cyl(add(tc,(0,0,-.085)),add(tc,(0,0,-.130)),.040,'Cast alloy',20);cyl(add(tc,(0,0,-.130)),add(tc,(0,0,-.160)),.044,'Gunmetal',20)
component('Twin wastegate and bypass valves','废气泄压阀与旁通阀','涡轮增压与排气',(0,-.22,-.30))
for sd in (-1,1):
    tc=TC[sd];wg=(sd*.40,CY-.12,-1.90)
    pipe([(sd*.27,CY-.125,-1.89),(sd*.33,CY-.12,-1.90),(wg[0],wg[1],wg[2])],.020,'Exhaust',12)
    shell(wg,(0,1,0),[(0,0),(0,.052),(.018,.054),(.050,.048),(.080,.030),(.090,0)],'Polished',32)
    cyl(add(wg,(0,.090,0)),add(wg,(0,.108,0)),.012,'Polished',12);cyl(add(wg,(0,.108,0)),add(wg,(0,.114,0)),.016,'Anodised blue',12)
component('Right intercooler','右中冷器','涡轮增压与排气',(-.30,.40,-.10));IC={-1:(-.560,.600,-1.620),1:(.560,.600,-1.620)}
for sd,tag,zh in ((1,'Left','左'),):
    pass
box(IC[-1],(.200,.200,.360),'Steel')
for j in range(18):box((IC[-1][0]-.100,IC[-1][1]-.085+j*.010,IC[-1][2]),(.004,.003,.34),'Black')
for dz in (-.200,.200):box((IC[-1][0],IC[-1][1],IC[-1][2]+dz),(.21,.21,.040),'Cast alloy')
component('Left intercooler','左中冷器','涡轮增压与排气',(.30,.40,-.10))
box(IC[1],(.200,.200,.360),'Steel')
for j in range(18):box((IC[1][0]+.100,IC[1][1]-.085+j*.010,IC[1][2]),(.004,.003,.34),'Black')
for dz in (-.200,.200):box((IC[1][0],IC[1][1],IC[1][2]+dz),(.21,.21,.040),'Cast alloy')
def coupler(c,axis,r=.044,length=.055):
    cyl(add(c,mul(axis,-length/2)),add(c,mul(axis,length/2)),r,'Silicone',18)
    for k in (-1,1):tor(add(c,mul(axis,k*length*.32)),axis,r+.002,.0025,'Steel',18,4)
component('Charge-air pipes','增压空气管路','涡轮增压与排气',(0,.34,-.34))
for sd in (-1,1):
    tc=TC[sd]
    pipe([add(tc,(0,0,-.160)),(sd*.32,CY-.03,-2.04),(sd*.46,CY+.20,-1.96),(sd*.56,IC[sd][1],IC[sd][2]-.24)],.032,'Copper',14)
    pipe([(sd*.56,IC[sd][1],IC[sd][2]+.24),(sd*.50,PY-.08,-1.30),(sd*.25,PY,-1.30),(0,PY,CZ0[2]+.04)],.032,'Polished',14)
    coupler((sd*.56,IC[sd][1],IC[sd][2]-.24),unit((0,0,1)),.038);coupler((sd*.56,IC[sd][1],IC[sd][2]+.235),unit((0,0,1)),.038)
component('Silencer and tailpipes','消音器与排气尾管','涡轮增压与排气',(0,-.30,-.30))
cyl((-.0,.36,-2.04),(0,.35,-1.84),.095,'Exhaust',26)
for sd in (-1,1):
    pipe([(sd*.255,CY-.115,-2.065),(sd*.10,.40,-2.02),(sd*.04,.37,-1.96)],.030,'Exhaust',12)
    cyl((sd*.30,.34,-2.02),(sd*.30,.34,-2.17),.040,'Exhaust',20)
    pipe([(0,.36,-2.04),(sd*.16,.34,-2.10),(sd*.30,.34,-2.17)],.028,'Exhaust',12)

# ── Gearbox and four-wheel drive ─────────────────────────────────────────────────────────
group('gearbox','Gearbox and 4WD','变速箱与四驱系统',(-.85,.20,.10),'六速手动变速箱位于发动机前方、两后轮之间；输出轴小齿轮直驱后差速器，前端的 PSK 耦合器经前传动轴驱动前差速器。可进入内部拆解。')
IY,OY=CY,.385
component('Flywheel and clutch','飞轮与离合器','离合器',(0,0,.30));motion(role='input',y=CY)
ZF=CZ0[0]+.12
cyl((0,CY,ZF),(0,CY,ZF-.025),.130,'Steel',40)
for k in range(2):cyl((0,CY,ZF+.010+k*.020),(0,CY,ZF+.024+k*.020),.112,'Black',36)
component('Gearbox case','变速箱壳体','变速箱',(0,.24,0));motion(role='shell')
box((0,.45,-.82),(.26,.26,.54),'Cast alloy')
shell((0,CY,ZF+.20),(0,0,1),[(0,.145),(.10,.145),(.15,.105),(.15,0)],'Cast alloy',32)
GZ=[-.640-.062*k for k in range(6)]
DRIVE=[11,14,17,20,23,26];DRIVEN=[43-n for n in DRIVE]
M=(IY-OY)*2/43
component('Input shaft','输入轴','变速箱',(.26,.06,0));motion(role='input',y=IY)
cyl((0,IY,ZF+.24),(0,IY,-.56),.016,'Steel',14)
component('Output shaft and pinion','输出轴与小齿轮','变速箱',(.26,-.10,0));motion(role='output',y=OY)
cyl((0,OY,-1.08),(0,OY,-.46),.018,'Steel',14)
cyl((0,OY,-1.08),(0,OY,-1.115),.026,'Gunmetal',20)
for k in range(6):
    z=GZ[k];rd=DRIVE[k]*M/2;rn=DRIVEN[k]*M/2
    component('Gear %d driver'%(k+1),'%d 挡主动齿轮'%(k+1),'变速箱',(.30,.12,0));motion(role='driver',gear=k+1,y=IY)
    gear((0,IY,z),(0,0,1),rd,.016,.017,DRIVE[k],'Steel',helix=.3)
    component('Gear %d driven'%(k+1),'%d 挡从动齿轮'%(k+1),'变速箱',(.30,-.16,0));motion(role='driven',gear=k+1,y=OY)
    gear((0,OY,z),(0,0,1),rn,.018,.017,DRIVEN[k],'Gunmetal',helix=-.3)
ZR=GZ[5]-.085
component('Reverse driver','倒挡主动齿轮','变速箱',(.30,.12,.06));motion(role='reverseIn',y=IY)
gear((0,IY,ZR),(0,0,1),.034,.016,.017,13,'Steel')
component('Reverse driven','倒挡从动齿轮','变速箱',(.30,-.16,.06));motion(role='reverseOut',y=OY)
gear((0,OY,ZR),(0,0,1),.064,.018,.017,25,'Gunmetal')
component('Reverse idler','倒挡惰轮','变速箱',(.38,0,.06));motion(role='idler',x=.078,y=(IY+OY)/2)
gear((.078,(IY+OY)/2,ZR),(0,0,1),.030,.010,.017,12,'Steel')
SLOTS=[(1,2),(3,4),(5,6),(-1,0)]
for j,(lo,hi) in enumerate(SLOTS):
    zc=(GZ[lo-1]+GZ[hi-1])/2 if hi else ZR-.034
    component('Sliding collar %d'%(j+1),'%d 号接合套'%(j+1),'变速箱',(.22,-.10,0));motion(role='collar',slot=j+1,low=lo,high=hi,y=OY)
    sleeve((0,OY,zc),(0,0,1),.040,.020,.012,'Silver',28)
    component('Selector fork %d'%(j+1),'%d 号拨叉'%(j+1),'变速箱',(-.24,.18,0));motion(role='fork',slot=j+1,low=lo,high=hi)
    box((0,OY+.055,zc),(.012,.050,.010),'Gunmetal');path([(0,OY+.080,zc),(-.07+.035*j,OY+.12,zc)],.005,'Gunmetal',6)
component('PSK centre coupling','PSK 中央耦合器','中央差速器与传动轴',(0,.02,.30));motion(role='centre',y=OY)
cyl((0,OY,-.50),(0,OY,-.42),.070,'Steel',28)
for k in range(5):cyl((0,OY,-.495+k*.014),(0,OY,-.489+k*.014),.064,'Black' if k%2 else 'Silver',28)
# Front propshaft from the PSK coupling forward to the front differential.
FA=(0,OY,-.42);FB=(0,.30,FZ-.10);FAX=unit(sub(FB,FA))
component('Front propshaft','前传动轴','中央差速器与传动轴',(0,-.26,.10));motion(role='prop',pivot=list(FA),axis=list(FAX))
cyl(FA,FB,.024,'Steel',14)
for q in (add(FA,mul(FAX,.04)),mix(FA,FB,.5),add(FB,mul(FAX,-.04))):cyl(add(q,mul(FAX,-.02)),add(q,mul(FAX,.02)),.038,'Gunmetal',16)
for zone,zc,yc in (('front',FZ,.30),('rear',RZ,.31)):
    tag='Front' if zone=='front' else 'Rear';zh='前' if zone=='front' else '后'
    component(tag+' differential case',zh+'差速器壳','中央差速器与传动轴',(0,-.24,.22 if zone=='front' else -.22));motion(role='shell')
    sgn=1 if zone=='front' else -1
    if zone=='front':shell((0,yc,zc-.10),(0,0,1),[(-.02,.0),(-.02,.07),(.09,.07),(.13,.04),(.13,0)],'Cast alloy',28)
    else:shell((0,yc,zc+.10),(0,0,-1),[(-.02,.0),(-.02,.07),(.07,.07),(.09,.04),(.09,0)],'Cast alloy',28)
    shell((0,yc,zc),(1,0,0),[(-.12,.03),(-.12,.105),(.12,.105),(.12,.03)],'Cast alloy',32)
    component(tag+' crownwheel and carrier',zh+'差速器冠齿与壳体','中央差速器与传动轴',(0,-.20,.38*sgn));motion(role='diff',zone=zone,y=yc,z=zc)
    gear((.05,yc,zc),(1,0,0),.078 if zone=='rear' else .090,.04,.020,41,'Steel');cyl((-.06,yc,zc),(.06,yc,zc),.055,'Gunmetal',24)
    for k in (-1,1):cyl((k*.06,yc,zc),(k*.15,yc,zc),.026,'Steel',16)
for s in (-1,1):
    for zone,zc,xc,yc in (('front',FZ,FX,.30),('rear',RZ,RX,.31)):
        tag=('Front' if zone=='front' else 'Rear')+(' left' if s>0 else ' right');zh=('前' if zone=='front' else '后')+('左' if s>0 else '右')
        component(tag+' driveshaft',zh+'半轴','中央差速器与传动轴',(s*.30,-.05,0))
        component_meta[cur].update(zone=zone,side=s,carry='shaft')
        a=(s*.15,yc,zc);b=(s*(xc-.09),TR,zc)
        motion(role='axle',zone=zone,side=s,pivot=list(a),axis=list(unit(sub(b,a))))
        cyl(a,b,.016,'Steel',12)
        for p in (a,b):shell(p,unit(sub(b,a)),[(-.04,.020),(-.02,.042),(.02,.042),(.04,.020)],'Black',18)

# ── Suspension, steering and brakes ──────────────────────────────────────────────────────
group('susp','Suspension, steering and brakes','悬挂、转向与制动',(0,-.30,0),'前后双叉臂，每个车轮配两支并排弹簧减振器（可调车高）；齿轮齿条转向、通风盘与四活塞卡钳。可进入内部拆解。')
rig={}
def carry(zone,s,kind):component_meta[cur].update(zone=zone,side=s,**({'carry':kind} if kind else {}))
for zc,xc,front in ((FZ,FX,True),(RZ,RX,False)):
    zone='front' if front else 'rear'
    for s in (-1,1):
        where=('前' if front else '后')+('左' if s>0 else '右');en=('Front' if front else 'Rear')+(' left' if s>0 else ' right')
        hub=(s*(xc-.085),TR,zc)
        lo_in=(s*.34,.24,zc);lo_ball=(s*(xc-.11),TR-.12,zc);up_in=(s*.36,.52,zc);up_ball=(s*(xc-.11),TR+.13,zc)
        top=(s*.54,.74 if front else .80,zc-(.03 if front else .02));foot=mix(lo_in,lo_ball,.80)
        outer=(s*(xc-.13),.30,zc+.12) if front else None
        if s>0:
            rig[zone]=dict(type='wishbone',z=zc,lowerInner=(.34,.24,zc),lowerBall=(xc-.11,TR-.12,zc),upperInner=(.36,.52,zc),upperBall=(xc-.11,TR+.13,zc),
                           hub=(xc-.09,TR,zc),foot=(foot[0],foot[1],foot[2]),top=(top[0],top[1],top[2]),shaftInner=(.15,.30 if front else .31,zc),
                           linkInner=(.34,.34,FZ+.18) if front else None,linkOuter=(xc-.13,.30,FZ+.12) if front else None)
        component(en+' hub carrier',where+'转向节','转向节与轮毂',(s*.30,0,0));carry(zone,s,'upright')
        if front:motion(role='upright',side=s)
        box(add(hub,(-s*.03,0,0)),(.05,.22,.10),'Cast alloy');cyl(hub,add(hub,(s*.05,0,0)),.055,'Steel',20)
        if front:
            cyl(add(hub,(-s*.045,-.03,.04)),outer,.011,'Cast alloy',10)
            cyl(add(outer,(0,-.012,0)),add(outer,(0,.012,0)),.016,'Steel',14)
        for lvl,yb,yi in (('upper',TR+.13,.52),('lower',TR-.12,.24)):
            component('%s %s wishbone'%(en,lvl),'%s%s叉臂'%(where,'上' if lvl=='upper' else '下'),'摆臂与连杆',(s*.12,.15 if lvl=='upper' else -.18,0));carry(zone,s,lvl)
            ball=(s*(xc-.11),yb,zc)
            for dz in (.15,-.13):
                inner=(s*(.34 if lvl=='lower' else .36),yi,zc+dz);cyl(inner,ball,.014,'Frame',10);sleeve(inner,(0,0,1),.020,.009,.04,'Black',14)
            cyl(add(ball,(0,-.012,0)),add(ball,(0,.012,0)),.020,'Steel',14)
        for k,dz in enumerate((-.085,.085)):
            component(en+' coil-over damper %d'%(k+1),where+'弹簧减振器'+str(k+1),'弹簧与减振器',(s*.22,.36,dz));carry(zone,s,'strut')
            bot=add(foot,(0,0,dz));tp=add(top,(0,0,dz))
            cyl(bot,mix(bot,tp,.74),.027,'Damper',16);cyl(mix(bot,tp,.70),tp,.011,'Silver',10);cyl(add(tp,(0,-.03,0)),add(tp,(0,.01,0)),.040,'Black',16)
            spring(mix(bot,tp,.40),mix(bot,tp,.92),.048,.0065,'Spring enamel')
            sleeve(bot,(0,0,1),.020,.008,.04,'Black',14)
        component(en+' ventilated brake disc',where+'通风刹车盘','制动',(s*.40,0,0));carry(zone,s,'upright')
        motion(role='frontWheel' if front else 'wheel',side=s,zone=zone,pivot=[s*xc,TR,zc],axis=[1,0,0])
        dx=s*(xc-.040)
        for k in (-1,1):cyl((dx+k*.008,TR,zc),(dx+k*.014,TR,zc),.158,'Steel',48)
        cyl((dx-.006,TR,zc),(dx+.006,TR,zc),.150,'Gunmetal',48)
        component(en+' four-piston caliper',where+'四活塞卡钳','制动',(s*.45,.10,0));carry(zone,s,'upright')
        if front:motion(role='caliper',side=s)
        ca=(.9 if front else -.9);box((dx,TR+.14*cos(ca),zc+.14*sin(ca)),(.07,.06,.12),'Red')
groups['susp']['linkage']=dict(travel=rig)
component('Rack-and-pinion steering','齿轮齿条转向机','转向',(0,-.10,.25));motion(role='rack')
cyl((-.34,.34,FZ+.18),(.34,.34,FZ+.18),.022,'Cast alloy',16)
for s in (-1,1):
    component(('Left' if s>0 else 'Right')+' track rod',('左' if s>0 else '右')+'转向横拉杆','转向',(s*.10,.08,.13));motion(role='tieRod',side=s);carry('front',s,None)
    a=(s*.34,.34,FZ+.18);b=(s*(FX-.13),.30,FZ+.12);cyl(a,b,.010,'Steel',10)
    for p in (a,b):sleeve(p,(0,1,0),.016,.007,.022,'Steel',12)
component('Power steering line','动力转向油管','转向',(0,-.10,.25))
pipe([(.10,.34,FZ+.18),(.20,.45,.90),(.30,.62,.55),(.36,.68,.20)],.012,'Steel',10)

# ── Cooling: front water radiator, with coolant lines to the rear heads ──────────────────
group('cooling','Front radiator','前置散热器',(0,.25,.55),'车头水箱与电子风扇，热风经引擎盖下方排出；冷却液管穿过车身通往后置发动机的水冷缸盖。')
part('Water radiator and fan')
grid(lambda x,t:(x,.30+.30*t,1.88-.30*t),seq(-.36,.36,8),[0,1],'Steel')
for k in range(14):path([(-.35,.31+k*.021,1.875-k*.0211),(.35,.31+k*.021,1.875-k*.0211)],.003,'Black',4)
cyl((0,.46,1.70),(0,.46,1.65),.15,'Black',28)
part('Coolant lines')
for s in (-1,1):pipe([(s*.30,.40,1.76),(s*.22,.24,1.00),(s*.22,.24,-.80),(s*.28,.40,-1.40),(s*.31,CY,-1.60)],.016,'Silicone',10)
