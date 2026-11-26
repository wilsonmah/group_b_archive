# Steel monocoque with roll cage and subframes, cockpit and wheels of the 959 Paris-Dakar car.

# ── Chassis ───────────────────────────────────────────────────────────────────────────────
group('chassis','Steel monocoque, cage and subframes','钢制车身骨架与防滚架',(0,0,0),'钢制整体式车身底盘，加装焊接防滚架；前副车架承载转向与前悬挂，后部发动机支架承载平置六缸。')
def tube(a,b,r=.016):cyl(a,b,r,'Frame',10)
mat('Frame','2A2E33',.45,.40)
part('Floorpan, sills and tunnel')
for s in (-1,1):
    tube((s*.74,.24,.72),(s*.74,.24,-.62),.022);tube((s*.34,.22,.80),(s*.34,.22,-.66),.018)
    tube((s*.74,.24,.72),(s*.34,.22,.80));tube((s*.74,.24,-.62),(s*.34,.22,-.66))
box((0,.205,.08),(1.46,.012,1.40),'Charcoal')
box((0,.31,.08),(.26,.18,1.40),'Charcoal')                      # propshaft tunnel
for s in (-1,1):box((s*.74,.35,.08),(.020,.22,1.36),'Charcoal')    # sill sides
part('Roll cage')
for s in (-1,1):
    # Main hoop, front hoop, roof rails, rear stays and door bars.
    tube((s*.74,.24,-.42),(s*.70,1.06,-.42));tube((s*.70,1.06,-.42),(s*.49,1.22,-.42))
    tube((s*.74,.24,.62),(s*.68,.86,.62));tube((s*.68,.86,.62),(s*.49,1.22,.12))
    tube((s*.49,1.22,.12),(s*.49,1.22,-.42))
    tube((s*.70,1.06,-.42),(s*.46,1.12,-.96));tube((s*.46,1.12,-.96),(s*.46,.62,-1.10))
    tube((s*.74,.28,.58),(s*.74,.66,-.38));tube((s*.74,.66,.58),(s*.74,.30,-.38))
tube((-.49,1.22,-.42),(.49,1.22,-.42));tube((-.49,1.22,.12),(.49,1.22,.12))
tube((-.70,1.06,-.42),(.74,.24,-.42));tube((.70,1.06,-.42),(-.74,.24,-.42))
tube((-.46,1.12,-.96),(.46,1.12,-.96))
part('Front subframe')
for s in (-1,1):
    tube((s*.34,.24,.80),(s*.34,.26,2.00));tube((s*.34,.52,.90),(s*.34,.48,1.98))
    tube((s*.68,.86,.62),(s*.34,.52,.90));tube((s*.34,.26,2.00),(s*.34,.48,1.98))
    tube((s*.34,.26,1.40),(s*.58,.54,1.18));tube((s*.58,.54,1.18),(s*.34,.52,.90))
tube((-.34,.26,2.00),(.34,.26,2.00));tube((-.34,.48,1.98),(.34,.48,1.98));tube((-.58,.54,1.18),(.58,.54,1.18))
part('Rear engine cradle')
for s in (-1,1):
    tube((s*.74,.24,-.62),(s*.42,.28,-.84));tube((s*.42,.28,-.84),(s*.42,.30,-1.95))
    tube((s*.46,1.12,-.96),(s*.42,.94,-1.40));tube((s*.42,.94,-1.40),(s*.40,.62,-1.95))
    tube((s*.42,.30,-1.95),(s*.40,.62,-1.95));tube((s*.42,.30,-1.30),(s*.42,.94,-1.40))
    tube((s*.42,.28,-.84),(s*.60,.78,-1.10))
tube((-.42,.30,-1.95),(.42,.30,-1.95));tube((-.40,.62,-1.95),(.40,.62,-1.95));tube((-.42,.94,-1.40),(.42,.94,-1.40))
# Firewall between the cabin and the engine bay, with the gearbox tunnel left open.
for s in (-1,1):box((s*.46,.66,-.66),(.54,.84,.012),'Charcoal')
box((0,.98,-.66),(.34,.26,.012),'Charcoal')
part('Safety fuel cell')
box((0,.30,1.55),(.80,.14,.50),'Black')

# ── Cockpit ───────────────────────────────────────────────────────────────────────────────
group('cockpit','Cockpit','驾驶舱',(0,1.0,-.25),'左舵驾驶舱：仪表台、赛车座椅、安全带、方向盘、踏板、换挡杆与领航台。')
mat('Brushed','B8BCBE',.75,.38);mat('Dash','1B1D20',0,.82);mat('Kevlar floor','5A5A3C',.2,.7);mat('Foil','C9CDD0',.9,.25)
part('Dashboard and instruments')
# Black dash with a binnacle of five round gauges, as in the 911-based 959.
box((0,.760,.560),(1.40,.100,.280),'Dash')
grid(lambda x,t:(x,.810+.030*t,.440+.200*t),seq(-.68,.68,14),[0,1],'Dash')
box((.36,.830,.470),(.50,.110,.140),'Dash')                      # instrument binnacle over the wheel
for k,x in enumerate((.20,.28,.36,.44,.52)):
    r=.040 if k==2 else .032
    cyl((x,.800,.395),(x,.800,.390),r+.005,'Charcoal',28);cyl((x,.800,.390),(x,.800,.388),r,'Lens',28)
