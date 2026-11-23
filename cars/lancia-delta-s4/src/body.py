# Lancia Delta S4 coachwork. Metres; x to the car's left, y up, z forward, origin on the ground
# midway between the axles. Side heights and lengths come from the side view of the 1986 rally
# four-view drawing (2.440 m wheelbase as the scale), widths from its front and rear views scaled
# to the 1.880 m body width.
FZ,RZ=1.22,-1.22            # axle stations
TR=.300                     # rolling radius
FX,RX=.750,.760             # wheel-centre half tracks
RA=.375                     # wheel-arch radius (arch tops at 0.68 m on the drawing)
ZN,ZT=2.030,-1.985          # nose face, tail face
DZ0,DZ1=-.38,.66            # door shut lines (drawing: front 0.66 m, rear 0.29-0.41 m behind centre)
CREASE=.735                 # waistline crease
XF,XD,XC,XR=.940,.866,.835,.505   # flares, door skin, window sill, roof rail

def arch_y(z,zc):
    # Rounded-square openings, as on the S4's box flares.
    d=abs(z-zc);return TR+RA*(1-(d/RA)**3)**(1/3) if d<RA else -1
def bonnet_y(z):return .900-(.900-.665)*clamp((z-.74)/(1.92-.74),0,1)-.040*clamp((z-1.92)/.11,0,1)**2
def W(z):
    """Half-width below the crease: box flares over both axles, door skin between them."""
    f=clamp((z-.62)/.08,0,1);r=clamp((-.38-z)/.08,0,1)
    w=XD+(XF-XD)*max(f*f*(3-2*f),r*r*(3-2*r))
    w-=.040*clamp((-1.90-z)/.085,0,1)**2
    if z>ZN-NR:w=min(w,.70+.24*sqrt(max(0,ZN-z)/NR))
    return w
NR=.12
def face_z(x):
    u=clamp((abs(x)-.70)/.24,0,1);return ZN-NR*u*u
def bonnet_w(z):return min(.80,W(z)-.005)
def upper(z):
    """Height and half-width of the top of the side: bonnet edge ahead of the screen, window
    sill along the cabin, rear deck behind."""
    if z>DZ1:return bonnet_y(z),min(.800,W(z))
    if z>DZ0:return .835+.010*(DZ1-z)/(DZ1-DZ0),XC
    return .860,.800
def sill(z):return .255 if -.85<z<.85 else (.235 if z>0 else .245)
def bottom(z):return max(sill(z),arch_y(z,FZ),arch_y(z,RZ))
def side_x(z,y):
    if y<=CREASE:
        tuck=.016*clamp((sill(z)+.035-y)/.035,0,1)
        return W(z)-tuck
    yu,xu=upper(z);w=W(z)
    return w-(w-xu)*clamp((y-CREASE)/(yu-CREASE),0,1)
def zstations(z0,z1,n,extra=()):
    zs=set(round(z,5) for z in seq(z0,z1,n))
    for zc in (FZ,RZ):
        for i in range(41):
            z=zc+RA*cos(pi*i/40)
            if z0<z<z1:zs.add(round(z,5))
    for z in extra:
        if z0<z<z1:zs.add(round(z,5))
    return sorted(zs)
def side_skin(z0,z1,s,n=40):
    zs=zstations(z0,z1,n,(.62,.66,.70,-.38,-.42,-.46,1.93,-1.90))
    for a,b in zip(zs,zs[1:]):
        # Two bands split exactly at the waist crease, so no face straddles the crease while the
        # wheel-opening edge changes height quickly along the arch.
        ya,yb=bottom(a),bottom(b)
        ua,ub=upper(a)[0],upper(b)[0]
        ca,cb=max(ya,min(CREASE,ua)),max(yb,min(CREASE,ub))
        for (la,lb,ha,hb,n) in ((ya,yb,ca,cb,4),(ca,cb,ua,ub,3)):
            for t0,t1 in zip(seq(0,1,n),seq(0,1,n)[1:]):
                pts=[]
                for z,y0,y1,t in [(a,la,ha,t0),(b,lb,hb,t0),(b,lb,hb,t1),(a,la,ha,t1)]:
                    y=y0+(y1-y0)*t;pts.append((s*side_x(z,y),y,z))
                face(pts if s<0 else pts[::-1],'Ivory')

