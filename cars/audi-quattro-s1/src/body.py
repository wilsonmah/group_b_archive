# Audi Sport quattro S1 E2 coachwork. Metres; x to the car's left, y up, z forward, origin on the
# ground midway between the axles. Proportions come from the side photo of car Nº 2 (wheelbase
# 2.224 m as the scale) and the four-view drawing for plan widths.
FZ,RZ=1.112,-1.112          # axle stations
TR=.292                     # rolling radius (side photo: wheel centre 0.28-0.29 m)
FX,RX=.7325,.751            # wheel-centre half tracks (1465 / 1502 mm)
RA=.326                     # wheel-arch radius (arch tops at 0.61-0.62 m)
DZ0,DZ1=-.54,.62            # door shut lines
ZT,ZN,ZS=-1.905,1.865,2.075 # tail face, nose face, splitter lip
XD,XF,XI,XG=.835,.925,.800,.785   # door skin, flare skin, inner front wing, cabin base

def arch_y(z,zc):
    d=abs(z-zc);return TR+sqrt(RA*RA-d*d) if d<RA else -1
def door_top(z):return .855+(z-DZ0)/(DZ1-DZ0)*.060
def rear_top(z):return sinterp(z,[(ZT,.935),(-1.70,.925),(-1.45,.906),(-.70,.905),(DZ0,.905)])
def shoulder(z):return sinterp(z,[(.60,.937),(.80,.930),(1.0,.915),(1.3,.886),(1.6,.857),(1.78,.830),(ZN,.805)])
def ledge(z):return sinterp(z,[(.62,.775),(.87,.740),(1.31,.612),(1.74,.425),(2.05,.270)])
def flare_bottom(z):return sinterp(z,[(.62,.294),(.80,.292),(1.46,.300),(1.70,.260),(2.05,.196)])
def rear_bottom(z):return sinterp(z,[(ZT,.212),(-1.62,.222),(-1.45,.250),(-.80,.292),(DZ0,.294)])

# Livery bands up the side, bottom to top: yellow, pinstripes, white, pinstripes, yellow (side photo).
STRIPES=[(.008,'Orange'),(.006,'Ivory'),(.010,'Yellow'),(.006,'Ivory'),(.010,'Orange')]
def stripe_set(y0,up=True):
    out=[];y=y0
    for h,m in (STRIPES if up else STRIPES[::-1]):
        out.append((y,y+h,m));y+=h
    return out
def side_bands(lo_yellow=.352,hi_yellow=.680):
    return [(-1,lo_yellow,'Yellow')]+stripe_set(lo_yellow)+[(lo_yellow+.040,hi_yellow,'Ivory')]+stripe_set(hi_yellow,False)+[(hi_yellow+.040,9,'Yellow')]
BANDS=side_bands()

def banded(fn,zs,low,high,bands,flip=False,ny=3):
    """Emit a surface fn(z,y) between low(z) and high(z), coloured by horizontal bands (y ranges)."""
    for a,b in zip(zs,zs[1:]):
        la,ha,lb,hb=low(a),high(a),low(b),high(b)
        if ha<=la and hb<=lb:continue
        A=bands(a) if callable(bands) else bands;Bb=bands(b) if callable(bands) else bands
        for (y0,y1,m),(w0,w1,_) in zip(A,Bb):
            p0,p1=max(y0,la),min(y1,ha);q0,q1=max(w0,lb),min(w1,hb)
            if p1<=p0 and q1<=q0:continue
            if p1<p0:p0=p1=clamp(y0,la,ha)
            if q1<q0:q0=q1=clamp(w0,lb,hb)
            n=max(1,int(ny*max(p1-p0,q1-q0)/.1+.5))
            for k in range(n):
                t,T=k/n,(k+1)/n
                pts=[fn(a,p0+(p1-p0)*t),fn(b,q0+(q1-q0)*t),fn(b,q0+(q1-q0)*T),fn(a,p0+(p1-p0)*T)]
                face(pts[::-1] if flip else pts,m)