box((-.15,.690,.425),(.70,.100,.030),'Charcoal')                  # centre console with switches
for k in range(8):box((-.45+k*.06,.700,.408),(.030,.020,.006),'Red' if k%3==0 else 'Black')
# Rally additions: co-driver's trip computer and a map light on the right side.
box((-.45,.860,.470),(.30,.130,.090),'Black');box((-.45,.860,.424),(.26,.090,.004),'Amber')
cyl((-.04,.690,.410),(-.04,.690,.388),.010,'Red',10)
part('Floor and tunnel covers')
box((0,.212,.10),(1.36,.006,1.10),'Kevlar floor')
box((0,.335,.05),(.26,.160,.90),'Foil')
part('Steering wheel')
hub=(.36,.700,.200);axis=unit((0,.30,-1))
tor(hub,axis,.185,.017,'Black',40,10)
top_=unit(sub((0,1,0),mul(axis,dot((0,1,0),axis))));box(add(hub,mul(top_,.185)),(.022,.022,.022),'Gold')
for a in (0,2.1,4.2):cyl(hub,add(hub,mul(add(mul(basis(axis)[0],cos(a)),mul(basis(axis)[1],sin(a))),.178)),.010,'Gunmetal',8)
cyl(hub,add(hub,mul(axis,-.36)),.020,'Gunmetal',10);cyl(hub,add(hub,mul(axis,.02)),.038,'Black',20)
part('Pedals and gear lever')
for x in (.27,.35,.43):
    path([(x,.50,.58),(x,.35,.50)],.008,'Steel');box((x,.34,.49),(.06,.08,.012),'Brushed')
path([(.10,.36,.04),(.10,.58,-.02)],.008,'Steel');shell((.10,.36,.04),unit((0,.58,-.20)),[(0,.040),(.10,.012),(.11,0)],'Foil',14)
shell((.10,.58,-.02),(0,1,0),[(-.025,0),(-.025,.012),(0,.024),(.025,.012),(.03,0)],'Black',16)
for s in (-1,1):
    part('Bucket seat '+('L' if s>0 else 'R'))
    x=s*.36
    box((x,.40,-.14),(.46,.07,.48),'Seat');box((x,.70,-.37),(.48,.60,.07),'Seat')
    for k in (-1,1):box((x+k*.23,.56,-.20),(.06,.30,.36),'Seat')
    for k in (-1,1):path([(x+k*.09,.98,-.41),(x+k*.07,.64,-.14)],.018,'Belt',6)
    path([(x-.19,.46,-.04),(x+.19,.46,-.04)],.018,'Belt',6)

# ── Wheels: white hollow-spoke wheels on Michelin rally tyres ────────────────────────────────
def build_wheel(key,zc,xc,w,s):
    group(key,('Front ' if zc>0 else 'Rear ')+('left' if s>0 else 'right')+' wheel',('前' if zc>0 else '后')+('左' if s>0 else '右')+'车轮',(s*.55,0,0),'白色空心辐条轮圈与拉力赛胎。')
    part('Tyre')
    R,r=TR,.215
    prof=[(-w/2,r+.012),(-w/2+.010,R-.030),(-w/2+.030,R-.004),(0,R),(w/2-.030,R-.004),(w/2-.010,R-.030),(w/2,r+.012)]
    shell((s*xc,TR,zc),(s,0,0),prof,'Rubber',60)
    for k in range(40):
        a=2*pi*k/40;p=(s*xc,TR+(R+.002)*cos(a),zc+(R+.002)*sin(a));u=(0,-sin(a),cos(a))
        face([add(add(p,mul(u,-.013)),(-w*.42,0,0)),add(add(p,mul(u,.013)),(-w*.42,0,0)),add(add(p,mul(u,.013)),(w*.42,0,0)),add(add(p,mul(u,-.013)),(w*.42,0,0))],'Tread')
    part('Hollow-spoke wheel')
    fx=s*(xc+w/2-.026);rr=.205
    shell((s*xc,TR,zc),(s,0,0),[(-w/2+.012,rr-.006),(w/2-.016,rr-.006),(w/2-.016,rr),(-w/2+.012,rr),(-w/2+.012,rr-.006)],'Wheel',56)
    tor((fx,TR,zc),(1,0,0),rr-.004,.011,'Wheel',56,8)
    cyl((fx-s*.050,TR,zc),(fx,TR,zc),.060,'Wheel',32)
    for k in range(10):
        a=2*pi*k/10+.15
        p0=(fx,TR+.050*cos(a),zc+.050*sin(a));p1=(fx,TR+(rr-.012)*cos(a+.10),zc+(rr-.012)*sin(a+.10))
        path([p0,mix(p0,p1,.5),p1],.011,'Wheel',8)
        cyl(add(mix(p0,p1,.5),(s*-.004,0,0)),add(mix(p0,p1,.5),(s*.004,0,0)),.016,'Wheel',10)
    cyl((fx,TR,zc),(fx+s*.012,TR,zc),.042,'Gunmetal',20);cyl((fx+s*.012,TR,zc),(fx+s*.020,TR,zc),.024,'Gold',16)
for key,zc,xc,w,s in [('frontL',FZ,FX,.235,1),('frontR',FZ,FX,.235,-1),('rearL',RZ,RX,.255,1),('rearR',RZ,RX,.255,-1)]:
    build_wheel(key,zc,xc,w,s)
    for n in ('Tyre','Hollow-spoke wheel'):
        drive_extras[(key,n)]=dict(run=dict(role='frontWheel' if zc>0 else 'wheel',side=s,zone='front' if zc>0 else 'rear',pivot=[s*xc,TR,zc],axis=[1,0,0]))
drive_extras[('cockpit','Steering wheel')]=dict(run=dict(role='handwheel',pivot=list(hub),axis=list(axis)))
