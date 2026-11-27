# Porsche 959 Paris-Dakar coachwork, rebuilt as smooth lofted cross-sections in the 911 family
# shape. Metres; x to the car's left, y up, z forward, origin on the ground midway between the axles.
# Published figures: wheelbase 2.272 m, length 4.26 m, width 1.84 m; the Dakar cars stand about
# 0.08 m taller on long-travel suspension and tall tyres. Lines follow side, 3/4 and rear photos of
# the Rothmans 186 car (RM Sotheby's) and its sister cars.
FZ,RZ=1.136,-1.136          # axle stations
TR=.360                     # rolling radius (tall rally tyres)
FX,RX=.752,.775             # wheel-centre half tracks
RA=.425                     # wheel-arch radius
ZN,ZT=2.030,-2.230          # nose and tail faces
DZ0,DZ1=-.470,.640          # door shut lines (B-pillar and front edge of the door)
ZW=.660                     # windscreen base at the centreline
BELT=.955                   # window sill
def sm(t):t=clamp(t,0,1);return t*t*(3-2*t)
def arch_y(z,zc):
    d=abs(z-zc);return TR+sqrt(RA*RA-d*d) if d<RA else -1

# ── Section parameters along the car ─────────────────────────────────────────────────────
# ws: half-width at the shoulder; ys: shoulder height; (xc,yc): the crest where the side turns
# onto the top (front-wing crest, window sill, rear-hip crest); ycen: centreline height of the top
# (bonnet, unused deck under the cabin, engine lid).
WS=[(ZT,.770),(-2.12,.860),(-1.90,.912),(-1.40,.922),(-.90,.905),(-.50,.872),(.00,.866),(.62,.872),(.85,.892),(1.20,.890),(1.60,.868),(1.86,.820),(1.98,.760),(ZN,.715)]
YS=[(ZT,.560),(-1.90,.600),(-1.10,.610),(-.50,.590),(.60,.580),(1.30,.570),(1.80,.540),(ZN,.500)]
XCR=[(ZT,.560),(-2.10,.660),(-1.80,.720),(-1.30,.760),(-.95,.790),(-.50,.800),(.62,.800),(.80,.640),(1.20,.600),(1.70,.575),(1.92,.545),(ZN,.500)]
YCR=[(ZT,.860),(-2.10,.905),(-1.80,.935),(-1.30,.965),(-.95,.985),(-.50,.968),(.00,.958),(.62,.950),(.80,.932),(1.10,.910),(1.45,.875),(1.70,.835),(1.86,.790),(1.96,.730),(ZN,.660)]
YCEN=[(ZT,.880),(-2.06,.935),(-1.70,.975),(-1.18,1.040),(-1.00,1.06),(.62,1.06),(.80,.885),(1.10,.835),(1.45,.780),(1.75,.725),(1.92,.675),(ZN,.630)]
def P(tab,z):return sinterp(z,tab)
def body_floor(z):
    if z>1.70:return .250+.040*clamp((ZN-z)/.30,0,1)
    if z<-1.70:return .320
    return .305
def bottom(z):return max(body_floor(z),arch_y(z,FZ),arch_y(z,RZ))
NL,NU,NT=4,9,10            # samples: lower side, shoulder-to-crest, crest-to-centre
def section(z,top=True):
    """Half cross-section from the bottom edge to the centreline (x>=0)."""
    ws,ys,xc,yc,ycen=P(WS,z),P(YS,z),P(XCR,z),P(YCR,z),P(YCEN,z)
    yc=max(yc,ys+.02);xc=min(xc,ws-.01)
    b=bottom(z);pts=[]
    e=.62
    def upper(a):return (xc+(ws-xc)*cos(a)**e,ys+(yc-ys)*sin(a)**e)
    if b<ys:
        for k in range(NL):
            y=b+(ys-b)*k/NL;tuck=.030*clamp((b+.05-y)/.05,0,1)**2
            pts.append((ws-tuck,y))
        a0=0
    else:
        a0=math.asin(clamp((b-ys)/(yc-ys),0,.999)**(1/e))
        pts+= [upper(a0)]*NL
    for k in range(NU+1):pts.append(upper(a0+(pi/2-a0)*k/NU))
    if top:
        for k in range(1,NT+1):
            t=k/NT;pts.append((xc*(1-t),yc+(ycen-yc)*sm(t)))
    return pts
def side_x(z,y):
    """Outer skin x at height y (lower side and shoulder up to the crest)."""
    pts=section(z,False)
    if y<=pts[0][1]:return pts[0][0]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        if y0<=y<=y1 and y1>y0:return x0+(x1-x0)*(y-y0)/(y1-y0)
    return pts[-1][0]
