# Steel monocoque, cockpit and wheels of the S1 E2.

# ── Monocoque ─────────────────────────────────────────────────────────────────────────────
group('chassis','Steel monocoque','钢制承载式车身',(0,0,0),'缩短 320 mm 的 quattro 钢制车身：地板、门槛、防火墙、中央通道、前后轮罩与后备厢散热舱。')
part('Floor pan, sills and tunnel')
box((0,.205,-.20),(1.50,.012,1.80),'Charcoal')
for s in (-1,1):
    box((s*.775,.245,-.03),(.11,.10,1.24),'Charcoal')       # sill box section
    box((s*.79,.33,-.03),(.01,.07,1.10),'Gunmetal')
box((0,.30,.05),(.30,.19,1.40),'Charcoal')                 # transmission tunnel
part('Firewall and scuttle')
box((0,.52,.70),(1.56,.62,.012),'Ivory')
box((0,.86,.66),(1.40,.05,.10),'Ivory')
part('Front and rear inner wheel arches')
for s in (-1,1):
    for zc in (FZ,RZ):
        pts=[(TR+.345*sin(pi*k/16),zc-.345*cos(pi*k/16)) for k in range(17)]
        for (y0,z0),(y1,z1) in zip(pts,pts[1:]):
            face([(s*.60,y0,z0),(s*.60,y1,z1),(s*.90,y1,z1),(s*.90,y0,z0)],'Ivory' if zc>0 else 'Charcoal')
part('Front strut towers and brace')
for s in (-1,1):
    st=(s*.5625,.86,1.072)
    cyl(add(st,(0,-.10,0)),add(st,(0,.004,0)),.085,'Ivory',28);cyl(add(st,(0,.004,0)),add(st,(0,.012,0)),.040,'Gunmetal',16)
    for a in range(3):bolt(add(st,(.060*cos(a*2.1),.012,.060*sin(a*2.1))),(0,1,0),.007,'Steel')
    path([add(st,(0,.026,0)),(s*.25,.875,.735)],.016,'Polished',14)
    plate([(s*.25-.04,.86,.725),(s*.25+.04,.86,.725),(s*.25+.04,.89,.725),(s*.25-.04,.89,.725)],'Gunmetal',(0,0,-.010))
path([(-.5625,.886,1.072),(.5625,.886,1.072)],.016,'Polished',14)
part('Brake and clutch fluid reservoirs')
for x in (-.08,0,.08):
    cyl((x,.770,.775),(x,.835,.775),.026,'Lens',20);cyl((x,.835,.775),(x,.850,.775),.020,'Red',16)
box((0,.765,.775),(.22,.012,.06),'Gunmetal')
part('Cabin air intake grille')
box((-.46,.80,.770),(.20,.11,.10),'Mesh');path([(-.56,.855,.72),(-.36,.855,.72),(-.36,.855,.82),(-.56,.855,.82),(-.56,.855,.72)],.005,'Silver',6)
part('Front subframe rails')
for s in (-1,1):
    box((s*.42,.30,1.35),(.07,.09,1.20),'Charcoal')
    box((s*.42,.46,1.30),(.05,.05,1.10),'Gunmetal')
box((0,.27,1.86),(.95,.07,.06),'Charcoal')
part('Rear floor and cooler bay')
box((0,.30,-1.52),(1.40,.012,.74),'Charcoal')
for s in (-1,1):box((s*.45,.27,-1.45),(.06,.08,.95),'Charcoal')

# ── Cockpit ───────────────────────────────────────────────────────────────────────────────
group('cockpit','Cockpit and roll cage','驾驶舱与防滚架',(0,1.0,-.4),'左舵驾驶舱：仪表台、Recaro 赛车座椅、四点安全带、方向盘、踏板和焊接防滚架。')
part('Dashboard and instruments')
box((0,.700,.560),(1.44,.130,.260),'Black')
box((0,.780,.470),(1.40,.030,.140),'Seat')
box((.37,.735,.425),(.36,.140,.040),'Black')
for k,x in enumerate([.27,.37,.47]):
    cyl((x,.745,.402),(x,.745,.398),.045 if k==1 else .036,'Charcoal',28)
    cyl((x,.745,.397),(x,.745,.396),.040 if k==1 else .031,'Lens',28)
box((-.20,.66,.43),(.32,.10,.04),'Charcoal')
part('Steering wheel')
hub=(.37,.700,.300);axis=unit((0,.32,-1))
tor(hub,axis,.170,.016,'Black',40,10)
for a in (0,2.1,4.2):cyl(hub,add(hub,mul(add(mul(basis(axis)[0],cos(a)),mul(basis(axis)[1],sin(a))),.165)),.010,'Gunmetal',8)
cyl(hub,add(hub,mul(axis,-.36)),.020,'Gunmetal',10)
cyl(hub,add(hub,mul(axis,.02)),.035,'Black',20)
part('Pedals and gear lever')
for k,x in enumerate([.27,.35,.44]):
    path([(x,.48,.70),(x,.34,.60)],.008,'Steel');box((x,.33,.59),(.06,.08,.012),'Steel')
