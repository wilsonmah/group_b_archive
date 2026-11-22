# Delta S4 powertrain, drivetrain, suspension and cooling.
# The 1,759 cc (88.5 x 71.5 mm) 16-valve Lancia 233 ATR 18S inline-four sits longitudinally behind
# the cabin, twin-charged by an Abarth Volumex supercharger and a KKK turbo with an intercooler on
# top. The five-speed gearbox sits ahead of it with the centre differential at its front; shafts run
# forward to the front differential and back under the engine to the rear differential. Internal
# dimensions are reconstructions from public descriptions, the cutaway drawing and photos.
mat('Spring enamel','D8C02A',.25,.30)
mat('Damper','E8C21E',.35,.32)
mat('Cast alloy','B7B9B4',.55,.42)
mat('Polished','D8DCDD',.92,.16)
mat('Anodised blue','2D63C8',.6,.3)
def motion(**k):component_meta[cur]['run']=k
BORE,STROKE,ROD=.0885,.0715,.130
CY=.620                                   # crank axis height
CZ=[-1.150,-1.055,-.960,-.865]            # cylinder 1 at the rear (timing) end
THROW={0:0,1:180,2:180,3:0}
FIRE=[0,540,180,360]                      # firing angles of cylinders 1-4 (order 1-3-4-2)
CM=(CZ[0]+CZ[3])/2
def crankpin(i):
    a=THROW[i]*pi/180;return (STROKE/2*sin(a),CY+STROKE/2*cos(a),CZ[i])
def pin_height(i):
    x,y,z=crankpin(i);return y+sqrt(ROD*ROD-x*x)
LET={'A':[((0,0),(2,6)),((2,6),(4,0)),((1,2.5),(3,2.5))],
     'B':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((0,3),(3,3)),((3,3),(4,2)),((4,2),(4,1)),((4,1),(3,0)),((3,0),(0,0))],
     'R':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((3,3),(0,3)),((2,3),(4,0))],
     'T':[((0,6),(4,6)),((2,6),(2,0))],'H':[((0,0),(0,6)),((4,0),(4,6)),((0,3),(4,3))]}
def lettering(text,x0,y,z0,size,adv,m):
    for k,ch in enumerate(text):
        for (u0,v0),(u1,v1) in LET[ch]:
            P=lambda u,v:(x0+(v-3)*size,y,z0-(k*adv+u*size))
            cyl(P(u0,v0),P(u1,v1),size*.40,m,6)

# ── Engine ───────────────────────────────────────────────────────────────────────────────
group('engine','Twin-charged inline-four','双增压直列四缸发动机',(0,.70,-.45),'1.8 升 16 气门直列四缸，纵置于驾驶舱后方；Abarth Volumex 机械增压器与 KKK 涡轮串联增压，顶部中冷器。可进入内部拆解。')
DECK=CY+.235;HEAD=DECK+.003
component('Cast-iron cylinder block','铸铁缸体','缸体与润滑',(0,0,0));motion(role='shell')
box((0,(CY+DECK)/2+.02,CM),(.20,DECK-CY-.04,.40),'Gunmetal')
for s in (-1,1):
    box((s*.105,CY-.01,CM),(.03,.10,.40),'Gunmetal')
    for i in range(5):box((s*.108,CY+.12,CZ[0]-.047+.095*i),(.012,.20,.012),'Gunmetal')
for z in CZ:tor((0,DECK+.001,z),(0,1,0),BORE/2+.004,.003,'Steel',28,6)
component('Dry sump pan','干式油底壳','缸体与润滑',(0,-.24,0));motion(role='shell')
box((0,CY-.090,CM),(.20,.080,.42),'Cast alloy')
for k in range(8):box((0,CY-.132,CZ[0]-.03+.055*k),(.19,.006,.010),'Cast alloy')
component('Crankshaft','曲轴','曲柄连杆机构',(0,-.16,0));motion(role='crank')
for k in range(5):cyl((0,CY,CZ[0]-.0475+.095*k-.012),(0,CY,CZ[0]-.0475+.095*k+.012),.030,'Steel',20)
for i in range(4):
    p=crankpin(i)
    for side in (-1,1):
        z=CZ[i]+side*.024;a=THROW[i]*pi/180
        d=(sin(a),cos(a),0);n=(cos(a),-sin(a),0)
        q=[add((0,CY,z),add(mul(d,-.038),mul(n,-.042))),add((0,CY,z),add(mul(d,-.038),mul(n,.042))),
           add((0,CY,z),add(mul(d,.048),mul(n,.030))),add((0,CY,z),add(mul(d,.048),mul(n,-.030)))]
        plate(q,'Steel',(0,0,-side*.014))
    cyl((p[0],p[1],CZ[i]-.017),(p[0],p[1],CZ[i]+.017),.024,'Silver',18)
