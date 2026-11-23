# Steel tubular spaceframe, cockpit and wheels of the Delta S4.

# ── Spaceframe ────────────────────────────────────────────────────────────────────────────
group('chassis','Steel tubular spaceframe','钢管空间车架',(0,0,0),'铬钼钢管空间车架与一体式防滚架：前后副车架、中央驾驶舱、发动机舱框架、油箱与地板。')
def tube(a,b,r=.016):cyl(a,b,r,'Frame',10)
mat('Frame','2A2E33',.45,.40)
part('Central cell and roll cage')
# Floor-level longerons, sill tubes and the cage hoops.
for s in (-1,1):
    tube((s*.72,.26,.72),(s*.72,.26,-.48));tube((s*.30,.22,.75),(s*.30,.22,-.50))
    tube((s*.72,.26,.72),(s*.30,.22,.75));tube((s*.72,.26,-.48),(s*.30,.22,-.50))
    # Main hoop and front hoop legs, roof rails.
    tube((s*.72,.26,-.46),(s*.70,1.10,-.46));tube((s*.70,1.10,-.46),(s*.48,1.24,-.46))
    tube((s*.72,.26,.68),(s*.66,.90,.70));tube((s*.66,.90,.70),(s*.48,1.22,.22))
    tube((s*.48,1.22,.22),(s*.48,1.24,-.46))
    tube((s*.72,.30,.64),(s*.72,.62,-.40))          # door bar
    tube((s*.72,.62,.20),(s*.72,.30,-.40))          # door bar cross
tube((-.48,1.24,-.46),(.48,1.24,-.46));tube((-.48,1.22,.22),(.48,1.22,.22));tube((-.48,1.24,-.46),(.48,1.22,.22))
tube((-.70,1.10,-.46),(.72,.26,-.46))
box((0,.205,.12),(1.40,.012,1.20),'Charcoal')
box((0,.30,.12),(.24,.16,1.20),'Charcoal')                  # transmission tunnel
part('Front subframe')
for s in (-1,1):
    tube((s*.30,.22,.75),(s*.30,.24,1.95));tube((s*.30,.55,.90),(s*.30,.50,1.90))
    tube((s*.66,.90,.70),(s*.30,.55,.90));tube((s*.30,.24,1.95),(s*.30,.50,1.90))
    tube((s*.30,.24,1.40),(s*.30,.55,1.25));tube((s*.30,.55,1.25),(s*.56,.82,1.12))   # strut tower
    tube((s*.72,.26,.72),(s*.30,.24,1.10))
tube((-.30,.24,1.95),(.30,.24,1.95));tube((-.30,.50,1.90),(.30,.50,1.90));tube((-.56,.82,1.12),(.56,.82,1.12))
part('Rear subframe and engine bay frame')
for s in (-1,1):
    tube((s*.72,.26,-.48),(s*.36,.28,-.60));tube((s*.36,.28,-.60),(s*.36,.30,-1.90))
    tube((s*.70,1.10,-.46),(s*.40,1.02,-1.30));tube((s*.40,1.02,-1.30),(s*.38,.62,-1.90))
    tube((s*.36,.30,-1.90),(s*.38,.62,-1.90));tube((s*.36,.30,-1.20),(s*.40,1.02,-1.30))
    tube((s*.36,.30,-.80),(s*.58,.86,-1.10));tube((s*.58,.86,-1.10),(s*.40,1.02,-1.30))  # damper tower
    tube((s*.36,.30,-1.45),(s*.58,.86,-1.10))
tube((-.36,.30,-1.90),(.36,.30,-1.90));tube((-.38,.62,-1.90),(.38,.62,-1.90));tube((-.40,1.02,-1.30),(.40,1.02,-1.30))
# Cabin bulkhead, split around the gearbox that runs back between the seats.
for s in (-1,1):box((s*.43,.70,-.70),(.54,.84,.012),'Charcoal')
box((0,.97,-.70),(.32,.30,.012),'Charcoal')
part('Safety fuel cells under the seats')
for s in (-1,1):box((s*.45,.30,-.18),(.42,.16,.50),'Black')

# ── Cockpit ───────────────────────────────────────────────────────────────────────────────
group('cockpit','Cockpit','驾驶舱',(0,1.0,-.25),'左舵驾驶舱：仪表台、赛车座椅、安全带、方向盘、踏板与换挡杆。')
part('Dashboard and instruments')
mat('Brushed','B8BCBE',.75,.38);mat('Felt','1E2C58',0,.95);mat('Kevlar floor','5A5A3C',.2,.7);mat('Foil','C9CDD0',.9,.25)
# Brushed-aluminium panel under a navy felt top pad, as in the preserved car.
box((0,.660,.555),(1.40,.200,.020),'Brushed')
grid(lambda x,t:(x,.765+.030*t,.560+.180*t),seq(-.70,.70,14),[0,1],'Felt')
box((0,.775,.640),(1.42,.020,.200),'Felt')
box((-.47,.530,.585),(.40,.140,.060),'Brushed')                    # co-driver electronics box
for k,(x,y) in enumerate([(.37,.700),(.28,.690),(.46,.690),(.58,.640),(.58,.590)]):
    r=.050 if k==0 else .030
    cyl((x,y,.546),(x,y,.540),r+.006,'Charcoal',28);cyl((x,y,.540),(x,y,.538),r,'Lens',28)
for k,(x,y,m) in enumerate([(.64,.700,'Red'),(.66,.700,'Red'),(.64,.680,'Red'),(.66,.680,'Red'),(.70,.700,'Black'),(.72,.700,'Black'),(.22,.640,'Amber'),(.50,.640,'Red')]):
    box((x,y,.543),(.016,.016,.006),m)
