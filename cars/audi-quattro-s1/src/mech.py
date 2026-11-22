# Powertrain, quattro drivetrain, suspension and cooling of the S1 E2.
# The 2,110 cc (79.3 x 85.4 mm) twenty-valve inline-five sits longitudinally ahead of the front
# axle with the turbocharger on the right; the gearbox follows it with the front differential in
# its nose, a centre differential at its tail, a propshaft and a rear differential. Internal
# dimensions are reconstructions from public descriptions.
mat('Spring enamel','C3262B',.25,.30)
mat('Damper','2B3034',.55,.36)
mat('Cast alloy','B7B9B4',.55,.42)

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
component('Oil sump','油底壳','缸体与润滑',(0,-.22,0));motion(role='shell')
shell((0,CY-.045,(CZ[0]+CZ[4])/2),(0,0,1),[(-.26,.0),(-.26,.115),(.26,.115),(.26,.0)],'Cast alloy',4)
box((0,CY-.105,(CZ[0]+CZ[4])/2),(.21,.12,.52),'Cast alloy')
for k in range(9):box((0,CY-.168,CZ[0]-.02+.06*k),(.20,.008,.010),'Cast alloy')
component('Crankshaft','曲轴','曲柄连杆机构',(.32,-.10,0));motion(role='crank')
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
    component('Connecting rod '+str(no+1),str(no+1)+' 号连杆','曲柄连杆机构',(.20+.03*no,.06,0));motion(role='rod',i=no)
    cyl(p,top,.010,'Steel',10);sleeve(p,(0,0,1),.031,.024,.020,'Steel',20);sleeve(top,(0,0,1),.016,.011,.018,'Steel',16)
    component('Piston '+str(no+1),str(no+1)+' 号活塞','曲柄连杆机构',(.0,.26,0));motion(role='piston',i=no)
    shell((0,top[1]-.030,CZ[no]),(0,1,0),[(0,BORE/2-.001),(.060,BORE/2-.001),(.064,BORE/2-.004),(.064,0)],'Alloy',28)
    for k in range(3):tor((0,top[1]+.018+k*.0075,CZ[no]),(0,1,0),BORE/2-.0005,.0012,'Steel',28,4)
component('Head gasket','气缸垫','缸盖与配气',(0,.16,0));motion(role='shell')
box((0,DECK+.0015,(CZ[0]+CZ[4])/2),(.205,.003,.50),'Copper')
HEAD=DECK+.003
component('20-valve cylinder head','二十气门铝合金缸盖','缸盖与配气',(0,.34,0));motion(role='shell')
box((0,HEAD+.055,(CZ[0]+CZ[4])/2),(.22,.11,.50),'Cast alloy')
for s in (-1,1):
    for z in CZ:box((s*.115,HEAD+.040,z),(.02,.05,.050),'Cast alloy')
FIRE=[0,144,576,288,432]      # firing angle of cylinders 1-5 in degrees (order 1-2-4-5-3)
for s_,side_en,side_zh in ((-1,'Exhaust','排气'),(1,'Intake','进气')):
    component(side_en+' camshaft',side_zh+'凸轮轴','缸盖与配气',(s_*.10,.50,0));motion(role='cam',side=s_,intake=side_en=='Intake',x=s_*.045,y=HEAD+.130)
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
        component('%s valves %d'%(side_en,i+1),'%d 号缸%s气门'%(i+1,side_zh),'缸盖与配气',(s_*.06,.40+.02*i,0));motion(role='valve',i=i,side=s_,intake=side_en=='Intake')
        for dz in (-.017,.017):
            b=(s_*.026,HEAD+.008,z+dz);t=(s_*.045,HEAD+.110,z+dz)
            cyl(b,t,.0032,'Steel',6);cyl(b,add(b,(0,.003,0)),.014,'Steel',14)
            spring(add(t,(0,-.040,0)),add(t,(0,-.008,0)),.010,.0016,'Steel')
component('Cam cover','凸轮轴罩盖','缸盖与配气',(0,.62,0));motion(role='shell')
shell((0,HEAD+.165,(CZ[0]+CZ[4])/2),(0,0,1),[(-.265,0),(-.265,.085),(.265,.085),(.265,0)],'Crinkle',6)
box((0,HEAD+.150,(CZ[0]+CZ[4])/2),(.23,.06,.53),'Crinkle')
for k in range(6):box((0,HEAD+.183,CZ[0]-.03+.095*k),(.17,.006,.012),'Crinkle')
box((0,HEAD+.186,(CZ[0]+CZ[4])/2),(.11,.004,.26),'Red')
component('Spark plugs and coil packs','火花塞与点火线圈','点火与正时',(0,.70,0))
for z in CZ:
    cyl((0,HEAD+.04,z),(0,HEAD+.20,z),.008,'Silver',8);box((0,HEAD+.205,z),(.03,.03,.05),'Black')