cyl((0,CY,CZ[3]+.045),(0,CY,CZ[3]+.10),.030,'Steel',20);cyl((0,CY,CZ[0]-.11),(0,CY,CZ[0]-.045),.022,'Steel',16)
for no in range(4):
    p=crankpin(no);top=(0,pin_height(no),CZ[no])
    component('Connecting rod '+str(no+1),str(no+1)+' 号连杆','曲柄连杆机构',(.24,-.05,0));motion(role='rod',i=no)
    cyl(p,top,.010,'Steel',10);sleeve(p,(0,0,1),.031,.024,.020,'Steel',20);sleeve(top,(0,0,1),.016,.011,.018,'Steel',16)
    component('Piston '+str(no+1),str(no+1)+' 号活塞','曲柄连杆机构',(0,.22,0));motion(role='piston',i=no)
    shell((0,top[1]-.028,CZ[no]),(0,1,0),[(0,BORE/2-.001),(.056,BORE/2-.001),(.060,BORE/2-.004),(.060,0)],'Alloy',28)
    for k in range(3):tor((0,top[1]+.016+k*.007,CZ[no]),(0,1,0),BORE/2-.0005,.0012,'Steel',28,4)
component('Head gasket','气缸垫','缸盖与配气',(0,.30,0));motion(role='shell')
box((0,DECK+.0015,CM),(.205,.003,.40),'Copper')
component('16-valve cylinder head','十六气门铝合金缸盖','缸盖与配气',(0,.40,0));motion(role='shell')
box((0,HEAD+.055,CM),(.22,.11,.40),'Cast alloy')
for s in (-1,1):
    for z in CZ:box((s*.115,HEAD+.040,z),(.02,.05,.050),'Cast alloy')
for s_,side_en,side_zh in ((-1,'Exhaust','排气'),(1,'Intake','进气')):
    component(side_en+' camshaft',side_zh+'凸轮轴','缸盖与配气',(s_*.10,.62,0));motion(role='cam',side=s_,intake=side_en=='Intake',x=s_*.045,y=HEAD+.130)
    cyl((s_*.045,HEAD+.130,CZ[3]+.07),(s_*.045,HEAD+.130,CZ[0]-.08),.013,'Steel',14)
    for i,z in enumerate(CZ):
        for dz in (-.018,.018):
            peak=FIRE[i]*pi/180+(pi*2.5 if side_en=='Intake' else pi*1.5)
            a=-pi/2-peak/2;c=(s_*.045,HEAD+.130,z+dz)
            plate([add(c,((.016+.006*max(0,cos(t)))*cos(a+t),(.016+.006*max(0,cos(t)))*sin(a+t),-.006)) for t in seq(0,2*pi,14)[:-1]],'Steel',(0,0,.012))
    pul=(s_*.045,HEAD+.130,CZ[0]-.090)
    cyl(add(pul,(0,0,-.012)),add(pul,(0,0,.012)),.058,'Gunmetal',36)
for s_,side_en,side_zh in ((-1,'Exhaust','排气'),(1,'Intake','进气')):
    for i,z in enumerate(CZ):
        component('%s valves %d'%(side_en,i+1),'%d 号缸%s气门'%(i+1,side_zh),'缸盖与配气',(s_*.10,.50,0));motion(role='valve',i=i,side=s_,intake=side_en=='Intake')
        for dz in (-.017,.017):
            b=(s_*.026,HEAD+.008,z+dz);t=(s_*.045,HEAD+.110,z+dz)
            cyl(b,t,.0032,'Steel',6);cyl(b,add(b,(0,.003,0)),.014,'Steel',14)
            spring(add(t,(0,-.040,0)),add(t,(0,-.008,0)),.010,.0016,'Steel')
