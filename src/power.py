# Serviceable components. Coordinates use metres with the crankshaft along Z.
component_meta={}
def component(en,zh,family,travel):
    part(en)
    component_meta[cur]=dict(zh=zh,en=en,family=family,vec=travel)

def radial(c,axis,angle,r):
    u,v=basis(unit(axis))
    return add(c,add(mul(u,r*cos(angle)),mul(v,r*sin(angle))))

def shell(c,axis,profile,m,N=40):
    """Surface of revolution. Profile is a closed sequence of (axial distance, radius)."""
    d=unit(axis);u,v=basis(d)
    for (h,r),(H,R) in zip(profile,profile[1:]):
        if r==R and H==h:continue
        for j in range(N):
            ns=[add(mul(u,cos(2*pi*k/N)),mul(v,sin(2*pi*k/N))) for k in (j,j+1)]
            def vertex(ax,rr,n):return add(add(c,mul(d,ax)),mul(n,rr))
            points=[vertex(h,r,ns[0]),vertex(h,r,ns[1]),vertex(H,R,ns[1]),vertex(H,R,ns[0])]
            normals=[unit(add(mul(n,H-h),mul(d,r-R))) for n in (ns[0],ns[1],ns[1],ns[0])]
            face(points,m,normals)
def sleeve(c,axis,ro,ri,length,m,N=40):
    a=length/2;b=min((ro-ri)*.22,length*.12,.0017)
    shell(c,axis,[(-a,ri),(-a,ro-b),(-a+b,ro),(a-b,ro),(a,ro-b),(a,ri),(a-.0003,ri),(-a,ri)],m,N)
def bolt(c,axis,r,m='Steel'):
    d=unit(axis);cyl(c,add(c,mul(d,r*.67)),r,m,6)
def spline(anchors,steps=6):
    """Catmull-Rom centreline through the anchor points."""
    pts=[]
    for i in range(len(anchors)-1):
        a,b,c,d=[anchors[clamp(j,0,len(anchors)-1)] for j in (i-1,i,i+1,i+2)]
        for t in seq(0,1,steps)[:-1]:
            pts.append(tuple(.5*((2*y)+(-x+z)*t+(2*x-5*y+4*z-w)*t*t+(-x+3*y-3*z+w)*t**3) for x,y,z,w in zip(a,b,c,d)))
    pts.append(anchors[-1]);return pts
def pipe(anchors,r,m,N=12):
    pts=spline(anchors);last=None
    for i,p in enumerate(pts):
        tangent=unit(sub(pts[min(i+1,len(pts)-1)],pts[max(0,i-1)]))
        if last is None:u,v=basis(tangent)
        else:u=unit(sub(u,mul(tangent,dot(tangent,u))));v=cross(tangent,u)
        ns=[add(mul(u,cos(2*pi*k/N)),mul(v,sin(2*pi*k/N))) for k in range(N)]
        ring=[add(p,mul(n,r)) for n in ns]
        if last:
            for k in range(N):
                j=(k+1)%N;face([last[k],last[j],ring[j],ring[k]],m,[ln[k],ln[j],ns[j],ns[k]])
        last,ln=ring,ns

def gear(c,axis,rad,bore,w,teeth,m='Steel',phase=0,helix=0,cone=0,witness=False):
    """Open-bore gear with chamfered faces and a flanked tooth profile."""
    d=unit(axis);u,v=basis(d)
    pts=[]
    for i in range(teeth):
        for a,f in [(0,.90),(.16,.90),(.32,1),(.58,1),(.77,.90)]:
            pts.append((2*pi*(i+a)/teeth+phase,rad*f))
    def pt(h,a,r):
        r*=1+cone*h/w
        return add(c,add(mul(d,h),add(mul(u,r*cos(a)),mul(v,r*sin(a)))))
    for j,(a,r) in enumerate(pts):
        A,R=pts[(j+1)%len(pts)]
        finish='Ivory' if witness and j<5 else m
        for h,H,f,F in [(-w*.5,-w*.40,.98,1),(-w*.4,w*.4,1,1),(w*.4,w*.5,1,.98)]:
            face([pt(h,a+helix*h/w,r*f),pt(h,A+helix*h/w,R*f),pt(H,A+helix*H/w,R*F),pt(H,a+helix*H/w,r*F)],finish)
        for h in [-w*.5,w*.5]:
            q=a+helix*h/w;Q=A+helix*h/w
            face([pt(h,q,bore),pt(h,q,r*.98),pt(h,Q,R*.98),pt(h,Q,bore)],finish)
        face([pt(-w*.5,a-helix/2,bore),pt(w*.5,a+helix/2,bore),pt(w*.5,A+helix/2,bore),pt(-w*.5,A-helix/2,bore)],finish)
def cast_strip(z,xs,ys,depth,m):
    p=[(x,y,z) for x,y in zip(xs,ys)]
    for i in range(len(p)):
        a,b=p[i],p[(i+1)%len(p)];face([a,b,add(b,(0,0,-depth)),add(a,(0,0,-depth))],m)
def deck_cell(z,y,outerx,outerz,bore,m,N=48,innerY=None):
    # Mating face around one circular opening, with rectangular outer boundaries.
    for i in range(N):
        angles=[2*pi*i/N,2*pi*(i+1)/N]
        def pt(a,inner):
            dx,dz=cos(a),sin(a);r=bore if inner else min(outerx/max(1e-8,abs(dx)),outerz/max(1e-8,abs(dz)))
            return (r*dx,y,z+r*dz)
        a,b=angles;face([pt(a,False),pt(b,False),pt(b,True),pt(a,True)],m)
        if innerY is not None:
            A=pt(a,True);B=pt(b,True);face([A,B,(B[0],innerY,B[2]),(A[0],innerY,A[2])],'Steel')
def wrapped(anchors,r,pitch,wire,m):
    """Spiral heat-shield wire wound around a hose centreline."""
    pts=spline(anchors,12);dense=[pts[0]];s=[0.]
    for a,b in zip(pts,pts[1:]):
        L=sqrt(dot(sub(b,a),sub(b,a)));n=max(1,int(L/(pitch/9)))
        for k in range(1,n+1):dense.append(mix(a,b,k/n));s.append(s[-1]+L/n)
    coil=[];u=None
    for i,p in enumerate(dense):
        t=unit(sub(dense[min(i+1,len(dense)-1)],dense[max(0,i-1)]))
        if u is None:u,v=basis(t)
        else:u=unit(sub(u,mul(t,dot(t,u))));v=cross(t,u)
        a=2*pi*s[i]/pitch;coil.append(add(p,add(mul(u,r*cos(a)),mul(v,r*sin(a)))))
    path(coil,wire,m,5)