# ── Front clamshell ────────────────────────────────────────────────────────────────────────
group('nose','Front body','前车身',(0,.40,.80),'可整体掀开的碳纤维前车头：引擎盖与散热出风口、带方形轮眉的前翼子板、四圆灯、格栅与前唇。')
part('Front wings and bonnet')
for s in (-1,1):side_skin(DZ1,ZN,s)
def bonnet(x,z):
    c=.014*(1-(x/.80)**2);return (x,bonnet_y(z)+c,z)
grid(lambda u,z:bonnet(u*bonnet_w(z),z),seq(-1,1,20),zstations(DZ1,ZN,30,(1.92,ZN-.06,ZN-.03)),'Ivory',True)
# Radiator outlet in the bonnet, with louvres.
for sx in (-1,1):
    xc=sx*.25
    box((xc,bonnet(xc,.885)[1]-.004,.885),(.30,.010,.17),'Mesh')
    for k in range(6):
        z=.815+k*.028;box((xc,bonnet(xc,z)[1]+.002,z),(.29,.004,.012),'Black')
for s in (-1,1):
    for z in (.95,1.80):
        q=bonnet(s*.70,z);cyl(q,add(q,(0,.007,0)),.016,'Steel',14)
part('Nose, headlamps and grille')
# Front face: upper panel with four round lamps, grille, intake slot, indicators, spoiler.
def face_x(y):return W(ZN)-.010
grid(lambda x,t:(x,.170+(bonnet(clamp(x,-bonnet_w(face_z(x)),bonnet_w(face_z(x))),face_z(x))[1]-.170)*t,face_z(x)-.020*t*t),seq(-.94,.94,32),seq(0,1,10),'Ivory')
for s in (-1,1):
    for x in (.548,.745):
        cx=s*x
        fz=face_z(cx)
        cyl((cx,.565,fz-.010),(cx,.565,fz+.004),.098,'Black',36)
        cyl((cx,.565,fz+.004),(cx,.565,fz+.010),.088,'Reflector',36)
        cyl((cx,.565,fz+.010),(cx,.565,fz+.016),.089,'Optical glass',36)
        tor((cx,.565,fz+.012),(0,0,1),.091,.006,'Gunmetal',36,6)
    # Grille openings either side of the shield.
    gq=[(s*.075,.585),(s*.355,.600),(s*.345,.512),(s*.075,.500)]
    plate([(x,y,ZN+.006) for x,y in gq][::s],'Black',(0,0,-.010))
    for k in range(5):box((s*.215,.513+k*.017,ZN+.009),(.26,.005,.006),'Mesh')
    for k in range(9):box((s*(.095+k*.030),.548,ZN+.010),(.004,.085,.006),'Mesh')
    # Square driving lamps and indicators in the lower panel.
    for x in (.40,.47):box((s*x,.355,ZN+.004),(.058,.050,.012),'Black');box((s*x,.355,ZN+.011),(.048,.040,.004),'Lens')
    box((s*.62,.355,ZN+.004),(.060,.040,.012),'Amber')
# Lancia shield in the centre of the grille.
shield=[(0,.630),(.060,.610),(.055,.520),(0,.480),(-.055,.520),(-.060,.610)]
plate([(x,y,ZN+.010) for x,y in shield],'Silver',(0,0,-.006))
plate([(x*.82,.555+(y-.555)*.82,ZN+.013) for x,y in shield],'Navy',(0,0,-.002))
box((0,.415,ZN+.002),(.660,.050,.010),'Black')
for k in range(3):box((0,.400+k*.015,ZN+.008),(.64,.004,.006),'Mesh')
# Registration plate above the intake.
box((0,.470,ZN+.006),(.400,.050,.006),'Ivory')
# Spoiler lip and splitter.
grid(lambda x,t:(x*(1-.02*t),.170-.030*t,face_z(x)+.060*t),seq(-.94,.94,26),[0,1],'Ivory',True)
grid(lambda x,z:(x,.138,z),seq(-.86,.86,10),seq(1.60,ZN+.055,5),'Black')
for s in (-1,1):
    # Nose corners: close the face to the flares.
    # Angled spoiler cheeks running back along the flares (PIRELLI panels on the photos).
    grid(lambda t,y:(s*(W(ZN-NR)-.004),y,ZN-NR-.30*t),[0,1],[.150,.172],'Black',s<0)