component('Abarth cam cover','Abarth 凸轮轴罩盖','缸盖与配气',(0,.74,0));motion(role='shell')
box((0,HEAD+.137,CM),(.230,.054,.430),'Cast alloy')
for x in (-.095,-.070,.070,.095):box((x,HEAD+.168,CM),(.009,.010,.40),'Cast alloy')
for z in CZ:
    for k in (-1,1):bolt((k*.108,HEAD+.165,z+.045),(0,1,0),.006,'Steel')
lettering('ABARTH',-.040,HEAD+.172,CM+.130,.0055,.044,'Red')
lettering('ABARTH',.040,HEAD+.172,CM+.130,.0055,.044,'Red')
component('Plug caps and HT leads','火花塞帽与高压线','点火与正时',(.06,.86,0))
for z in CZ:
    cyl((0,HEAD+.150,z),(0,HEAD+.192,z),.012,'Red',14)
    pipe([(0,HEAD+.192,z),(.04,HEAD+.20,z),(.10,HEAD+.18,CZ[3]+.10)],.004,'Black',8)
component('Distributor','分电器','点火与正时',(.12,.80,.12))
cyl((.10,HEAD+.10,CZ[3]+.10),(.10,HEAD+.15,CZ[3]+.10),.034,'Black',20);cyl((.10,HEAD+.15,CZ[3]+.10),(.10,HEAD+.16,CZ[3]+.10),.028,'Red',20)
component('Timing belt drive','正时皮带','点火与正时',(0,.02,-.24));motion(role='shell')
FZB=CZ[0]-.090
cyl((0,CY,FZB-.012),(0,CY,FZB+.012),.070,'Gunmetal',36)
path([(0,CY-.072,FZB),(.072,CY,FZB),(.10,HEAD+.13,FZB),(.045,HEAD+.19,FZB),(-.045,HEAD+.19,FZB),(-.10,HEAD+.13,FZB),(-.072,CY,FZB),(0,CY-.072,FZB)],.006,'Black',6)
box((0,(CY-.09+HEAD+.165)/2,FZB-.030),(.26,HEAD+.165-CY+.09,.010),'Black')
component('Crank pulley','曲轴皮带轮','点火与正时',(0,-.04,-.32));motion(role='crank')
cyl((0,CY,FZB-.035),(0,CY,FZB-.060),.080,'Black',36)
component('Intake plenum and runners','进气稳压腔与进气歧管','进气与燃油',(.34,.20,0))
IX=.22
cyl((IX,HEAD+.15,CZ[3]+.07),(IX,HEAD+.15,CZ[0]-.07),.052,'Cast alloy',24)
for z in CZ:pipe([(.11,HEAD+.05,z),(.17,HEAD+.08,z),(IX,HEAD+.15,z)],.020,'Cast alloy',12)
cyl((IX,HEAD+.15,CZ[3]+.07),(IX,HEAD+.15,CZ[3]+.13),.036,'Cast alloy',18)
component('Fuel rail and injectors','燃油导轨与喷油器','进气与燃油',(.24,.46,0))
cyl((.15,HEAD+.10,CZ[3]+.04),(.15,HEAD+.10,CZ[0]-.04),.009,'Steel',10)
for z in CZ:cyl((.15,HEAD+.10,z),(.13,HEAD+.06,z),.007,'Black',8)
component('Tubular exhaust manifold','管式排气歧管','涡轮增压与排气',(-.32,.04,0))
TC=(-.30,CY+.10,-1.42)
for i,z in enumerate(CZ):
    pipe([(-.11,HEAD+.03,z),(-.18,HEAD-.01,z),(-.22,CY+.06,mix((0,0,z),(0,0,TC[2]),.45)[2]),(-.27,CY+.08,TC[2]+.08)],.019,'Exhaust',12)