LETTERS={
    'A':[((0,0),(2,6)),((2,6),(4,0)),((1,2.3),(3,2.3))],
    'B':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((0,3),(3,3)),((3,3),(4,2)),((4,2),(4,1)),((4,1),(3,0)),((3,0),(0,0))],
    'R':[((0,0),(0,6)),((0,6),(3,6)),((3,6),(4,5)),((4,5),(4,4)),((4,4),(3,3)),((3,3),(0,3)),((2,3),(4,0))],
    'T':[((0,6),(4,6)),((2,6),(2,0))],
    'H':[((0,0),(0,6)),((4,0),(4,6)),((0,3),(4,3))]}
def emboss(text,centre,along,up,height,m,lift=.0022):
    """Raised cast lettering; along x up is the outward face normal."""
    s=height/6;w=1.15*s;adv=6.6*s;n=unit(cross(along,up))
    start=-(len(text)*adv-2.6*s)/2
    for k,ch in enumerate(text):
        for (u0,v0),(u1,v1) in LETTERS[ch]:
            a=(start+k*adv+u0*s,(v0-3)*s);b=(start+k*adv+u1*s,(v1-3)*s)
            d=unit((b[0]-a[0],b[1]-a[1],0));q=(-d[1]*w/2,d[0]*w/2);e=(d[0]*w/2,d[1]*w/2)
            corners=[(a[0]-e[0]+q[0],a[1]-e[1]+q[1]),(b[0]+e[0]+q[0],b[1]+e[1]+q[1]),(b[0]+e[0]-q[0],b[1]+e[1]-q[1]),(a[0]-e[0]-q[0],a[1]-e[1]-q[1])]
            plate([add(add(centre,mul(n,lift)),add(mul(along,cu),mul(up,cv))) for cu,cv in corners],m,mul(n,-lift-.0006))
def cover_section(x0,inset,drop):
    # Rounded-rectangle section of a crinkle-finish cam cover, flange lip included.
    hw=.045-inset;base=.618;top=.669-drop;r=.017
    pts=[(x0-hw-.0045,base),(x0-hw,base+.003)]
    pts+=[(x0-hw+r+r*cos(a),top-r+r*sin(a)) for a in seq(pi,pi/2,8)]
    pts+=[(x0+hw-r+r*cos(a),top-r+r*sin(a)) for a in seq(pi/2,0,8)]
    return pts+[(x0+hw,base+.003),(x0+hw+.0045,base)]
def cam_cover(x0,zA=-1.134,zB=-.703,E=.017):
    def inset(z):
        d=clamp(min(z-zA,zB-z),0,E);return E-sqrt(max(0,E*E-(E-d)**2))
    stations=[zA+E*(1-cos(a)) for a in seq(0,pi/2,7)]+seq(zA+E,zB-E,10)[1:-1]+[zB-E*(1-cos(a)) for a in seq(pi/2,0,7)]
    rings=[[(x,y,z) for x,y in cover_section(x0,inset(z),.8*inset(z))] for z in stations]
    for A,B in zip(rings,rings[1:]):
        for j in range(len(A)-1):face([A[j],A[j+1],B[j+1],B[j]],'Crinkle')
    for ring in (rings[0],rings[-1]):face(ring[1:-1],'Crinkle')
    # Cast longitudinal ribs either side of the lettering band.
    for dx in [-.0255,-.0185,.0185,.0255]:
        box((x0+dx,.6698,(zA+zB)/2),(.0030,.0026,zB-zA-2*E-.018),'Crinkle')
    emboss('ABARTH',(x0,.669,(zA+zB)/2),Z,X,.023,'Red')
    for z in [-.726,-.823,-.919,-1.017,-1.113]:
        for k in [-1,1]:
            cyl((x0+k*.0475,.618,z),(x0+k*.0475,.6215,z),.0062,'Steel',16)
            bolt((x0+k*.0475,.6215,z),Y,.0042,'Gunmetal')
    for z in [zA+.021,zB-.021]:
        cyl((x0,.668,z),(x0,.6715,z),.0068,'Steel',16);bolt((x0,.6715,z),Y,.0046,'Gunmetal')
Y=(0,1,0);Z=(0,0,1);X=(1,0,0)
zs=[-.762-i*.104 for i in range(4)]
group('engine','Tipo 232 AR4 engine','机械增压发动机',(.78,.38,-.83),'2.0 升纵置直列四缸。选择上方发动机页签可拆开曲柄连杆机构、十六气门缸盖与机械增压器。')
component('Iron crankcase','铸铁缸体','缸体与润滑',(-.05,.0,0))
for z in zs:
    deck_cell(z,.546,.092,.052,.042,'Gunmetal',64,.397)
    for side_ in [-1,1]:
        box((side_*.089,.462,z),(.012,.167,.104),'Gunmetal')
        cyl((side_*.094,.452,z),(side_*.099,.452,z),.025,'Gunmetal',28,.023)
        cyl((side_*.10,.452,z),(side_*.101,.452,z),.019,'Gold',28)
        cast_strip(z+.046,[side_*.088,side_*.115,side_*.103,side_*.088],[.49,.331,.315,.48],.008,'Gunmetal')
for x in [-.105,.105]:
    box((x,.335,-.918),(.018,.068,.429),'Gunmetal')
    for z in [*zs,-1.114]:bolt((x,.311,z),(0,-1,0),.006)
for z in [-.71,-1.126]:
    cast_strip(z,[-.101,.101,.112,.107,-.107,-.112],[.54,.54,.339,.306,.306,.339],.009,'Gunmetal')
for x in [-.068,.068]:
    for z in [-.722,-.815,-.921,-1.025,-1.118]:
        cyl((x,.542,z),(x,.548,z),.006,'Black',16)
