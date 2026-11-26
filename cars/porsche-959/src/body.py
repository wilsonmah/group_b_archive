# Porsche 959 coachwork (Paris-Dakar car). Metres; x to the car's left, y up, z forward, origin on the
# ground midway between the axles. Wheelbase 2.272 m, body width 1.84 m, length 4.26 m, height 1.28 m
# (published figures for the 959). The profile follows the 911-derived coupe shape: a low sloping
# nose, a steeply raked screen, a roof that falls away in one long fastback to the tail, and wide
# flared hips over the rear axle.
FZ,RZ=1.136,-1.136          # axle stations
TR=.322                     # rolling radius
FX,RX=.752,.775             # wheel-centre half tracks (front 1.504 m, rear 1.550 m)
RA=.385                     # wheel-arch radius
ZN,ZT=2.130,-2.130          # nose face, tail face
DZ0,DZ1=-.46,.66            # door shut lines
SHOULDER=.72                # height of the body shoulder (widest point)
BELT=.885                   # window sill
XD,XF,XR=.865,.912,.924     # half-widths: door skin, front wings, rear hips
XC=.800                     # half-width at the window sill
NR=.12;FR=.07               # nose plan radius, front-wing top radius

def sm(t):t=clamp(t,0,1);return t*t*(3-2*t)
def arch_y(z,zc):
    d=abs(z-zc);return TR+sqrt(RA*RA-d*d) if d<RA else -1
HOOD=[(.66,.886),(1.0,.826),(1.4,.775),(1.8,.704),(2.0,.640),(2.13,.585)]
def bonnet_y(z):return sinterp(z,HOOD)
YT=[(-2.13,.80),(-1.85,.885),(-1.50,.965),(-1.15,1.035),(-.75,1.165),(-.46,1.255),(-.20,1.272),(.06,1.262)]
XT=[(-2.13,.64),(-1.90,.70),(-1.40,.66),(-.90,.58),(-.46,.52),(.06,.49)]
def W(z):
    """Half-width at shoulder height: front wings, door skin, wide rear hips."""
    f=sm((z-.52)/.28);r=sm((-.28-z)/.38)
    w=XD+(XF-XD)*f if z>0 else XD+(XR-XD)*r
    w-=.15*clamp((z-1.75)/.38,0,1)**2
    w-=.12*clamp((-1.88-z)/.25,0,1)**2
    if z>ZN-NR:w=min(w,.70+.24*sqrt(max(0,ZN-z)/NR))
    return w
def sill(z):return .215 if -.95<z<.95 else (.205 if z>0 else .235)
def bottom(z):return max(sill(z),arch_y(z,FZ),arch_y(z,RZ))
def upper_y(z):
    if z>DZ1:return bonnet_y(z)
    if z>DZ0:return BELT+.012*(DZ1-z)/(DZ1-DZ0)
    return sinterp(z,YT)
def top_w(z):
    """Half-width of the top surface where it meets the side skin."""
    if z>DZ1:return W(z)-FR
    if z>DZ0:return XC
    return sinterp(z,XT)
def side_x(z,y):
    w=W(z)
    if z>DZ1:
        yu=bonnet_y(z)
        if y>yu-FR:
            k=clamp((y-(yu-FR))/FR,0,1);return w-FR*(1-sqrt(1-k*k))
    if y<=SHOULDER:
        tuck=.016*clamp((sill(z)+.035-y)/.035,0,1);return w-tuck
    yu,xu=upper_y(z),top_w(z)
    return w-(w-xu)*clamp((y-SHOULDER)/max(.001,yu-SHOULDER),0,1)**1.5
def zstations(z0,z1,n,extra=()):
    zs=set(round(z,5) for z in seq(z0,z1,n))
    for zc in (FZ,RZ):
        for i in range(41):
            z=zc+RA*cos(pi*i/40)
            if z0<z<z1:zs.add(round(z,5))
    for z in extra:
        if z0<z<z1:zs.add(round(z,5))
    return sorted(zs)