component('KKK turbocharger','KKK 涡轮增压器','涡轮增压与排气',(-.40,.06,-.18))
shell(add(TC,(0,0,.03)),(0,0,-1),[(0,.0),(0,.088),(.07,.092),(.075,.0)],'Heat',32)
shell(add(TC,(0,0,-.06)),(0,0,-1),[(0,.0),(0,.072),(.07,.078),(.08,.0)],'Cast alloy',32)
cyl(add(TC,(0,0,-.14)),add(TC,(0,0,-.20)),.040,'Cast alloy',20)
component('Wastegate','废气泄压阀','涡轮增压与排气',(-.38,.30,-.12))
WG=(-.34,CY+.22,-1.30)
pipe([(-.27,CY+.08,TC[2]+.08),(-.31,CY+.15,-1.32),(WG[0],WG[1]-.05,WG[2])],.022,'Exhaust',12)
shell(WG,(0,1,0),[(0,.0),(0,.058),(.012,.060),(.040,.052),(.062,.030),(.070,.0)],'Polished',36)
cyl(add(WG,(0,.070,0)),add(WG,(0,.082,0)),.010,'Anodised blue',12)
component('Abarth Volumex supercharger','Abarth Volumex 机械增压器','涡轮增压与排气',(.42,.04,-.08))
SC=(.28,CY+.02,-1.05)
cyl(add(SC,(0,0,.14)),add(SC,(0,0,-.14)),.075,'Cast alloy',28)
for k in range(5):tor(add(SC,(0,0,.10-k*.05)),(0,0,1),.076,.004,'Cast alloy',28,4)
cyl(add(SC,(0,0,-.14)),add(SC,(0,0,-.17)),.060,'Gunmetal',28);cyl(add(SC,(0,0,-.17)),add(SC,(0,0,-.19)),.050,'Black',28)
path([add(SC,(0,0,-.18)),(0,CY,FZB-.05)],.008,'Black',6)
component('Intercooler','中冷器','涡轮增压与排气',(0,.36,-.10))
IC=(0,1.085,-1.28)
box(IC,(.62,.065,.36),'Steel')
for k in range(18):box((-.29+k*.034,IC[1]+.034,IC[2]),(.004,.004,.34),'Black')
for x in (-.33,.33):box((x,IC[1],IC[2]),(.04,.08,.38),'Cast alloy')
component('Charge-air pipes','增压管路','涡轮增压与排气',(.10,.50,-.35))
def coupler(c,axis,r=.042,length=.05):cyl(add(c,mul(axis,-length/2)),add(c,mul(axis,length/2)),r,'Silicone',18)
pipe([add(TC,(0,0,-.20)),(-.24,.86,-1.55),(-.20,1.02,-1.46),(-.33,1.10,-1.36)],.036,'Polished',14)
coupler((-.24,.86,-1.55),unit((0,1,.3)))
pipe([(.33,1.10,-1.20),(.34,.95,-1.10),(.30,.78,-1.05),add(SC,(0,.07,.0))],.036,'Polished',14)
coupler((.34,.95,-1.10),unit((0,-1,.3)))
pipe([add(SC,(0,0,.14)),(.26,.70,-.78),(IX,HEAD+.15,CZ[3]+.13)],.034,'Polished',14)
coupler((.26,.70,-.78),unit((0,.3,1)))
component('Exhaust and silencer','排气管与消音器','涡轮增压与排气',(-.20,-.25,-.25))
pipe([add(TC,(0,-.09,.03)),(-.30,.52,-1.55),(-.26,.42,-1.80),(-.22,.40,-2.10)],.034,'Exhaust',14)
cyl((-.24,.41,-1.72),(-.23,.405,-1.98),.065,'Exhaust',20)