def zstations(z0,z1,n,extra=()):
    zs=set(round(z,5) for z in seq(z0,z1,n))
    for zc in (FZ,RZ):
        for i in range(41):
            z=zc+RA*cos(pi*i/40)
            if z0<z<z1:zs.add(round(z,5))
    for z in extra:
        if z0<z<z1:zs.add(round(z,5))
    return sorted(zs)

# ── Front clamshell ────────────────────────────────────────────────────────────────────────
group('nose','Front body','前车身',(0,.42,.78),'整体前车头：引擎盖、带斜面宽体轮眉的前翼子板、前保险杠扰流板、格栅与大灯。')
part('Front wings and bonnet')
def nose_low(z):
    a=arch_y(z,FZ);return max(flare_bottom(z),a)
zf=zstations(.62,ZN,48,(.74,1.46,1.74))
for s in (-1,1):
    # Flare skin below the sloping ledge. Bottom bands follow the flare's lower edge to the splitter.
    def flare_pt(z,y,s=s):
        tuck=-.012*clamp((nose_low(z)+.03-y)/.03,0,1)
        roll=-.010*clamp((y-ledge(z)+.02)/.02,0,1)
        corner=-.07*clamp((z-1.86)/.21,0,1)**2
        x=XF+tuck+roll+corner if z>.74 else XD+(XF-XD)*clamp((z-.62)/.12,0,1)
        return (s*x,y,z)
    def flare_bands(z):
        b=flare_bottom(z)
        return [(-1,b+.058,'Yellow')]+stripe_set(b+.058)+[(b+.098,9,'Ivory')]
    banded(flare_pt,zf,nose_low,ledge,flare_bands,flip=s<0)
    # The ledge: a shallow inward-sloping shelf from the flare top to the inner wing.
    zl=[z for z in zf if z>=.74]
    for a,b in zip(zl,zl[1:]):
        pa=(s*(XF-.010),ledge(a),a);pb=(s*(XF-.010),ledge(b),b)
        qa=(s*XI,ledge(a)+.022,a);qb=(s*XI,ledge(b)+.022,b)
        face([pa,pb,qb,qa] if s>0 else [qa,qb,pb,pa],'Ivory')
    # Riveted polished-aluminium strip along the ledge edge (front photos).
    path([(s*(XF-.006),ledge(z)+.006,z) for z in zl],.007,'Silver',6)
    for z in zl[::3]:cyl((s*(XF-.006),ledge(z)+.012,z),(s*(XF-.006),ledge(z)+.016,z),.004,'Steel',6)
    # Inner wing side above the ledge: yellow band with the Audi Sport / Castrol lettering.
    def inner_pt(z,y,s=s):
        return (s*(XI-.012*clamp((y-ledge(z))/(shoulder(z)-ledge(z)+1e-6),0,1)),y,z)
    def inner_bands(z):
        l=ledge(z)+.022
        return [(-1,l+.105,'Yellow')]+stripe_set(l+.105)+[(l+.145,9,'Ivory')]
    banded(inner_pt,[z for z in zf if z>=.74],lambda z:ledge(z)+.022,shoulder,inner_bands,flip=s<0)
    # Front step from the door skin out to the flare, just behind the arch.
    def step_pt(t,y,s=s):
        z=.62+.12*t;x=XD+(XF-XD)*t
        return (s*x,y,z)
    banded(step_pt,seq(0,1,4),lambda t:flare_bottom(.62),lambda t:ledge(.62+.12*t),BANDS,flip=s<0)
    # Upper cowl strip between the inner wing and door top, in front of the A-pillar.
    for a,b in zip(seq(.62,.74,3),seq(.62,.74,3)[1:]):
        face([(s*XD,door_top(.62),a),(s*XD,door_top(.62),b),(s*XI,shoulder(b),b),(s*XI,shoulder(a),a)][::s],'Ivory')