component('Oil sump casting','油底壳','缸体与润滑',(0,-.20,.0))
# Open sump, with a ribbed exterior and gasket lip.
for x in [-.102,.102]:box((x,.283,-.92),(.012,.067,.428),'Alloy')
for z in [-.712,-1.128]:box((0,.283,z),(.201,.068,.012),'Alloy')
box((0,.252,-.92),(.208,.012,.424),'Alloy')
for i in range(11):box((0,.242,-.733-i*.038),(.197,.008,.008),'Silver')
bolt((.105,.263,-1.05),X,.012,'Gold')
component('Oil pickup strainer','吸油滤网与吸油管','缸体与润滑',(-.11,-.11,-.11))
pipe([(-.061,.342,-.79),(-.061,.292,-.83),(0,.275,-.98)],.011,'Steel')
cyl((0,.27,-.98),(0,.281,-.98),.041,'Gunmetal',32)
for i in range(-4,5):
    h=sqrt(.036**2-(i*.008)**2);box((i*.008,.269,-.98),(.002,.002,h*2),'Steel')
component('Crankshaft','曲轴','曲柄连杆机构',(.40,-.075,.015))
crank=.36;throw=.045
for i,z in enumerate(zs):
    offset=throw if i in (0,3) else -throw
    cyl((0,crank+offset,z-.016),(0,crank+offset,z+.016),.018,'Silver',36)
    for dz in [-.023,.023]:
        cyl((0,crank,z+dz-.005),(0,crank,z+dz+.005),.032,'Gunmetal',32)
        cyl((0,crank-.016*(1 if offset>0 else -1),z+dz-.005),(0,crank-.016*(1 if offset>0 else -1),z+dz+.005),.032,'Gunmetal',32)
        cyl((0,crank,z+dz),(0,crank+offset,z+dz),.019,'Gunmetal',20)
for k in range(5):
    z=zs[0]+.052-k*.104;cyl((0,crank,z-.021),(0,crank,z+.021),.022,'Silver',32)
cyl((0,crank,-.708),(0,crank,-.652),.018,'Steel',32)
cyl((0,crank,-1.126),(0,crank,-1.145),.038,'Steel',32)
for i,z in enumerate(zs):
    no=i+1;offset=throw if i in (0,3) else -throw;yy=crank+offset;yp=yy+.119
    spread=(1.5-i)*.043
    component('Connecting rod '+str(no),f'{no} 缸连杆','曲柄连杆机构',(.42,.05,spread))
    sleeve((0,yy,z),Z,.027,.0183,.021,'Steel');sleeve((0,yp,z),Z,.0145,.0091,.020,'Steel')
    for dz in [-.006,.006]:
        plate([(-.013,yy+.022,z+dz),(-.008,yp-.011,z+dz),(.008,yp-.011,z+dz),(.013,yy+.022,z+dz)],'Steel',(0,0,-.002))
    box((0,(yy+yp)/2,z),(.005,.095,.012),'Gunmetal')
    for x in [-.021,.021]:bolt((x,yy-.019,z),(0,-1,0),.006,'Gunmetal')
    component('Piston '+str(no),f'{no} 缸活塞','活塞组',(.39,.255,spread))
    prof=[(-.025,.034),(-.025,.040),(-.017,.0414),(.009,.0411),(.011,.0398),(.013,.0411),(.017,.0411),(.018,.0395),(.020,.0411),(.025,.0411),(.027,.0404),(.027,.0004),(.021,.0004),(.021,.034),(-.025,.034)]
    shell((0,yp,z),Y,prof,'Alloy',48)
    for x in [-.022,.022]:
        for dz in [-.013,.013]:
            cyl((x,yp+.0267,z+dz),(x,yp+.0274,z+dz),.009,'Steel',20)
    component('Wrist pin '+str(no),f'{no} 缸活塞销','活塞组',(.58,.208,spread+.042))
    sleeve((0,yp,z),Z,.009,.0052,.065,'Silver',24)
    component('Ring pack '+str(no),f'{no} 缸活塞环组','活塞组',(.39,.339,spread))
    for dy in [.0107,.0183,.0226]:sleeve((0,yp+dy,z),Y,.042,.039,.0016,'Gunmetal',42)
component('Head gasket','气缸垫','缸盖与配气',(-.26,.15,.02))
for z in zs:
    deck_cell(z,.548,.092,.052,.043,'Charcoal')
    tor((0,.5485,z),Y,.043,.0011,'Steel',40,6)
component('16-valve head casting','十六气门铝合金缸盖','缸盖与配气',(-.43,.255,-.13))
for z in zs:
    deck_cell(z,.551,.115,.052,.037,'Alloy')
    deck_cell(z,.599,.115,.052,.015,'Alloy')
    sleeve((0,.604,z),Y,.019,.011,.014,'Alloy',32)
    for sign in [-1,1]:
        for dz in [-.017,.017]:
            c=(sign*.034,.602,z+dz)
            sleeve(c,unit((sign*.36,1,0)),.012,.004,.011,'Gold',20)
        bx=sign*.047
        for xx in [-.021,.021]:
            box((bx+xx,.611,z+.036),(.014,.028,.015),'Alloy')
            bolt((bx+xx,.626,z+.036),Y,.0044,'Gunmetal')
    for side_ in [-1,1]:
        box((side_*.111,.574,z),(.009,.049,.104),'Alloy')
        sleeve((side_*.119,.576,z),X,.021,.0155,.012,'Silver',28)
        for dz in [-.030,.030]:bolt((side_*.118,.578,z+dz),(side_,0,0),.004)