# ── Rear body ───────────────────────────────────────────────────────────────────────────────
group('tail','Rear body','后车身',(0,.55,-.85),'可整体掀开的后车身：方形后轮眉、发动机舱百叶盖、车尾网格面板、尾灯与挡泥板。')
part('Rear wings and quarter panels')
for s in (-1,1):side_skin(ZT,DZ0,s)
part('Louvred engine cover')
# The hatch is a black louvred engine cover sloping from the roof to the tail (rear photos).
def hatch(u,t):
    a=(u*.505,1.290,-1.000);b=(u*.800,.880,-1.955)
    return add(mix(a,b,t),(0,.010*sin(pi*t),0))
grid(hatch,seq(-1,1,16),seq(0,1,8),'Charcoal')
for row in range(2):
    for k in range(4):
        x0=-.42+k*.24
        for j in range(6):
            t=.05+row*.10+j*.014
            face([add(hatch(x0/.62,t),(0,.004,0)),add(hatch((x0+.16)/.62,t),(0,.004,0)),add(hatch((x0+.16)/.62,t+.010),(0,.012,-.004)),add(hatch(x0/.62,t+.010),(0,.012,-.004))],'Black')
for u in (-1,1):path([hatch(u,t) for t in seq(0,1,8)],.008,'Black',6)
part('Tail panel')
# Tail face, top to bottom: white header band, full-width black mesh panel with the square tail
# lamps either side, white PIRELLI / plate band; open below with the exhaust and gearbox.
zt=ZT
grid(lambda x,y:(x,y,zt),seq(-.90,.90,22),seq(.800,.870,2),'Ivory')
box((0,.660,zt-.004),(1.30,.260,.012),'Mesh')
for k in range(12):box((0,.540+k*.021,zt-.012),(1.28,.004,.004),'Black')
for k in range(30):box((-.62+k*.0428,.660,zt-.013),(.003,.25,.004),'Black')
for s in (-1,1):
    box((s*.800,.660,zt-.006),(.170,.260,.012),'Ivory')
    box((s*.800,.700,zt-.014),(.130,.110,.010),'Tail');box((s*.800,.625,zt-.014),(.130,.050,.010),'Amber')
grid(lambda x,y:(x,y,zt),seq(-.90,.90,22),seq(.400,.530,2),'Ivory')
for s in (-1,1):grid(lambda t,y:(s*(.90+(W(zt+.05)-.90)*t),y,zt+.05*t),[0,1],seq(.40,.87,6),'Ivory',s>0)

# ── Cabin ───────────────────────────────────────────────────────────────────────────────────
group('canopy','Roof and glazing','车顶与玻璃',(0,1.20,-.05),'车顶、前风挡、A 柱与车顶尾翼。')
part('Windscreen')
def wind(u,t):
    zb=.740+.030*(1-u*u);xb=.660*u;yb=.900
    zt_=.255+.015*(1-u*u);xt=.490*u;yt=1.272
    p=mix((xb,yb,zb),(xt,yt,zt_),t)
    return add(p,(0,.010*sin(pi*t),.004*sin(pi*t)))
grid(wind,seq(-1,1,20),seq(0,1,10),'Glass')
for s in (-1,1):path([wind(s,t) for t in seq(0,1,12)],.010,'Black')
path([wind(u,0) for u in seq(-1,1,20)],.010,'Black');path([wind(u,1) for u in seq(-1,1,20)],.010,'Black')
part('Roof')
def roof(u,z):
    w=.500+.012*clamp((-z-.2)/1.0,0,1)
    return (u*w,1.272+.014*(1-u*u)+.018*clamp((-z-.20)/1.0,0,1)-.010*abs(u)**6,z)