# Bonnet and wing tops: flat across with a soft crown, rolling over the front edge.
def top_y(x,z):
    sh=shoulder(z);c=.012*(1-(abs(x)/XI)**2)
    roll=-.030*clamp((z-1.82)/.045,0,1)**2
    return sh+c+roll
bx=seq(-XI,XI,24);bz=zstations(.60,ZN,40,(1.82,1.84))
grid(lambda x,z:(x,top_y(x,z),z),bx,bz,'Ivory',True)
# Front of the bonnet turns down to the grille header.
grid(lambda x,t:(x,top_y(x,ZN)-.028*t,ZN+.002-.004*t),bx,[0,1],'Ivory')

part('Grille, headlamps and bumper')
# Black grille panel across the nose.
gh=lambda x:top_y(x,ZN)-.030
grid(lambda x,t:(x,.500+(gh(x)-.500)*t,ZN),seq(-.76,.76,24),[0,1],'Black')
# White nose corners outboard of the black panel.
for s in (-1,1):grid(lambda x,t:(s*x,.500+(gh(x)-.500)*t,ZN-.002),seq(.76,.84,3),[0,1],'Ivory',s<0)
for k in range(14):
    y=.535+k*.016
    box((0,y,ZN+.006),(.80,.006,.010),'Charcoal')
for s in (-1,1):
    # Rectangular headlamp, set into the black panel at each outer end.
    hx=s*.600
    box((hx,.664,ZN+.004),(.236,.146,.016),'Gunmetal')
    box((hx,.664,ZN+.013),(.216,.126,.006),'Reflector')
    box((hx,.664,ZN+.018),(.212,.122,.004),'Optical glass')
    for k in range(7):box((hx-.090+k*.030,.664,ZN+.021),(.003,.116,.002),'Lens')
# Four-ring badge.
for k in range(4):
    tor((-.111+k*.074,.668,ZN+.012),(0,0,1),.040,.0045,'Silver',40,6)
# Yellow valance band with the indicators and a black lower intake.
grid(lambda x,t:(x,.440+.060*t,ZN+.004*t),seq(-.82,.82,24),[0,1],'Yellow')
for s in (-1,1):
    box((s*.700,.462,ZN+.010),(.120,.056,.020),'Amber')
    box((s*.700,.462,ZN+.021),(.112,.048,.004),'Lens')
box((0,.395,ZN-.004),(.84,.090,.012),'Black')
for k in range(5):box((0,.360+k*.017,ZN+.004),(.82,.004,.008),'Mesh')
# Sloping white bumper face down to the yellow splitter lip.
def bumper(x,t):
    z=ZN+(2.040-ZN)*t;y=.440-(.440-.215)*t
    taper=.060*clamp((abs(x)-.62)/.30,0,1)*t
    return (x,y,z-taper)
grid(bumper,seq(-.90,.90,30),seq(0,1,6),'Ivory',True)
def lip(x,t):
    taper=.060*clamp((abs(x)-.62)/.30,0,1)
    z=2.040+.035*t-taper;y=.215-.075*t
    return (x,y,z)
grid(lip,seq(-.90,.90,30),seq(0,1,3),'Yellow',True)
# Splitter blade underneath, running back to the front axle line.
grid(lambda x,z:(x,.138,z),seq(-.90,.90,10),seq(1.45,ZS-.03,6),'Black')
for s in (-1,1):
    # Close the bumper corners against the flare skin.
    for a,b in zip(seq(0,1,6),seq(0,1,6)[1:]):
        p=bumper(s*.90,a);q=bumper(s*.90,b)
        face([p,q,(s*.90,flare_bottom(q[2]),q[2]),(s*.90,flare_bottom(p[2]),p[2])][::s],'Yellow')

