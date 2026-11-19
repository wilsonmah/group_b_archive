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
def pipe(anchors,r,m,N=12):
    pts=[]
    for i in range(len(anchors)-1):
        a,b,c,d=[anchors[clamp(j,0,len(anchors)-1)] for j in (i-1,i,i+1,i+2)]
        for t in seq(0,1,6)[:-1]:
            pts.append(tuple(.5*((2*y)+(-x+z)*t+(2*x-5*y+4*z-w)*t*t+(-x+3*y-3*z+w)*t**3) for x,y,z,w in zip(a,b,c,d)))
    pts.append(anchors[-1]);last=None
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
    x=side_*.050
    for z in [-1.134,-.703]:
        face([(x+.047*cos(a),.620+.042*sin(a),z) for a in seq(0,pi,32)],'Engine')
    grid(lambda a,z:(x+.047*cos(a),.62+.042*sin(a),z),seq(0,pi,32),[-1.134,-.703],'Engine')
    for k in [-1,1]:box((x+k*.046,.617,-.919),(.014,.012,.44),'Engine')
    for k in [-2,-1,0,1,2]:
        dx=k*.010;box((x+dx,.622+.042*sqrt(1-(dx/.047)**2),-.919),(.0035,.003,.375),'Alloy')
    for z in [-.726,-.823,-1.017,-1.113]:
        for k in [-1,1]:bolt((x+k*.044,.625,z),Y,.0048)
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
component('Ignition loom','高压点火线束','点火与正时',(-.30,.57,.17))
for i,z in enumerate(zs):
    pipe([(0,.628,z),(-.013,.688,z),(-.102,.681,z+.015),(-.148,.612,-.749-i*.014)],.0038,'Rubber',8)
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
component('Charge manifold','进气歧管','进气与排气',(-.46,.24,-.30))
for z in zs:pipe([(-.116,.576,z),(-.16,.599,z),(-.198,.593,z),(-.214,.549,z)],.016,'Alloy',16)
box((-.217,.548,-.915),(.089,.039,.37),'Alloy')
component('Exhaust manifold','四合一排气歧管','进气与排气',(.52,.16,-.39))
for i,z in enumerate(zs):
    pipe([(.114,.577,z),(.171,.597,z),(.231+i*.018,.577,z-.011),(.28+i*.012,.484,z-.057),(.303+i*.009,.412,z-.11),(.34,.382,-1.38)],.0185,'Exhaust',16)
    sleeve((.136,.582,z),X,.022,.018,.009,'Exhaust',22)
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