for z in [-.710,-1.126]:box((0,.575,z),(.22,.048,.009),'Alloy')
for side_ in [-1,1]:
    tag='进气' if side_<0 else '排气'
    component(tag+' camshaft',tag+'凸轮轴','缸盖与配气',(side_*.20,.452,0))
    cyl((side_*.045,.629,-1.128),(side_*.045,.629,-.682),.012,'Silver',32)
    for i,z in enumerate(zs):
        for dz in [-.018,.018]:
            firing=[0,3*pi,pi,2*pi][i]
            peak=(2.5*pi if side_<0 else 1.5*pi)+firing
            a=math.atan2(-1,-side_*.36)-peak/2
            def cam_point(theta,Zp):
                angle=(theta-a+pi)%(2*pi)-pi
                r=.018+(.010*cos(2*angle)**2 if abs(angle)<pi/4 else 0)
                return (side_*.045+r*cos(theta),.629+r*sin(theta),Zp)
            grid(cam_point,seq(0,2*pi,36),[z+dz-.006,z+dz+.006],'Gunmetal')
            for zz in [z+dz-.006,z+dz+.006]:face([cam_point(theta,zz) for theta in seq(0,2*pi,36)[:-1]],'Steel')
        sleeve((side_*.045,.629,z+.04),Z,.017,.012,.011,'Silver',28)
    component(tag+' cam cover',tag+'侧凸轮轴盖','缸盖与配气',(side_*.28,.65,-.034))
    # Separate gold crinkle covers leave the plug well open between them.
    cam_cover(side_*.053)
    for i,z in enumerate(zs):
        for j,dz in enumerate([-.017,.017]):
            n=f'{i+1} 缸{tag}门 {j+1}';base=(side_*.020,.553,z+dz);axis=unit((side_*.36,1,0));topv=add(base,mul(axis,.070))
            vec=(side_*(.103+j*.024),.20+(j*.032),(1.5-i)*.034+dz*.34)
            component(n,n,'气门与弹簧',vec)
            cyl(base,add(base,mul(axis,.003)),.014,'Steel',28,.013)
            cyl(add(base,mul(axis,.003)),add(base,mul(axis,.010)),.013,'Gunmetal',24,.0031)
            cyl(add(base,mul(axis,.009)),topv,.0031,'Silver',16)
            component(n+' spring',f'{i+1} 缸{tag}门弹簧 {j+1}','气门与弹簧',(vec[0]*1.34,vec[1]+.105,vec[2]))
            p=add(base,mul(axis,.027));q=add(base,mul(axis,.065))
            spring(p,q,.008,.0014,'Gunmetal')
            sleeve(q,axis,.010,.0032,.0028,'Silver',20)
component('Ignition loom','高压点火线束与硅胶火花塞帽','点火与正时',(-.30,.57,.17))
cap_z=-1.205;towers=[(-.045+.017*cos(a),.629+.017*sin(a)) for a in [pi*.56,pi*.78,pi,pi*1.22]]
for i,z in enumerate(zs):
    # Red silicone boots stand in the plug well; leads loop over the intake cover.
    cyl((0,.622,z),(0,.667,z),.0072,'Silicone',18)
    cyl((0,.667,z),(0,.679,z),.0072,'Silicone',18,.0046)
    for dy in [.632,.656]:tor((0,dy,z),Y,.0072,.0011,'Silicone',18,5)
    yb=.630+.0078*i;tx,ty=towers[i]
    pipe([(0,.678,z),(-.014,.693,z),(-.058,.697,z+.004),(-.098,.684,z-.004),(-.113,.662,z-.03),(-.113,yb,z-.06),
          (-.113,yb,-1.118),(-.102,yb+.004,-1.17),(tx,ty,cap_z-.022),(tx,ty,cap_z-.004)],.0034,'Black',8)
for zc,n in [(-.94,2),(-1.122,4)]:
    box((-.113,.630+.0039*(n-1),zc),(.0115,.0078*n+.007,.009),'Charcoal')
    for k in range(n):cyl((-.1195,.630+.0078*k,zc),(-.1065,.630+.0078*k,zc),.0046,'Black',10)
component('Distributor and coil','分电器与点火线圈','点火与正时',(-.12,.24,-.42))
# Driven from the flywheel end of the intake camshaft.
cyl((-.045,.629,-1.134),(-.045,.629,-1.146),.020,'Alloy',28)
cyl((-.045,.629,-1.146),(-.045,.629,-1.166),.024,'Alloy',32,.026)
for a in [.3,pi+.3]:bolt((-.045+.025*cos(a),.629+.025*sin(a),-1.150),(0,0,-1),.0035)
cyl((-.045,.629,-1.166),(-.045,.629,-1.172),.031,'Charcoal',36)
cyl((-.045,.629,-1.172),(-.045,.629,cap_z),.030,'Black',36,.026)
for tx,ty in towers+[(-.045,.629)]:
    cyl((tx,ty,cap_z),(tx,ty,cap_z-.012),.0058,'Black',14)
    cyl((tx,ty,cap_z-.012),(tx,ty,cap_z-.016),.0040,'Silicone',12)
for a in [pi*.25,pi*1.75]:
    cyl((-.045+.028*cos(a),.629+.028*sin(a),-1.168),(-.045+.028*cos(a),.629+.028*sin(a),-1.190),.0028,'Steel',8)
cyl((-.150,.548,-1.196),(-.150,.612,-1.196),.021,'Black',32)
cyl((-.150,.612,-1.196),(-.150,.622,-1.196),.014,'Charcoal',24)
cyl((-.150,.622,-1.196),(-.150,.631,-1.196),.0045,'Gold',12)
for y in [.556,.604]:tor((-.150,y,-1.196),Y,.022,.0020,'Steel',32,6)
box((-.128,.580,-1.196),(.012,.040,.030),'Gunmetal')
pipe([(-.045,.629,cap_z-.016),(-.060,.632,-1.236),(-.120,.640,-1.226),(-.150,.636,-1.196)],.0034,'Black',8)
for i,z in enumerate(zs):
    component('Plug '+str(i+1),f'{i+1} 缸火花塞','点火与正时',(.025,.47,(1.5-i)*.052))
    cyl((0,.571,z),(0,.598,z),.006,'Steel',20)
    bolt((0,.598,z),Y,.009,'Silver')
    cyl((0,.605,z),(0,.626,z),.0057,'Ivory',18)
    for j in range(4):tor((0,.610+j*.003,z),Y,.0059,.0013,'Pearl',16,5)
    cyl((0,.625,z),(0,.633,z),.003,'Gold')
component('Timing belt','凸轮轴正时带','点火与正时',(.015,.14,.29))
belt=[(-.050,.666,-.682),(.05,.666,-.682),(.080,.643,-.682),(.078,.618,-.682),(.031,.352,-.682),(0,.329,-.682),(-.029,.352,-.682),(-.08,.617,-.682),(-.08,.644,-.682),(-.05,.666,-.682)]
strip(belt,(0,0,.018),'Rubber')
for side_ in [-1,1]:
    component('Timing wheel '+str(side_),('进气' if side_<0 else '排气')+'正时齿轮','点火与正时',(side_*.13,.29,.19))
    gear((side_*.045,.629,-.676),Z,.037,.011,.017,29,'Gold')
    box((side_*.045,.656,-.666),(.0025,.009,.002),'Ivory')