part('Bonnet louvres and fasteners')
# Nº 2's bonnet (front photos): a louvred outlet near the screen on each side and a small
# black mesh vent towards the front of the right-hand side.
def on_bonnet(x,z,lift=.002):return (x,top_y(x,z)+lift,z)
for s in (-1,1):
    x0=s*.40;xa,xb=x0-.12,x0+.12;za,zb=.86,1.08
    q=[on_bonnet(xa,za),on_bonnet(xb,za),on_bonnet(xb,zb),on_bonnet(xa,zb)]
    face(q if s<0 else q[::-1],'Black');face(q[::-1] if s<0 else q,'Black')
    for k in range(8):
        z=za+.012+k*.026
        p0=on_bonnet(xa+.008,z,.003);p1=on_bonnet(xb-.008,z,.003)
        slat=[p0,p1,add(p1,(0,.011,-.016)),add(p0,(0,.011,-.016))]
        face(slat,'Charcoal');face(slat[::-1],'Charcoal')
    path([on_bonnet(x,z,.003) for x,z in [(xa,za),(xb,za),(xb,zb),(xa,zb),(xa,za)]],.004,'Black',4)
mx,mz=-.46,1.66
q=[on_bonnet(mx-.10,mz-.04,.003),on_bonnet(mx+.10,mz-.04,.003),on_bonnet(mx+.10,mz+.04,.003),on_bonnet(mx-.10,mz+.04,.003)]
face(q[::-1],'Mesh');path(q+[q[0]],.003,'Black',4)
for s in (-1,1):
    for z in (.82,1.74):
        q=(s*.63,top_y(.63,z),z);cyl(q,add(q,(0,.007,0)),.016,'Steel',14)

# ── Rear body ───────────────────────────────────────────────────────────────────────────────
group('tail','Rear body and wing','后车身与尾翼',(0,.55,-.95),'后宽体翼子板、车尾面板、散热出风格栅、尾灯和大型尾翼。')
part('Rear wings and quarter panels')
def tail_low(z):
    a=arch_y(z,RZ);return max(rear_bottom(z),a)
zr=zstations(-1.80,-.70,40,(-1.45,))
for s in (-1,1):
    def rear_pt(z,y,s=s):
        tuck=-.012*clamp((tail_low(z)+.03-y)/.03,0,1)
        roll=-.014*clamp((y-rear_top(z)+.025)/.025,0,1)**2
        return (s*(XF+tuck+roll),y,z)
    banded(rear_pt,zr,tail_low,rear_top,BANDS,flip=s>0)
    # Rear corner wraps round to the tail face.
    def corner_pt(t,y,s=s):
        a=t*pi/2;z=-1.80-.105*sin(a);x=XF-.045+.045*cos(a)
        return (s*x,y,z)
    banded(corner_pt,seq(0,1,6),lambda t:rear_bottom(-1.80-.105*t),lambda t:rear_top(-1.80-.105*t),BANDS,flip=s>0)
    # Step from the door skin to the flare carrying the black side intake.
    def rstep(t,y,s=s):return (s*(XD+(XF-XD)*t),y,DZ0-.16*t)
    banded(rstep,seq(0,1,4),lambda t:rear_bottom(DZ0-.16*t),lambda t:min(door_top(DZ0)+.05*t,rear_top(DZ0)),BANDS,flip=s<0)
    q=[rstep(t,y) for t,y in [(.08,.250),(.92,.250),(.92,.735),(.08,.735)]]
    face([add(p,(s*.004,0,.003)) for p in q][::s],'Mesh')
    for k in range(16):
        y=.262+k*.030
        a=rstep(.10,y);b=rstep(.90,y)
        face([add(a,(s*.006,0,.004)),add(b,(s*.006,0,.004)),add(b,(s*.006,.012,.004)),add(a,(s*.006,.012,.004))][::s],'Black')
    # Shelf on top of the rear wing between the cabin and the flare edge.
    zz=[z for z in zr]
    for a,b in zip(zz,zz[1:]):
        face([(s*XG,rear_top(a)+.004,a),(s*XG,rear_top(b)+.004,b),(s*(XF-.014),rear_top(b),b),(s*(XF-.014),rear_top(a),a)][::-s],'Ivory')
    # Turbo-air louvre strip high on the rear flank.
    for k in range(18):
        z=-1.82+k*.028
        box((s*(XF+.002),.887,z),(.004,.014,.016),'Black')