def side_skin(z0,z1,s,n=44):
    zs=zstations(z0,z1,n,(.62,.66,.70,DZ0,DZ0-.04,1.93,2.0,2.08,-1.90,-2.0,-2.08))
    for a,b in zip(zs,zs[1:]):
        ya,yb=bottom(a),bottom(b);ua,ub=upper_y(a),upper_y(b)
        sa,sb=max(ya,min(SHOULDER,ua)),max(yb,min(SHOULDER,ub))
        for (la,lb,ha,hb,k) in ((ya,yb,sa,sb,4),(sa,sb,ua,ub,5)):
            for t0,t1 in zip(seq(0,1,k),seq(0,1,k)[1:]):
                pts=[]
                for z,y0,y1,t in [(a,la,ha,t0),(b,lb,hb,t0),(b,lb,hb,t1),(a,la,ha,t1)]:
                    y=y0+(y1-y0)*t;pts.append((s*side_x(z,y),y,z))
                face(pts if s<0 else pts[::-1],'Ivory')
def crown(u,c=.012):return c*(1-u*u)
def bonnet(x,z):return (x,bonnet_y(z)+crown(x/max(.2,top_w(z))),z)
def sealed_face(z,ys,m,s=1):
    """A flat panel at station z spanning the body outline between the heights in ys."""
    grid(lambda u,y:(u*side_x(z,y),y,z),seq(-1,1,24),ys,m,s<0)

# ── Front clamshell ────────────────────────────────────────────────────────────────────────
group('nose','Front body','前车身',(0,.40,.80),'可整体掀开的前车身：低矮倾斜的引擎盖（前行李箱盖）、前翼子板、大灯、前保险杠与辅助灯。')
part('Front wings and bonnet')
for s in (-1,1):side_skin(DZ1,ZN,s)
grid(lambda u,z:bonnet(u*top_w(z),z),seq(-1,1,22),zstations(DZ1,ZN,34,(1.93,2.0,2.08)),'Ivory',True)
# Bonnet pins and a shallow central ridge.
for s in (-1,1):
    for z in (1.10,1.85):
        q=bonnet(s*.50,z);cyl(q,add(q,(0,.007,0)),.016,'Steel',14)
part('Nose, headlamps and bumper')
# Front face: smooth panel from the bumper line up to the bonnet edge.
ys=[.20+(bonnet_y(ZN)-.20)*t for t in seq(0,1,9)]
grid(lambda u,y:(u*side_x(ZN,y),y,ZN-.035*(1-(y-.20)/(bonnet_y(ZN)-.20))**2),seq(-1,1,30),ys,'Ivory')
for s in (-1,1):
    # Rectangular headlamp in the wing, with round reflector and clear cover.
    cx=s*.560;cy=.480;fz=ZN-.012
    box((cx,cy,fz),(.250,.120,.012),'Black')
    box((cx,cy,fz+.008),(.236,.108,.006),'Reflector')
    cyl((cx-s*.035,cy,fz+.010),(cx-s*.035,cy,fz+.016),.046,'Lens',30)
    cyl((cx+s*.065,cy,fz+.010),(cx+s*.065,cy,fz+.016),.030,'Lens',24)
    box((cx,cy,fz+.020),(.252,.124,.004),'Optical glass')
    # Indicator and fog lamp low in the bumper.
    box((s*.700,.350,ZN-.012),(.060,.050,.012),'Amber')
    for dx in (.20,.40):
        cyl((s*dx,.330,ZN-.010),(s*dx,.330,ZN+.004),.062,'Black',30);cyl((s*dx,.330,ZN+.004),(s*dx,.330,ZN+.010),.054,'Reflector',30)
        cyl((s*dx,.330,ZN+.010),(s*dx,.330,ZN+.016),.055,'Optical glass',30);tor((s*dx,.330,ZN+.012),(0,0,1),.058,.005,'Gunmetal',30,6)