component('Crank drive pulley','曲轴皮带轮','点火与正时',(.03,-.05,.29))
shell((0,crank,-.667),Z,[(-.019,.012),(-.019,.044),(-.016,.044),(-.011,.038),(-.007,.044),(-.004,.044),(.001,.038),(.005,.044),(.011,.044),(.011,.012),(-.019,.012)],'Gunmetal')
component('Roots blower housing','Volumex 增压器壳体','进气与排气',(-.56,.04,.19))
for x in [-.248,-.191]:
    sleeve((x,.488,-.905),Z,.058,.050,.245,'Alloy',40)
for j in range(8):box((-.220,.545,-.804-j*.029),(.090,.008,.007),'Silver')
for side_ in [-1,1]:
    component('Blower rotor '+str(side_),'增压器转子 '+('A' if side_<0 else 'B'),'进气与排气',(-.50-side_*.11,.14,.47))
    x=-.219+side_*.0285
    def rotor(a,t):
        r=.032+.013*cos(2*a+(0 if side_<0 else pi))
        return (x+r*cos(a),.488+r*sin(a),t)
    grid(rotor,seq(0,2*pi,64),[-1.018,-.793],'Steel')
    for z in [-1.018,-.793]:face([rotor(a,z) for a in seq(0,2*pi,64)[:-1]],'Alloy')
    cyl((x,.488,-1.04),(x,.488,-.772),.008,'Silver',24)
component('Blower drive','增压器带轮与传动带','进气与排气',(-.28,.019,.41))
for x,y in [(0,crank),(-.247,.488)]:
    sleeve((x,y,-.639),Z,.042,.010,.019,'Gunmetal')
path([(-.264,.449,-.638),(-.018,.321,-.638),(.018,.398,-.638),(-.226,.526,-.638),(-.264,.449,-.638)],.006,'Black',8)
component('Intake plenum and runners','铝制稳压腔与进气歧管','进气与排气',(-.46,.24,-.30))
# Fabricated cylindrical plenum with welded domed tail and a square throttle flange at the front.
plx,ply=-.205,.668
shell((plx,ply,-.92),Z,[(-.200,0),(-.198,.020),(-.193,.032),(-.186,.039),(-.178,.042),(.192,.042),(.192,.046),(.200,.046),(.200,0)],'Alloy',44)
for dz in [-.178,.186]:tor((plx,ply,-.92+dz),Z,.042,.0022,'Silver',44,6)
for z in zs:
    pipe([(-.116,.576,z),(-.138,.587,z),(-.163,.608,z),(-.186,.642,z)],.016,'Alloy',16)
    tor((-.170,.617,z),unit((-.023,.034,0)),.016,.0018,'Silver',24,5)
for z in [-.86,-.98,-1.06]:
    cyl((plx,.705,z),(plx,.716,z),.0095,'Alloy',20);bolt((plx,.716,z),Y,.0068,'Steel')
# Barbed take-off and the hex boss seen on the outboard face.
cyl((-.244,ply,-.88),(-.258,ply,-.88),.012,'Alloy',20)
bolt((-.258,ply,-.88),(-1,0,0),.0105,'Steel')
cyl((-.265,ply,-.88),(-.292,ply,-.88),.0058,'Steel',16)
for x in [-.272,-.280,-.288]:tor((x,ply,-.88),X,.0058,.0012,'Steel',16,5)
cyl((-.190,.700,-.78),(-.190,.716,-.78),.0085,'Alloy',18);bolt((-.190,.716,-.78),Y,.0075,'Steel')
cyl((-.190,.721,-.78),(-.190,.734,-.78),.0042,'Steel',14)
component('Throttle body and linkage','节气门体与油门连杆','进气与排气',(-.42,.30,.30))
for z,s in [(-.716,.080),(-.668,.068)]:
    box((plx,ply,z),(s,s,.008),'Alloy')
    for dx in [-1,1]:
        for dy in [-1,1]:bolt((plx+dx*(s/2-.007),ply+dy*(s/2-.007),z+.004),Z,.0040)
cyl((plx,ply,-.712),(plx,ply,-.672),.033,'Gunmetal',32)
box((plx,ply-.030,-.692),(.040,.014,.030),'Gunmetal')
cyl((-.246,ply,-.692),(-.164,ply,-.692),.0042,'Steel',12)
cyl((-.246,ply,-.692),(-.252,ply,-.692),.010,'Gunmetal',16)
plate([(-.252,ply-.006,-.692),(-.252,ply+.006,-.692),(-.252,.712,-.712),(-.252,.700,-.716)],'Steel',(-.003,0,0))
cyl((-.255,.706,-.714),(-.262,.706,-.714),.0035,'Silver',10)
box((-.254,.702,-.792),(.005,.028,.012),'Steel')
for dy in [-.008,.008]:spring((-.257,.706+dy*.4,-.718),(-.257,.702+dy,-.786),.0042,.0008,'Steel')
pipe([(-.262,.706,-.714),(-.272,.720,-.68),(-.268,.735,-.60)],.0016,'Steel',6)
cyl((-.160,ply+.020,-.700),(-.150,ply+.020,-.700),.0035,'Gold',10)
bolt((-.150,ply+.020,-.700),X,.0045,'Steel')
component('Supercharger delivery duct','增压出气弯管与硅胶接头','进气与排气',(-.60,.22,.36))
duct=[(plx,ply,-.668),(plx,ply,-.646),(-.226,.656,-.614),(-.268,.632,-.606),(-.292,.612,-.645),(-.292,.606,-.735),(-.276,.600,-.800),(-.264,.590,-.832),(-.262,.578,-.842)]
pipe(duct,.026,'Alloy',24)
cyl((-.262,.540,-.842),(-.262,.570,-.842),.026,'Alloy',28)
box((-.262,.544,-.842),(.062,.008,.062),'Alloy')
for c,axis in [((plx,ply,-.652),Z),((-.262,.574,-.842),Y)]:
    sleeve(c,axis,.0305,.0262,.026,'Silicone',32)
    for k in [-.0085,.0085]:
        q=add(c,mul(axis,k));tor(q,axis,.031,.0019,'Steel',32,6)
        bolt(add(q,mul(unit(cross(axis,X if axis!=X else Y)),.032)),unit(cross(axis,X if axis!=X else Y)),.0032)