part('Boot lid and tail panel')
BOX=1.085   # top of the raised rear box under the wing
def box_top(x,z):return BOX+.006*(1-(x/XG)**2)
# Short boot ramp from the rear-window foot up to the box, then the flat box top.
grid(lambda x,t:(x,.968+(box_top(x,-1.60)-.968)*t,-1.50-.10*t),seq(-XG,XG,16),seq(0,1,3),'Ivory',True)
grid(lambda x,z:(x,box_top(x,z),z),seq(-XG,XG,16),seq(ZT+.004,-1.60,6),'Ivory',True)
for s in (-1,1):
    # Box sides between the rear-wing shelves and the box top.
    side=[(s*XG,.905,-1.50),(s*XG,.905,ZT),(s*XG,BOX,ZT),(s*XG,BOX,-1.60),(s*XG,.968,-1.50)]
    face(side if s<0 else side[::-1],'Ivory')
# Tail face, bottom to top: yellow lip, white lower panel with the perforated strip, white
# surround with the two outlets and a pinstripe pair, yellow Audi/quattro band, white box face.
tail_bands=[(.212,.262,'Yellow'),(.262,.596,'Ivory'),(.596,.603,'Orange'),(.603,.609,'Ivory'),(.609,.616,'Yellow'),
            (.616,.742,'Ivory'),(.742,.750,'Orange'),(.750,.852,'Yellow'),(.852,.860,'Orange'),(.860,BOX,'Ivory')]
for y0,y1,m in tail_bands:
    w=.88 if y0<.905 else XG
    grid(lambda x,t:(x,y0+(y1-y0)*t,ZT),seq(-w,w,22),[0,1],m)
def rounded_rect(cx,cy,w,h,r,n=6):
    pts=[]
    for qx,qy,a0 in [(1,1,0),(-1,1,pi/2),(-1,-1,pi),(1,-1,3*pi/2)]:
        c=(cx+qx*(w/2-r),cy+qy*(h/2-r))
        pts+=[(c[0]+r*cos(a0+pi/2*k/n),c[1]+r*sin(a0+pi/2*k/n)) for k in range(n+1)]
    return pts
for s in (-1,1):
    # Rounded black outlet for the boot-mounted radiators, with a fine grille.
    cx=s*.305
    o=rounded_rect(cx,.620,.505,.228,.038)
    face([(x,y,ZT-.003) for x,y in o][::-s] if s>0 else [(x,y,ZT-.003) for x,y in o],'Mesh')
    path([(x,y,ZT-.004) for x,y in o+[o[0]]],.006,'Black',6)
    for k in range(12):box((cx,.522+k*.0178,ZT-.008),(.48,.004,.004),'Black')
    for k in range(16):box((cx-.225+k*.030,.620,ZT-.009),(.003,.212,.004),'Black')
    # Dark smoked tail lamp at each outer end, at outlet height.
    box((s*.715,.640,ZT-.008),(.230,.170,.016),'Smoke')
    box((s*.715,.640,ZT-.017),(.214,.154,.003),'Smoke')
    box((s*.715,.690,ZT-.018),(.200,.040,.002),'Tail')
    box((s*.655,.590,ZT-.018),(.070,.040,.002),'Amber')
    # Black vertical vent on the back of each rear flare.
    box((s*.865,.560,ZT+.004),(.060,.300,.012),'Mesh')
box((0,.344,ZT-.006),(1.24,.072,.010),'Steel')
for k in range(40):
    for j in range(3):cyl((-.60+k*.0307,.322+j*.022,ZT-.012),(-.60+k*.0307,.322+j*.022,ZT-.0115),.006,'Black',8)