def zstations(z0,z1,n,extra=()):
    zs=set(round(z,5) for z in seq(z0,z1,n))
    for zc in (FZ,RZ):
        for i in range(41):
            z=zc+RA*cos(pi*i/40)
            if z0<z<z1:zs.add(round(z,5))
    for z in extra:
        if z0<z<z1:zs.add(round(z,5))
    return sorted(zs)
def loft(z0,z1,n,top=True,mat='Ivory',sides=(-1,1),k1=None):
    zs=zstations(z0,z1,n)
    secs=[section(z,top) for z in zs]
    for s in sides:
        for (za,A),(zb,B) in zip(zip(zs,secs),zip(zs[1:],secs[1:])):
            m=len(A) if k1 is None else k1
            for k in range(m-1):
                q=[(s*A[k][0],A[k][1],za),(s*B[k][0],B[k][1],zb),(s*B[k+1][0],B[k+1][1],zb),(s*A[k+1][0],A[k+1][1],za)]
                if q[0]==q[3] and q[1]==q[2]:continue
                face(q if s<0 else q[::-1],mat)
def cap(z,dz,mat='Ivory'):
    """Close the loft at station z with a fan to the centre."""
    sec=section(z,True);c=(0,(sec[0][1]+sec[-1][1])/2,z+dz)
    for s in (-1,1):
        for a,b in zip(sec,sec[1:]):
            q=[c,(s*a[0],a[1],z),(s*b[0],b[1],z)]
            face(q if s*dz>0 else q[::-1],mat)

# ── Front body ──────────────────────────────────────────────────────────────────────────────
group('nose','Front body','前车身',(0,.40,.80),'前车身：前翼子板、大灯、低矮的前行李箱盖与前保险杠。')
part('Front wings and bonnet')
loft(DZ1,ZN,40)
cap(ZN,.0)
def bonnet(x,z):
    sec=section(z,True);xc=sec[NL+NU][0]
    if abs(x)>=xc:return (x,side_x(z,P(YCR,z)),z)
    t=1-abs(x)/xc;return (x,P(YCR,z)+(P(YCEN,z)-P(YCR,z))*sm(t),z)
def face_zf(y):return ZN
FY0=.300
for s in (-1,1):
    for z in (1.00,1.82):
        q=bonnet(s*.40,z);cyl(q,add(q,(0,.007,0)),.014,'Steel',14)
part('Headlamps')
# Round headlamps set into the wing fronts, tilted up with the wing line (911 family).
HLZ=1.935
for s in (-1,1):
    c=(s*.560,.715,HLZ+.030);n=unit((s*.06,.30,1))
    cyl(add(c,mul(n,-.110)),add(c,mul(n,.004)),.104,'Ivory',40)
    tor(add(c,mul(n,.004)),n,.094,.008,'Charcoal',44,8)
    cyl(add(c,mul(n,.000)),add(c,mul(n,.006)),.088,'Reflector',44)
    cyl(add(c,mul(n,.006)),add(c,mul(n,.016)),.088,'Optical glass',44)
part('Front bumper, intakes and indicators')
# Blue bumper face: central air intake, two outer intakes, amber indicators in the corners.
for x0,x1 in ((-.30,.30),(-.62,-.40),(.40,.62)):
    box(((x0+x1)/2,.380,ZN+.006),(x1-x0,.100,.012),'Black')
    for k in range(5):box(((x0+x1)/2,.340+k*.020,ZN+.013),(x1-x0-.01,.004,.004),'Mesh')
for s in (-1,1):
    box((s*.62,.500,ZN+.004),(.140,.040,.012),'Amber');box((s*.62,.500,ZN+.011),(.13,.032,.003),'Lens')
part('Skid plate and spoiler lip')
grid(lambda x,z:(x,.235,z),seq(-.64,.64,10),seq(1.55,ZN+.02,6),'Silver')
for k in range(8):
    for j in range(3):cyl((-.56+k*.16,.236,1.72+j*.10),(-.56+k*.16,.242,1.72+j*.10),.022,'Black',10)
grid(lambda x,t:(x,.250-.020*t,ZN+.035*t),seq(-.70,.70,20),[0,1],'Charcoal',True)

# ── Rear body ───────────────────────────────────────────────────────────────────────────────
group('tail','Rear body','后车身',(0,.55,-.85),'后车身：宽大后翼子板、发动机舱盖、959 环形尾翼与中冷器格栅、尾灯带与后保险杠。')
part('Rear wings and engine lid')
loft(ZT,DZ0,44)
cap(ZT,0)
def lid(u,z):
    sec=section(z,True);xc=sec[NL+NU][0];x=u*xc
    t=1-abs(x)/max(xc,.01);return (x,P(YCR,z)+(P(YCEN,z)-P(YCR,z))*sm(t),z)