component('Exhaust manifold','四合一排气歧管','进气与排气',(.52,.16,-.39))
for i,z in enumerate(zs):
    pipe([(.114,.577,z),(.171,.597,z),(.231+i*.018,.577,z-.011),(.28+i*.012,.484,z-.057),(.303+i*.009,.412,z-.11),(.34,.382,-1.38)],.0185,'Exhaust',16)
    sleeve((.136,.582,z),X,.022,.018,.009,'Exhaust',22)
    box((.127,.580,z),(.008,.052,.090),'Exhaust')
    for dz in [-.034,.034]:
        cyl((.131,.580,z+dz),(.139,.580,z+dz),.0035,'Steel',8);bolt((.139,.580,z+dz),X,.0058,'Gold')
component('Silencer and outlets','消声器与双尾管','进气与排气',(.09,-.06,-.37))
pipe([(.34,.382,-1.38),(.35,.374,-1.59),(.312,.374,-1.738),(.256,.38,-1.77)],.039,'Exhaust',16)
cyl((-.29,.375,-1.772),(.31,.375,-1.772),.084,'Silver',48)
for x in [-.24,-.208,.209,.264]:tor((x,.375,-1.772),X,.084,.004,'Gunmetal',32,6)
for x in [-.22,-.091]:
    pipe([(x,.365,-1.803),(x,.336,-1.921)],.039,'Steel')
    sleeve((x,.337,-1.964),Z,.041,.036,.114,'Steel',32)
component('Mechanical injection pump','机械喷射泵与供油管','进气与排气',(-.38,.07,-.12))
box((-.138,.409,-.956),(.059,.057,.129),'Gunmetal')
for i,z in enumerate(zs):
    zp=-.905-i*.031
    bolt((-.138,.439,zp),Y,.0048,'Gold')
    pipe([(-.138,.44,zp),(-.15,.493,zp),(-.151,.558,z),(-.14,.587,z)],.0018,'Gold',8)
component('Lubrication filter','机油滤清器','缸体与润滑',(.19,-.08,-.21))
cyl((.104,.398,-1.062),(.179,.391,-1.062),.031,'Charcoal',36,.030)
sleeve((.112,.397,-1.062),X,.033,.029,.007,'Silver',28)
component('Dry-sump oil tank','干式油底壳铝制储油罐','缸体与润滑',(-.52,.04,.30))
tx,ty,tz=-.405,.468,-.705
box((tx,ty,tz),(.080,.150,.104),'Alloy')
for dx in [-.040,.040]:
    for dz in [-.052,.052]:path([(tx+dx,ty-.075,tz+dz),(tx+dx,ty+.075,tz+dz)],.0028,'Silver',6)
for dy in [-.075,.075]:
    path([(tx+dx,ty+dy,tz+dz) for dx,dz in [(-.040,-.052),(.040,-.052),(.040,.052),(-.040,.052),(-.040,-.052)]],.0026,'Silver',6)
for dy in [-.042,.042]:
    path([(tx+dx,ty+dy,tz+dz) for dx,dz in [(-.0425,-.0545),(.0425,-.0545),(.0425,.0545),(-.0425,.0545),(-.0425,-.0545)]],.0035,'Black',6)
cyl((tx,ty+.075,tz+.018),(tx,ty+.096,tz+.018),.016,'Alloy',28)
cyl((tx,ty+.096,tz+.018),(tx,ty+.106,tz+.018),.022,'Steel',12)
for k in range(2):box((tx,ty+.110,tz+.018),(.034 if k==0 else .006,.006,.006 if k==0 else .034),'Steel')
cyl((tx-.020,ty+.075,tz-.026),(tx-.020,ty+.094,tz-.026),.0055,'Steel',14)
fittings=[((tx+.040,ty-.050,tz),'Blue'),((tx+.040,ty+.034,tz-.020),'Red')]
for (fx,fy,fz),m in fittings:
    cyl((fx,fy,fz),(fx+.008,fy,fz),.0095,'Alloy',16);cyl((fx+.008,fy,fz),(fx+.020,fy,fz),.0105,m,6)
component('Heat-wrapped oil lines','隔热缠绕机油管','缸体与润滑',(-.36,-.20,.22))
feed=[(tx+.060,ty-.050,tz),(-.300,.400,-.700),(-.210,.352,-.716),(-.140,.318,-.742),(-.116,.300,-.770)]
ret=[(.140,.348,-1.062),(.124,.250,-1.010),(.020,.228,-.920),(-.140,.278,-.820),(-.290,.452,-.760),(tx+.060,ty+.034,tz-.020)]
for line in (feed,ret):
    pipe(line,.0085,'Rubber',10);wrapped(line,.0091,.0105,.0016,'Gold')
    for p,q in [(line[0],line[1]),(line[-1],line[-2])]:
        d=unit(sub(q,p));cyl(p,add(p,mul(d,.016)),.0105,'Blue' if line is feed else 'Red',6)
component('Cam cover breather line','凸轮轴盖通风编织管','缸盖与配气',(.06,.42,.14))
cyl((.053,.669,-.752),(.053,.680,-.752),.0080,'Alloy',18);bolt((.053,.680,-.752),Y,.0072,'Steel')
breather=[(.053,.686,-.752),(.040,.704,-.770),(-.010,.714,-.786),(-.100,.714,-.792),(-.160,.736,-.786),(-.190,.740,-.780),(-.190,.734,-.780)]
pipe(breather,.0056,'Braid',10)
pts=spline(breather,8)
for k in range(4,len(pts)-4,2):tor(pts[k],unit(sub(pts[k+1],pts[k-1])),.0057,.0009,'Charcoal',10,4)
for p,d in [((.053,.686,-.752),Y),((-.190,.728,-.780),(0,-1,0))]:
    cyl(p,add(p,mul(d,.012)),.0075,'Steel',6)