# Intake and number-plate recess in the bumper.
box((0,.285,ZN-.006),(.500,.090,.012),'Black')
for k in range(5):box((0,.255+k*.018,ZN+.002),(.480,.005,.006),'Mesh')
box((0,.440,ZN-.004),(.40,.100,.010),'Ivory')
# Front spoiler lip and splitter.
grid(lambda x,t:(x*(1-.03*t),.200-.045*t,ZN-.035+.045*t),seq(-.76,.76,24),[0,1],'Ivory',True)
grid(lambda x,z:(x,.150,z),seq(-.70,.70,10),seq(1.70,ZN+.010,5),'Black')
# PIRELLI-style cheek fins are not on the 959: plain body-colour lower corners instead.
# ── Rear body ───────────────────────────────────────────────────────────────────────────────
group('tail','Rear body','后车身',(0,.55,-.85),'可整体掀开的后车身：宽大后翼子板、发动机舱盖与进气格栅、尾翼、车尾灯带与保险杠。')
part('Rear wings and quarter panels')
for s in (-1,1):side_skin(ZT,DZ0,s)
# Quarter glass in each C-pillar.
for s in (-1,1):
    def qg(z,y):return (s*(side_x(z,y)+.003),y,z)
    G=[qg(-.52,.99),qg(-.50,1.185),qg(-.80,1.150),qg(-.86,1.020)]
    face(G if s<0 else G[::-1],'Glass');path(G+[G[0]],.008,'Black',6)
part('Rear quarter intake vents')
for s in (-1,1):
    for k in range(5):
        z=-.80-k*.060
        q=[(s*(side_x(z,y)+.002),y,z) for y in (.56,.66)]
        box((s*(side_x(z,.61)+.001),.61,z),(.012,.115,.030),'Black')
part('Engine lid and grille')
rear_lo=-1.14
def lid(u,z):return (u*top_w(z),upper_y(z)+crown(u,.014),z)
zl=zstations(ZT,rear_lo,18,(-1.20,-1.30))
grid(lid,seq(-1,1,22),zl,'Ivory',True)
# Air intake grille across the lid, behind the rear window.
for k in range(9):
    z=-1.28-k*.062;box(add(lid(0,z),(0,.003,0)),(.74,.006,.020),'Black')
box(add(lid(0,-1.50),(0,.002,0)),(.78,.003,.58),'Mesh')
for k in range(9):
    z=-1.28-k*.062;box(add(lid(0,z),(0,.006,0)),(.76,.004,.012),'Charcoal')
for u in (-.4,0,.4):path([add(lid(u,z),(0,.007,0)) for z in seq(-1.24,-1.78,6)],.005,'Charcoal',6)
part('Tail panel and spoiler')
# Tail: full-width black valance carrying the lamp bar; a small lip spoiler on the lid edge.
zt=ZT
for (y0,y1) in ((.28,.40),):
    grid(lambda u,y:(u*side_x(zt,y),y,zt),seq(-1,1,24),[y0,y1],'Black')
grid(lambda u,y:(u*side_x(zt,y),y,zt),seq(-1,1,24),seq(.40,.80,6),'Ivory')
for s in (-1,1):
    box((s*.60,.560,zt-.006),(.46,.090,.012),'Tail');box((s*.60,.560,zt-.011),(.44,.070,.004),'Smoke')
    box((s*.60,.465,zt-.006),(.20,.040,.012),'Amber')
box((0,.560,zt-.006),(.44,.090,.012),'Black')
box((0,.480,zt-.004),(.46,.110,.008),'Ivory')
for s in (-1,1):cyl((s*.30,.34,zt-.02),(s*.30,.34,zt-.14),.040,'Exhaust',20);shell((s*.30,.34,zt-.14),(0,0,-1),[(0,.040),(.01,.034)],'Black',20)
grid(lambda u,t:(u*.60,.800+.025*t,-2.060-.060*t),seq(-1,1,18),[0,1],'Ivory',True)
# Under-tray.
grid(lambda x,z:(x,.265,z),seq(-.80,.80,12),seq(-2.10,-1.40,6),'Charcoal')

# ── Cabin ───────────────────────────────────────────────────────────────────────────────────
group('canopy','Roof and glazing','车顶与玻璃',(0,1.20,-.05),'车顶、前风挡、A 柱、后窗与天线。')
HZ=.06
def wind(u,t):
    zb=.700+.020*(1-u*u);xb=.660*u;yb=.862
    zt_=HZ+.010*(1-u*u);xt=.490*u;yt=1.262
    p=mix((xb,yb,zb),(xt,yt,zt_),t)
    return add(p,(0,.012*sin(pi*t),.004*sin(pi*t)))