part('Rear wing and end plates')
def wing(x,t):
    # Long-chord plane from the leading edge over the rear window (z -1.27) to a high trailing
    # edge at z -2.02, as in the side and rear photos.
    z=-1.27-.75*t;y=1.212+.103*t-.016*sin(pi*t)
    return (x,y,z)
WX=.865
grid(wing,seq(-WX,WX,20),seq(0,1,10),'Ivory',True)
grid(lambda x,t:add(wing(x,t),(0,-.030*sin(pi*clamp(t*1.25,0,1))-.004,0)),seq(-WX,WX,20),seq(0,1,10),'Pearl')
grid(lambda x,t:(x,wing(x,1)[1]-.004+.034*t,wing(x,1)[2]-.004*t),seq(-WX,WX,20),[0,1],'Ivory')
for s in (-1,1):
    ep=[(-1.205,.905),(-1.95,.905),(-2.035,1.00),(-2.035,1.352),(-1.88,1.345),(-1.24,1.238),(-1.225,1.10)]
    plate([(s*WX,y,z) for z,y in ep],'Ivory',(-s*.008,0,0))

# ── Cabin ───────────────────────────────────────────────────────────────────────────────────
group('canopy','Roof and glazing','车顶与玻璃',(0,1.25,0),'钢制车顶、前风挡、溜背式后窗与 A/C 柱。')
part('Windscreen')
def wind(u,t):
    zb=.632+.073*(1-u*u);xb=.740*u;yb=.940
    zt=.104+.022*(1-u*u);xt=.585*u;yt=1.269+.008*(1-u*u)
    p=mix((xb,yb,zb),(xt,yt,zt),t)
    return add(p,(0,.012*sin(pi*t)*(1-.5*u*u),.006*sin(pi*t)))
grid(wind,seq(-1,1,24),seq(0,1,10),'Glass')
for s in (-1,1):path([wind(s,t) for t in seq(0,1,12)],.010,'Black')
path([wind(u,0) for u in seq(-1,1,24)],.010,'Black');path([wind(u,1) for u in seq(-1,1,24)],.010,'Black')
grid(lambda u,t:add(wind(u,t),(0,.002,.003)),seq(-1,1,16),[.86,.995],'Black')
part('Roof')
RW=.600
def roof(u,z):
    fall=.012*clamp((-.62-z)/.22,0,1)**2
    return (u*RW,1.294+.012*(1-u*u)-fall-.010*abs(u)**6,z)
grid(roof,seq(-1,1,24),seq(-.84,.13,14),'Ivory',True)
grid(lambda u,t:mix(roof(u,.13),add(wind(u,1),(0,.004,0)),t),seq(-1,1,24),[0,1],'Ivory')
for s in (-1,1):path([roof(s,z) for z in seq(-.84,.13,8)],.010,'Ivory')
part('Rear window and sail panels')
def rearwin(u,t):
    # Long quattro fastback: the glass runs from the roof almost to the short boot lid.
    a=(u*.585,1.278,-.840);b=(u*.700,.968,-1.500)
    return add(mix(a,b,t),(0,.014*sin(pi*t),0))
grid(rearwin,seq(-1,1,20),seq(0,1,8),'Glass')
path([rearwin(u,0) for u in seq(-1,1,20)],.010,'Black');path([rearwin(u,1) for u in seq(-1,1,20)],.010,'Black')
grid(lambda u,t:mix(roof(u,-.84),rearwin(u,0),t),seq(-1,1,20),[0,1],'Ivory')
for s in (-1,1):
    path([rearwin(s,t) for t in seq(0,1,8)],.010,'Black')