group('gearbox','ZF five-speed transaxle','五速变速驱动桥',(.90,.32,-1.63),'纵置五速手动变速箱，包含离合器、两根传动轴、五组常啮合齿轮、倒挡组件与差速器。')
component('Bell housing','离合器钟形壳','壳体与轴承',(-.32,.20,.28))
shell((0,.36,-1.202),Z,[(-.063,.078),(-.060,.088),(.022,.134),(.045,.143),(.051,.143),(.051,.134),(.024,.125),(-.06,.072),(-.063,.078)],'Alloy',56)
for j in range(8):
    a=j*pi/4
    pipe([(r*cos(a),.36+r*sin(a),z) for r,z in [(.087,-1.258),(.137,-1.167),(.143,-1.155)]],.004,'Silver',8)
component('Flywheel ring gear','带起动齿圈的飞轮','离合器',(-.10,.19,.55))
gear((0,.36,-1.15),Z,.115,.020,.012,76,'Gunmetal')
sleeve((0,.36,-1.157),Z,.101,.026,.010,'Silver',56)
for j in range(6):
    a=j*pi/3;bolt((.031*cos(a),.36+.031*sin(a),-1.165),(0,0,-1),.005)
component('Clutch disc','离合器摩擦片','离合器',(.05,.20,.43))
sleeve((0,.36,-1.169),Z,.097,.061,.007,'Charcoal',56)
sleeve((0,.36,-1.169),Z,.066,.014,.005,'Steel',40)
gear((0,.36,-1.169),Z,.028,.010,.014,18,'Gunmetal')
for j in range(8):
    a=j*pi/4
    for r in [.071,.089]:
        cyl((r*cos(a),.36+r*sin(a),-1.173),(r*cos(a),.36+r*sin(a),-1.174),.0023,'Gold',10)
component('Clutch pressure plate','膜片弹簧与压盘','离合器',(.14,.21,.33))
sleeve((0,.36,-1.183),Z,.101,.066,.015,'Alloy',48)
for j in range(18):
    a=j*2*pi/18;plate([(r*cos(a+b),.36+r*sin(a+b),z) for r,b,z in [(.022,-.13,-1.207),(.072,-.12,-1.19),(.072,.12,-1.19),(.022,.13,-1.207)]],'Gunmetal',(0,0,.002))
component('Release bearing','分离轴承','离合器',(.21,.20,.22))
sleeve((0,.36,-1.217),Z,.030,.015,.021,'Steel')
def casing_end(a,b):
    # Rounded polygonal flanks on the cast central gear housing.
    return math.copysign(abs(a)**.81,a), math.copysign(abs(b)**.81,b)
def halfcase(side_):
    sections=[(-1.259,.109,.106),(-1.29,.139,.122),(-1.387,.127,.110),(-1.444,.111,.101),(-1.650,.104,.096),(-1.753,.090,.084),(-1.788,.073,.066)]
    ang=seq(0,pi,36) if side_>0 else seq(pi,2*pi,36)
    for (z,rx,ry),(Zp,Rx,Ry) in zip(sections,sections[1:]):
        for k in [0,.006]:
            grid(lambda a,t:((rx+(Rx-rx)*t-k)*casing_end(cos(a),sin(a))[0],.326+(ry+(Ry-ry)*t-k)*casing_end(cos(a),sin(a))[1],z+t*(Zp-z)),ang,[0,1],'Alloy')
        for k in [-1,1]:
            plate([(k*rx,.326,z),(k*Rx,.326,Zp),(k*(Rx+.009),.326,Zp),(k*(rx+.009),.326,z)],'Silver',(0,side_*.003,0))
    for z,rx,ry in sections:
        for a,b in zip(ang,ang[1:]):
            face([(r*casing_end(cos(theta),sin(theta))[0],.326+y*casing_end(cos(theta),sin(theta))[1],z) for theta,r,y in [(a,rx,ry),(b,rx,ry),(b,rx-.006,ry-.006),(a,rx-.006,ry-.006)]],'Silver')
    for z in [-1.31,-1.357,-1.428,-1.50,-1.55,-1.606,-1.657,-1.718,-1.754]:
        rx=interp(-z,[(-a,b) for a,b,c in sections]);ry=interp(-z,[(-a,c) for a,b,c in sections])
        for a,b in zip(ang,ang[1:]):
            for dh,dr,DH,DR in [(-.005,.001,-.003,.007),(-.003,.007,.003,.007),(.003,.007,.005,.001)]:
                face([((rx+r)*casing_end(cos(t),sin(t))[0],.326+(ry+r)*casing_end(cos(t),sin(t))[1],z+h) for t,h,r in [(a,dh,dr),(b,dh,dr),(b,DH,DR),(a,DH,DR)]],'Alloy')
        for k in [-1,1]:bolt((k*(rx+.004),.326+side_*.003,z),(0,side_,0),.0057)
for s in [-1,1]:
    component('Transaxle '+('upper' if s>0 else 'lower')+' shell',('上' if s>0 else '下')+'半箱体','壳体与轴承',(-.25,.41 if s>0 else -.23,-.10))
    halfcase(s)
    for xp in [-1,1]:
        for a in [.31,.75]:
            f,g=casing_end(cos(a),sin(a));f*=xp;g*=s
            pipe([(rx*f,.326+ry*g,z) for z,rx,ry in [(-1.294,.138,.12),(-1.388,.127,.110),(-1.444,.111,.101),(-1.65,.104,.096),(-1.75,.09,.084)]],.004,'Alloy',8)
    if s>0:
        box((.052,.407,-1.534),(.066,.026,.132),'Alloy')
        for x in [.026,.077]:
            for z in [-1.477,-1.59]:bolt((x,.421,z),Y,.005,'Gunmetal')
        cyl((.031,.419,-1.49),(.031,.447,-1.49),.008,'Gold',18)
        cyl((.031,.446,-1.49),(.031,.451,-1.49),.012,'Gunmetal',18)

component('Tail cap','箱体后端盖','壳体与轴承',(-.10,.12,-.54))
cyl((0,.326,-1.788),(0,.326,-1.802),.072,'Alloy',40,.069)
for j in range(7):
    a=2*pi*j/7;bolt((.061*cos(a),.326+.061*sin(a),-1.803),(0,0,-1),.0053)