part('Windscreen')
grid(wind,seq(-1,1,20),seq(0,1,10),'Glass')
for s in (-1,1):path([wind(s,t) for t in seq(0,1,12)],.010,'Black')
path([wind(u,0) for u in seq(-1,1,20)],.010,'Black');path([wind(u,1) for u in seq(-1,1,20)],.010,'Black')
part('Roof')
def roof(u,z):return (u*top_w(z),upper_y(z)+crown(u,.016),z)
grid(roof,seq(-1,1,20),seq(-.46,HZ,8),'Ivory',True)
grid(lambda u,t:mix(roof(u,HZ),add(wind(u,1),(0,.004,0)),t),seq(-1,1,20),[0,1],'Ivory')
# Short sunroof-style cover strip at the rear of the roof is not fitted; plain roof panel.
part('A-pillars')
for s in (-1,1):
    A=[wind(s,t) for t in seq(0,1,10)]
    C=[mix((s*.800,.882,.670),(s*.505,1.248,.100),t) for t in seq(0,1,10)]
    for i in range(len(A)-1):face([A[i],A[i+1],C[i+1],C[i]][::s],'Ivory')
    # Side-glass-to-roof band along the roof edge.
    R=[roof(s,z) for z in seq(.06,DZ0,8)]
    for i in range(len(R)-1):
        a,b=R[i],R[i+1]
        face([a,b,(s*(abs(b[0])+.018),b[1]-.012,b[2]),(s*(abs(a[0])+.018),a[1]-.012,a[2])][::s],'Ivory')
part('Rear window')
def rglass(u,z):return (u*top_w(z)*.80,upper_y(z)+crown(u*.80,.016)+.002,z)
grid(rglass,seq(-1,1,18),seq(-1.14,-.46,10),'Glass',True)
for z in (-1.14,-.46):path([rglass(u,z) for u in seq(-1,1,14)],.008,'Black',6)
for s in (-1,1):path([rglass(s,z) for z in seq(-1.14,-.46,10)],.008,'Black',6)
# Gap strips between the rear glass and the quarter panels.
for s in (-1,1):
    grid(lambda t,z:mix(rglass(s,z),roof(s,z),t),[0,1],seq(-1.14,-.46,10),'Ivory',s>0)
part('Aerial')
cyl((.60,upper_y(-1.40)+.005,-1.40),(.60,upper_y(-1.40)+.016,-1.40),.014,'Black',16);cyl((.60,upper_y(-1.40)+.016,-1.40),(.66,1.22,-1.84),.0022,'Gunmetal',8)

# ── Doors ───────────────────────────────────────────────────────────────────────────────────
for s in (-1,1):
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.15,.20,.10),'车门带无框侧窗、门把手与外后视镜。')
    part('Door outer skin')
    zd=seq(DZ0,DZ1,16)
    for a,b in zip(zd,zd[1:]):
        for t0,t1 in zip(seq(0,1,7),seq(0,1,7)[1:]):
            pts=[]
            for z,t in [(a,t0),(b,t0),(b,t1),(a,t1)]:
                y=.235+(upper_y(z)-.235)*t;pts.append((s*(side_x(z,y)+.002),y,z))
            face(pts if s<0 else pts[::-1],'Ivory')
    for z in (DZ0,DZ1):path([(s*(side_x(z,y)+.003),y,z) for y in seq(.235,upper_y(z),6)],.004,'Black',6)
    box((s*(XD+.004),.760,-.30),(.012,.024,.12),'Black')
    part('Side window and mirror')
    G=[(s*.800,.890,.650),(s*.505,1.247,.100),(s*.520,1.256,DZ0+.015),(s*.800,.898,DZ0+.015)]
    face(G if s<0 else G[::-1],'Glass');path(G+[G[0]],.010,'Black')
    m0=(s*.810,.950,.560);cyl(m0,(s*.900,.975,.545),.011,'Black',8)
    box((s*.930,.985,.540),(.065,.075,.110),'Ivory');box((s*.930,.985,.484),(.058,.066,.004),'Glass')