grid(roof,seq(-1,1,20),seq(-1.00,.20,14),'Ivory',True)
grid(lambda u,t:mix(roof(u,.20),add(wind(u,1),(0,.004,0)),t),seq(-1,1,20),[0,1],'Ivory')
grid(lambda u,t:mix(roof(u,-1.00),add(hatch(u,0),(0,.004,0)),t),seq(-1,1,16),[0,1],'Ivory')
part('Roof air scoop')
sc=[roof(u,z) for u,z in [(-.30,.12),(.30,.12),(.30,-.10),(-.30,-.10)]]
face([add(p,(0,.004,0)) for p in sc],'Black')
grid(lambda u,t:add(roof(u*.30,.12),(0,.040*t,0)),seq(-1,1,8),[0,1],'Black')
grid(lambda u,z:add(roof(u*.30,z),(0,.040*clamp((z+.10)/.22,0,1),0)),seq(-1,1,8),seq(-.10,.12,4),'Black',True)
for s in (-1,1):grid(lambda z,t:add(roof(s*.30,z),(0,.040*clamp((z+.10)/.22,0,1)*t,0)),seq(-.10,.12,4),[0,1],'Black')
part('A-pillars and rear quarter panels')
for s in (-1,1):
    # A-pillar / cant-rail band between the screen edge, the roof edge and the door glass.
    A=[wind(s,t) for t in seq(0,1,10)]+[roof(s,z) for z in seq(.20,DZ0,6)][1:]
    C=[mix((s*.835,.850,.660),(s*.520,1.255,.262),t) for t in seq(0,1,10)]+[mix((s*.520,1.255,.262),(s*.520,1.262,DZ0),k/6) for k in range(1,7)]
    for i in range(len(A)-1):face([A[i],A[i+1],C[i+1],C[i]][::s],'Ivory')
    # Solid rear quarter panel (painted over the Delta's rear side window), B-pillar to hatch.
    Q=[(s*.835,.858,DZ0),(s*.520,1.262,DZ0),(s*.507,1.290,-1.00),(s*.800,.882,-1.955),(s*.800,.860,-1.10)]
    face(Q if s<0 else Q[::-1],'Ivory')
    def qx(y):return .835-(.835-.507)*(y-.858)/(1.29-.858)+.004
    RG=[(s*qx(.880),.880,DZ0-.050),(s*qx(1.250),1.250,DZ0-.050),(s*qx(1.262),1.262,-.920),(s*qx(.888),.888,-1.095)]
    face(RG if s<0 else RG[::-1],'Glass');path(RG+[RG[0]],.010,'Black')
    face([(s*.835,.858,DZ0),(s*.800,.860,-1.10),(s*.800,.860,DZ0-.03)][::(-s)],'Ivory')
part('Roof wing')
# Black roof wing standing at the back of the roof, LANCIA MARTINI on its rear-facing board.
WW=.620
def wing(u,t):return (u*WW,1.315+.165*t,-1.030-.230*t)
grid(wing,seq(-1,1,12),seq(0,1,6),'Black',True)
grid(lambda u,t:add(wing(u,t),(0,-.012,0)),seq(-1,1,12),seq(0,1,6),'Black')
for s in (-1,1):
    ep=[(-.99,1.290),(-1.30,1.260),(-1.30,1.495),(-1.22,1.495),(-1.00,1.335)]
    plate([(s*WW,y,z) for z,y in ep],'Black',(-s*.008,0,0))


# ── Doors ───────────────────────────────────────────────────────────────────────────────────
for s in (-1,1):
    group('door'+str(s),'Left door' if s>0 else 'Right door','左侧车门' if s>0 else '右侧车门',(s*1.15,.20,.10),'空心凯夫拉车门，带侧窗、滑动小窗和外后视镜。')
    part('Door outer skin')
    zd=seq(DZ0,DZ1,16)
    for a,b in zip(zd,zd[1:]):
        for t0,t1 in zip(seq(0,1,6),seq(0,1,6)[1:]):
            pts=[]
            for z,t in [(a,t0),(b,t0),(b,t1),(a,t1)]:
                y=.265+(upper(z)[0]-.265)*t;pts.append((s*(side_x(z,y)+.002),y,z))
            face(pts if s<0 else pts[::-1],'Ivory')
    for z in (DZ0,DZ1):path([(s*(side_x(z,y)+.003),y,z) for y in seq(.265,upper(z)[0],6)],.004,'Black',6)
    box((s*(XD+.004),.770,-.300),(.012,.024,.10),'Black')
    part('Side window and mirror')
    G=[(s*.840,.852,.650),(s*.524,1.250,.262),(s*.524,1.258,DZ0+.015),(s*.840,.856,DZ0+.015)]
    face(G if s<0 else G[::-1],'Glass');path(G+[G[0]],.011,'Black')
    sw=[mix(mix(G[0],G[3],.30),mix(G[1],G[2],.30),v) for v in (.15,.62)]
    path([sw[0],add(sw[0],(0,0,-.17)),add(sw[1],(0,0,-.17)),sw[1],sw[0]],.004,'Steel',6)
    m0=(s*.845,.905,.600);cyl(m0,(s*.935,.930,.585),.011,'Black',8)
    box((s*.965,.950,.580),(.065,.070,.100),'Black');box((s*.965,.950,.528),(.058,.062,.004),'Glass')