for k in range(12):box((-.20+(k%4)*.035,.700-(k//4)*.030,.543),(.020,.018,.006),'Black')
box((-.47,.700,.543),(.22,.050,.006),'Black');box((-.47,.700,.540),(.20,.035,.002),'Amber')
box((-.47,.620,.543),(.18,.040,.006),'Charcoal')
cyl((-.04,.700,.543),(-.04,.700,.520),.010,'Red',10)                # battery cut-off
part('Kevlar floor and foil-wrapped tunnel')
box((0,.212,.20),(1.30,.006,.90),'Kevlar floor')
box((0,.330,.10),(.26,.160,.80),'Foil')
part('Steering wheel')
hub=(.37,.700,.300);axis=unit((0,.32,-1))
tor(hub,axis,.170,.016,'Black',40,10)
top_=unit(sub((0,1,0),mul(axis,dot((0,1,0),axis))));box(add(hub,mul(top_,.170)),(.022,.022,.022),'Yellow')
for a in (0,2.1,4.2):cyl(hub,add(hub,mul(add(mul(basis(axis)[0],cos(a)),mul(basis(axis)[1],sin(a))),.165)),.010,'Gunmetal',8)
cyl(hub,add(hub,mul(axis,-.36)),.020,'Gunmetal',10);cyl(hub,add(hub,mul(axis,.02)),.035,'Black',20)
part('Pedals and gear lever')
for x in (.27,.35,.44):
    path([(x,.48,.70),(x,.34,.60)],.008,'Steel');box((x,.33,.59),(.06,.08,.012),'Brushed')
    for k in range(3):cyl((x,.31+k*.022,.585),(x,.31+k*.022,.583),.008,'Black',8)
path([(.13,.40,.12),(.13,.66,.04)],.008,'Steel');shell((.13,.41,.11),unit((0,.97,-.23)),[(0,.040),(.10,.012),(.11,0)],'Foil',14)
shell((.13,.66,.04),(0,1,0),[(-.025,0),(-.025,.012),(0,.024),(.025,.012),(.03,0)],'Black',16)
for s in (-1,1):
    part('Bucket seat '+('L' if s>0 else 'R'))
    x=s*.36
    box((x,.42,-.06),(.44,.07,.44),'Seat');box((x,.72,-.27),(.46,.60,.07),'Seat')
    for k in (-1,1):box((x+k*.22,.58,-.14),(.05,.30,.34),'Seat')
    for k in (-1,1):path([(x+k*.08,1.00,-.31),(x+k*.07,.66,-.06)],.018,'Belt',6)
    path([(x-.18,.48,.04),(x+.18,.48,.04)],.018,'Belt',6)

# ── Wheels: white multi-hole Speedline wheels on Pirelli rally tyres ───────────────────────
def build_wheel(key,zc,xc,w,s):
    group(key,('Front ' if zc>0 else 'Rear ')+('left' if s>0 else 'right')+' wheel',('前' if zc>0 else '后')+('左' if s>0 else '右')+'车轮',(s*.55,0,0),'白色多孔 Speedline 轮圈与 Pirelli 拉力胎。')
    part('Tyre')
    R,r=TR,.205
    prof=[(-w/2,r+.012),(-w/2+.010,R-.030),(-w/2+.030,R-.004),(0,R),(w/2-.030,R-.004),(w/2-.010,R-.030),(w/2,r+.012)]
    shell((s*xc,TR,zc),(s,0,0),prof,'Rubber',60)
    for k in range(36):
        a=2*pi*k/36;p=(s*xc,TR+(R+.002)*cos(a),zc+(R+.002)*sin(a));u=(0,-sin(a),cos(a))
        face([add(add(p,mul(u,-.014)),(-w*.42,0,0)),add(add(p,mul(u,.014)),(-w*.42,0,0)),add(add(p,mul(u,.014)),(w*.42,0,0)),add(add(p,mul(u,-.014)),(w*.42,0,0))],'Tread')
    part('Multi-hole wheel')
    fx=s*(xc+w/2-.022)
    shell((s*xc,TR,zc),(s,0,0),[(-w/2+.012,.192),(w/2-.016,.192),(w/2-.016,.198),(-w/2+.012,.198),(-w/2+.012,.192)],'Wheel',56)
    tor((fx,TR,zc),(1,0,0),.192,.010,'Wheel',56,8)
    cyl((fx-s*.030,TR,zc),(fx,TR,zc),.186,'Wheel',56)
    for k in range(10):
        a=2*pi*k/10+.31;c=(fx+s*.001,TR+.128*cos(a),zc+.128*sin(a))
        cyl(c,add(c,(s*.002,0,0)),.030,'Black',18)
    for k in range(5):
        a=2*pi*k/5;cyl((fx,TR+.045*cos(a),zc+.045*sin(a)),(fx+s*.010,TR+.045*cos(a),zc+.045*sin(a)),.009,'Steel',6)
    cyl((fx,TR,zc),(fx+s*.014,TR,zc),.030,'Gunmetal',16)
for key,zc,xc,w,s in [('frontL',FZ,FX,.235,1),('frontR',FZ,FX,.235,-1),('rearL',RZ,RX,.255,1),('rearR',RZ,RX,.255,-1)]:
    build_wheel(key,zc,xc,w,s)
    for n in ('Tyre','Multi-hole wheel'):
        drive_extras[(key,n)]=dict(run=dict(role='frontWheel' if zc>0 else 'wheel',side=s,zone='front' if zc>0 else 'rear',pivot=[s*xc,TR,zc],axis=[1,0,0]))
drive_extras[('cockpit','Steering wheel')]=dict(run=dict(role='handwheel',pivot=list(hub),axis=list(axis)))