component('Toothed timing belt drive','正时皮带与皮带轮','点火与正时',(0,.10,.32))
FZB=CZ[4]+.090
motion(role='shell')
pul=[((0,CY,FZB),.072),((.07,CY+.18,FZB),.030)]
for (c,r) in pul:cyl(add(c,(0,0,-.012)),add(c,(0,0,.012)),r,'Gunmetal',36);cyl(add(c,(0,0,.012)),add(c,(0,0,.016)),r*.35,'Steel',16)
belt=[(0,CY-.075,FZB),(.075,CY,FZB),(.10,CY+.18,FZB),(.10,HEAD+.13,FZB),(.045,HEAD+.19,FZB),(-.045,HEAD+.19,FZB),(-.104,HEAD+.13,FZB),(-.075,CY,FZB),(0,CY-.075,FZB)]
path(belt,.006,'Black',6)
box((0,HEAD-.02,FZB+.028),(.24,.38,.006),'Black')
component('Vibration damper and crank pulley','曲轴减振皮带轮','点火与正时',(0,-.05,.40));motion(role='crank')
cyl((0,CY,FZB+.035),(0,CY,FZB+.060),.085,'Black',36);cyl((0,CY,FZB+.060),(0,CY,FZB+.064),.030,'Steel',16)
component('Intake plenum and runners','进气稳压腔与进气歧管','进气与燃油',(.36,.20,0))
IX=.30
cyl((IX,HEAD+.10,CZ[0]-.07),(IX,HEAD+.10,CZ[4]+.08),.062,'Cast alloy',24)
for z in CZ:pipe([(.11,HEAD+.05,z),(.19,HEAD+.06,z),(.25,HEAD+.085,z),(IX,HEAD+.10,z)],.019,'Cast alloy',12)
cyl((IX,HEAD+.10,CZ[4]+.08),(IX,HEAD+.10,CZ[4]+.14),.040,'Steel',20)
component('Fuel rail and injectors','燃油导轨与喷油器','进气与燃油',(.30,.38,0))
cyl((.17,HEAD+.12,CZ[0]-.03),(.17,HEAD+.12,CZ[4]+.04),.009,'Steel',10)
for z in CZ:cyl((.17,HEAD+.12,z),(.15,HEAD+.07,z),.007,'Black',8)
component('Exhaust manifold','排气歧管','涡轮增压与排气',(-.36,.08,0))
for i,z in enumerate(CZ):
    pipe([(-.11,HEAD+.03,z),(-.18,HEAD+.00,z),(-.23,CY+.14,mix((0,0,z),(0,0,1.48),.5)[2]),(-.26,CY+.12,1.48)],.020,'Heat',12)
component('KKK turbocharger','KKK 涡轮增压器','涡轮增压与排气',(-.50,.18,.05))
TC=(-.30,CY+.10,1.46)
shell(add(TC,(0,0,-.03)),(0,0,1),[(0,.0),(0,.088),(.07,.092),(.075,.0)],'Heat',32)
shell(add(TC,(0,0,.06)),(0,0,1),[(0,.0),(0,.075),(.07,.080),(.08,.0)],'Cast alloy',32)
cyl(add(TC,(0,0,.14)),add(TC,(0,0,.22)),.040,'Cast alloy',20)
cyl(add(TC,(0,.075,.02)),add(TC,(0,.15,.02)),.022,'Cast alloy',14)
component('Wastegate and blow-off valve','废气泄压阀与泄压阀','涡轮增压与排气',(-.55,.30,-.05))
cyl(add(TC,(-.06,.06,-.05)),add(TC,(-.10,.13,-.05)),.030,'Heat',16);cyl(add(TC,(-.10,.13,-.05)),add(TC,(-.10,.16,-.05)),.040,'Gunmetal',16)
component('Intercooler and boost pipes','中冷器与增压管路','涡轮增压与排气',(0,.06,.55))
box((0,.50,1.815),(.64,.17,.06),'Steel')
for k in range(16):box((-.30+k*.04,.50,1.848),(.004,.16,.004),'Black')
pipe([add(TC,(0,0,.22)),(-.30,.47,1.70),(-.26,.50,1.79)],.034,'Silicone',14)
pipe([(.26,.50,1.79),(.30,.62,1.72),(IX,HEAD+.10,CZ[4]+.14)],.034,'Silicone',14)
component('Alternator and water pump','发电机与水泵','附件',(.40,-.05,.20))
cyl((.17,CY+.07,CZ[4]-.02),(.17,CY+.07,CZ[4]+.10),.060,'Cast alloy',24)
cyl((0,CY+.15,FZB-.05),(0,CY+.15,FZB-.005),.045,'Cast alloy',20)
component('Oil filter','机油滤清器','缸体与润滑',(.30,-.10,-.05))
cyl((.12,CY+.02,CZ[1]),(.20,CY+.02,CZ[1]),.040,'Black',20)
component('Turbo downpipe','涡轮下排气管','涡轮增压与排气',(-.25,-.20,0))
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
component('Two-piece propeller shaft','两段式传动轴','传动轴与半轴',(0,-.28,0));motion(role='prop',y=.30)
cyl((0,GY-.04,.48),(0,.30,-.25),.026,'Steel',14);cyl((0,.30,-.25),(0,.31,-.95),.026,'Steel',14)
for z in (.48,-.25,-.95):cyl((0,GY-.04 if z>0 else .30,z-.02),(0,GY-.04 if z>0 else .30,z+.02),.040,'Gunmetal',16)
component('Rear differential','后差速器','中央与后差速器',(0,-.20,-.20));motion(role='diff',zone='rear',y=.31,z=RZ)
shell((0,.31,RZ+.10),(0,0,1),[(-.02,.0),(-.02,.07),(.09,.07),(.13,.04),(.13,0)],'Cast alloy',28)
cyl((-.12,.31,RZ),(.12,.31,RZ),.105,'Cast alloy',32)
gear((.05,.31,RZ),(1,0,0),.090,.04,.020,41,'Steel')
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