path([(.05,.36,.10),(.05,.60,.05)],.008,'Steel');cyl((.05,.60,.05),(.05,.64,.05),.022,'Black',12)
box((.05,.35,.10),(.10,.03,.14),'Black')
for s in (-1,1):
    part('Recaro bucket seat '+('L' if s>0 else 'R'))
    x=s*.36
    box((x,.30,-.02),(.44,.07,.46),'Seat')
    box((x,.62,-.24),(.46,.62,.07),'Seat')
    for k in (-1,1):box((x+k*.22,.47,-.10),(.05,.30,.36),'Seat')
    box((x,.90,-.24),(.24,.12,.08),'Seat')
    for k in (-1,1):path([(x+k*.08,.96,-.28),(x+k*.07,.56,-.02)],.018,'Belt',6)
    path([(x-.18,.38,.08),(x+.18,.38,.08)],.018,'Belt',6)
part('Welded roll cage')
cage=dict(r=.019,m='Pearl')
def tube(a,b):cyl(a,b,cage['r'],cage['m'],10)
for s in (-1,1):
    hoop=[(s*.72,.23,-.48),(s*.68,1.10,-.50),(s*.52,1.25,-.52)]
    path(hoop,cage['r'],cage['m'],10)
    tube((s*.52,1.25,-.52),(s*.52,1.25,.10))
    tube((s*.52,1.25,.10),(s*.70,.92,.60));tube((s*.70,.92,.60),(s*.72,.23,.60))
    tube((s*.70,.30,.55),(s*.72,.60,-.45))            # door bar
    tube((s*.66,1.10,-.50),(s*.60,.40,-1.30))          # rear stay
tube((-.52,1.25,-.52),(.52,1.25,-.52));tube((-.52,1.25,.10),(.52,1.25,.10))
tube((-.70,.30,-.48),(.52,1.25,-.52))
tube((-.52,1.25,-.52),(.52,1.25,.10))
part('Fire extinguisher and battery box')
cyl((-.20,.26,-.45),(.20,.26,-.45),.055,'Red',20)
box((-.45,.30,-1.30),(.24,.18,.17),'Black')

# ── Wheels ────────────────────────────────────────────────────────────────────────────────
def build_wheel(key,zc,xc,w,s):
    group(key,('Front ' if zc>0 else 'Rear ')+('left' if s>0 else 'right')+' wheel',('前' if zc>0 else '后')+('左' if s>0 else '右')+'车轮',(s*.55,0,0),'白色五辐条锻造轮圈与 Michelin 拉力胎。')
    part('Tyre')
    R,r=TR,.205;inner,outer=xc-w/2,xc+w/2
    prof=[(-w/2,r+.012),(-w/2+.010,R-.030),(-w/2+.030,R-.004),(0,R),(w/2-.030,R-.004),(w/2-.010,R-.030),(w/2,r+.012)]
    shell((xc*s,TR,zc),(s,0,0),prof,'Rubber',60)
    for k in range(32):
        a=2*pi*k/32;n=(0,cos(a),sin(a))
        p=(s*xc,TR+(R+.002)*cos(a),zc+(R+.002)*sin(a))
        u=(0,-sin(a),cos(a))
        face([add(add(p,mul(u,-.012)),(-w*.42,0,0)),add(add(p,mul(u,.012)),(-w*.42,0,0)),add(add(p,mul(u,.012)),(w*.42,0,0)),add(add(p,mul(u,-.012)),(w*.42,0,0))],'Tread')
    part('Five-spoke wheel')
    face_x=s*(outer-.020)
    shell((s*xc,TR,zc),(s,0,0),[(-w/2+.012,.192),(w/2-.016,.192),(w/2-.016,.198),(-w/2+.012,.198),(-w/2+.012,.192)],'Wheel',56)
    tor((face_x,TR,zc),(1,0,0),.192,.010,'Wheel',56,8)
    cyl((face_x-s*.040,TR,zc),(face_x-s*.008,TR,zc),.062,'Wheel',32)
    for j in range(5):
        a=2*pi*j/5+.31
        q=[(face_x-s*.004,TR+.058*cos(a+d),zc+.058*sin(a+d)) for d in (-.36,.36)]+[(face_x-s*.010,TR+.188*cos(a+d),zc+.188*sin(a+d)) for d in (.13,-.13)]
        plate(q,'Wheel',(-s*.026,0,0))
    for j in range(5):
        a=2*pi*j/5;cyl((face_x,TR+.040*cos(a),zc+.040*sin(a)),(face_x+s*.010,TR+.040*cos(a),zc+.040*sin(a)),.009,'Steel',6)
    cyl((face_x,TR,zc),(face_x+s*.012,TR,zc),.026,'Gunmetal',16)
for key,zc,xc,w,s in [('frontL',FZ,FX,.235,1),('frontR',FZ,FX,.235,-1),('rearL',RZ,RX,.245,1),('rearR',RZ,RX,.245,-1)]:
    build_wheel(key,zc,xc,w,s)
    for n in ('Tyre','Five-spoke wheel'):
        drive_extras[(key,n)]=dict(run=dict(role='frontWheel' if zc>0 else 'wheel',side=s,zone='front' if zc>0 else 'rear',pivot=[s*xc,TR,zc],axis=[1,0,0]))
drive_extras[('cockpit','Steering wheel')]=dict(run=dict(role='handwheel',pivot=list(hub),axis=list(axis)))