shafts=[.36,.2784]
for row,y in enumerate(shafts):
    lab='输入' if row==0 else '输出';dy=.14 if row==0 else -.02
    component(lab+' shaft',lab+'轴','齿轮传动',(.05+row*.15,dy,-.02))
    cyl((0,y,-1.785),(0,y,-1.255 if row else -1.165),.013 if not row else .015,'Silver',40)
    for z in [-1.402,-1.722]:
        sleeve((0,y,z),Z,.022,.013,.018,'Gunmetal',28)
    for j in range(12):
        a=j*pi/6;r=.014
        cyl((r*cos(a),y+r*sin(a),-1.251),(r*cos(a),y+r*sin(a),-1.182 if not row else -1.242),.0018,'Steel',6)
    for i,teeth in enumerate([14,18,23,27,31]):
        n=teeth if row==0 else 48-teeth;rad=(n+2)*.0017;z=-1.437-.062*i
        component(f'{lab} gear {i+1}',f'{i+1} 挡'+('主动齿轮' if row==0 else '从动齿轮'),'齿轮传动',(.06+row*.17,dy+.094*(1-row)-.081*row,(2-i)*.053))
        gear((0,y,z),Z,rad,.014 if not row else .016,.023,n,'Steel',phase=0 if row==0 else pi/n,helix=.06 if row==0 else -.06)
        sleeve((0,y,z+.012),Z,min(rad*.76,.033),.016,.008,'Gunmetal',32)
        cyl((0,y+rad*.76,z+.012),(0,y+rad*.76,z+.0137),.0028,'Gold',12)
    for end,z in [('前',-1.41),('后',-1.749)]:
        component(lab+end+' bearing',lab+'轴'+end+'轴承','壳体与轴承',(.10+row*.24,dy, .18 if end=='前' else -.20))
        sleeve((0,y,z),Z,.031,.026,.014,'Steel',36)
        sleeve((0,y,z),Z,.020,.014,.014,'Gunmetal',36)
        for a in seq(0,2*pi,12)[:-1]:
            cyl((.023*cos(a),y+.023*sin(a),z-.005),(.023*cos(a),y+.023*sin(a),z+.005),.0034,'Silver',10)
for i,z in enumerate([-1.469,-1.591,-1.711]):
    component('Sliding collar '+str(i+1),f'{i+1} 号接合套','选挡与倒挡',(.33,.009,(1-i)*.11))
    gear((0,.2784,z),Z,.031,.016,.020,24,'Gunmetal')
    for dz in [-.007,.007]:sleeve((0,.2784,z+dz),Z,.033,.018,.004,'Steel',32)
    component('Selector fork '+str(i+1),f'{i+1} 号拨叉','选挡与倒挡',(.33,.15,(1-i)*.11))
    pipe([(.034*cos(a),.2784+.034*sin(a),z) for a in seq(-.44,pi+.44,12)],.005,'Gold',8)
    cyl((0,.309,z),(.054,.366,z),.005,'Gold',12);sleeve((.057,.369,z),Z,.012,.006,.015,'Gunmetal',20)
component('Shift rails','选挡导杆','选挡与倒挡',(.34,.26,.015))
for j in range(3):cyl((.044+j*.012,.369,-1.731),(.044+j*.012,.369,-1.419),.004,'Silver',18)
component('Reverse idler','倒挡惰轮','选挡与倒挡',(.32,.17,-.32))
gear((.038,.321,-1.736),Z,.028,.008,.02,18,'Steel')
component('Reverse idler shaft','倒挡惰轮轴','选挡与倒挡',(.36,.21,-.40))
cyl((.038,.321,-1.761),(.038,.321,-1.713),.0078,'Silver',20)
for row,y in enumerate(shafts):
    component('Reverse gear '+str(row),'倒挡'+('主动轮' if row==0 else '从动轮'),'选挡与倒挡',(.12+row*.11,.2-row*.27,-.34))
    gear((0,y,-1.737),Z,.031,.015,.018,18,'Gunmetal')
component('Final drive pinion','主减速主动锥齿轮','差速与终传',(.16,-.09,.12))
gear((0,.2784,-1.353),Z,.033,.015,.024,13,'Steel',cone=.45)
component('Crownwheel','主减速大齿圈','差速与终传',(.52,.04,.22))
gear((.044,.315,-1.291),X,.094,.044,.016,45,'Steel',helix=.035,cone=.10)
for j in range(8):
    a=j*pi/4;bolt((.054,.315+.056*cos(a),-1.291+.056*sin(a)),X,.006,'Gunmetal')
component('Differential carrier','差速器壳架','差速与终传',(.37,.04,.22))
for x in [-.042,.034]:sleeve((x,.315,-1.291),X,.059,.035,.013,'Gunmetal',36)
for j in range(4):
    a=pi*j/2+pi/4;cyl((-.04,.315+.047*cos(a),-1.291+.047*sin(a)),(.036,.315+.047*cos(a),-1.291+.047*sin(a)),.012,'Gunmetal',16)
for s in [-1,1]:
    component('Side gear '+str(s),('左' if s>0 else '右')+'半轴齿轮','差速与终传',(.34+s*.20,.065,.26))
    gear((s*.021,.315,-1.291),X,.029,.012,.012,16,'Steel',cone=s*.32,witness=True)
    bolt((s*.027,.334,-1.291),(s,0,0),.0026,'Gold')
    component('Drive flange '+str(s),('左' if s>0 else '右')+'半轴输出法兰','差速与终传',(.32+s*.36,.01,.18))
    cyl((s*.043,.315,-1.291),(s*.174,.315,-1.291),.018,'Steel')
    sleeve((s*.168,.315,-1.291),X,.043,.018,.012,'Gunmetal')
    for j in range(6):
        a=j*pi/3;bolt((s*.174,.315+.032*cos(a),-1.291+.032*sin(a)),(s,0,0),.0046)
component('Differential cross pin','差速行星齿轮轴','差速与终传',(.34,.205,.25))
cyl((0,.272,-1.291),(0,.358,-1.291),.005,'Steel',24)
for side_ in [-1,1]:
    y=.315+side_*.027
    component('Spider bevel '+str(side_),('上' if side_>0 else '下')+'差速行星齿轮','差速与终传',(.34,.205+side_*.060,.25))
    gear((0,y,-1.291),Y,.0195,.005,.012,12,'Gunmetal',cone=side_*.36,witness=True)
    # An asymmetric dot stays on the rotating face, visible in the carrier frame.
    cyl((.011,y+side_*.0062,-1.291),( .011,y+side_*.0075,-1.291),.0021,'Ivory',14)