# ── Gearbox and four-wheel drive ─────────────────────────────────────────────────────────
group('gearbox','Gearbox and 4WD','变速箱与四驱系统',(-.85,.20,.10),'Hewland 五速变速箱置于发动机前方，前端为中央差速器，前传动轴通往前差速器，后传动轴从发动机下方通往后差速器。可进入内部拆解。')
IY,OY=CY,CY-.11
component('Flywheel and clutch','飞轮与离合器','离合器',(0,0,.30));motion(role='input',y=CY)
cyl((0,CY,CZ[3]+.10),(0,CY,CZ[3]+.125),.125,'Steel',40)
for k in range(2):cyl((0,CY,CZ[3]+.135+k*.020),(0,CY,CZ[3]+.150+k*.020),.108,'Black',36)
component('Gearbox case','变速箱壳体','变速箱',(0,.24,0));motion(role='shell')
box((0,CY-.055,-.50),(.26,.24,.40),'Cast alloy')
shell((0,CY,CZ[3]+.10),(0,0,1),[(0,.15),(.10,.15),(.14,.11),(.14,0)],'Cast alloy',32)
GZ=[-.640+.060*k for k in range(5)]
DRIVE=[12,15,18,21,23];DRIVEN=[43-n for n in DRIVE]
M=.220/43
component('Input shaft','输入轴','变速箱',(.26,.06,0));motion(role='input',y=IY)
cyl((0,IY,CZ[3]+.16),(0,IY,-.34),.016,'Steel',14)
component('Output shaft','输出轴','变速箱',(.26,-.10,0));motion(role='output',y=OY)
cyl((0,OY,-.70),(0,OY,-.27),.018,'Steel',14)
for k in range(5):
    z=GZ[k];rd=DRIVE[k]*M/2;rn=DRIVEN[k]*M/2
    component('Gear %d driver'%(k+1),'%d 挡主动齿轮'%(k+1),'变速箱',(.30,.12,0));motion(role='driver',gear=k+1,y=IY)
    gear((0,IY,z),(0,0,1),rd,.016,.016,DRIVE[k],'Steel',helix=.3)
    component('Gear %d driven'%(k+1),'%d 挡从动齿轮'%(k+1),'变速箱',(.30,-.16,0));motion(role='driven',gear=k+1,y=OY)
    gear((0,OY,z),(0,0,1),rn,.018,.016,DRIVEN[k],'Gunmetal',helix=-.3)
ZR=-.36
component('Reverse driver','倒挡主动齿轮','变速箱',(.30,.12,.06));motion(role='reverseIn',y=IY)
gear((0,IY,ZR),(0,0,1),.034,.016,.016,13,'Steel')
component('Reverse driven','倒挡从动齿轮','变速箱',(.30,-.16,.06));motion(role='reverseOut',y=OY)
gear((0,OY,ZR),(0,0,1),.064,.018,.016,25,'Gunmetal')
component('Reverse idler','倒挡惰轮','变速箱',(.38,0,.06));motion(role='idler',x=.078,y=(IY+OY)/2)
gear((.078,(IY+OY)/2,ZR),(0,0,1),.030,.010,.016,12,'Steel')
SLOTS=[(1,2),(3,4),(5,0),(-1,0)]
for j,(lo,hi) in enumerate(SLOTS):
    zc=(GZ[lo-1]+GZ[hi-1])/2 if hi else (GZ[4]+.030 if lo==5 else ZR-.030)
    component('Sliding collar %d'%(j+1),'%d 号接合套'%(j+1),'变速箱',(.22,-.10,0));motion(role='collar',slot=j+1,low=lo,high=hi,y=OY)
    sleeve((0,OY,zc),(0,0,1),.040,.020,.012,'Silver',28)
    component('Selector fork %d'%(j+1),'%d 号拨叉'%(j+1),'变速箱',(-.24,.18,0));motion(role='fork',slot=j+1,low=lo,high=hi)
    box((0,OY+.055,zc),(.012,.050,.010),'Gunmetal');path([(0,OY+.080,zc),(-.07+.035*j,OY+.12,zc)],.005,'Gunmetal',6)
component('Centre differential','中央差速器','中央差速器与传动轴',(0,.02,.22));motion(role='centre',y=OY)
cyl((0,OY,-.27),(0,OY,-.19),.072,'Steel',28)
for k in range(4):
    a=k*pi/2;cyl((.04*cos(a),OY+.04*sin(a),-.23),(.055*cos(a),OY+.055*sin(a),-.23),.016,'Gunmetal',10)