part('Rear quarter intakes')
# Black intake slots in the rear wings ahead of the rear wheels (959 feature).
for s in (-1,1):
    for k in range(4):
        z=-.62-k*.050;y0,y1=.62,.76
        box((s*(side_x(z,.69)+.003),.69,z),(.012,.13,.028),'Black')
part('Rear wing loop and intercooler grille')
# The 959's integrated loop wing: a blade across the tail joined to both rear wings, with the
# intercooler grille seen through the opening beneath it.
WY,WZ0,WZ1=1.005,-1.985,-2.150
def blade(u,t):
    z=WZ0+(WZ1-WZ0)*t;x=u*(P(XCR,z)+.10)
    return (x,WY+.020*sin(pi*t)-.010*u*u,z)
grid(blade,seq(-1,1,20),seq(0,1,5),'Ivory',True)
grid(lambda u,t:add(blade(u,t),(0,-.022,0)),seq(-1,1,20),seq(0,1,5),'Ivory')
grid(lambda u,t:(blade(u,0)[0],blade(u,0)[1]-.022*t,WZ0),seq(-1,1,20),[0,1],'Ivory')
grid(lambda u,t:(blade(u,1)[0],blade(u,1)[1]-.022*t,WZ1),seq(-1,1,20),[0,1],'Ivory')
for s in (-1,1):
    # End uprights down to the hips.
    z=(WZ0+WZ1)/2;x=s*(P(XCR,z)+.06)
    plate([(x,P(YCR,z)-.01,WZ0+.02),(x,WY-.01,WZ0+.02),(x,WY-.01,WZ1-.02),(x,P(YCR,z)-.01,WZ1-.02)],'Ivory',(-s*.06,0,0))
box((0,.925,-2.050),(.70,.070,.200),'Black')                      # intercooler intake under the blade
for k in range(16):box((-.33+k*.044,.962,-2.050),(.006,.004,.19),'Mesh')
part('Tail lamps and bumper')
for s in (-1,1):
    box((s*.62,.760,ZT-.004),(.240,.070,.012),'Tail');box((s*.62,.760,ZT-.011),(.23,.060,.003),'Smoke')
    box((s*.42,.760,ZT-.004),(.160,.070,.012),'Amber')
box((0,.760,ZT-.004),(.680,.070,.012),'Tail');box((0,.760,ZT-.011),(.676,.060,.003),'Smoke')   # full-width reflector strip
box((0,.470,ZT-.006),(.420,.090,.010),'Yellow')                    # registration plate
for s in (-1,1):cyl((s*.36,.380,ZT+.02),(s*.36,.380,ZT-.08),.034,'Exhaust',20);cyl((s*.36,.380,ZT-.08),(s*.36,.380,ZT-.082),.026,'Black',20)
grid(lambda x,z:(x,.300,z),seq(-.62,.62,10),seq(-2.20,-1.55,6),'Silver')

# ── Cabin ───────────────────────────────────────────────────────────────────────────────────
group('canopy','Roof and glazing','车顶与玻璃',(0,1.20,-.05),'车顶、前风挡、A 柱、后窗、C 柱侧窗与车顶信号灯。')
HZ=.040                     # windscreen header
RZ0,RW0=-.560,-1.170        # roof rear edge / rear-window foot
def roof_y(z):return sinterp(z,[(RZ0,1.272),(-.30,1.292),(HZ,1.282)])
def edge(z):
    """Outer edge of the glasshouse top (A-pillar, roof rail, rear-window side) at station z."""
    if z>=HZ:t=(z-HZ)/(ZW-HZ);return (.530+(.715-.530)*t,1.282+(BELT-1.282)*t)
    if z>=RZ0:return (.548-.012*((z-RZ0)/(HZ-RZ0)),roof_y(z))
    t=(RZ0-z)/(RZ0-RW0);return (.548+(.640-.548)*t,1.272+(1.040-1.272)*sm(t)**.9)
def belt(z):
    if z>=DZ0:return (P(XCR,z),BELT)
    return (P(XCR,z),sinterp(z,[(RW0,P(YCR,RW0)),(-.80,.975),(DZ0,BELT)]))
def wind(u,t):
    zb=ZW+.020*(1-u*u);xb=.715*u;yb=BELT
    zt_=HZ+.012*(1-u*u);xt=.530*u;yt=1.282
    p=mix((xb,yb,zb),(xt,yt,zt_),t)
    return add(p,(0,.016*sin(pi*t),.006*sin(pi*t)))
part('Windscreen')
grid(wind,seq(-1,1,20),seq(0,1,10),'Glass')
for s in (-1,1):path([wind(s,t) for t in seq(0,1,12)],.012,'Black')
path([wind(u,0) for u in seq(-1,1,20)],.012,'Black');path([wind(u,1) for u in seq(-1,1,20)],.012,'Black')
part('Roof')
def roof(u,z):
    x,y=edge(z);return (u*x,y+.022*(1-u*u),z)