# ── Doors ───────────────────────────────────────────────────────────────────────────────────
for s in (-1,1):
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.15,.20,.10),'钢制车门，带侧窗框、外后视镜和车组姓名。')
    part('Door outer skin')
    def door_pt(z,y,s=s):
        tumble=-.020*clamp((y-.30)/.56,0,1)
        return (s*(XD+tumble),y,z)
    zd=seq(DZ0,DZ1,18)
    banded(door_pt,zd,lambda z:.294,door_top,BANDS,flip=s<0)
    for z in (DZ0,DZ1):path([door_pt(z,y) for y in (.294,.60,door_top(z))],.004,'Black')
    path([door_pt(z,.294) for z in zd],.004,'Black')
    box((s*(XD-.004),.760,-.420),(.022,.026,.110),'Black')
    part('Side window frame and glass')
    # Door glass between the A-pillar line, the roof rail and the B-pillar.
    a0=wind(s,0);a1=wind(s,1)
    pts=[(s*.818,door_top(.55)+.004,.55),add(a1,(s*.012,-.012,-.040)),(s*.602,1.260,-.540),(s*.812,door_top(DZ0)+.004,DZ0+.012)]
    face(pts if s<0 else pts[::-1],'Glass')
    path(pts+[pts[0]],.012,'Black')
    # Mirror on a stalk at the front of the door.
    m0=(s*.835,.905,.500);m1=(s*.945,.935,.470)
    cyl(m0,m1,.012,'Black',8)
    box((s*.975,.950,.465),(.07,.075,.105),'Black')
    box((s*.975,.950,.410),(.062,.066,.004),'Glass')

# ── Fixed glass behind the B-pillar and the sails ───────────────────────────────────────────
current='canopy';part('Rear quarter windows')
for s in (-1,1):
    QTR=(s*.596,1.244,-.930);QBR=(s*.786,.912,-1.180)
    q=[(s*.808,door_top(DZ0)+.006,DZ0-.050),(s*.602,1.262,DZ0-.060),QTR,QBR,(s*.800,.910,-1.060)]
    face(q if s<0 else q[::-1],'Glass');path(q+[q[0]],.011,'Black')
    # B-pillar.
    bp=[(s*.818,door_top(DZ0),DZ0+.004),(s*.604,1.266,DZ0-.004),(s*.604,1.266,DZ0-.060),(s*.812,door_top(DZ0),DZ0-.055)]
    plate(bp,'Black',(-s*.012,0,0))
    # Roof rail over the quarter glass back to the sail.
    face([(s*.602,1.262,DZ0-.060),(s*.600,1.282,DZ0-.060),(s*.598,1.282,-.842),QTR][::s],'Ivory')
    # Wide C-pillar sail from the quarter-glass rear edge back to the rear-window edge, painted
    # with diagonal red, taupe and black bands parallel to the glass edge (side photo).
    def front_edge(t):return mix(QTR,QBR,t)
    def rear_edge(t):
        top=(s*.600,1.282,-.842);bot=(s*XG,.968,-1.500)
        return add(mix(top,bot,t),(s*.010*sin(pi*t),0,0))
    for a_,b_ in zip(seq(0,1,10),seq(0,1,10)[1:]):
        Fa,Fb,Ra,Rb=front_edge(a_),front_edge(b_),rear_edge(a_),rear_edge(b_)
        wa=sqrt(dot(sub(Ra,Fa),sub(Ra,Fa)));wb=sqrt(dot(sub(Rb,Fb),sub(Rb,Fb)))
        edges=[0,.045,.050,.115,.120,.330,9]
        mats=['Red','Ivory','Taupe','Ivory','Black','Ivory']
        for (d0,d1),m in zip(zip(edges,edges[1:]),mats):
            ka0,ka1=min(1,d0/wa),min(1,d1/wa);kb0,kb1=min(1,d0/wb),min(1,d1/wb)
            if ka0>=1 and kb0>=1:continue
            quad=[mix(Fa,Ra,ka0),mix(Fb,Rb,kb0),mix(Fb,Rb,kb1),mix(Fa,Ra,ka1)]
            face(quad[::-1] if s>0 else quad,m)
    # Cabin base strip under the quarter glass and the sail.
    face([QBR,(s*.800,.910,-1.060),(s*XG,.905,-1.06),(s*XG,.905,-1.50),rear_edge(1)][::s],'Ivory')