# Front propshaft from the centre differential forward to the front differential.
FA=(0,OY,-.19);FB=(0,.30,FZ-.10);FAX=unit(sub(FB,FA))
component('Front propshaft','前传动轴','中央差速器与传动轴',(0,-.26,.10));motion(role='prop',pivot=list(FA),axis=list(FAX))
cyl(FA,FB,.024,'Steel',14)
for q in (add(FA,mul(FAX,.03)),mix(FA,FB,.5),add(FB,mul(FAX,-.04))):cyl(add(q,mul(FAX,-.02)),add(q,mul(FAX,.02)),.038,'Gunmetal',16)
# Rear propshaft from a transfer drop under the gearbox, back beneath the sump to the rear pinion.
RA_=(.14,.33,-.30);RB=(.03,.31,RZ+.12);RAX=unit(sub(RB,RA_))
component('Rear propshaft','后传动轴','中央差速器与传动轴',(.20,-.22,-.05));motion(role='prop',pivot=list(RA_),axis=list(RAX))
cyl(RA_,RB,.024,'Steel',14)
for q in (add(RA_,mul(RAX,.03)),mix(RA_,RB,.5),add(RB,mul(RAX,-.04))):cyl(add(q,mul(RAX,-.02)),add(q,mul(RAX,.02)),.038,'Gunmetal',16)
component('Transfer drop gears','分动齿轮','中央差速器与传动轴',(.24,.10,.12));motion(role='shell')
box((.07,(OY+.33)/2,-.30),(.22,OY-.33+.10,.05),'Cast alloy')
for zone,zc,yc in (('front',FZ,.30),('rear',RZ,.31)):
    tag='Front' if zone=='front' else 'Rear';zh='前' if zone=='front' else '后'
    component(tag+' differential case',zh+'差速器壳','中央差速器与传动轴',(0,-.24,.22 if zone=='front' else -.22));motion(role='shell')
    sgn=1 if zone=='front' else -1
    shell((0,yc,zc-sgn*.10),(0,0,sgn),[(-.02,.0),(-.02,.07),(.09,.07),(.13,.04),(.13,0)],'Cast alloy',28)
    shell((0,yc,zc),(1,0,0),[(-.12,.03),(-.12,.105),(.12,.105),(.12,.03)],'Cast alloy',32)
    component(tag+' crownwheel and carrier',zh+'差速器冠齿与壳体','中央差速器与传动轴',(0,-.20,.38*sgn));motion(role='diff',zone=zone,y=yc,z=zc)
    gear((.05,yc,zc),(1,0,0),.090,.04,.020,41,'Steel');cyl((-.06,yc,zc),(.06,yc,zc),.055,'Gunmetal',24)
    for k in (-1,1):cyl((k*.06,yc,zc),(k*.15,yc,zc),.026,'Steel',16)
for s in (-1,1):
    for zone,zc,xc,yc in (('front',FZ,FX,.30),('rear',RZ,RX,.31)):
        tag=('Front' if zone=='front' else 'Rear')+(' left' if s>0 else ' right');zh=('前' if zone=='front' else '后')+('左' if s>0 else '右')
        component(tag+' driveshaft',zh+'半轴','中央差速器与传动轴',(s*.30,-.05,0))
        a=(s*.15,yc,zc);b=(s*(xc-.09),TR,zc)
        motion(role='axle',zone=zone,side=s,pivot=list(a),axis=list(unit(sub(b,a))))
        cyl(a,b,.016,'Steel',12)
        for p in (a,b):shell(p,unit(sub(b,a)),[(-.04,.020),(-.02,.042),(.02,.042),(.04,.020)],'Black',18)