grid(roof,seq(-1,1,20),seq(RZ0,HZ,10),'Ivory',True)
grid(lambda u,t:mix(roof(u,HZ),add(wind(u,1),(0,.002,0)),t),seq(-1,1,20),[0,1],'Ivory')
part('Rear window')
def rglass(u,z):x,y=edge(z);return (u*(x-.040),y+.022*(1-u*u)+.002,z)
grid(rglass,seq(-1,1,18),seq(RW0,RZ0,10),'Glass',True)
for z in (RW0,RZ0):path([rglass(u,z) for u in seq(-1,1,14)],.008,'Black',6)
for s in (-1,1):path([rglass(s,z) for z in seq(RW0,RZ0,10)],.008,'Black',6)
for s in (-1,1):grid(lambda t,z:mix(rglass(s,z),roof(s,z),t),[0,1],seq(RW0,RZ0,10),'Ivory',s>0)
grid(lambda u,t:mix(rglass(u,RW0),lid(u,RW0-.02),t),seq(-1,1,18),[0,1],'Ivory')
part('Pillars and rear quarters')
for s in (-1,1):
    zs=seq(RW0,ZW,40)
    for a,b in zip(zs,zs[1:]):
        if DZ0<a<DZ1 and DZ0<b<DZ1:continue        # the door carries its own frame and glass
        pa,pb=belt(a),belt(b);ea,eb=edge(a),edge(b)
        q=[(s*pa[0],pa[1],a),(s*pb[0],pb[1],b),(s*eb[0],eb[1],b),(s*ea[0],ea[1],a)]
        face(q if s<0 else q[::-1],'Ivory')
    # Rear quarter window, painted black on the rally car (Shell / 959 panel).
    def qw(z,v):
        p,e=belt(z),edge(z);return add(mix((s*p[0],p[1],z),(s*e[0],e[1],z),v),(s*.004,0,0))
    zq=seq(-1.02,-.52,8)
    for a,b in zip(zq,zq[1:]):
        vtop=lambda z:.86-.10*clamp((-.70-z)/.32,0,1)
        q=[qw(a,.10),qw(b,.10),qw(b,vtop(b)),qw(a,vtop(a))]
        face(q if s<0 else q[::-1],'Black')
part('Roof beacons')
for s in (-1,1):
    b=roof(s*.62,RZ0+.03)
    cyl(b,add(b,(0,.050,0)),.008,'Gunmetal',8);box(add(b,(0,.085,0)),(.070,.060,.050),'Tail');box(add(b,(0,.050,0)),(.074,.010,.054),'Black')
part('Aerial')
cyl((.48,1.205,-.80),(.48,1.215,-.80),.012,'Black',16);cyl((.48,1.215,-.80),(.52,1.62,-1.10),.0022,'Gunmetal',8)

# ── Doors ───────────────────────────────────────────────────────────────────────────────────
for s in (-1,1):
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.15,.20,.10),'车门、黑框侧窗、门把手与外后视镜。')
    part('Door outer skin')
    loft(DZ0,DZ1,16,top=False,sides=(s,))
    for z in (DZ0,DZ1):path([(s*(side_x(z,y)+.003),y,z) for y in seq(bottom(z),BELT,8)],.004,'Black',6)
    box((s*(side_x(-.33,.84)+.006),.840,-.33),(.012,.024,.12),'Black')
    part('Side window and mirror')
    zs=seq(DZ0,ZW,14)
    for a,b in zip(zs,zs[1:]):
        pa,pb=belt(a),belt(b);ea,eb=edge(min(a,ZW)),edge(min(b,ZW))
        q=[(s*pa[0],pa[1],a),(s*pb[0],pb[1],b),(s*eb[0],eb[1],b),(s*ea[0],ea[1],a)]
        face(q if s<0 else q[::-1],'Glass')
    path([(s*belt(z)[0],belt(z)[1],z) for z in seq(DZ0,ZW,10)],.010,'Black',6)
    path([(s*edge(z)[0],edge(z)[1],z) for z in seq(DZ0,ZW,12)],.012,'Black',6)
    path([(s*belt(DZ0)[0],BELT,DZ0),(s*edge(DZ0)[0],edge(DZ0)[1],DZ0)],.016,'Black',6)
    m0=(s*.80,.985,.53);cyl(m0,(s*.89,1.005,.515),.011,'Black',8)
    box((s*.920,1.015,.505),(.060,.075,.115),'Ivory');box((s*.920,1.015,.447),(.052,.064,.004),'Glass')