# ── Suspension, steering and brakes ──────────────────────────────────────────────────────
group('susp','Suspension, steering and brakes','悬挂、转向与制动',(0,-.30,0),'前后双叉臂：前轮单组同轴弹簧减振器，后轮双减振器；齿轮齿条转向、通风盘与四活塞卡钳。可进入内部拆解。')
for zc,xc,front in ((FZ,FX,True),(RZ,RX,False)):
    for s in (-1,1):
        where=('前' if front else '后')+('左' if s>0 else '右');en=('Front' if front else 'Rear')+(' left' if s>0 else ' right')
        hub=(s*(xc-.085),TR,zc)
        component(en+' hub carrier',where+'转向节','转向节与轮毂',(s*.30,0,0))
        if front:motion(role='upright',side=s)
        box(add(hub,(-s*.03,0,0)),(.05,.22,.10),'Cast alloy');cyl(hub,add(hub,(s*.05,0,0)),.055,'Steel',20)
        for lvl,yb,yi in (('upper',TR+.13,.62),('lower',TR-.12,.24)):
            component('%s %s wishbone'%(en,lvl),'%s%s叉臂'%(where,'上' if lvl=='upper' else '下'),'摆臂与连杆',(s*.12,.15 if lvl=='upper' else -.18,0))
            ball=(s*(xc-.11),yb,zc)
            for dz in (.15,-.13):
                inner=(s*.36,yi,zc+dz);cyl(inner,ball,.013,'Steel',10);sleeve(inner,(0,0,1),.020,.009,.04,'Black',14)
        dampers=[0] if front else [-.09,.09]
        for k,dz in enumerate(dampers):
            component(en+' coil-over damper'+('' if front else ' %d'%(k+1)),where+'弹簧减振器'+('' if front else str(k+1)),'弹簧与减振器',(s*.22,.36,dz))
            bot=(s*(xc-.14),TR-.08,zc+dz);top=(s*.56,.86 if front else .84,zc+dz-(.05 if front else .02))
            cyl(bot,mix(bot,top,.62),.026,'Damper',16);cyl(mix(bot,top,.55),top,.011,'Silver',10)
            spring(mix(bot,top,.40),mix(bot,top,.92),.050,.007,'Spring enamel')
        component(en+' ventilated brake disc',where+'通风刹车盘','制动',(s*.40,0,0))
        motion(role='frontWheel' if front else 'wheel',side=s,zone='front' if front else 'rear',pivot=[s*xc,TR,zc],axis=[1,0,0])
        dx=s*(xc-.040)
        for k in (-1,1):cyl((dx+k*.008,TR,zc),(dx+k*.014,TR,zc),.150,'Steel',48)
        cyl((dx-.006,TR,zc),(dx+.006,TR,zc),.148,'Gunmetal',48)
        component(en+' four-piston caliper',where+'四活塞卡钳','制动',(s*.45,.10,0))
        if front:motion(role='caliper',side=s)
        ca=(.9 if front else -.9);box((dx,TR+.13*cos(ca),zc+.13*sin(ca)),(.07,.06,.12),'Gold')
component('Rack-and-pinion steering','齿轮齿条转向机','转向',(0,-.10,.25));motion(role='rack')
cyl((-.34,.34,FZ+.18),(.34,.34,FZ+.18),.022,'Cast alloy',16)
for s in (-1,1):cyl((s*.34,.34,FZ+.18),(s*(FX-.13),.30,FZ+.12),.010,'Steel',10)
pipe([(.10,.34,FZ+.18),(.20,.45,.90),(.30,.62,.55),(.37,.70,.30)],.012,'Steel',10)

# ── Cooling: front water radiator ventilated through the bonnet ──────────────────────────
group('cooling','Front radiator','前置散热器',(0,.25,.55),'车头水箱与电子风扇，热风经引擎盖百叶排出；冷却液管穿过车身通往后置发动机。')
part('Water radiator and fan')
grid(lambda x,t:(x,.30+.30*t,1.84-.36*t),seq(-.36,.36,8),[0,1],'Steel')
for k in range(14):path([(-.35,.31+k*.021,1.835-k*.0252),(.35,.31+k*.021,1.835-k*.0252)],.003,'Black',4)
cyl((0,.46,1.62),(0,.46,1.57),.15,'Black',28)
part('Coolant lines')
for s in (-1,1):pipe([(s*.30,.40,1.70),(s*.20,.24,1.00),(s*.20,.24,-.60),(s*.14,.62,CZ[0]-.10)],.016,'Silicone',10)
